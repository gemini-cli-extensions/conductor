#!/usr/bin/env python3
"""Upstream Sync Bot for Conductor

Synchronizes from upstream repositories:
- gemini-cli-extensions/conductor (primary)
- jnorthrup/conductor2 (secondary)

Usage:
    python scripts/sync_upstream.py [--dry-run] [--source SOURCE]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Colors:
    """Terminal colors"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


class UpstreamSync:
    """Syncs from upstream repositories"""

    UPSTREAMS = {
        "gemini-cli-extensions": {
            "name": "gemini-cli-extensions/conductor",
            "url": "https://github.com/gemini-cli-extensions/conductor.git",
            "priority": "primary",
        },
        "jnorthrup": {
            "name": "jnorthrup/conductor2",
            "url": "https://github.com/jnorthrup/conductor2.git",
            "priority": "secondary",
        },
    }

    def __init__(self, base_path: Path = Path("."), dry_run: bool = False):
        self.base_path = base_path.resolve()
        self.dry_run = dry_run
        self.sync_results: Dict[str, Dict] = {}
        self.errors: List[str] = []

    def log(self, message: str, color: str = "") -> None:
        """Print colored message"""
        if color and sys.stdout.isatty():
            print(f"{color}{message}{Colors.END}")
        else:
            print(message)

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None, check: bool = False) -> Tuple[int, str, str]:
        """Run a git command"""
        if self.dry_run:
            self.log(f"[DRY-RUN] Would run: {' '.join(cmd)}", Colors.YELLOW)
            return 0, "", ""

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if check and result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def add_upstream_remote(self, source: str) -> bool:
        """Add upstream remote if not exists"""
        upstream = self.UPSTREAMS.get(source)
        if not upstream:
            self.log(f"❌ Unknown upstream source: {source}", Colors.RED)
            return False

        remote_name = f"upstream-{source}"

        # Check if remote already exists
        code, stdout, stderr = self.run_command(["git", "remote", "-v"])
        if remote_name in stdout:
            self.log(f"✅ Remote {remote_name} already exists", Colors.GREEN)
            return True

        # Add remote
        self.log(f"📡 Adding remote {remote_name}...", Colors.BLUE)
        code, stdout, stderr = self.run_command(["git", "remote", "add", remote_name, upstream["url"]])

        if code == 0:
            self.log(f"✅ Added remote {remote_name}", Colors.GREEN)
            return True
        else:
            self.log(f"❌ Failed to add remote: {stderr}", Colors.RED)
            return False

    def fetch_upstream(self, source: str) -> bool:
        """Fetch from upstream repository"""
        remote_name = f"upstream-{source}"
        upstream = self.UPSTREAMS.get(source)

        self.log(f"\n🔄 Fetching from {upstream['name']}...", Colors.BLUE)

        code, stdout, stderr = self.run_command(["git", "fetch", remote_name, "--tags"])

        if code == 0:
            self.log(f"✅ Fetched successfully", Colors.GREEN)
            return True
        else:
            self.log(f"❌ Fetch failed: {stderr}", Colors.RED)
            return False

    def compare_branches(self, source: str) -> Dict:
        """Compare local and upstream branches"""
        remote_name = f"upstream-{source}"

        # Get current branch
        code, stdout, stderr = self.run_command(["git", "branch", "--show-current"])
        current_branch = stdout.strip() if code == 0 else "main"

        # Compare commits
        local_ref = f"HEAD"
        remote_ref = f"{remote_name}/{current_branch}"

        # Check if remote branch exists
        code, stdout, stderr = self.run_command(["git", "rev-parse", "--verify", remote_ref])

        if code != 0:
            # Try main instead of current branch
            remote_ref = f"{remote_name}/main"
            code, stdout, stderr = self.run_command(["git", "rev-parse", "--verify", remote_ref])

            if code != 0:
                return {
                    "source": source,
                    "ahead": 0,
                    "behind": 0,
                    "diverged": False,
                    "error": "Remote branch not found",
                }

        # Count commits behind
        code, stdout, stderr = self.run_command(["git", "rev-list", "--count", f"{local_ref}..{remote_ref}"])
        behind = int(stdout.strip()) if code == 0 else 0

        # Count commits ahead
        code, stdout, stderr = self.run_command(["git", "rev-list", "--count", f"{remote_ref}..{local_ref}"])
        ahead = int(stdout.strip()) if code == 0 else 0

        # Check if diverged
        diverged = ahead > 0 and behind > 0

        return {
            "source": source,
            "ahead": ahead,
            "behind": behind,
            "diverged": diverged,
            "local_branch": current_branch,
            "remote_branch": remote_ref,
        }

    def create_sync_branch(self, source: str) -> Optional[str]:
        """Create a branch for syncing changes"""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"sync-{source}-{timestamp}"

        self.log(f"🌿 Creating branch: {branch_name}", Colors.BLUE)

        code, stdout, stderr = self.run_command(["git", "checkout", "-b", branch_name])

        if code == 0:
            self.log(f"✅ Created branch {branch_name}", Colors.GREEN)
            return branch_name
        else:
            self.log(f"❌ Failed to create branch: {stderr}", Colors.RED)
            return None

    def merge_upstream(self, source: str, branch: str) -> bool:
        """Merge upstream changes into current branch"""
        remote_name = f"upstream-{source}"
        upstream = self.UPSTREAMS.get(source)

        self.log(f"🔀 Merging {upstream['name']}...", Colors.BLUE)

        # Get current branch
        code, stdout, stderr = self.run_command(["git", "branch", "--show-current"])
        current_branch = stdout.strip() if code == 0 else "main"

        # Try to merge
        remote_ref = f"{remote_name}/{current_branch}"
        code, stdout, stderr = self.run_command(["git", "merge", remote_ref, "--no-edit"])

        if code == 0:
            self.log(f"✅ Merged successfully", Colors.GREEN)
            return True
        else:
            # Check if it's a conflict
            if "CONFLICT" in stderr or "conflict" in stderr.lower():
                self.log(f"⚠️  Merge conflict detected!", Colors.YELLOW)
                self.log(f"   Manual resolution required", Colors.YELLOW)
                return False
            else:
                self.log(f"❌ Merge failed: {stderr}", Colors.RED)
                return False

    def generate_diff_summary(self, source: str) -> str:
        """Generate a summary of changes"""
        remote_name = f"upstream-{source}"

        # Get list of changed files
        code, stdout, stderr = self.run_command(["git", "diff", "--name-only", f"HEAD..{remote_name}/main"])

        if code == 0:
            files = stdout.strip().split("\n") if stdout.strip() else []
            return f"Changed files: {len(files)}"
        return "Could not generate summary"

    def sync_source(self, source: str) -> Dict:
        """Sync from a specific upstream source"""
        self.log(f"\n{'=' * 60}", Colors.BLUE)
        self.log(f"Syncing from: {self.UPSTREAMS[source]['name']}", Colors.BLUE)
        self.log(f"{'=' * 60}", Colors.BLUE)

        result = {
            "source": source,
            "success": False,
            "changes": 0,
            "conflicts": False,
            "branch": None,
        }

        # Add remote
        if not self.add_upstream_remote(source):
            result["error"] = "Failed to add remote"
            return result

        # Fetch
        if not self.fetch_upstream(source):
            result["error"] = "Failed to fetch"
            return result

        # Compare branches
        comparison = self.compare_branches(source)
        self.log(f"\n📊 Comparison:", Colors.BLUE)
        self.log(
            f"   Behind: {comparison['behind']} commits", Colors.YELLOW if comparison["behind"] > 0 else Colors.GREEN
        )
        self.log(f"   Ahead: {comparison['ahead']} commits", Colors.YELLOW if comparison["ahead"] > 0 else Colors.GREEN)
        self.log(
            f"   Diverged: {'Yes' if comparison['diverged'] else 'No'}",
            Colors.YELLOW if comparison["diverged"] else Colors.GREEN,
        )

        if comparison["behind"] == 0:
            self.log(f"\n✅ Already up to date!", Colors.GREEN)
            result["success"] = True
            result["changes"] = 0
            return result

        # Create sync branch
        if not self.dry_run:
            branch = self.create_sync_branch(source)
            if not branch:
                result["error"] = "Failed to create sync branch"
                return result
            result["branch"] = branch

        # Merge
        if comparison["diverged"]:
            self.log(f"\n⚠️  Branches have diverged!", Colors.YELLOW)
            self.log(f"   Creating PR for manual review", Colors.YELLOW)
            result["conflicts"] = True
        else:
            if self.merge_upstream(source, branch if not self.dry_run else ""):
                result["success"] = True
                result["changes"] = comparison["behind"]
                self.log(f"\n✅ Synced {comparison['behind']} commit(s)", Colors.GREEN)
            else:
                result["error"] = "Merge failed"
                result["conflicts"] = True

        return result

    def sync_all(self, sources: Optional[List[str]] = None) -> bool:
        """Sync from all or specified upstream sources"""
        if sources is None:
            sources = list(self.UPSTREAMS.keys())

        self.log("\n🚀 Conductor Upstream Sync Bot", Colors.BLUE)
        self.log(f"{'=' * 60}", Colors.BLUE)
        self.log(f"Base path: {self.base_path}")
        self.log(f"Sources: {', '.join(sources)}")
        if self.dry_run:
            self.log("Mode: DRY-RUN (no changes will be made)", Colors.YELLOW)
        self.log(f"{'=' * 60}\n", Colors.BLUE)

        all_success = True

        for source in sources:
            if source not in self.UPSTREAMS:
                self.log(f"❌ Unknown source: {source}", Colors.RED)
                all_success = False
                continue

            result = self.sync_source(source)
            self.sync_results[source] = result

            if not result["success"] and not result.get("conflicts"):
                all_success = False

        self.print_summary()
        return all_success

    def print_summary(self) -> None:
        """Print sync summary"""
        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("SYNC SUMMARY", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        total_changes = 0
        total_conflicts = 0

        for source, result in self.sync_results.items():
            upstream_name = self.UPSTREAMS[source]["name"]

            if result["success"]:
                if result["changes"] > 0:
                    self.log(f"\n✅ {upstream_name}: Synced {result['changes']} commit(s)", Colors.GREEN)
                    if result.get("branch"):
                        self.log(f"   Branch: {result['branch']}", Colors.BLUE)
                else:
                    self.log(f"\n✅ {upstream_name}: Already up to date", Colors.GREEN)
            elif result.get("conflicts"):
                self.log(f"\n⚠️  {upstream_name}: Conflicts detected", Colors.YELLOW)
                if result.get("branch"):
                    self.log(f"   Branch: {result['branch']} (needs manual merge)", Colors.YELLOW)
                total_conflicts += 1
            else:
                self.log(f"\n❌ {upstream_name}: Failed - {result.get('error', 'Unknown error')}", Colors.RED)

            total_changes += result.get("changes", 0)

        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log(f"Total changes: {total_changes}", Colors.BLUE)
        self.log(f"Conflicts: {total_conflicts}", Colors.YELLOW if total_conflicts > 0 else Colors.GREEN)
        self.log("=" * 60 + "\n", Colors.BLUE)

        if total_conflicts > 0:
            self.log("⚠️  Some syncs have conflicts and need manual resolution.", Colors.YELLOW)
            self.log("   Please review the branches and create PRs for manual merge.\n", Colors.YELLOW)

    def save_state(self) -> None:
        """Save sync state to file"""
        state_file = self.base_path / ".upstream-sync-state.json"
        state = {
            "last_sync": datetime.now().isoformat(),
            "results": self.sync_results,
        }

        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Sync from upstream repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/sync_upstream.py                    # Sync all sources
  python scripts/sync_upstream.py --source gemini    # Sync specific source
  python scripts/sync_upstream.py --dry-run          # Preview changes only
        """,
    )

    parser.add_argument(
        "--source",
        choices=["gemini-cli-extensions", "jnorthrup"],
        help="Sync from specific upstream source only",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without making them",
    )
    parser.add_argument(
        "--save-state",
        action="store_true",
        help="Save sync state to file",
    )

    args = parser.parse_args()

    sync = UpstreamSync(dry_run=args.dry_run)

    sources = [args.source] if args.source else None
    success = sync.sync_all(sources)

    if args.save_state:
        sync.save_state()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
