#!/usr/bin/env python3
"""Repository Rename Coordinator - Handle repository rename from conductor to conductor-next.

This script helps coordinate the repository rename by:
1. Scanning codebase for old repository references
2. Generating list of files requiring updates
3. Implementing URL replacement logic
4. Creating migration guide for users
"""

import os
import re
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Tuple


class RenameCoordinator:
    """Coordinate repository rename operations."""

    def __init__(
        self,
        old_name: str = "conductor",
        new_name: str = "conductor-next",
        old_owner: str = "edithatogo",
        exclude_patterns: Optional[List[str]] = None,
    ):
        """Initialize rename coordinator.

        Args:
            old_name: Old repository name
            new_name: New repository name
            old_owner: Repository owner
            exclude_patterns: Patterns to exclude from scanning
        """
        self.old_name = old_name
        self.new_name = new_name
        self.old_owner = old_owner
        self.exclude_patterns = exclude_patterns or [
            "*.pyc",
            "__pycache__",
            "node_modules",
            ".git",
            "*.min.js",
            "*.min.css",
            "*.lock",
            "package-lock.json",
            ".venv",
            "venv",
            "dist",
            "build",
        ]
        self.base_path = Path.cwd()

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from scanning.

        Args:
            path: Path to check

        Returns:
            True if path should be excluded
        """
        path_str = str(path)
        for pattern in self.exclude_patterns:
            if pattern.startswith("*"):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False

    def scan_for_references(self) -> Dict[str, List[Tuple[int, str]]]:
        """Scan codebase for old repository references.

        Returns:
            Dict mapping file paths to list of (line_number, line_content) tuples
        """
        print(f"[SCAN] Scanning for '{self.old_name}' references...")

        results = {}
        files_scanned = 0
        files_with_refs = 0

        # Patterns to match
        patterns = [
            # GitHub URLs
            rf"github\.com/{self.old_owner}/{self.old_name}",
            rf"github\.com/.+?/{self.old_name}(?:\.git)?",
            # Import statements
            rf"from {self.old_name}",
            rf"import {self.old_name}",
            # Package references
            rf"pip install {self.old_name}",
            rf"npm install.*{self.old_name}",
            # Documentation references
            rf"conductor (?:CLI|tool|extension)",
            # Git remote URLs
            rf"git@github\.com:{self.old_owner}/{self.old_name}\.git",
            rf"https://github\.com/{self.old_owner}/{self.old_name}\.git",
        ]

        combined_pattern = re.compile("|".join(patterns), re.IGNORECASE)

        for file_path in self.base_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self.should_exclude(file_path):
                continue

            # Only scan text files
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except (IOError, OSError):
                continue

            files_scanned += 1
            matches = []

            for line_num, line in enumerate(lines, 1):
                if combined_pattern.search(line):
                    matches.append((line_num, line.rstrip()))

            if matches:
                files_with_refs += 1
                rel_path = str(file_path.relative_to(self.base_path))
                results[rel_path] = matches

        print(f"[INFO] Scanned {files_scanned} files")
        print(f"[INFO] Found references in {files_with_refs} files")

        return results

    def generate_replacement_map(self) -> Dict[str, str]:
        """Generate map of old strings to new strings.

        Returns:
            Dict mapping old strings to replacement strings
        """
        return {
            # URLs
            f"github.com/{self.old_owner}/{self.old_name}": f"github.com/{self.old_owner}/{self.new_name}",
            f"github.com/{self.old_owner}/{self.old_name}.git": f"github.com/{self.old_owner}/{self.new_name}.git",
            f"git@github.com:{self.old_owner}/{self.old_name}.git": f"git@github.com:{self.old_owner}/{self.new_name}.git",
            # Commands
            f"pip install {self.old_name}": f"pip install {self.new_name}",
            f"npm install -g {self.old_name}": f"npm install -g {self.new_name}",
            f"npx {self.old_name}": f"npx {self.new_name}",
            # Documentation
            f"Conductor-Next CLI": f"Conductor-Next CLI",
            f"conductor-next CLI": f"conductor-next CLI",
            f"conductor-next tool": f"conductor-next tool",
            f"conductor-next extension": f"conductor-next extension",
        }

    def update_file(self, file_path: Path, dry_run: bool = True) -> int:
        """Update a single file with new repository references.

        Args:
            file_path: Path to file to update
            dry_run: If True, don't write changes

        Returns:
            Number of replacements made
        """
        replacement_map = self.generate_replacement_map()

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (IOError, OSError) as e:
            print(f"[WARN] Could not read {file_path}: {e}")
            return 0

        original_content = content
        replacements = 0

        for old_str, new_str in replacement_map.items():
            count = content.count(old_str)
            if count > 0:
                content = content.replace(old_str, new_str)
                replacements += count
                if not dry_run:
                    print(f"  [REPLACE] '{old_str}' -> '{new_str}' ({count} occurrences)")

        if replacements > 0 and not dry_run:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
            except (IOError, OSError) as e:
                print(f"[ERROR] Could not write {file_path}: {e}")
                return 0

        return replacements

    def update_all_files(self, dry_run: bool = True) -> Dict[str, int]:
        """Update all files with new repository references.

        Args:
            dry_run: If True, don't write changes

        Returns:
            Dict mapping file paths to number of replacements
        """
        print(f"\n[UPDATE] {'(DRY RUN) ' if dry_run else ''}Updating files...")

        results = {}
        total_replacements = 0

        for file_path in self.base_path.rglob("*"):
            if not file_path.is_file():
                continue

            if self.should_exclude(file_path):
                continue

            try:
                replacements = self.update_file(file_path, dry_run)
                if replacements > 0:
                    rel_path = str(file_path.relative_to(self.base_path))
                    results[rel_path] = replacements
                    total_replacements += replacements
            except Exception as e:
                print(f"[WARN] Error processing {file_path}: {e}")

        print(f"\n[SUMMARY] Total replacements: {total_replacements}")
        print(f"[SUMMARY] Files updated: {len(results)}")

        return results

    def generate_migration_guide(self, output_path: Path) -> str:
        """Generate migration guide for users.

        Args:
            output_path: Path to save migration guide

        Returns:
            Generated guide content
        """
        guide = f"""# Repository Rename Migration Guide

