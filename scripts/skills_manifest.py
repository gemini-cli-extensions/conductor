from __future__ import annotations

import json
from typing import TYPE_CHECKING

from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path

MANIFEST_SCHEMA_VERSION = 1


def load_manifest(manifest_path: Path) -> dict:
    with open(manifest_path, encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("manifest_version") != MANIFEST_SCHEMA_VERSION:
        raise ValueError("Unsupported manifest_version")
    return manifest


def iter_skills(manifest: dict) -> Iterable[dict]:
    return manifest.get("skills", [])


def get_extension(manifest: dict, tool_name: str) -> dict | None:
    return manifest.get("extensions", {}).get(tool_name)


def render_skill(manifest_path: Path, templates_dir: Path, skill_id: str) -> str:
    manifest = load_manifest(manifest_path)
    skill = next((item for item in iter_skills(manifest) if item["id"] == skill_id), None)
    if not skill:
        raise KeyError(f"Unknown skill id: {skill_id}")
    return render_skill_content(skill, templates_dir)


def render_skill_content(skill: dict, templates_dir: Path) -> str:
    env = Environment(loader=FileSystemLoader(str(templates_dir)), keep_trailing_newline=True)
    template = env.get_template("SKILL.md.j2")

    # Normalize skill data to match template expectations
    # The manifest uses "commands" but we might need to ensure other fields exist
    triggers = []
    if "commands" in skill:
        if "claude" in skill["commands"]:
            triggers.append(skill["commands"]["claude"])
        if "codex" in skill["commands"]:
            triggers.append(skill["commands"]["codex"])

    skill_data = {
        "id": skill["id"],
        "name": skill["name"],
        "description": skill["description"],
        "triggers": triggers,
        "version": skill.get("version", "0.1.0"),
        "engine_compatibility": ">=0.2.0",
        "commands": skill.get("commands", {}),
        "capabilities": [],  # Populate if available in manifest
    }

    # Override triggers if explicit trigger list exists (future proofing)
    if "triggers" in skill:
        skill_data["triggers"] = skill["triggers"]

    return template.render(skill=skill_data)


def render_antigravity_workflow_content(skill: dict, templates_dir: Path) -> str:
    template_path = templates_dir / f"{skill['template']}.j2"
    template_content = template_path.read_text(encoding="utf-8")

    header = "\n".join(
        [
            "---",
            f"description: {skill['description']}",
            "---",
            "",
        ]
    )
    return header + template_content
