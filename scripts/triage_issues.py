#!/usr/bin/env python3
"""Issue Triage Bot for Conductor

Analyzes GitHub issues from upstream repositories and creates
tracks for applicable issues.

Usage:
    python scripts/triage_issues.py [--dry-run] [--create-tracks]
"""

import argparse
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Optional


class Colors:
    """Terminal colors"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


class IssueTriager:
    """Triages GitHub issues and creates conductor tracks"""

    # High-priority issues to track
    TRACKABLE_ISSUES = {
        "113": {"title": "Auto-create .gitignore on git init", "priority": "high"},
        "112": {"title": "Update workflow with overwrite confirmation", "priority": "high"},
        "108": {"title": "Fix TOML references", "priority": "medium"},
        "105": {"title": "AskUser tool integration", "priority": "high"},
        "103": {"title": "Auto-update metadata.json timestamps", "priority": "medium"},
        "97": {"title": "Single commit option", "priority": "medium"},
        "96": {"title": "Separate metadata/output commits", "priority": "low"},
        "115": {"title": "Multi-agent support", "priority": "high"},
    }

    UPSTREAM_REPO = "gemini-cli-extensions/conductor"

    def __init__(self, base_path: Path = Path(), dry_run: bool = False) -> None:
        self.base_path = base_path.resolve()
        self.dry_run = dry_run
        self.issues_analyzed: list[dict] = []
        self.tracks_created: list[str] = []

    def log(self, message: str, color: str = "") -> None:
        """Print colored message"""
        if color and sys.stdout.isatty():
            print(f"{color}{message}{Colors.END}")
        else:
            print(message)

    def fetch_issues(self, state: str = "open") -> list[dict]:
        """Fetch issues from GitHub API"""
        self.log(f"\n[FETCH] Fetching {state} issues from {self.UPSTREAM_REPO}...", Colors.BLUE)

        try:
            url = f"https://api.github.com/repos/{self.UPSTREAM_REPO}/issues?state={state}&per_page=100"
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "conductor-triage")

            with urllib.request.urlopen(req, timeout=30) as response:
                issues = json.loads(response.read().decode())
                # Filter out PRs (they are also returned as issues)
                issues = [i for i in issues if "pull_request" not in i]
                self.log(f"[PASS] Fetched {len(issues)} issues", Colors.GREEN)
                return issues
        except Exception as e:
            self.log(f"[FAIL] Failed to fetch issues: {e}", Colors.RED)
            return []

    def classify_issue(self, issue: dict) -> dict:
        """Classify an issue by type and priority"""
        title = issue.get("title", "").lower()
        body = issue.get("body", "").lower()
        labels = [label["name"].lower() for label in issue.get("labels", [])]

        # Determine type
        issue_type = "other"
        if "bug" in labels or "bug" in title:
            issue_type = "bug"
        elif "feature" in labels or "enhancement" in labels:
            issue_type = "feature"
        elif "documentation" in labels or "docs" in labels:
            issue_type = "docs"

        # Determine priority
        priority = "medium"
        if "priority:high" in labels or "high" in labels:
            priority = "high"
        elif "priority:low" in labels or "low" in labels:
            priority = "low"

        # Check if it's in our trackable list
        issue_num = str(issue.get("number", ""))
        is_trackable = issue_num in self.TRACKABLE_ISSUES

        if is_trackable:
            priority = self.TRACKABLE_ISSUES[issue_num]["priority"]

        return {
            "number": issue_num,
            "title": issue.get("title", ""),
            "type": issue_type,
            "priority": priority,
            "is_trackable": is_trackable,
            "url": issue.get("html_url", ""),
            "state": issue.get("state", ""),
        }

    def analyze_issues(self, issues: list[dict]) -> list[dict]:
        """Analyze all issues"""
        self.log("\n[SCAN] Analyzing issues...", Colors.BLUE)

        analyzed = []
        for issue in issues:
            classification = self.classify_issue(issue)
            analyzed.append(classification)

        return analyzed

    def should_create_track(self, issue: dict) -> bool:
        """Determine if we should create a track for this issue"""
        # Only create tracks for trackable issues
        if not issue["is_trackable"]:
            return False

        # Check if track already exists
        track_id = f"issue_{issue['number']}"
        tracks_md = self.base_path / "conductor" / "tracks.md"

        if tracks_md.exists():
            content = tracks_md.read_text()
            if track_id in content:
                return False

        return True

    def create_track(self, issue: dict) -> Optional[str]:
        """Create a conductor track for an issue"""
        issue_num = issue["number"]
        track_id = f"issue_{issue_num}_{datetime.now().strftime('%Y%m%d')}"

        self.log(f"\n[WRITE] Creating track for Issue #{issue_num}...", Colors.BLUE)

        if self.dry_run:
            self.log(f"[DRY-RUN] Would create track: {track_id}", Colors.YELLOW)
            return track_id

        # Create track directory
        track_dir = self.base_path / "conductor" / "tracks" / track_id
        track_dir.mkdir(parents=True, exist_ok=True)

        # Create index.md
        index_content = f"""# Track: {issue["title"]}

## Issue #{issue_num}

- **URL**: {issue["url"]}
- **Priority**: {issue["priority"]}
- **Type**: {issue["type"]}

## Links

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
"""
        (track_dir / "index.md").write_text(index_content)

        # Create spec.md
        spec_content = f"""# Specification: {issue["title"]}

## Overview

This track addresses Issue #{issue_num} from upstream repository.

