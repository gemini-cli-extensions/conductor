#!/usr/bin/env python3
"""Conductor Installation Verification

Verifies that all conductor components are correctly installed and functional.

Usage:
    python scripts/verify_installation.py [--verbose]
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class Colors:
    """Terminal colors"""

    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    END = "\033[0m"


class InstallationVerifier:
    """Verifies conductor installation"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warned = 0
        self.warnings: List[str] = []

    def log(self, message: str, color: str = "") -> None:
        """Print colored message"""
        if color and sys.stdout.isatty():
            print(f"{color}{message}{Colors.END}")
        else:
            print(message)

    def run_command(self, cmd: List[str], check: bool = True) -> Tuple[int, str, str]:
        """Run a shell command"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    def check_pass(self, message: str) -> None:
        """Log a passed check"""
        self.checks_passed += 1
        self.log(f"  ✅ {message}", Colors.GREEN)

    def check_fail(self, message: str) -> None:
        """Log a failed check"""
        self.checks_failed += 1
        self.log(f"  ❌ {message}", Colors.RED)

    def check_warn(self, message: str) -> None:
        """Log a warning"""
        self.checks_warned += 1
        self.warnings.append(message)
        self.log(f"  ⚠️  {message}", Colors.YELLOW)

    def verify_system_requirements(self) -> None:
        """Verify system meets requirements"""
        self.log("\n🔍 System Requirements", Colors.BLUE)

        # Check Python version
        code, stdout, stderr = self.run_command([sys.executable, "--version"])
        if code == 0:
            version = stdout.strip()
            self.check_pass(f"Python: {version}")
        else:
            self.check_fail("Python: Not found")

        # Check Git
        code, stdout, stderr = self.run_command(["git", "--version"])
        if code == 0:
            self.check_pass(f"Git: {stdout.strip()}")
        else:
            self.check_fail("Git: Not found")

        # Check Node.js (optional)
        code, stdout, stderr = self.run_command(["node", "--version"])
        if code == 0:
            self.check_pass(f"Node.js: {stdout.strip()}")
        else:
            self.check_warn("Node.js: Not found (optional)")

    def verify_conductor_core(self) -> None:
        """Verify conductor-core installation"""
        self.log("\n🔍 Conductor Core", Colors.BLUE)

        # Check if module can be imported
        code, stdout, stderr = self.run_command(
            [sys.executable, "-c", "import conductor_core; print(conductor_core.__version__)"]
        )
        if code == 0:
            version = stdout.strip()
            self.check_pass(f"conductor-core: v{version}")
        else:
            self.check_fail("conductor-core: Not installed or import error")
            if self.verbose:
                self.log(f"    Error: {stderr}")

    def verify_conductor_gemini(self) -> None:
        """Verify conductor-gemini installation"""
        self.log("\n🔍 Conductor Gemini", Colors.BLUE)

        # Check if module can be imported
        code, stdout, stderr = self.run_command([sys.executable, "-c", "import conductor_gemini; print('OK')"])
        if code == 0:
            self.check_pass("conductor-gemini: Installed")
        else:
            self.check_fail("conductor-gemini: Not installed or import error")
            if self.verbose:
                self.log(f"    Error: {stderr}")

        # Check CLI entry point
        code, stdout, stderr = self.run_command(["conductor-gemini", "--help"], check=False)
        if code == 0:
            self.check_pass("conductor-gemini CLI: Available")
        else:
            self.check_warn("conductor-gemini CLI: Not in PATH")

    def verify_vscode_extension(self) -> None:
        """Verify VS Code extension installation"""
        self.log("\n🔍 VS Code Extension", Colors.BLUE)

        # Check if VS Code is installed
        code, stdout, stderr = self.run_command(["code", "--version"], check=False)
        if code != 0:
            self.check_warn("VS Code: Not installed (optional)")
            return

        self.check_pass("VS Code: Installed")

        # Check if extension is installed
        code, stdout, stderr = self.run_command(["code", "--list-extensions"], check=False)
        if code == 0:
            extensions = stdout.lower()
            if "conductor" in extensions:
                self.check_pass("VS Code Extension: Installed")
            else:
                self.check_fail("VS Code Extension: Not found")
        else:
            self.check_fail("VS Code Extension: Could not check installed extensions")

    def verify_claude_commands(self) -> None:
        """Verify Claude Code commands installation"""
        self.log("\n🔍 Claude Code Commands", Colors.BLUE)

        claude_dir = Path.home() / ".claude"
        if claude_dir.exists():
            # Check for conductor skill
            conductor_skill = claude_dir / "skills" / "conductor"
            if conductor_skill.exists():
                self.check_pass("Claude Code: conductor skill installed")
            else:
                self.check_warn("Claude Code: conductor skill not found")

            # Check for commands
            commands_dir = claude_dir / "commands"
            if commands_dir.exists():
                cmd_files = list(commands_dir.glob("conductor*"))
                if cmd_files:
                    self.check_pass(f"Claude Code: {len(cmd_files)} conductor command(s)")
                else:
                    self.check_warn("Claude Code: No conductor commands found")
            else:
                self.check_warn("Claude Code: commands directory not found")
        else:
            self.check_warn("Claude Code: Not configured")

    def verify_mise_configuration(self) -> None:
        """Verify mise configuration"""
        self.log("\n🔍 Mise Configuration", Colors.BLUE)

        # Check if mise is installed
        code, stdout, stderr = self.run_command(["mise", "--version"], check=False)
        if code == 0:
            version = stdout.strip()
            self.check_pass(f"mise: v{version}")
        else:
            self.check_fail("mise: Not installed")
            return

        # Check if mise.toml exists
        mise_toml = Path("mise.toml")
        if mise_toml.exists():
            self.check_pass("mise.toml: Found")
        else:
            self.check_warn("mise.toml: Not found in current directory")

        # Check mise tasks
        code, stdout, stderr = self.run_command(["mise", "tasks", "ls"], check=False)
        if code == 0:
            tasks = stdout.strip().split("\n")
            conductor_tasks = [t for t in tasks if "conductor" in t.lower()]
            if conductor_tasks:
                self.check_pass(f"mise tasks: {len(conductor_tasks)} conductor task(s)")
            else:
                self.check_warn("mise tasks: No conductor tasks found")

    def verify_documentation(self) -> None:
        """Verify documentation is accessible"""
        self.log("\n🔍 Documentation", Colors.BLUE)

        readme = Path("README.md")
        if readme.exists():
            self.check_pass("README.md: Found")
        else:
            self.check_warn("README.md: Not found")

        workflow = Path("conductor/workflow.md")
        if workflow.exists():
            self.check_pass("conductor/workflow.md: Found")
        else:
            self.check_warn("conductor/workflow.md: Not found")

        style_guides = Path("templates/code_styleguides")
        if style_guides.exists():
            guides = list(style_guides.glob("*.md"))
            self.check_pass(f"Style guides: {len(guides)} guide(s)")
        else:
            self.check_warn("Style guides: Directory not found")

    def verify_scripts(self) -> None:
        """Verify installation scripts are present"""
        self.log("\n🔍 Installation Scripts", Colors.BLUE)

        scripts = [
            "scripts/conductor_install.py",
            "scripts/conductor_update.py",
            "scripts/verify_installation.py",
            "scripts/validate_docs.py",
        ]

        for script in scripts:
            script_path = Path(script)
            if script_path.exists():
                self.check_pass(f"{script}: Found")
            else:
                self.check_fail(f"{script}: Not found")

    def run_all_verifications(self) -> bool:
        """Run all verification checks"""
        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("  Conductor Installation Verification", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        self.verify_system_requirements()
        self.verify_conductor_core()
        self.verify_conductor_gemini()
        self.verify_vscode_extension()
        self.verify_claude_commands()
        self.verify_mise_configuration()
        self.verify_documentation()
        self.verify_scripts()

        return self.print_summary()

    def print_summary(self) -> bool:
        """Print verification summary"""
        total = self.checks_passed + self.checks_failed + self.checks_warned

        self.log("\n" + "=" * 60, Colors.BLUE)
        self.log("  VERIFICATION SUMMARY", Colors.BLUE)
        self.log("=" * 60, Colors.BLUE)

        self.log(f"\n  Total checks: {total}")
        self.log(f"  ✅ Passed: {self.checks_passed}", Colors.GREEN)
        self.log(f"  ⚠️  Warnings: {self.checks_warned}", Colors.YELLOW)
        self.log(f"  ❌ Failed: {self.checks_failed}", Colors.RED)

        if self.warnings:
            self.log("\n  Warnings:", Colors.YELLOW)
            for warning in self.warnings:
                self.log(f"    • {warning}", Colors.YELLOW)

        self.log("\n" + "=" * 60, Colors.BLUE)

        if self.checks_failed == 0:
            self.log("\n  ✅ All critical checks passed!", Colors.GREEN)
            if self.checks_warned > 0:
                self.log("  ⚠️  Some optional components are missing", Colors.YELLOW)
                self.log("     Run with --verbose for details\n")
            else:
                self.log("  🎉 Installation is complete and healthy!\n", Colors.GREEN)
            return True
        else:
            self.log(f"\n  ❌ {self.checks_failed} critical check(s) failed", Colors.RED)
            self.log("  Please review the errors above and reinstall if necessary\n")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Verify conductor installation",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed output",
    )

    args = parser.parse_args()

    verifier = InstallationVerifier(verbose=args.verbose)
    success = verifier.run_all_verifications()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
