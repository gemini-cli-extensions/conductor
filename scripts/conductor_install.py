#!/usr/bin/env python3
"""Conductor Universal Installer

Installs all conductor components:
- conductor-core (Python package)
- conductor-gemini (Python CLI)
- VS Code extension (.vsix)
- Claude Code commands

Usage:
    python scripts/conductor_install.py [--all] [--component COMPONENT]
"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


class Colors:
    """Terminal colors"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


class ConductorInstaller:
    """Installs conductor components"""

    def __init__(self, base_path: Path = Path()) -> None:
        self.base_path = base_path.resolve()
        self.os_name = platform.system().lower()
        self.errors: list[str] = []
        self.installed: list[str] = []
        self.skipped: list[str] = []

    def log(self, message: str, color: str = "") -> None:
        """Print colored message"""
        if color and sys.stdout.isatty():
            print(f"{color}{message}{Colors.END}")
        else:
            print(message)

    def detect_os(self) -> str:
        """Detect operating system"""
        system = platform.system()
        if system == "Darwin":
            return "macos"
        elif system == "Linux":
            return "linux"
        elif system == "Windows":
            return "windows"
        else:
            return system.lower()

    def detect_arch(self) -> str:
        """Detect system architecture"""
        machine = platform.machine().lower()
        if machine in ["amd64", "x86_64"]:
            return "x64"
        elif machine in ["arm64", "aarch64"]:
            return "arm64"
        return machine

    def check_command(self, command: str) -> bool:
        """Check if a command is available"""
        return shutil.which(command) is not None

    def run_command(self, cmd: list[str], cwd: Optional[Path] = None, check: bool = True) -> tuple[int, str, str]:
        """Run a shell command"""
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.base_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if check and result.returncode != 0:
                return result.returncode, result.stdout, result.stderr
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def install_component(self, component: str, force: bool = False) -> bool:
        """Install a specific component"""
        self.log(f"\n[PKG] Installing {component}...", Colors.BLUE)

        installers = {
            "core": self._install_core,
            "gemini": self._install_gemini,
            "vscode": self._install_vscode,
            "claude": self._install_claude,
        }

        if component not in installers:
            self.log(f"[FAIL] Unknown component: {component}", Colors.RED)
            return False

        try:
            success = installers[component](force)
            if success:
                self.installed.append(component)
                self.log(f"[PASS] {component} installed successfully", Colors.GREEN)
            return success
        except Exception as e:
            self.errors.append(f"{component}: {e}")
            self.log(f"[FAIL] Failed to install {component}: {e}", Colors.RED)
            return False

    def _install_core(self, force: bool = False) -> bool:
        """Install conductor-core"""
        core_path = self.base_path / "conductor-core"

        if not core_path.exists():
            self.log("[WARN]  conductor-core not found, skipping", Colors.YELLOW)
            self.skipped.append("core")
            return True

        # Check if already installed
        result = self.run_command([sys.executable, "-c", "import conductor_core"], check=False)
        if result[0] == 0 and not force:
            self.log("[INFO]  conductor-core already installed (use --force to reinstall)", Colors.YELLOW)
            return True

        # Install with uv if available, otherwise pip
        if self.check_command("uv"):
            self.log("Using uv for installation...")
            cmd = ["uv", "pip", "install", str(core_path)]
        else:
            self.log("Using pip for installation...")
            cmd = [sys.executable, "-m", "pip", "install", str(core_path)]

        code, stdout, stderr = self.run_command(cmd)
        if code != 0:
            raise Exception(f"Installation failed: {stderr}")

        return True

    def _install_gemini(self, force: bool = False) -> bool:
        """Install conductor-gemini"""
        gemini_path = self.base_path / "conductor-gemini"

        if not gemini_path.exists():
            self.log("[WARN]  conductor-gemini not found, skipping", Colors.YELLOW)
            self.skipped.append("gemini")
            return True

        # Install with uv if available, otherwise pip
        if self.check_command("uv"):
            cmd = ["uv", "pip", "install", str(gemini_path)]
        else:
            cmd = [sys.executable, "-m", "pip", "install", str(gemini_path)]

        code, stdout, stderr = self.run_command(cmd)
        if code != 0:
            raise Exception(f"Installation failed: {stderr}")

        return True

    def _install_vscode(self, force: bool = False) -> bool:
        """Install VS Code extension"""
        vscode_path = self.base_path / "conductor-vscode"
        vsix_path = self.base_path / "conductor.vsix"

        # Check if VS Code is installed
        if not self.check_command("code"):
            self.log("[WARN]  VS Code not found, skipping extension install", Colors.YELLOW)
            self.skipped.append("vscode")
            return True

        # Check if .vsix exists, if not try to build it
        if not vsix_path.exists():
            if vscode_path.exists():
                self.log("Building VS Code extension...")
                # Install npm dependencies
                self.run_command(["npm", "install"], cwd=vscode_path, check=False)
                # Build extension
                code, stdout, stderr = self.run_command(["npm", "run", "package"], cwd=vscode_path, check=False)
                if code != 0:
                    self.log(f"[WARN]  Failed to build extension: {stderr}", Colors.YELLOW)
                    self.skipped.append("vscode")
                    return True

        if not vsix_path.exists():
            self.log("[WARN]  conductor.vsix not found, skipping", Colors.YELLOW)
            self.skipped.append("vscode")
            return True

        # Install extension
        code, stdout, stderr = self.run_command(
            ["code", "--install-extension", str(vsix_path), "--force" if force else ""],
            check=False,
        )

        # Filter out empty string from command
        cmd = ["code", "--install-extension", str(vsix_path)]
        if force:
            cmd.append("--force")

        code, stdout, stderr = self.run_command(cmd, check=False)

        if code != 0:
            raise Exception(f"Extension install failed: {stderr}")

        return True

    def _install_claude(self, force: bool = False) -> bool:
        """Install Claude Code commands"""
        claude_source = self.base_path / ".claude"
        claude_dest = Path.home() / ".claude"

        if not claude_source.exists():
            self.log("[WARN]  .claude directory not found, skipping", Colors.YELLOW)
            self.skipped.append("claude")
            return True

        # Check if already installed
        if claude_dest.exists() and not force:
            self.log("[INFO]  Claude Code commands already installed (use --force to reinstall)", Colors.YELLOW)
            return True

        # Remove existing if force
        if claude_dest.exists() and force:
            shutil.rmtree(claude_dest)

        # Copy .claude directory
        if claude_dest.exists():
            shutil.rmtree(claude_dest)

        shutil.copytree(claude_source, claude_dest)
        self.log(f"[PASS] Copied Claude commands to {claude_dest}", Colors.GREEN)

        return True

    def verify_installation(self) -> bool:
        """Verify all installed components"""
        self.log("\n[SCAN] Verifying installation...", Colors.BLUE)

        all_good = True

        # Check conductor-core
        result = self.run_command(
            [sys.executable, "-c", "import conductor_core; print(conductor_core.__version__)"],
            check=False,
        )
        if result[0] == 0:
            self.log(f"[PASS] conductor-core: {result[1].strip()}", Colors.GREEN)
        else:
            self.log("[FAIL] conductor-core: Not installed or import error", Colors.RED)
            all_good = False

        # Check conductor-gemini
        result = self.run_command(
            [sys.executable, "-c", "import conductor_gemini"],
            check=False,
        )
        if result[0] == 0:
            self.log("[PASS] conductor-gemini: Installed", Colors.GREEN)
        else:
            self.log("[FAIL] conductor-gemini: Not installed", Colors.RED)
            all_good = False

        # Check VS Code extension
        if self.check_command("code"):
            result = self.run_command(
                ["code", "--list-extensions"],
                check=False,
            )
            if "conductor" in result[1].lower():
                self.log("[PASS] VS Code extension: Installed", Colors.GREEN)
            else:
                self.log("[WARN]  VS Code extension: Not found (may need manual install)", Colors.YELLOW)

        # Check Claude
        claude_dest = Path.home() / ".claude"
        if claude_dest.exists():
            self.log(f"[PASS] Claude Code commands: Installed at {claude_dest}", Colors.GREEN)
        else:
            self.log("[WARN]  Claude Code commands: Not installed", Colors.YELLOW)

        return all_good

    def print_summary(self) -> None:
        """Print installation summary"""
        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("INSTALLATION SUMMARY", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        if self.installed:
            self.log(f"\n[PASS] Successfully installed ({len(self.installed)}):", Colors.GREEN)
            for comp in self.installed:
                self.log(f"   • {comp}", Colors.GREEN)

        if self.skipped:
            self.log(f"\n⏭️  Skipped ({len(self.skipped)}):", Colors.YELLOW)
            for comp in self.skipped:
                self.log(f"   • {comp}", Colors.YELLOW)

        if self.errors:
            self.log(f"\n[FAIL] Errors ({len(self.errors)}):", Colors.RED)
            for error in self.errors:
                self.log(f"   • {error}", Colors.RED)

        self.log("\n" + "=" * 60, Colors.BLUE)

    def install_all(self, components: Optional[list[str]] = None, force: bool = False) -> bool:
        """Install all or specified components"""
        self.log("\n[START] Conductor Universal Installer", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)
        self.log(f"OS: {self.detect_os()} ({self.detect_arch()})")
        self.log(f"Base path: {self.base_path}")
        self.log("=" * 60, Colors.BLUE)

        if components is None:
            components = ["core", "gemini", "vscode", "claude"]

        success = True
        for component in components:
            if not self.install_component(component, force):
                success = False

        self.verify_installation()
        self.print_summary()

        return success and len(self.errors) == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install conductor components",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/conductor_install.py --all          # Install everything
  python scripts/conductor_install.py --core         # Install core only
  python scripts/conductor_install.py --all --force  # Force reinstall
        """,
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Install all components",
    )
    parser.add_argument(
        "--core",
        action="store_true",
        help="Install conductor-core only",
    )
    parser.add_argument(
        "--gemini",
        action="store_true",
        help="Install conductor-gemini only",
    )
    parser.add_argument(
        "--vscode",
        action="store_true",
        help="Install VS Code extension only",
    )
    parser.add_argument(
        "--claude",
        action="store_true",
        help="Install Claude Code commands only",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinstall even if already installed",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Only verify installation, don't install",
    )

    args = parser.parse_args()

    installer = ConductorInstaller()

    if args.verify:
        installer.verify_installation()
        return 0 if len(installer.errors) == 0 else 1

    # Determine components to install
    components = []
    if args.all:
        components = ["core", "gemini", "vscode", "claude"]
    else:
        if args.core:
            components.append("core")
        if args.gemini:
            components.append("gemini")
        if args.vscode:
            components.append("vscode")
        if args.claude:
            components.append("claude")

    # If no specific components, install all
    if not components:
        components = ["core", "gemini", "vscode", "claude"]

    success = installer.install_all(components, args.force)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
