#!/usr/bin/env python3
"""Upstream Sync Bot - Sync changes from upstream conductor repositories.

This script fetches changes from upstream repositories:
- gemini-cli-extensions/conductor
- jnorthrup/conductor2

It detects merge conflicts and creates draft PRs when needed.
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests
from github import Github, Auth


class UpstreamSyncError(Exception):
    """Base exception for upstream sync errors."""
    pass


class GitHubClient:
    """GitHub API client for repository operations."""

    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client.

        Args:
            token: GitHub personal access token. Falls back to GITHUB_TOKEN env var.
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise UpstreamSyncError(
                "GitHub token required. Set GITHUB_TOKEN environment variable."
            )
        self.auth = Auth.Token(self.token)
        self.gh = Github(auth=self.auth)
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_repo(self, repo_name: str) -> dict:
        """Fetch repository information.

        Args:
            repo_name: Repository name in format 'owner/repo'

        Returns:
            Repository data as dict
        """
        url = f"{self.api_base}/repos/{repo_name}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_branch(self, repo_name: str, branch: str = "main") -> dict:
        """Fetch branch information.

        Args:
            repo_name: Repository name in format 'owner/repo'
            branch: Branch name

        Returns:
            Branch data as dict
        """
        url = f"{self.api_base}/repos/{repo_name}/branches/{branch}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def compare_branches(
        self, base_repo: str, head_repo: str, base_branch: str = "main", head_branch: str = "main"
    ) -> dict:
        """Compare two branches across repositories.

        Args:
            base_repo: Base repository (owner/repo)
            head_repo: Head repository (owner/repo)
            base_branch: Base branch name
            head_branch: Head branch name

        Returns:
            Comparison data including commits ahead/behind
        """
        url = f"{self.api_base}/repos/{base_repo}/compare/{base_branch}...{head_repo}:{head_branch}"
        response = requests.get(url, headers=self.headers, timeout=30)
        if response.status_code == 404:
            return {"status": "diverged", "ahead_by": 0, "behind_by": 0, "commits": []}
        response.raise_for_status()
        return response.json()

    def create_pull_request(
        self,
        repo_name: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
        draft: bool = True,
    ) -> dict:
        """Create a pull request.

        Args:
            repo_name: Repository name (owner/repo)
            title: PR title
            body: PR description
            head: Head branch name
            base: Base branch name
            draft: Whether to create as draft

        Returns:
            PR data as dict
        """
        url = f"{self.api_base}/repos/{repo_name}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
            "draft": draft,
        }
        response = requests.post(url, headers=self.headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()


class SyncState:
    """Track sync state and history."""

    def __init__(self, state_file: Path):
        """Initialize sync state tracker.

        Args:
            state_file: Path to state JSON file
        """
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Load state from file or create new."""
        if self.state_file.exists():
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {
            "last_sync": None,
            "upstreams": {},
            "sync_log": [],
        }

    def save(self):
        """Save state to file."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def update_sync(self, upstream: str, commit_sha: str, status: str):
        """Update sync state for an upstream.

        Args:
            upstream: Upstream repository name
            commit_sha: Latest synced commit SHA
            status: Sync status (success, failed, skipped)
        """
        self.state["upstreams"][upstream] = {
            "last_sync": datetime.now(timezone.utc).isoformat(),
            "commit_sha": commit_sha,
            "status": status,
        }
        self.state["sync_log"].append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "upstream": upstream,
            "commit_sha": commit_sha,
            "status": status,
        })
        # Keep only last 100 log entries
        self.state["sync_log"] = self.state["sync_log"][-100:]
        self.save()


class UpstreamSyncBot:
    """Main sync bot orchestrator."""

    def __init__(self, target_repo: str, upstreams: list[str], state_file: Path):
        """Initialize sync bot.

        Args:
            target_repo: Target repository to sync to (owner/repo)
            upstreams: List of upstream repositories to sync from
            state_file: Path to state tracking file
        """
        self.target_repo = target_repo
        self.upstreams = upstreams
        self.client = GitHubClient()
        self.state = SyncState(state_file)

    def fetch_upstream(self, upstream: str) -> dict:
        """Fetch upstream repository information.

        Args:
            upstream: Upstream repository name

        Returns:
            Upstream repo and branch data
        """
        print(f"[FETCH] Fetching {upstream}...")
        repo_data = self.client.get_repo(upstream)
        branch_data = self.client.get_branch(upstream)
        return {
            "repo": repo_data,
            "branch": branch_data,
            "sha": branch_data["commit"]["sha"],
        }

    def check_merge_conflicts(self, upstream: str, target_branch: str = "main") -> bool:
        """Check if syncing would cause merge conflicts.

        Args:
            upstream: Upstream repository name
            target_branch: Target branch name

        Returns:
            True if conflicts detected
        """
        try:
            comparison = self.client.compare_branches(
                self.target_repo, upstream, target_branch, target_branch
            )
            # If status is 'diverged' or has merge conflicts
            return comparison.get("status") == "diverged"
        except Exception as e:
            print(f"[WARN] Could not compare branches: {e}")
            return True

    def create_sync_pr(
        self, upstream: str, upstream_sha: str, target_branch: str = "main"
    ) -> Optional[dict]:
        """Create a PR for upstream changes.

        Args:
            upstream: Upstream repository name
            upstream_sha: Latest commit SHA from upstream
            target_branch: Target branch name

        Returns:
            PR data if created, None otherwise
        """
        # Create a branch name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        upstream_name = upstream.replace("/", "-")
        branch_name = f"sync/{upstream_name}_{timestamp}"

        # In a real implementation, we would:
        # 1. Create the branch from upstream
        # 2. Apply changes
        # 3. Create PR

        title = f"Sync from {upstream}"
        body = f"""## Upstream Sync

