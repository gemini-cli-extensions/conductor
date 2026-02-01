import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _run(cmd: list[str]) -> bool:
    result = subprocess.run(cmd, cwd=ROOT, check=False)  # noqa: S603
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated artifacts and platform mappings.")
    parser.add_argument("--require-vsix", action="store_true", help="Require conductor.vsix to exist")
    parser.add_argument("--check-global", action="store_true", help="Validate Antigravity global workflows")
    parser.add_argument(
        "--check-antigravity-skills",
        action="store_true",
        help="Validate optional Antigravity skills output",
    )
    parser.add_argument("--fix", action="store_true", help="Rewrite repo-local outputs to match manifest")
    args = parser.parse_args()

    python = sys.executable
    check_cmd = [python, "scripts/check_skills_sync.py"]
    if args.fix:
        check_cmd.append("--fix")
    if args.check_global:
        check_cmd.append("--check-global")
    if args.check_antigravity_skills:
        check_cmd.append("--check-antigravity-skills")
    if args.require_vsix:
        check_cmd.append("--require-vsix")

    ok = True
    if not _run(check_cmd):
        ok = False
    if not _run([python, "scripts/validate_platforms.py"]):
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