**Date:** {datetime.now(timezone.utc).strftime("%Y-%m-%d")}

**Old Repository:** `{self.old_owner}/{self.old_name}`
**New Repository:** `{self.old_owner}/{self.new_name}`

## Why the Rename?

The repository has been renamed to `{self.new_name}` to better reflect its next-generation features and architecture.

## For Users

### Update Your Installation

#### If installed via pip:
```bash
# Uninstall old version
pip uninstall {self.old_name}

# Install new version
pip install {self.new_name}
```

#### If installed via npm:
```bash
# Uninstall old version
npm uninstall -g {self.old_name}

# Install new version
npm install -g {self.new_name}
```

#### If using npx:
```bash
# Just use the new name - no installation needed
npx {self.new_name} <command>
```

### Update Git Remotes

If you have a local clone of the repository:

```bash
cd path/to/your/clone

# Update remote URL
git remote set-url origin https://github.com/{self.old_owner}/{self.new_name}.git

# Verify the change
git remote -v

# Pull latest changes
git pull origin main
```

Or if you use SSH:

```bash
git remote set-url origin git@github.com:{self.old_owner}/{self.new_name}.git
```

### Update Bookmarks and Links

Update any bookmarks or documentation links:

**Old:** `https://github.com/{self.old_owner}/{self.old_name}`
**New:** `https://github.com/{self.old_owner}/{self.new_name}`

## For Developers

### Update Import Statements

If you import from this package in your code:

```python
# Old
from {self.old_name} import something

# New
from {self.new_name} import something
```

### Update Dependencies

Update your `requirements.txt`, `setup.py`, `pyproject.toml`, or `package.json`:

```diff
- {self.old_name}>=1.0.0
+ {self.new_name}>=1.0.0
```

### Update CI/CD Pipelines

Update any CI/CD configuration that references the old repository:

```yaml
# GitHub Actions
- uses: {self.old_owner}/{self.old_name}@v1
+ uses: {self.old_owner}/{self.new_name}@v1
```

## Common Issues

### Issue: "Module not found" after update

**Solution:** Make sure you've uninstalled the old package and cleared any cached imports:

```bash
pip uninstall {self.old_name}
pip cache purge  # For pip
python -c "import sys; print(sys.path)"  # Check for old installations
```

### Issue: Git remote still points to old repository

**Solution:** Verify and update your remote:

```bash
git remote -v
git remote set-url origin https://github.com/{self.old_owner}/{self.new_name}.git
```

### Issue: Old bookmarks still work

**Note:** GitHub will redirect old URLs to the new repository, but it's best to update your bookmarks to use the new URL directly.

