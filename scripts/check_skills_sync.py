import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.skills_manifest import (  # noqa: E402
    iter_skills,
    load_manifest,
    render_antigravity_workflow_content,
    render_skill_content,
)
from scripts.skills_validator import validate_manifest  # noqa: E402

TEMPLATES_DIR = ROOT / "conductor-core" / "src" / "conductor_core" / "templates"
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
SCHEMA_PATH = ROOT / "skills" / "manifest.schema.json"

REPO_SKILL_DIRS = [
    ROOT / "skills",
    ROOT / ".antigravity" / "skills",
    ROOT / "conductor-vscode" / "skills",
]
ANTIGRAVITY_WORKSPACE_DIR = ROOT / ".agent" / "workflows"
ANTIGRAVITY_GLOBAL_DIR = Path.home() / ".gemini" / "antigravity" / "global_workflows"
ANTIGRAVITY_SKILLS_WORKSPACE_DIR = ROOT / ".agent" / "skills"
ANTIGRAVITY_SKILLS_GLOBAL_DIR = Path.home() / ".gemini" / "antigravity" / "skills"
VSIX_PATH = ROOT / "conductor.vsix"

EXTENSION_PATHS = {
    "gemini": ROOT / "gemini-extension.json",
    "qwen": ROOT / "qwen-extension.json",
}


def _check_skill_dir(skills: list[dict], templates_dir: Path, target_dir: Path, *, fix: bool) -> list[str]:
    mismatches: list[str] = []
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


def _check_extensions(manifest: dict, *, fix: bool) -> list[str]:
    mismatches: list[str] = []
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


def _check_antigravity_workflows(
    skills: list[dict],
    templates_dir: Path,
    target_dir: Path,
    *,
    fix: bool,
    optional: bool = False,
) -> list[str]:
    mismatches: list[str] = []
    if optional:
        return mismatches
    if not target_dir.exists():
        return [f"Missing directory: {target_dir}"]

    for skill in skills:
        expected = render_antigravity_workflow_content(skill, templates_dir)
        workflow_file = target_dir / f"{skill['name']}.md"
        if not workflow_file.exists():
            mismatches.append(f"Missing: {workflow_file}")
            if fix:
                target_dir.mkdir(parents=True, exist_ok=True)
                workflow_file.write_text(expected, encoding="utf-8")
            continue
        actual = workflow_file.read_text(encoding="utf-8")
        if actual != expected:
            mismatches.append(f"Mismatch: {workflow_file}")
            if fix:
                workflow_file.write_text(expected, encoding="utf-8")
    return mismatches


def _check_vsix_artifact(vsix_path: Path, *, require: bool) -> list[str]:
    if not require:
        return []
    if not vsix_path.exists():
        return [f"Missing VSIX: {vsix_path}"]
    if vsix_path.stat().st_size == 0:
        return [f"Empty VSIX: {vsix_path}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated skill artifacts for drift.")
    parser.add_argument("--fix", action="store_true", help="Rewrite repo-local outputs to match manifest")
    parser.add_argument("--check-global", action="store_true", help="Validate Antigravity global workflows if present")
    parser.add_argument("--require-vsix", action="store_true", help="Require conductor.vsix to exist")
    parser.add_argument("--check-antigravity-skills", action="store_true", help="Validate Antigravity skills output")
    args = parser.parse_args()

    validate_manifest(MANIFEST_PATH, SCHEMA_PATH)

    manifest = load_manifest(MANIFEST_PATH)
    skills = list(iter_skills(manifest))

    mismatches: list[str] = []
    for target_dir in REPO_SKILL_DIRS:
        mismatches.extend(_check_skill_dir(skills, TEMPLATES_DIR, target_dir, fix=args.fix))

    mismatches.extend(
        _check_antigravity_workflows(skills, TEMPLATES_DIR, ANTIGRAVITY_WORKSPACE_DIR, fix=args.fix, optional=False)
    )
    global_required = args.check_global or os.environ.get("CONDUCTOR_VALIDATE_GLOBAL_ANTIGRAVITY") == "1"
    mismatches.extend(
        _check_antigravity_workflows(
            skills,
            TEMPLATES_DIR,
            ANTIGRAVITY_GLOBAL_DIR,
            fix=args.fix,
            optional=not global_required,
        )
    )

    mismatches.extend(_check_extensions(manifest, fix=args.fix))
    mismatches.extend(_check_vsix_artifact(VSIX_PATH, require=args.require_vsix))

    check_skills = args.check_antigravity_skills or os.environ.get("CONDUCTOR_VALIDATE_ANTIGRAVITY_SKILLS") == "1"
    if check_skills:
        mismatches.extend(_check_skill_dir(skills, TEMPLATES_DIR, ANTIGRAVITY_SKILLS_WORKSPACE_DIR, fix=args.fix))
        mismatches.extend(_check_skill_dir(skills, TEMPLATES_DIR, ANTIGRAVITY_SKILLS_GLOBAL_DIR, fix=args.fix))

    if mismatches:
        for _item in mismatches:
            pass
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
