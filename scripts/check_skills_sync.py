import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.skills_manifest import iter_skills, load_manifest, render_skill_content  # noqa: E402
from scripts.skills_validator import validate_manifest  # noqa: E402

TEMPLATES_DIR = ROOT / "conductor-core" / "src" / "conductor_core" / "templates"
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
SCHEMA_PATH = ROOT / "skills" / "manifest.schema.json"

REPO_SKILL_DIRS = [
    ROOT / "skills",
    ROOT / ".antigravity" / "skills",
    ROOT / "conductor-vscode" / "skills",
]

EXTENSION_PATHS = {
    "gemini": ROOT / "gemini-extension.json",
    "qwen": ROOT / "qwen-extension.json",
}


def _check_skill_dir(
    skills: List[Dict], templates_dir: Path, target_dir: Path, fix: bool
) -> List[str]:
    mismatches = []
    if not target_dir.exists():
        return [f"Missing directory: {target_dir}"]

    for skill in skills:
        expected = render_skill_content(skill, templates_dir)
        skill_file = target_dir / skill["name"] / "SKILL.md"
        if not skill_file.exists():
            mismatches.append(f"Missing: {skill_file}")
            if fix:
                skill_file.parent.mkdir(parents=True, exist_ok=True)
                skill_file.write_text(expected, encoding="utf-8")
            continue
        actual = skill_file.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(f"Mismatch: {skill_file}")
            if fix:
                skill_file.write_text(expected, encoding="utf-8")
    return mismatches


def _check_extensions(manifest: Dict, fix: bool) -> List[str]:
    mismatches = []
    extensions = manifest.get("extensions", {})
    for tool_name, target_path in EXTENSION_PATHS.items():
        expected = extensions.get(tool_name)
        if not expected:
            mismatches.append(f"Missing extension metadata: {tool_name}")
            continue
        if not target_path.exists():
            mismatches.append(f"Missing: {target_path}")
            if fix:
                target_path.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
            continue
        actual = json.loads(target_path.read_text(encoding="utf-8"))
        if actual != expected:
            mismatches.append(f"Mismatch: {target_path}")
            if fix:
                target_path.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated skill artifacts for drift.")
    parser.add_argument("--fix", action="store_true", help="Rewrite repo-local outputs to match manifest")
    args = parser.parse_args()

    validate_manifest(MANIFEST_PATH, SCHEMA_PATH)

    manifest = load_manifest(MANIFEST_PATH)
    skills = list(iter_skills(manifest))

    mismatches: List[str] = []
    for target_dir in REPO_SKILL_DIRS:
        mismatches.extend(_check_skill_dir(skills, TEMPLATES_DIR, target_dir, args.fix))

    mismatches.extend(_check_extensions(manifest, args.fix))

    if mismatches:
        print("Skill sync issues detected:")
        for item in mismatches:
            print(f"- {item}")
        return 1

    print("Skill outputs are in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
