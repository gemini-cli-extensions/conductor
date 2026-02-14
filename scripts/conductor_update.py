#!/usr/bin/env python3
"""Conductor Update Checker and Updater

Checks for updates and applies them to conductor components.

Usage:
    python scripts/conductor_update.py [--check-only] [--all] [--component COMPONENT]
"""

import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Optional


class Colors:
    """Terminal colors"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


class UpdateChecker:
    """Checks and applies updates to conductor components"""

    def __init__(self, base_path: Path = Path()) -> None:
        self.base_path = base_path.resolve()
        self.updates_available: dict[str, dict] = {}
        self.current_versions: dict[str, str] = {}

    def log(self, message: str, color: str = "") -> None:
        """Print colored message"""
        if color and sys.stdout.isatty():
            print(f"{color}{message}{Colors.END}")
        else:
            print(message)

    def run_command(self, cmd: list[str], cwd: Optional[Path] = None) -> tuple[int, str, str]:
        """Run a shell command"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_path,
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def get_current_version(self, component: str) -> Optional[str]:
        """Get current installed version of a component"""
        if component == "core":
            # Try to import and get version
            code, stdout, stderr = self.run_command(
                [sys.executable, "-c", "import conductor_core; print(conductor_core.__version__)"]
            )
            if code == 0:
                return stdout.strip()

        elif component == "gemini":
            code, stdout, stderr = self.run_command(
                [sys.executable, "-c", "import conductor_gemini; print(conductor_gemini.__version__)"]
            )
            if code == 0:
                return stdout.strip()

        elif component == "vscode":
            # Check VS Code extension version
            code, stdout, stderr = self.run_command(["code", "--list-extensions", "--show-versions"])
            if code == 0:
                for line in stdout.split("\n"):
                    if "conductor" in line.lower():
                        match = re.search(r"@(\d+\.\d+\.\d+)", line)
                        if match:
                            return match.group(1)

        return None

    def get_latest_github_release(self, repo: str) -> Optional[str]:
        """Get latest release version from GitHub"""
        try:
            url = f"https://api.github.com/repos/{repo}/releases/latest"
            req = urllib.request.Request(url)
            req.add_header("Accept", "application/vnd.github.v3+json")
            req.add_header("User-Agent", "conductor-updater")

            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                tag = data.get("tag_name", "")
                # Remove 'v' prefix if present
                return tag.lstrip("v")
        except Exception:
            return None

    def get_latest_git_tag(self, component: str) -> Optional[str]:
        """Get latest version from git tags"""
        component_dir = self.base_path / f"conductor-{component}"
        if not component_dir.exists():
            return None

        code, stdout, stderr = self.run_command(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=component_dir,
        )
        if code == 0:
            return stdout.strip().lstrip("v")
        return None

    def check_updates(self, component: str) -> Optional[dict]:
        """Check for updates for a specific component"""
        current = self.get_current_version(component)
        latest = self.get_latest_git_tag(component)

        if current and latest:
            if current != latest:
                return {
                    "component": component,
                    "current": current,
                    "latest": latest,
                    "update_available": True,
                }
            else:
                return {
                    "component": component,
                    "current": current,
                    "latest": latest,
                    "update_available": False,
                }

        return None

    def check_all_updates(self) -> dict[str, dict]:
        """Check for updates for all components"""
        self.log("\n[SCAN] Checking for updates...", Colors.BLUE)

        components = ["core", "gemini", "vscode", "claude"]

        for component in components:
            result = self.check_updates(component)
            if result:
                self.current_versions[component] = result.get("current", "unknown")
                if result.get("update_available"):
                    self.updates_available[component] = result

        return self.updates_available

    def print_update_report(self) -> None:
        """Print update status report"""
        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("UPDATE STATUS", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        if self.updates_available:
            self.log(f"\n[PKG] Updates available ({len(self.updates_available)}):", Colors.YELLOW)
            for component, info in self.updates_available.items():
                self.log(
                    f"   • {component}: {info['current']} → {info['latest']}",
                    Colors.YELLOW,
                )
        else:
            self.log("\n[PASS] All components are up to date!", Colors.GREEN)

        # Show all versions
        self.log("\n[LIST] Installed versions:", Colors.BLUE)
        for component, version in self.current_versions.items():
            status = "[PASS]" if component not in self.updates_available else "[UP]"
            self.log(f"   {status} {component}: {version}")

        self.log("\n" + "=" * 60, Colors.BLUE)

    def update_component(self, component: str) -> bool:
        """Update a specific component"""
        self.log(f"\n[UP]  Updating {component}...", Colors.BLUE)

        if component == "core":
            return self._update_core()
        elif component == "gemini":
            return self._update_gemini()
        elif component == "vscode":
            return self._update_vscode()
        elif component == "claude":
            return self._update_claude()

        return False

    def _update_core(self) -> bool:
        """Update conductor-core"""
        core_path = self.base_path / "conductor-core"
        if not core_path.exists():
            self.log("[WARN]  conductor-core not found", Colors.YELLOW)
            return True

        # Pull latest changes
        code, stdout, stderr = self.run_command(["git", "pull"], cwd=core_path)
        if code != 0:
            self.log(f"[FAIL] Git pull failed: {stderr}", Colors.RED)
            return False

        # Reinstall
        code, stdout, stderr = self.run_command([sys.executable, "-m", "pip", "install", "--upgrade", str(core_path)])
        if code != 0:
            self.log(f"[FAIL] Reinstall failed: {stderr}", Colors.RED)
            return False

        return True

    def _update_gemini(self) -> bool:
        """Update conductor-gemini"""
        gemini_path = self.base_path / "conductor-gemini"
        if not gemini_path.exists():
            self.log("[WARN]  conductor-gemini not found", Colors.YELLOW)
            return True

        code, stdout, stderr = self.run_command(["git", "pull"], cwd=gemini_path)
        if code != 0:
            self.log(f"[FAIL] Git pull failed: {stderr}", Colors.RED)
            return False

        code, stdout, stderr = self.run_command([sys.executable, "-m", "pip", "install", "--upgrade", str(gemini_path)])
        if code != 0:
            self.log(f"[FAIL] Reinstall failed: {stderr}", Colors.RED)
            return False

        return True

    def _update_vscode(self) -> bool:
        """Update VS Code extension"""
        vscode_path = self.base_path / "conductor-vscode"
        if not vscode_path.exists():
            self.log("[WARN]  conductor-vscode not found", Colors.YELLOW)
            return True

        # Pull changes
        code, stdout, stderr = self.run_command(["git", "pull"], cwd=vscode_path)
        if code != 0:
            self.log(f"[FAIL] Git pull failed: {stderr}", Colors.RED)
            return False

        # Rebuild
        code, stdout, stderr = self.run_command(["npm", "run", "package"], cwd=vscode_path)
        if code != 0:
            self.log(f"[FAIL] Build failed: {stderr}", Colors.RED)
            return False

        # Reinstall extension
        vsix_path = self.base_path / "conductor.vsix"
        if vsix_path.exists():
            code, stdout, stderr = self.run_command(["code", "--install-extension", str(vsix_path), "--force"])
            if code != 0:
                self.log(f"[FAIL] Extension install failed: {stderr}", Colors.RED)
                return False

        return True

    def _update_claude(self) -> bool:
        """Update Claude Code commands"""
        import shutil

        claude_source = self.base_path / ".claude"
        claude_dest = Path.home() / ".claude"

        if not claude_source.exists():
            self.log("[WARN]  .claude not found", Colors.YELLOW)
            return True

        # Pull changes
        code, stdout, stderr = self.run_command(["git", "pull"])
        if code != 0:
            self.log(f"[FAIL] Git pull failed: {stderr}", Colors.RED)
            return False

        # Update .claude directory
        if claude_dest.exists():
            shutil.rmtree(claude_dest)
        shutil.copytree(claude_source, claude_dest)

        return True

    def update_all(self, components: Optional[list[str]] = None) -> bool:
        """Update all or specified components"""
        if not self.updates_available:
            self.log("\n[PASS] No updates available", Colors.GREEN)
            return True

        if components is None:
            components = list(self.updates_available.keys())
        else:
            # Only update components that have updates
            components = [c for c in components if c in self.updates_available]

        if not components:
            self.log("\n[PASS] No updates available for specified components", Colors.GREEN)
            return True

        self.log(f"\n[UP]  Updating {len(components)} component(s)...", Colors.BLUE)

        success = True
        for component in components:
            if not self.update_component(component):
                success = False

        if success:
            self.log("\n[PASS] All updates applied successfully!", Colors.GREEN)
        else:
            self.log("\n[WARN]  Some updates failed", Colors.YELLOW)

        return success


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check for and apply conductor updates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/conductor_update.py --check-only    # Check only, don't update
  python scripts/conductor_update.py --all           # Update everything
  python scripts/conductor_update.py --core          # Update core only
        """,
    )

    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check for updates, don't apply them",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Update all components with available updates",
    )
    parser.add_argument(
        "--core",
        action="store_true",
        help="Update conductor-core only",
    )
    parser.add_argument(
        "--gemini",
        action="store_true",
        help="Update conductor-gemini only",
    )
    parser.add_argument(
        "--vscode",
        action="store_true",
        help="Update VS Code extension only",
    )
    parser.add_argument(
        "--claude",
        action="store_true",
        help="Update Claude Code commands only",
    )

    args = parser.parse_args()

    checker = UpdateChecker()

    # Check for updates
    checker.check_all_updates()
    checker.print_update_report()

    if args.check_only:
        return 0 if not checker.updates_available else 1

    # Determine components to update
    components = []
    if args.all:
        components = None  # Update all with updates
    else:
        if args.core:
            components.append("core")
        if args.gemini:
            components.append("gemini")
        if args.vscode:
            components.append("vscode")
        if args.claude:
            components.append("claude")

    # If no specific components, update all
    if not components and not args.all:
        components = None

    # Apply updates
    success = checker.update_all(components)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
