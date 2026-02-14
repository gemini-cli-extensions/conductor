#!/usr/bin/env python3
"""Repository Rename Coordinator

Prepares and coordinates the repository rename from 'conductor' to 'conductor-next'.

Usage:
    python scripts/rename_repo.py [--check] [--apply]

NOTE: The actual repository rename must be done manually via GitHub UI.
      This script prepares all necessary changes.
"""

import argparse
import re
import sys
from pathlib import Path


class Colors:
    """Terminal colors"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


class RepoRenameCoordinator:
    """Coordinates repository rename from conductor to conductor-next"""

    OLD_NAME = "edithatogo/conductor"
    NEW_NAME = "edithatogo/conductor-next"

    def __init__(self, base_path: Path = Path()) -> None:
        self.base_path = base_path.resolve()
        self.files_to_update: list[tuple[Path, int]] = []
        self.changes_made: list[str] = []

    def log(self, message: str, color: str = "") -> None:
        """Print colored message"""
        if color and sys.stdout.isatty():
            print(f"{color}{message}{Colors.END}")
        else:
            print(message)

    def scan_for_references(self) -> list[tuple[Path, list[int]]]:
        """Scan codebase for old repository references"""
        self.log("\n[SCAN] Scanning for old repository references...", Colors.BLUE)

        findings = []
        patterns = [
            r"edithatogo/conductor[^-]",
            r"github\.com/edithatogo/conductor[^-]",
        ]

        # Files to check
        extensions = [".md", ".py", ".yml", ".yaml", ".json", ".toml", ".sh", ".ps1"]

        for ext in extensions:
            for file_path in self.base_path.rglob(f"*{ext}"):
                # Skip certain directories
                if any(x in str(file_path) for x in [".git", "node_modules", "__pycache__"]):
                    continue

                try:
                    content = file_path.read_text(encoding="utf-8")
                    lines_found = []

                    for i, line in enumerate(content.split("\n"), 1):
                        for pattern in patterns:
                            if re.search(pattern, line):
                                lines_found.append(i)
                                break

                    if lines_found:
                        findings.append((file_path, lines_found))

                except Exception:
                    continue

        return findings

    def generate_update_list(self, findings: list[tuple[Path, list[int]]]) -> None:
        """Generate list of files that need updating"""
        self.log("\n[LIST] Files requiring updates:", Colors.YELLOW)

        for file_path, lines in findings:
            self.log(f"  {file_path} (lines: {', '.join(map(str, lines))})")
            self.files_to_update.append((file_path, len(lines)))

        total_files = len(findings)
        total_refs = sum(len(lines) for _, lines in findings)

        self.log(f"\nTotal: {total_files} files, {total_refs} references", Colors.BLUE)

    def update_file(self, file_path: Path) -> bool:
        """Update references in a single file"""
        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content

            # Replace repository references
            # Replace edithatogo/conductor (but not edithatogo/conductor-next)
            content = re.sub(
                r"(edithatogo/conductor)(?!-next)",
                r"edithatogo/conductor-next",
                content,
            )

            # Replace github.com/edithatogo/conductor (but not with -next)
            content = re.sub(
                r"(github\.com/edithatogo/conductor)(?!-next)",
                r"github.com/edithatogo/conductor-next",
                content,
            )

            # Replace install.cat/edithatogo/conductor (but not with -next)
            content = re.sub(
                r"(install\.cat/edithatogo/conductor)(?!-next)",
                r"install.cat/edithatogo/conductor-next",
                content,
            )

            if content != original_content:
                file_path.write_text(content, encoding="utf-8")
                self.changes_made.append(str(file_path))
                return True

            return False

        except Exception as e:
            self.log(f"[FAIL] Error updating {file_path}: {e}", Colors.RED)
            return False

    def apply_updates(self) -> int:
        """Apply all necessary updates"""
        self.log("\n[WRITE] Applying updates...", Colors.BLUE)

        updated = 0
        for file_path, _ in self.files_to_update:
            if self.update_file(file_path):
                updated += 1
                self.log(f"  [PASS] Updated: {file_path}", Colors.GREEN)

        return updated

    def create_migration_guide(self) -> Path:
        """Create migration guide for users"""
        guide_path = self.base_path / "REPO_RENAME_MIGRATION.md"

        content = """# Repository Rename Migration Guide