## Timeline

- **Announcement Date:** {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
- **Redirect Period:** Indefinite (GitHub provides automatic redirects)
- **Old Package Deprecation:** Immediate

## Questions?

If you encounter any issues during migration, please open an issue at:
https://github.com/{self.old_owner}/{self.new_name}/issues

---
*Generated automatically by the Repository Rename Coordinator*
"""

        if not output_path.parent.exists():
            output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(guide)

        print(f"[INFO] Migration guide saved to {output_path}")
        return guide

    def generate_announcement(self) -> str:
        """Generate announcement template for users.

        Returns:
            Announcement content
        """
        return f"""# 📢 Repository Rename Announcement

## The {self.old_name} repository is now {self.new_name}!

We're excited to announce that our repository has been renamed to better reflect its next-generation capabilities.

### What's Changing?

- **Repository Name:** `{self.old_owner}/{self.old_name}` → `{self.old_owner}/{self.new_name}`
- **Package Name:** `{self.old_name}` → `{self.new_name}`
- **GitHub URL:** https://github.com/{self.old_owner}/{self.old_name} → https://github.com/{self.old_owner}/{self.new_name}

### What's NOT Changing?

- All existing functionality remains the same
- Your existing workflows will continue to work (GitHub provides automatic redirects)
- No breaking changes to the API

### Action Required

Please update your installations and bookmarks:

```bash
# Uninstall old, install new
pip uninstall {self.old_name} && pip install {self.new_name}
```

See our [Migration Guide](docs/REPO_RENAME.md) for detailed instructions.

### Questions?

Open an issue if you encounter any problems: https://github.com/{self.old_owner}/{self.new_name}/issues

Thank you for your continued support!

---
*The {self.new_name} Team*
"""


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Coordinate repository rename from conductor to conductor-next"
    )
    parser.add_argument(
        "--old-name",
        default="conductor",
        help="Old repository name (default: conductor)",
    )
    parser.add_argument(
        "--new-name",
        default="conductor-next",
        help="New repository name (default: conductor-next)",
    )
    parser.add_argument(
        "--owner",
        default="edithatogo",
        help="Repository owner (default: edithatogo)",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan for old references only (don't update)",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update files with new references",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Dry run - don't make changes (default: True)",
    )
    parser.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="dry_run",
        help="Actually make changes (not just dry run)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/REPO_RENAME.md"),
        help="Path for migration guide output",
    )
    parser.add_argument(
        "--generate-guide",
        action="store_true",
        help="Generate migration guide",
    )
    parser.add_argument(
        "--generate-announcement",
        action="store_true",
        help="Generate announcement template",
    )

    args = parser.parse_args()

    print("="*60)
    print("Repository Rename Coordinator")
    print("="*60)
    print(f"Old: {args.old_name}")
    print(f"New: {args.new_name}")
    print(f"Owner: {args.owner}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print("="*60)

    coordinator = RenameCoordinator(
        old_name=args.old_name,
        new_name=args.new_name,
        old_owner=args.owner,
    )

    # Scan for references
    if args.scan or not (args.update or args.generate_guide or args.generate_announcement):
        references = coordinator.scan_for_references()

        if references:
            print("\n[REFERENCES FOUND]")
            for file_path, matches in list(references.items())[:20]:  # Show first 20
                print(f"\n{file_path}:")
                for line_num, line in matches[:5]:  # Show first 5 matches per file
                    print(f"  Line {line_num}: {line[:80]}...")
                if len(matches) > 5:
                    print(f"  ... and {len(matches) - 5} more")

            # Save full report
            report_path = Path(".github/rename_scan_report.json")
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w") as f:
                json.dump(references, f, indent=2)
            print(f"\n[INFO] Full report saved to {report_path}")
        else:
            print("[INFO] No references found")

    # Update files
    if args.update:
        results = coordinator.update_all_files(dry_run=args.dry_run)

        if results and not args.dry_run:
            print("\n[UPDATED FILES]")
            for file_path, count in results.items():
                print(f"  {file_path}: {count} replacements")

    # Generate migration guide
    if args.generate_guide:
        coordinator.generate_migration_guide(args.output)

    # Generate announcement
    if args.generate_announcement:
        announcement = coordinator.generate_announcement()
        print("\n" + "="*60)
        print("ANNOUNCEMENT TEMPLATE")
        print("="*60)
        print(announcement)

    return 0


if __name__ == "__main__":
    sys.exit(main())
