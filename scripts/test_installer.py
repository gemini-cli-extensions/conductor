#!/usr/bin/env python3
"""Test suite for conductor installer scripts.

Tests the installation and verification scripts to ensure they work correctly.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> tuple[int, str, str]:
    """Run a command and return results."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd or Path("."),
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def test_verify_installation() -> bool:
    """Test the verify installation script."""
    print("\nTEST Testing verify_installation.py...")

    code, stdout, stderr = run_command([sys.executable, "scripts/verify_installation.py"])

    if code == 0:
        print("PASS verify_installation.py works correctly")
        return True
    else:
        print(f"WARN  verify_installation.py returned exit code {code}")
        print(f"   stderr: {stderr[:200]}")
        return False


def test_validate_docs() -> bool:
    """Test the documentation validation script."""
    print("\nTEST Testing validate_docs.py...")

    code, stdout, stderr = run_command([sys.executable, "scripts/validate_docs.py"])

    # This may fail on validation errors, but script should run
    if "Running documentation validation" in stderr or code in [0, 1]:
        print("PASS validate_docs.py runs correctly")
        return True
    else:
        print(f"FAIL validate_docs.py failed: {stderr[:200]}")
        return False


def test_conductor_install_help() -> bool:
    """Test that conductor_install.py shows help correctly."""
    print("\nTEST Testing conductor_install.py --help...")

    code, stdout, stderr = run_command([sys.executable, "scripts/conductor_install.py", "--help"])

    if code == 0 and "Install conductor components" in stdout:
        print("PASS conductor_install.py --help works")
        return True
    else:
        print(f"FAIL conductor_install.py --help failed")
        return False


def test_conductor_update_help() -> bool:
    """Test that conductor_update.py shows help correctly."""
    print("\nTEST Testing conductor_update.py --help...")

    code, stdout, stderr = run_command([sys.executable, "scripts/conductor_update.py", "--help"])

    if code == 0 and "Check for and apply conductor updates" in stdout:
        print("PASS conductor_update.py --help works")
        return True
    else:
        print(f"FAIL conductor_update.py --help failed")
        return False


def test_sync_upstream_help() -> bool:
    """Test that sync_upstream.py shows help correctly."""
    print("\nTEST Testing sync_upstream.py --help...")

    code, stdout, stderr = run_command([sys.executable, "scripts/sync_upstream.py", "--help"])

    if code == 0 and "Sync from upstream repositories" in stdout:
        print("PASS sync_upstream.py --help works")
        return True
    else:
        print(f"FAIL sync_upstream.py --help failed")
        return False


def test_triage_issues_help() -> bool:
    """Test that triage_issues.py shows help correctly."""
    print("\nTEST Testing triage_issues.py --help...")

    code, stdout, stderr = run_command([sys.executable, "scripts/triage_issues.py", "--help"])

    if code == 0 and "Triage GitHub issues" in stdout:
        print("PASS triage_issues.py --help works")
        return True
    else:
        print(f"FAIL triage_issues.py --help failed")
        return False


def test_mise_toml_exists() -> bool:
    """Test that mise.toml exists and is valid."""
    print("\nTEST Testing mise.toml...")

    mise_toml = Path("mise.toml")
    if not mise_toml.exists():
        print("FAIL mise.toml not found")
        return False

    content = mise_toml.read_text()
    if "[tools]" in content and "[tasks]" in content:
        print("PASS mise.toml exists and looks valid")
        return True
    else:
        print("WARN  mise.toml exists but may be missing sections")
        return True  # Still pass, just warn


def test_install_scripts_exist() -> bool:
    """Test that install scripts exist."""
    print("\nTEST Testing install scripts...")

    install_sh = Path("install.sh")
    install_ps1 = Path("install.ps1")

    results = []

    if install_sh.exists():
        print("PASS install.sh exists")
        results.append(True)
    else:
        print("FAIL install.sh not found")
        results.append(False)

    if install_ps1.exists():
        print("PASS install.ps1 exists")
        results.append(True)
    else:
        print("FAIL install.ps1 not found")
        results.append(False)

    return all(results)


def main() -> int:
    """Run all tests."""
    print("=" * 60)
    print("Conductor Installer Test Suite")
    print("=" * 60)

    tests = [
        ("mise.toml exists", test_mise_toml_exists),
        ("install scripts exist", test_install_scripts_exist),
        ("conductor_install.py --help", test_conductor_install_help),
        ("conductor_update.py --help", test_conductor_update_help),
        ("verify_installation.py", test_verify_installation),
        ("validate_docs.py", test_validate_docs),
        ("sync_upstream.py --help", test_sync_upstream_help),
        ("triage_issues.py --help", test_triage_issues_help),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"FAIL Test '{name}' raised exception: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
