import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PYTHONPATH = f"{ROOT}/conductor-gemini/src:{ROOT}/conductor-core/src"

def run_command(cmd, cwd=None, env=None):
    print(f"Executing: {cmd}")
    process_env = {**os.environ, "PYTHONPATH": PYTHONPATH, "MPLBACKEND": "Agg"}
    if env:
        process_env.update(env)
    
    result = subprocess.run(
        cmd, 
        shell=True, 
        cwd=cwd or ROOT, 
        capture_output=True, 
        text=True,
        env=process_env
    )
    return result

def test_step(name):
    print(f"\n[STEP] {name}")

def main():
    all_passed = True

    # 1. Verify Extension Manifest
    test_step("Verifying conductor-vscode/package.json")
    pkg_path = ROOT / "conductor-vscode" / "package.json"
    with open(pkg_path, "r") as f:
        pkg = json.load(f)
    
    chat_participants = pkg.get("contributes", {}).get("chatParticipants", [])
    if any(p.get("id") == "conductor.agent" for p in chat_participants):
        print("✅ chatParticipants 'conductor.agent' found.")
    else:
        print("❌ chatParticipants 'conductor.agent' MISSING.")
        all_passed = False

    # 2. Verify Compiled Extension Logic
    test_step("Verifying conductor-vscode/out/extension.js logic")
    ext_js_path = ROOT / "conductor-vscode" / "out" / "extension.js"
    if ext_js_path.exists():
        content = ext_js_path.read_text()
        if "conductor.agent" in content and "runConductorCommandAsync" in content:
            print("✅ Copilot handler and async runner found in compiled JS.")
        else:
            print("❌ Copilot handler logic NOT found in compiled JS.")
            all_passed = False
    else:
        print("❌ conductor-vscode/out/extension.js NOT found. Run 'npm run compile' in conductor-vscode.")
        all_passed = False

    # 3. Run Skill Sync Unit Test
    test_step("Running Antigravity skill sync unit tests")
    res = run_command("pytest conductor-core/tests/test_sync_skills_antigravity.py")
    if res.returncode == 0:
        print("✅ Unit tests passed.")
    else:
        print(f"❌ Unit tests FAILED.\n{res.stdout}\n{res.stderr}")
        all_passed = False

    # 4. Run VS Code Contract Tests
    test_step("Running VS Code contract integration tests")
    res = run_command("pytest conductor-gemini/tests/test_vscode_contract.py")
    if res.returncode == 0:
        print("✅ Contract tests passed.")
    else:
        print(f"❌ Contract tests FAILED.\n{res.stdout}\n{res.stderr}")
        all_passed = False

    # 5. Verify .antigravity/skills structure
    test_step("Verifying .antigravity/skills structure")
    ag_skills_dir = ROOT / ".antigravity" / "skills"
    if ag_skills_dir.exists() and any(ag_skills_dir.iterdir()):
        print(f"✅ .antigravity/skills contains {len(list(ag_skills_dir.iterdir()))} skills.")
    else:
        print("❌ .antigravity/skills is empty or missing. Run 'python scripts/sync_skills.py'.")
        all_passed = False

    if all_passed:
        print("\n✨ ALL ANTIGRAVITY INTEGRATION CHECKS PASSED! ✨")
        sys.exit(0)
    else:
        print("\n❌ SOME CHECKS FAILED. Please review the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
