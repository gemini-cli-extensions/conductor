#!/usr/bin/env python3
"""Create tracks from upstream GitHub issues.

This script creates conductor tracks for key upstream issues:
- #113: Auto-create .gitignore
- #112: Overwrite confirmation
- #105: AskUser tool integration
- #115: Multi-agent support
- #108, #103, #97, #96: Other issues
"""

import os
import sys
from datetime import datetime, timezone
from pathlib import Path


# Issue definitions with titles and descriptions
UPSTREAM_ISSUES = {
    113: {
        "title": "Auto-create .gitignore for new tracks",
        "description": "Automatically create .gitignore files when creating new conductor tracks",
        "priority": "P1",
        "labels": ["enhancement", "developer-experience"],
    },
    112: {
        "title": "Add overwrite confirmation for file operations",
        "description": "Prompt user before overwriting existing files during track creation or sync",
        "priority": "P1",
        "labels": ["enhancement", "safety"],
    },
    105: {
        "title": "AskUser tool integration for interactive prompts",
        "description": "Integrate AskUser tool for interactive user prompts during conductor operations",
        "priority": "P0",
        "labels": ["enhancement", "user-interaction"],
    },
    115: {
        "title": "Multi-agent support for parallel track execution",
        "description": "Support running multiple conductor agents in parallel for different tracks",
        "priority": "P1",
        "labels": ["enhancement", "multi-agent"],
    },
    108: {
        "title": "Improve error messages for track creation failures",
        "description": "Provide clearer error messages when track creation fails",
        "priority": "P2",
        "labels": ["enhancement", "error-handling"],
    },
    103: {
        "title": "Add track dependency visualization",
        "description": "Create visual representation of track dependencies using Mermaid diagrams",
        "priority": "P2",
        "labels": ["enhancement", "visualization"],
    },
    97: {
        "title": "Support for custom track templates",
        "description": "Allow users to define custom templates for new tracks",
        "priority": "P2",
        "labels": ["enhancement", "customization"],
    },
    96: {
        "title": "Add track completion checklist",
        "description": "Automated checklist for track completion criteria",
        "priority": "P2",
        "labels": ["enhancement", "workflow"],
    },
}