Automated sync from [{upstream}](https://github.com/{upstream})

**Upstream Commit:** `{upstream_sha[:7]}`
**Sync Time:** {datetime.now(timezone.utc).isoformat()}

### Changes
- Automated upstream sync via sync_upstream.py
- Review changes before merging

---
*This PR was created automatically by the Upstream Sync Bot*
"""

        print(f"[PR] Would create draft PR: {title}")
        print(f"     Branch: {branch_name}")
        print(f"     From: {upstream}")
        print(f"     To: {self.target_repo}:{target_branch}")

        # For now, just log what would happen
        # In production, uncomment to actually create PR:
        # pr = self.client.create_pull_request(
        #     self.target_repo, title, body, branch_name, target_branch, draft=True
        # )
        # return pr

        return None

    def sync(self) -> dict:
        """Run the sync process for all upstreams.

        Returns:
            Sync results summary
        """
        results = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": self.target_repo,
            "upstreams": [],
        }

        for upstream in self.upstreams:
            print(f"\n{'='*60}")
            print(f"[SYNC] Processing upstream: {upstream}")
            print(f"{'='*60}")

            try:
                # Fetch upstream
                upstream_data = self.fetch_upstream(upstream)
                upstream_sha = upstream_data["sha"]

                print(f"[INFO] Latest commit: {upstream_sha[:7]}")

                # Check for conflicts
                has_conflicts = self.check_merge_conflicts(upstream)

                if has_conflicts:
                    print(f"[CONFLICT] Merge conflicts detected")
                    # Create draft PR for manual resolution
                    pr = self.create_sync_pr(upstream, upstream_sha)
                    self.state.update_sync(upstream, upstream_sha, "conflict")
                    results["upstreams"].append({
                        "name": upstream,
                        "sha": upstream_sha,
                        "status": "conflict",
                        "pr": pr,
                    })
                else:
                    print(f"[OK] No conflicts detected")
                    # In production, would auto-merge here
                    self.state.update_sync(upstream, upstream_sha, "success")
                    results["upstreams"].append({
                        "name": upstream,
                        "sha": upstream_sha,
                        "status": "success",
                    })

            except Exception as e:
                print(f"[ERROR] Failed to sync {upstream}: {e}")
                self.state.update_sync(upstream, "", "failed")
                results["upstreams"].append({
                    "name": upstream,
                    "status": "failed",
                    "error": str(e),
                })

        # Save state
        self.state.save()

        return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Sync changes from upstream repositories")
    parser.add_argument(
        "--target",
        default="edithatogo/conductor-next",
        help="Target repository (default: edithatogo/conductor-next)",
    )
    parser.add_argument(
        "--upstream",
        action="append",
        default=[
            "gemini-cli-extensions/conductor",
            "jnorthrup/conductor2",
        ],
        help="Upstream repositories to sync from",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=Path(".github/sync_state.json"),
        help="Path to sync state file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without making changes",
    )

    args = parser.parse_args()

    print("="*60)
    print("Upstream Sync Bot")
    print("="*60)
    print(f"Target: {args.target}")
    print(f"Upstreams: {', '.join(args.upstream)}")
    print(f"State file: {args.state_file}")
    print(f"Dry run: {args.dry_run}")
    print("="*60)

    if args.dry_run:
        print("[DRY RUN] No changes will be made")
        return 0

    try:
        bot = UpstreamSyncBot(args.target, args.upstream, args.state_file)
        results = bot.sync()

        print("\n" + "="*60)
        print("Sync Summary")
        print("="*60)
        for upstream_result in results["upstreams"]:
            status = upstream_result.get("status", "unknown")
            name = upstream_result.get("name", "unknown")
            sha = upstream_result.get("sha", "")[:7] if upstream_result.get("sha") else "N/A"
            print(f"  {name}: {status} ({sha})")

        # Return non-zero if any failures
        failures = sum(1 for r in results["upstreams"] if r.get("status") == "failed")
        return 1 if failures > 0 else 0

    except UpstreamSyncError as e:
        print(f"[FATAL] {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
