#!/usr/bin/env python3
"""Deterministic non-MCP Linear transport for hooks, CI, and headless sessions.

The Linear MCP (Cursor Linear plugin / claude.ai Linear connector) is the primary
path for interactive agent sessions. This CLI is the deterministic fallback: plain
GraphQL over LINEAR_API_KEY, no OAuth, no browser. Skills follow
**Linear MCP -> linear_cli.py -> ask the user**.

Requires LINEAR_API_KEY (Linear -> Settings -> API -> Personal API keys). See
conductor/linear.md in the consuming project for team identity.

Verbs:
  get-issue ABC-12              # JSON: identifier, title, description, state, labels, parent, url
  list-sub-issues ABC-12        # JSON list: identifier, title, state
  set-state ABC-12 "In Progress"
  comment ABC-12 "body markdown"

Exit codes (fail-open friendly for hook callers):
  0  success
  2  LINEAR_API_KEY not set (degraded — caller should fall back, not treat as error)
  1  hard failure after retries (network/API/validation)

Usage:
  LINEAR_API_KEY=lin_api_... python scripts/linear_cli.py get-issue ABC-12
  LINEAR_API_KEY=lin_api_... python scripts/linear_cli.py set-state ABC-12 "In Progress"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

GRAPHQL_URL = "https://api.linear.app/graphql"

# Bounded retry on transient transport errors.
_MAX_ATTEMPTS = 4
_BACKOFF_SECONDS = (2, 4, 8)

EXIT_OK = 0
EXIT_HARD_FAILURE = 1
EXIT_NO_KEY = 2


class LinearCliError(RuntimeError):
    """A hard failure that should surface as EXIT_HARD_FAILURE."""


def _sleep(seconds: float) -> None:  # indirection kept simple for test monkeypatching
    time.sleep(seconds)


def graphql(api_key: str, query: str, variables: dict | None = None) -> dict:
    """POST a GraphQL request, retrying transient transport errors with backoff.

    HTTP 429 and 5xx and URLError (network) are retried; GraphQL-level `errors`
    and 4xx (other than 429) fail immediately — retrying would not help.
    """
    payload = json.dumps({"query": query, "variables": variables or {}}).encode()
    last_exc: Exception | None = None
    for attempt in range(_MAX_ATTEMPTS):
        req = urllib.request.Request(
            GRAPHQL_URL,
            data=payload,
            headers={"Authorization": api_key, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode())
            if body.get("errors"):
                raise LinearCliError(json.dumps(body["errors"], indent=2))
            return body["data"]
        except urllib.error.HTTPError as exc:
            if exc.code != 429 and exc.code < 500:
                detail = exc.read().decode(errors="replace") if exc.fp else ""
                raise LinearCliError(f"HTTP {exc.code}: {detail}") from exc
            last_exc = exc
        except urllib.error.URLError as exc:
            last_exc = exc
        if attempt < _MAX_ATTEMPTS - 1:
            _sleep(_BACKOFF_SECONDS[attempt])
    raise LinearCliError(f"GraphQL request failed after {_MAX_ATTEMPTS} attempts: {last_exc}")


def _issue_by_identifier(api_key: str, identifier: str) -> dict:
    """Resolve PREFIX-XXX to its issue node (Linear `issue(id:)` accepts identifiers)."""
    query = """
    query Issue($id: String!) {
      issue(id: $id) {
        id
        identifier
        title
        description
        url
        state { name type }
        labels { nodes { name } }
        parent { identifier title }
        team { id }
      }
    }
    """
    data = graphql(api_key, query, {"id": identifier})
    issue = data.get("issue")
    if not issue:
        raise LinearCliError(f"Issue not found: {identifier}")
    return issue


def cmd_get_issue(api_key: str, identifier: str) -> dict:
    issue = _issue_by_identifier(api_key, identifier)
    return {
        "identifier": issue["identifier"],
        "title": issue["title"],
        "description": issue.get("description") or "",
        "state": (issue.get("state") or {}).get("name"),
        "state_type": (issue.get("state") or {}).get("type"),
        "labels": [n["name"] for n in (issue.get("labels") or {}).get("nodes", [])],
        "parent": (issue.get("parent") or {}).get("identifier"),
        "url": issue.get("url"),
    }


def cmd_list_sub_issues(api_key: str, identifier: str) -> list[dict]:
    query = """
    query SubIssues($id: String!) {
      issue(id: $id) {
        children { nodes { identifier title state { name } } }
      }
    }
    """
    data = graphql(api_key, query, {"id": identifier})
    issue = data.get("issue")
    if not issue:
        raise LinearCliError(f"Issue not found: {identifier}")
    return [
        {
            "identifier": n["identifier"],
            "title": n["title"],
            "state": (n.get("state") or {}).get("name"),
        }
        for n in (issue.get("children") or {}).get("nodes", [])
    ]


def _resolve_state_id(api_key: str, team_id: str, state_name: str) -> str:
    query = """
    query TeamStates($teamId: String!) {
      team(id: $teamId) { states { nodes { id name } } }
    }
    """
    data = graphql(api_key, query, {"teamId": team_id})
    nodes = (((data.get("team") or {}).get("states")) or {}).get("nodes", [])
    for node in nodes:
        if node["name"].strip().lower() == state_name.strip().lower():
            return node["id"]
    available = ", ".join(sorted(n["name"] for n in nodes))
    raise LinearCliError(f"State {state_name!r} not found for team. Available: {available}")


def cmd_set_state(api_key: str, identifier: str, state_name: str) -> dict:
    issue = _issue_by_identifier(api_key, identifier)
    state_id = _resolve_state_id(api_key, issue["team"]["id"], state_name)
    mutation = """
    mutation SetState($id: String!, $stateId: String!) {
      issueUpdate(id: $id, input: { stateId: $stateId }) {
        success
        issue { identifier state { name } }
      }
    }
    """
    data = graphql(api_key, mutation, {"id": issue["id"], "stateId": state_id})
    result = data["issueUpdate"]
    if not result["success"]:
        raise LinearCliError(f"Failed to set state on {identifier}")
    return {"identifier": identifier, "state": result["issue"]["state"]["name"]}


def cmd_comment(api_key: str, identifier: str, body: str) -> dict:
    issue = _issue_by_identifier(api_key, identifier)
    mutation = """
    mutation Comment($issueId: String!, $body: String!) {
      commentCreate(input: { issueId: $issueId, body: $body }) {
        success
        comment { id }
      }
    }
    """
    data = graphql(api_key, mutation, {"issueId": issue["id"], "body": body})
    result = data["commentCreate"]
    if not result["success"]:
        raise LinearCliError(f"Failed to comment on {identifier}")
    return {"identifier": identifier, "comment_id": result["comment"]["id"]}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="verb", required=True)

    p_get = sub.add_parser("get-issue", help="Fetch one issue as JSON")
    p_get.add_argument("identifier")

    p_sub = sub.add_parser("list-sub-issues", help="List an issue's children as JSON")
    p_sub.add_argument("identifier")

    p_state = sub.add_parser("set-state", help="Move an issue to a named workflow state")
    p_state.add_argument("identifier")
    p_state.add_argument("state")

    p_comment = sub.add_parser("comment", help="Post a markdown comment to an issue")
    p_comment.add_argument("identifier")
    p_comment.add_argument("body")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    api_key = os.environ.get("LINEAR_API_KEY", "").strip()
    if not api_key:
        print(
            "LINEAR_API_KEY not set — cannot reach Linear via the CLI fallback.\n"
            "Set it (Linear -> Settings -> API -> Personal API keys) or use the Linear MCP.\n"
            "See conductor/linear.md.",
            file=sys.stderr,
        )
        return EXIT_NO_KEY

    try:
        if args.verb == "get-issue":
            result: object = cmd_get_issue(api_key, args.identifier)
        elif args.verb == "list-sub-issues":
            result = cmd_list_sub_issues(api_key, args.identifier)
        elif args.verb == "set-state":
            result = cmd_set_state(api_key, args.identifier, args.state)
        elif args.verb == "comment":
            result = cmd_comment(api_key, args.identifier, args.body)
        else:  # pragma: no cover - argparse enforces the choices
            raise LinearCliError(f"Unknown verb: {args.verb}")
    except LinearCliError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_HARD_FAILURE

    print(json.dumps(result, indent=2))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
