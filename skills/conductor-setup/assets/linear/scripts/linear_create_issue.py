#!/usr/bin/env python3
"""Create a Linear issue via GraphQL.

Requires LINEAR_API_KEY (Personal API key from Linear → Settings → API).
Team name comes from ``--team`` or ``LINEAR_TEAM_NAME`` (see conductor/linear.md).
There is no product-specific default team.

Usage:
  LINEAR_API_KEY=lin_api_... LINEAR_TEAM_NAME="Widgets" \\
    python scripts/linear_create_issue.py --title "Example" --label Bug
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

GRAPHQL_URL = "https://api.linear.app/graphql"

EXIT_OK = 0
EXIT_HARD_FAILURE = 1
EXIT_NO_KEY = 2


class LinearCreateError(RuntimeError):
    """A hard failure that should surface as EXIT_HARD_FAILURE."""


def graphql(api_key: str, query: str, variables: dict | None = None) -> dict:
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
    if body.get("errors"):
        raise LinearCreateError(json.dumps(body["errors"], indent=2))
    return body["data"]


def resolve_team_name(flag: str, env: dict | None = None) -> str:
    """Resolve team name from --team or LINEAR_TEAM_NAME. No product default."""
    environ = env if env is not None else os.environ
    name = (flag or "").strip() or str(environ.get("LINEAR_TEAM_NAME", "")).strip()
    if not name:
        raise LinearCreateError(
            "Team name required: pass --team or set LINEAR_TEAM_NAME (see conductor/linear.md)."
        )
    return name


def fetch_team(api_key: str, team_name: str) -> dict:
    query = """
    query Team($name: String!) {
      teams(filter: { name: { eq: $name } }) {
        nodes { id name }
      }
    }
    """
    data = graphql(api_key, query, {"name": team_name})
    teams = data["teams"]["nodes"]
    if not teams:
        raise LinearCreateError(f"Team not found: {team_name}")
    return teams[0]


def fetch_label_ids(api_key: str, team_id: str, names: list[str]) -> list[str]:
    query = """
    query TeamLabels($teamId: String!) {
      team(id: $teamId) {
        labels { nodes { id name } }
      }
    }
    """
    data = graphql(api_key, query, {"teamId": team_id})
    by_name = {n["name"]: n["id"] for n in data["team"]["labels"]["nodes"]}
    missing = [n for n in names if n not in by_name]
    if missing:
        raise LinearCreateError(f"Labels not found on team: {missing}")
    return [by_name[n] for n in names]


def create_issue(
    api_key: str,
    *,
    team_id: str,
    title: str,
    description: str,
    label_ids: list[str],
    parent_id: str | None = None,
) -> dict:
    mutation = """
    mutation CreateIssue($input: IssueCreateInput!) {
      issueCreate(input: $input) {
        success
        issue {
          id
          identifier
          title
          url
        }
      }
    }
    """
    issue_input: dict = {
        "teamId": team_id,
        "title": title,
        "description": description,
        "labelIds": label_ids,
    }
    if parent_id:
        issue_input["parentId"] = parent_id
    data = graphql(api_key, mutation, {"input": issue_input})
    result = data["issueCreate"]
    if not result["success"]:
        raise LinearCreateError("issueCreate returned success=false")
    return result["issue"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--description-file", type=str, default="")
    parser.add_argument("--label", action="append", default=[], dest="labels")
    parser.add_argument("--parent-id", default="", help="Linear issue id (UUID) for sub-issues")
    parser.add_argument(
        "--team",
        default="",
        help="Linear team name (overrides LINEAR_TEAM_NAME)",
    )
    args = parser.parse_args(argv)

    api_key = os.environ.get("LINEAR_API_KEY", "").strip()
    if not api_key:
        print(
            "Set LINEAR_API_KEY (Linear → Settings → API → Personal API keys).",
            file=sys.stderr,
        )
        return EXIT_NO_KEY

    try:
        team_name = resolve_team_name(args.team, os.environ)
        description = args.description
        if args.description_file:
            with open(args.description_file, encoding="utf-8") as handle:
                description = handle.read()

        team = fetch_team(api_key, team_name)
        label_ids = fetch_label_ids(api_key, team["id"], args.labels) if args.labels else []
        parent_id = args.parent_id.strip() or None

        issue = create_issue(
            api_key,
            team_id=team["id"],
            title=args.title,
            description=description,
            label_ids=label_ids,
            parent_id=parent_id,
        )
    except LinearCreateError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_HARD_FAILURE

    print(json.dumps(issue, indent=2))
    return EXIT_OK


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as exc:
        print(exc.read().decode(), file=sys.stderr)
        raise SystemExit(EXIT_HARD_FAILURE) from exc
    except LinearCreateError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(EXIT_HARD_FAILURE) from exc
