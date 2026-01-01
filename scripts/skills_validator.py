import json
import re
from pathlib import Path
from typing import Any, Dict


def validate_manifest(manifest_path: Path, schema_path: Path) -> None:
    manifest = _load_json(manifest_path)
    schema = _load_json(schema_path)

    try:
        import jsonschema  # type: ignore

        jsonschema.validate(instance=manifest, schema=schema)
    except ImportError:
        _basic_validate(manifest, schema)

    skills_dir = manifest_path.parent
    _validate_skill_frontmatter(manifest, skills_dir)
    _validate_command_styles(manifest)


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _basic_validate(manifest: Dict[str, Any], schema: Dict[str, Any]) -> None:
    required = schema.get("required", [])
    for key in required:
        if key not in manifest:
            raise ValueError(f"Manifest missing required key: {key}")

    if not isinstance(manifest.get("manifest_version"), int):
        raise ValueError("manifest_version must be an integer")
    if not isinstance(manifest.get("tools"), dict):
        raise ValueError("tools must be an object")
    if not isinstance(manifest.get("skills"), list):
        raise ValueError("skills must be an array")


def _parse_frontmatter(path: Path) -> Dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing frontmatter in {path}")

    data = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def _validate_skill_frontmatter(manifest: Dict[str, Any], skills_dir: Path) -> None:
    for skill in manifest.get("skills", []):
        skill_path = skills_dir / skill["name"] / "SKILL.md"
        if not skill_path.exists():
            raise ValueError(f"Missing SKILL.md for {skill['name']}")
        frontmatter = _parse_frontmatter(skill_path)
        if frontmatter.get("name") != skill["name"]:
            raise ValueError(f"Frontmatter name mismatch for {skill['name']}")
        if frontmatter.get("description") != skill["description"]:
            raise ValueError(f"Frontmatter description mismatch for {skill['name']}")


def _validate_command_styles(manifest: Dict[str, Any]) -> None:
    style_patterns = {
        "slash-colon": re.compile(r"^/[^\s:]+:[^\s]+$"),
        "slash-dash": re.compile(r"^/[^\s/]+-[^\s]+$"),
        "dollar-dash": re.compile(r"^\$[^\s/]+-[^\s]+$"),
        "at-mention + slash": re.compile(r"^@[^\s]+\s+/[^\s]+$"),
    }

    tools = manifest.get("tools", {})
    for skill in manifest.get("skills", []):
        for tool_name, command in skill.get("commands", {}).items():
            tool = tools.get(tool_name, {})
            style = tool.get("command_style")
            if not style:
                raise ValueError(f"Missing command_style for tool: {tool_name}")
            pattern = style_patterns.get(style)
            if not pattern:
                raise ValueError(f"Unknown command_style: {style}")
            if not pattern.match(command):
                raise ValueError(f"Command style mismatch for {tool_name}: {command}")
