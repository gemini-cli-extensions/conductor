import json
from pathlib import Path
from typing import Dict, Iterable

MANIFEST_SCHEMA_VERSION = 1


def load_manifest(manifest_path: Path) -> Dict:
    with open(manifest_path, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("manifest_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError("Unsupported manifest_version")
    return manifest


def iter_skills(manifest: Dict) -> Iterable[Dict]:
    return manifest.get("skills", [])


def render_skill(manifest_path: Path, templates_dir: Path, skill_id: str) -> str:
    manifest = load_manifest(manifest_path)
    skill = next((item for item in iter_skills(manifest) if item["id"] == skill_id), None)
    if not skill:
        raise KeyError(f"Unknown skill id: {skill_id}")
    return render_skill_content(skill, templates_dir)


def render_skill_content(skill: Dict, templates_dir: Path) -> str:
    template_file = templates_dir / f"{skill['template']}.j2"
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    template_content = template_file.read_text(encoding="utf-8")

    content = [
        "---",
        f"name: {skill['name']}",
        f"description: {skill['description']}",
        "license: Apache-2.0",
        "compatibility: Works with Claude Code, Gemini CLI, and any Agent Skills compatible CLI",
        "---",
        "",
        template_content,
    ]

    return "\n".join(content)
