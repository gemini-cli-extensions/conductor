import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PYTHONPATH = f"{ROOT}/conductor-gemini/src:{ROOT}/conductor-core/src"


def run_command(cmd, cwd=None, env=None):
    process_env = {**os.environ, "PYTHONPATH": PYTHONPATH, "MPLBACKEND": "Agg"}
    if env:
        process_env.update(env)

    return subprocess.run(
        cmd, shell=True, cwd=cwd or ROOT, capture_output=True, text=True, env=process_env, check=False
    )


def test_step(name) -> None:
    pass


def main() -> None:
    all_passed = True

    # 1. Verify Extension Manifest
    test_step("Verifying conductor-vscode/package.json")
    pkg_path = ROOT / "conductor-vscode" / "package.json"
    with open(pkg_path) as f:
        pkg = json.load(f)

    chat_participants = pkg.get("contributes", {}).get("chatParticipants", [])
    if any(p.get("id") == "conductor.agent" for p in chat_participants):
        pass
    else:
        all_passed = False

    # 2. Verify Compiled Extension Logic
    test_step("Verifying conductor-vscode/out/extension.js logic")
    ext_js_path = ROOT / "conductor-vscode" / "out" / "extension.js"
    if ext_js_path.exists():
        content = ext_js_path.read_text()
        if "conductor.agent" in content and (
            "runConductorCommandAsync" in content or "runConductorCommand" in content
        ):
            pass
        else:
            all_passed = False
    else:
        all_passed = False

    # 3. Run Skill Sync Unit Test
    test_step("Running Antigravity skill sync unit tests")
    python = sys.executable
    res = run_command(f'"{python}" -m pytest conductor-core/tests/test_sync_skills_antigravity.py')
    if res.returncode == 0:
        pass
    else:
        all_passed = False

    # 4. Run VS Code Contract Tests
    test_step("Running VS Code contract integration tests")
    res = run_command(f'"{python}" -m pytest conductor-gemini/tests/test_vscode_contract.py')
    if res.returncode == 0:
        pass
    else:
        all_passed = False

    # 5. Verify .antigravity/skills structure
    test_step("Verifying .antigravity/skills structure")
    ag_skills_dir = ROOT / ".antigravity" / "skills"
    if ag_skills_dir.exists() and any(ag_skills_dir.iterdir()):
        pass
    else:
        all_passed = False

    if all_passed:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