def create_track(issue_number: int, issue_data: dict, tracks_dir: Path) -> Path:
    """Create a track directory with spec.md, plan.md, and metadata.json.

    Args:
        issue_number: GitHub issue number
        issue_data: Issue data (title, description, priority, labels)
        tracks_dir: Base tracks directory

    Returns:
        Path to created track directory
    """
    # Generate track ID
    timestamp = datetime.now().strftime("%Y%m%d")
    track_id = f"issue_{issue_number}_{timestamp}"
    track_dir = tracks_dir / track_id

    # Create directory
    track_dir.mkdir(parents=True, exist_ok=True)
    print(f"[CREATE] {track_dir}")

    # Create spec.md
    spec_content = f"""# Specification: {issue_data['title']}

**Source Issue:** gemini-cli-extensions/conductor#{issue_number}
**Priority:** {issue_data['priority']}
**Labels:** {', '.join(issue_data['labels'])}

## Overview

{issue_data['description']}

This track implements the feature/fix requested in the upstream issue.

## Requirements

### Functional Requirements
- Implement solution for issue #{issue_number}
- Follow conductor track conventions
- Integrate with existing conductor workflows

### Non-Functional Requirements
- Maintain backward compatibility
- Follow existing code style
- Include documentation

## Acceptance Criteria

- [ ] Solution addresses the upstream issue requirements
- [ ] Code follows project conventions
- [ ] Tests pass (if applicable)
- [ ] Documentation updated
- [ ] Track completes successfully

## References

- Upstream Issue: https://github.com/gemini-cli-extensions/conductor/issues/{issue_number}
- Conductor Next: https://github.com/edithatogo/conductor-next
"""

    with open(track_dir / "spec.md", "w") as f:
        f.write(spec_content)

    # Create plan.md
    plan_content = f"""# Implementation Plan: {issue_data['title']}

**Track ID:** {track_id}
**Source:** Upstream Issue #{issue_number}
**Priority:** {issue_data['priority']}

## Phase 1: Analysis

- [ ] Review upstream issue #{issue_number} discussion
- [ ] Identify implementation requirements
- [ ] Document technical approach
- [ ] Create test plan (if applicable)

## Phase 2: Implementation

- [ ] Implement core functionality
- [ ] Add/update tests
- [ ] Update documentation
- [ ] Run quality checks (lint, type check)

## Phase 3: Verification

- [ ] Test implementation
- [ ] Verify against acceptance criteria
- [ ] Code review
- [ ] Mark track complete

## References

- Upstream Issue: https://github.com/gemini-cli-extensions/conductor/issues/{issue_number}
"""

    with open(track_dir / "plan.md", "w") as f:
        f.write(plan_content)

    # Create metadata.json
    import json
    metadata = {
        "track_id": track_id,
        "type": "feature",
        "status": "new",
        "priority": issue_data["priority"],
        "depends_on": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "description": issue_data["title"],
        "upstream_issue": f"https://github.com/gemini-cli-extensions/conductor/issues/{issue_number}",
        "labels": issue_data["labels"],
    }

    with open(track_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # Create index.md
    index_content = f"""# Track: {issue_data['title']}

**Status:** new
**Priority:** {issue_data['priority']}
**Upstream Issue:** #{issue_number}

[Plan](./plan.md) | [Spec](./spec.md) | [Metadata](./metadata.json)

---

## Summary

{issue_data['description']}

## Progress

- [ ] Phase 1: Analysis
- [ ] Phase 2: Implementation
- [ ] Phase 3: Verification
"""

    with open(track_dir / "index.md", "w") as f:
        f.write(index_content)

    return track_dir


def update_tracks_md(tracks_dir: Path, issues: dict):
    """Update tracks.md with new track entries.

    Args:
        tracks_dir: Base tracks directory
        issues: Dict of issue numbers to data
    """
    tracks_md = tracks_dir.parent / "tracks.md"

    # Read existing content
    with open(tracks_md, "r") as f:
        content = f.read()

    # Find the position to insert new tracks (before "## Phase 5" or at end of active tracks)
    # For now, we'll just print what needs to be added
    print(f"\n[UPDATE] Add to {tracks_md}:")
    print("-" * 60)

    for issue_number in sorted(issues.keys()):
        timestamp = datetime.now().strftime("%Y%m%d")
        track_id = f"issue_{issue_number}_{timestamp}"
        issue_data = issues[issue_number]
        print(f"- [ ] **Track: {issue_data['title']}** (./tracks/{track_id}/)")
        print(f"  - Priority: {issue_data['priority']}")
        print(f"  - Source: gemini-cli-extensions/conductor#{issue_number}")
        print()

    print("-" * 60)
    print("[INFO] Manual update required for tracks.md")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Create tracks from upstream GitHub issues")
    parser.add_argument(
        "--issue",
        type=int,
        action="append",
        help="Specific issue number to create track for (can be repeated)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Create tracks for all defined upstream issues",
    )
    parser.add_argument(
        "--tracks-dir",
        type=Path,
        default=Path("conductor/tracks"),
        help="Base tracks directory (default: conductor/tracks)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating",
    )

    args = parser.parse_args()

    print("="*60)
    print("Upstream Issue Track Creator")
    print("="*60)

    # Determine which issues to process
    if args.all:
        issues_to_create = UPSTREAM_ISSUES
    elif args.issue:
        issues_to_create = {n: UPSTREAM_ISSUES[n] for n in args.issue if n in UPSTREAM_ISSUES}
    else:
        # Default: create tracks for high-priority issues
        issues_to_create = {
            n: d for n, d in UPSTREAM_ISSUES.items() if d["priority"] in ["P0", "P1"]
        }

    if not issues_to_create:
        print("[ERROR] No valid issues specified")
        return 1

    print(f"Issues to process: {list(issues_to_create.keys())}")
    print(f"Tracks directory: {args.tracks_dir}")
    print(f"Dry run: {args.dry_run}")
    print("="*60)

    if args.dry_run:
        print("\n[DRY RUN] Would create the following tracks:")
        for issue_number, issue_data in issues_to_create.items():
            timestamp = datetime.now().strftime("%Y%m%d")
            track_id = f"issue_{issue_number}_{timestamp}"
            print(f"  - {track_id}: {issue_data['title']}")
        return 0

    # Create tracks
    created_tracks = []
    for issue_number, issue_data in sorted(issues_to_create.items()):
        try:
            track_path = create_track(issue_number, issue_data, args.tracks_dir)
            created_tracks.append((issue_number, track_path))
            print(f"  [OK] Created: {track_path}")
        except Exception as e:
            print(f"  [ERROR] Failed to create track for #{issue_number}: {e}")

    # Update tracks.md
    if created_tracks:
        created_issues = {n: UPSTREAM_ISSUES[n] for n, _ in created_tracks}
        update_tracks_md(args.tracks_dir, created_issues)

    print("\n" + "="*60)
    print(f"Summary: Created {len(created_tracks)} tracks")
    print("="*60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
