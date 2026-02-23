#!/usr/bin/env python3
"""Auto-create .gitignore for new conductor tracks.

This script generates .gitignore files for conductor track directories
with appropriate patterns for common development artifacts.
"""

import sys
from pathlib import Path


# Standard .gitignore patterns for conductor tracks
TRACK_GITIGNORE = """# Conductor Track Artifacts
*.pyc
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Test artifacts
.pytest_cache/
.coverage
htmlcov/
.tox/

# Track-specific
*.log
*.tmp
.cache/

# Conductor state
setup_state.json
*.local.md
"""


def create_track_gitignore(track_dir: Path) -> Path:
    """Create .gitignore file in track directory.

    Args:
        track_dir: Path to track directory

    Returns:
        Path to created .gitignore file
    """
    gitignore_path = track_dir / ".gitignore"

    if gitignore_path.exists():
        print(f"[SKIP] {track_dir} - .gitignore already exists")
        return gitignore_path

    gitignore_path.write_text(TRACK_GITIGNORE)
    print(f"[CREATE] {track_dir}/.gitignore")

    return gitignore_path


def find_tracks(base_dir: Path) -> list[Path]:
    """Find all track directories.

    Args:
        base_dir: Base directory to search (conductor/tracks)

    Returns:
        List of track directory paths
    """
    tracks = []

    # Check for tracks in base_dir
    if (base_dir / "tracks").exists():
        tracks_dir = base_dir / "tracks"
    elif base_dir.name == "tracks":
        tracks_dir = base_dir
    else:
        tracks_dir = base_dir

    # Find all directories with plan.md (indicator of a track)
    for item in tracks_dir.iterdir():
        if item.is_dir() and (item / "plan.md").exists():
            tracks.append(item)

    # Also check archive subdirectory
    archive_dir = tracks_dir / "archive"
    if archive_dir.exists():
        for item in archive_dir.iterdir():
            if item.is_dir() and (item / "plan.md").exists():
                tracks.append(item)

    return tracks


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Auto-create .gitignore files for conductor tracks"
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path("conductor/tracks"),
        help="Base tracks directory (default: conductor/tracks)",
    )
    parser.add_argument(
        "--track",
        type=Path,
        help="Specific track directory to add .gitignore to",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating",
    )

    args = parser.parse_args()

    print("="*60)
    print("Auto-create .gitignore for Conductor Tracks")
    print("="*60)

    if args.track:
        # Single track mode
        tracks = [args.track]
    else:
        # Find all tracks
        tracks = find_tracks(args.dir)

    print(f"Tracks directory: {args.dir}")
    print(f"Found {len(tracks)} tracks")
    print(f"Dry run: {args.dry_run}")
    print("="*60)

    if args.dry_run:
        print("\n[DRY RUN] Would create .gitignore for:")
        for track in tracks:
            if not (track / ".gitignore").exists():
                print(f"  - {track}")
        return 0

    # Create .gitignore for each track
    created = 0
    skipped = 0

    for track in tracks:
        if (track / ".gitignore").exists():
            skipped += 1
        else:
            create_track_gitignore(track)
            created += 1

    print("\n" + "="*60)
    print(f"Summary: Created {created} .gitignore files, Skipped {skipped} (already exist)")
    print("="*60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