## Overview

The repository has been renamed from `edithatogo/conductor` to `edithatogo/conductor-next`.

## What You Need to Do

### 1. Update Your Local Clone

```bash
# Update the remote URL
git remote set-url origin https://github.com/edithatogo/conductor-next.git

# Verify the change
git remote -v
```

### 2. Update Forks

If you have a fork, GitHub should automatically redirect it. However, you should still update your remotes:

```bash
# In your forked repository
git remote set-url upstream https://github.com/edithatogo/conductor-next.git
```

### 3. Update Scripts and Automation

Update any scripts, CI/CD configurations, or automation that references the old URL:

- Update `git clone` commands
- Update GitHub Actions workflows
- Update documentation links
- Update package.json, setup.py, etc.

### 4. Update Installed Components

If you've installed conductor via the one-liner installer:

```bash
# Re-run the installer
mise run update-all
```

Or manually update:

```bash
cd ~/.local/share/conductor-next
git remote set-url origin https://github.com/edithatogo/conductor-next.git
git pull
```

## GitHub Redirects

GitHub will automatically redirect:
- Web requests from the old URL
- Git operations (clone, fetch, push)
- API requests

However, you should update your URLs as soon as possible.

## What Changed

- **Repository URL**: `github.com/edithatogo/conductor` → `github.com/edithatogo/conductor-next`
- **Install URL**: `install.cat/edithatogo/conductor` → `install.cat/edithatogo/conductor-next`

## Need Help?

If you encounter any issues:

1. Check the [documentation](./README.md)
2. Open an issue on GitHub
3. Run the verification script: `python scripts/verify_installation.py`
"""

        guide_path.write_text(content, encoding="utf-8")
        return guide_path

    def print_summary(self) -> None:
        """Print rename summary"""
        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("REPOSITORY RENAME SUMMARY", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        self.log(f"\nOld name: {self.OLD_NAME}", Colors.YELLOW)
        self.log(f"New name: {self.NEW_NAME}", Colors.GREEN)

        if self.changes_made:
            self.log(f"\n[PASS] Updated {len(self.changes_made)} files:", Colors.GREEN)
            for file in self.changes_made:
                self.log(f"  • {file}")

        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("NEXT STEPS:", Colors.YELLOW)
        self.log("=" * 60, Colors.BLUE)
        self.log("\n1. Review the changes made above")
        self.log("2. Commit the changes:")
        self.log("   git add -A")
        self.log("   git commit -m 'chore: prepare for repo rename to conductor-next'")
        self.log("3. Push to GitHub:")
        self.log("   git push origin main")
        self.log("4. Rename the repository via GitHub UI:")
        self.log("   - Go to: Settings → General → Repository Name")
        self.log("   - Change: conductor → conductor-next")
        self.log("   - Click: Rename")
        self.log("5. Update your local clone:")
        self.log("   git remote set-url origin https://github.com/edithatogo/conductor-next.git")
        self.log("\n" + "=" * 60 + "\n", Colors.BLUE)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Coordinate repository rename",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/rename_repo.py --check     # Check what needs updating
  python scripts/rename_repo.py --apply     # Apply updates (dry-run first)
        """,
    )

    parser.add_argument(
        "--check",
        action="store_true",
        help="Check what files need updating",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the updates",
    )

    args = parser.parse_args()

    coordinator = RepoRenameCoordinator()

    if not args.check and not args.apply:
        parser.print_help()
        return 1

    # Scan for references
    findings = coordinator.scan_for_references()

    if not findings:
        coordinator.log("\n[PASS] No references to old repository name found!", Colors.GREEN)
        return 0

    # Generate update list
    coordinator.generate_update_list(findings)

    if args.apply:
        updated = coordinator.apply_updates()
        coordinator.log(f"\n[PASS] Updated {updated} files", Colors.GREEN)

        # Create migration guide
        guide_path = coordinator.create_migration_guide()
        coordinator.log(f"[PASS] Created migration guide: {guide_path}", Colors.GREEN)

        coordinator.print_summary()
    else:
        coordinator.log("\n[WARN]  This was a dry-run. Use --apply to make changes.", Colors.YELLOW)

    return 0


if __name__ == "__main__":
    sys.exit(main())
