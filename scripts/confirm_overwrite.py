#!/usr/bin/env python3
"""Add overwrite confirmation for file operations in Conductor.

This script provides confirmation prompts before overwriting existing files
during conductor operations like track creation, sync, etc.
"""

import sys
from pathlib import Path
from typing import List, Optional


def confirm_overwrite(files: List[Path], dry_run: bool = False) -> bool:
    """Ask for confirmation before overwriting files.

    Args:
        files: List of file paths that would be overwritten
        dry_run: If True, just show what would happen

    Returns:
        True if user confirms, False otherwise
    """
    if not files:
        return True

    print("\n[OVERWRITE CONFIRMATION]")
    print(f"The following {len(files)} file(s) would be overwritten:")
    for f in files:
        print(f"  - {f}")

    if dry_run:
        print("\n[DRY RUN] Would ask for confirmation")
        return True

    # In production, this would use AskUser tool:
    # AskUser: {"type": "yesno", "question": "Proceed with overwriting these files?"}
    response = input("\nProceed with overwriting? [y/N]: ").strip().lower()
    return response in ('y', 'yes')


def find_files_to_create(track_dir: Path, force: bool = False) -> List[Path]:
    """Find files that would be overwritten during track creation.

    Args:
        track_dir: Track directory being created
        force: If True, skip confirmation

    Returns:
        List of existing files that would be overwritten
    """
    existing = []
    track_files = ['index.md', 'plan.md', 'spec.md', 'metadata.json']

    for fname in track_files:
        fpath = track_dir / fname
        if fpath.exists():
            existing.append(fpath)

    return existing


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Add overwrite confirmation for file operations"
    )
    parser.add_argument(
        "--check",
        type=Path,
        help="Check specific directory for files that would be overwritten",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without asking",
    )

    args = parser.parse_args()

    print("="*60)
    print("Overwrite Confirmation for Conductor Operations")
    print("="*60)

    if args.check:
        existing = find_files_to_create(args.check)
        if existing:
            confirm_overwrite(existing, args.dry_run)
        else:
            print(f"[OK] {args.check} - No files would be overwritten")
    else:
        print("This script provides overwrite confirmation for conductor operations.")
        print("It is integrated into conductor-newtrack and other file-modifying commands.")
        print("\nUsage:")
        print("  python confirm_overwrite.py --check <directory>")
        print("  python confirm_overwrite.py --check <directory> --dry-run")

    return 0


if __name__ == "__main__":
    sys.exit(main())
