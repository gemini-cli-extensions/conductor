import json
from pathlib import Path
from typing import Dict, Iterable, Optional

MANIFEST_SCHEMA_VERSION = 1


def load_manifest(manifest_path: Path) -> Dict:
    with open(manifest_path, "r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("manifest_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError("Unsupported manifest_version")
    return manifest


def iter_skills(manifest: Dict) -> Iterable[Dict]:
    return manifest.get("skills", [])


def get_extension(manifest: Dict, tool_name: str) -> Optional[Dict]:
    return manifest.get("extensions", {}).get(tool_name)


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

    rendered = "\n".join(content)
    _assert_rendered_matches_template(skill["name"], rendered, template_content)
    return rendered


def _assert_rendered_matches_template(
    skill_name: str, rendered: str, template_content: str
) -> None:
    if not template_content.strip():
        raise ValueError(f"Template content is empty for {skill_name}")
    if not rendered.endswith(template_content):
        raise ValueError(f"Rendered content diverged from template for {skill_name}")