**Original Issue**: [{issue["title"]}]({issue["url"]})

## Goals

- [ ] Analyze the issue requirements
- [ ] Design solution approach
- [ ] Implement the fix/feature
- [ ] Test the implementation
- [ ] Update documentation if needed

## Acceptance Criteria

- [ ] Issue #{issue_num} is resolved
- [ ] Solution follows conductor patterns
- [ ] Tests pass
- [ ] Documentation updated

## References

- Original Issue: {issue["url"]}
- Priority: {issue["priority"]}
"""
        (track_dir / "spec.md").write_text(spec_content)

        # Create plan.md
        plan_content = f"""# Implementation Plan: {issue["title"]}

## Phase 1: Analysis

- [ ] Review original issue #{issue_num}
- [ ] Understand current implementation
- [ ] Identify affected components
- [ ] Document findings

## Phase 2: Design

- [ ] Design solution approach
- [ ] Consider edge cases
- [ ] Plan testing strategy
- [ ] Update this plan with specific tasks

## Phase 3: Implementation

- [ ] Implement the solution
- [ ] Write tests
- [ ] Update documentation
- [ ] Run validation

## Phase 4: Verification

- [ ] Test the implementation
- [ ] Verify fix works as expected
- [ ] Check for regressions
- [ ] Complete conductor verification protocol
"""
        (track_dir / "plan.md").write_text(plan_content)

        # Update tracks.md
        self._add_track_to_registry(track_id, issue)

        self.log(f"[PASS] Created track: {track_id}", Colors.GREEN)
        return track_id

    def _add_track_to_registry(self, track_id: str, issue: dict) -> None:
        """Add track to tracks.md registry"""
        tracks_md = self.base_path / "conductor" / "tracks.md"

        entry = f"""
---

- [ ] **Track: Issue #{issue["number"]} - {issue["title"]}**
*Link: [./tracks/{track_id}/](./tracks/{track_id}/)*
- **Priority**: {issue["priority"]}
- **Source**: [{self.UPSTREAM_REPO}#{issue["number"]}]({issue["url"]})
"""

        if tracks_md.exists():
            content = tracks_md.read_text()
            # Add before the end or after existing tracks
            if "# Project Tracks" in content:
                content = content.rstrip() + entry
                tracks_md.write_text(content)
            else:
                # Create new tracks.md
                header = "# Project Tracks\n\nThis file tracks all issues from upstream repositories.\n"
                tracks_md.write_text(header + entry)

    def run_triage(self, create_tracks: bool = False) -> bool:
        """Run full triage process"""
        self.log("\n[START] Conductor Issue Triage Bot", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        # Fetch issues
        issues = self.fetch_issues()
        if not issues:
            self.log("[FAIL] No issues to triage", Colors.RED)
            return False

        # Analyze issues
        self.issues_analyzed = self.analyze_issues(issues)

        # Print summary
        self.print_summary()

        # Create tracks for trackable issues
        if create_tracks:
            trackable = [i for i in self.issues_analyzed if self.should_create_track(i)]
            self.log(f"\n[WRITE] Creating tracks for {len(trackable)} trackable issues...", Colors.BLUE)

            for issue in trackable:
                track_id = self.create_track(issue)
                if track_id:
                    self.tracks_created.append(track_id)

            self.log(f"\n[PASS] Created {len(self.tracks_created)} track(s)", Colors.GREEN)

        return True

    def print_summary(self) -> None:
        """Print triage summary"""
        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("TRIAGE SUMMARY", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        # Count by type
        by_type = {}
        by_priority = {}
        trackable_count = 0

        for issue in self.issues_analyzed:
            issue_type = issue["type"]
            priority = issue["priority"]

            by_type[issue_type] = by_type.get(issue_type, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1

            if issue["is_trackable"]:
                trackable_count += 1

        self.log(f"\n[STATS] Total issues analyzed: {len(self.issues_analyzed)}", Colors.BLUE)

        self.log("\nBy Type:", Colors.BLUE)
        for issue_type, count in sorted(by_type.items()):
            self.log(f"  {issue_type}: {count}")

        self.log("\nBy Priority:", Colors.BLUE)
        for priority in ["high", "medium", "low"]:
            if priority in by_priority:
                color = Colors.RED if priority == "high" else Colors.YELLOW if priority == "medium" else Colors.GREEN
                self.log(f"  {priority}: {by_priority[priority]}", color)

        self.log(f"\n[TARGET] Trackable issues: {trackable_count}", Colors.YELLOW)

        # List trackable issues
        if trackable_count > 0:
            self.log("\nTrackable Issues:", Colors.YELLOW)
            for issue in self.issues_analyzed:
                if issue["is_trackable"]:
                    color = Colors.RED if issue["priority"] == "high" else Colors.YELLOW
                    self.log(f"  #{issue['number']}: {issue['title'][:50]}...", color)

        self.log("\n" + "=" * 60, Colors.BLUE)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Triage GitHub issues from upstream",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/triage_issues.py                    # Analyze only
  python scripts/triage_issues.py --create-tracks    # Create tracks
  python scripts/triage_issues.py --dry-run          # Preview only
        """,
    )

    parser.add_argument(
        "--create-tracks",
        action="store_true",
        help="Create conductor tracks for applicable issues",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without creating tracks",
    )

    args = parser.parse_args()

    triager = IssueTriager(dry_run=args.dry_run)
    success = triager.run_triage(create_tracks=args.create_tracks)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
