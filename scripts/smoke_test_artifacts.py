import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def smoke_test():
    manifest_path = ROOT / "skills" / "manifest.json"
    if not manifest_path.exists():
        return False

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    skills = manifest.get("skills", [])
    success = True

    # 1. Check local skills directory
    for skill in skills:
        skill_name = skill["name"]
        skill_file = ROOT / "skills" / skill_name / "SKILL.md"
        if not skill_file.exists():
            success = False

    # 2. Check VS Code package.json
    vscode_pkg_path = ROOT / "conductor-vscode" / "package.json"
    if vscode_pkg_path.exists():
        with open(vscode_pkg_path, encoding="utf-8") as f:
            pkg_data = json.load(f)

        commands = [cmd["command"] for cmd in pkg_data.get("contributes", {}).get("commands", [])]
        for skill in skills:
            if skill.get("enabled", {}).get("vscode", False):
                cmd_id = f"conductor.{skill['id']}"
                if cmd_id not in commands:
                    success = False

    # 3. Check Gemini/Qwen manifests
    for ext in ["gemini-extension.json", "qwen-extension.json"]:
        path = ROOT / ext
        if path.exists():
            pass
            # Basic existence check for now

    if success:
        pass
    else:
        pass

    return success


if __name__ == "__main__":
    if not smoke_test():
        sys.exit(1)
