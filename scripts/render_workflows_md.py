import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from scripts.skills_manifest import iter_skills, load_manifest  # noqa: E402

MANIFEST_PATH = ROOT / "skills" / "manifest.json"
TEMPLATES_DIR = ROOT / "conductor-core" / "src" / "conductor_core" / "templates"
TARGET_PATH = ROOT / ".claude" / "skills" / "conductor" / "references" / "workflows.md"


def render() -> str:
    manifest = load_manifest(MANIFEST_PATH)
    skills = list(iter_skills(manifest))

    lines = [
        "# Conductor",
        "",
        "Context-Driven Development for Claude Code. Measure twice, code once.",
        "",
        "## Commands",
        "",
        "| Command | Description |",
        "| --- | --- |",
    ]

    for skill in skills:
        lines.append(f"| `{skill['name'].replace('conductor-', '')}` | {skill['description']} |")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Instructions",
            "",
            "This document is generated from `skills/manifest.json` and the core templates.",
            "For the full protocol for each command, see the corresponding command SKILL.md.",
        ]
    )

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    TARGET_PATH.parent.mkdir(parents=True, exist_ok=True)
    TARGET_PATH.write_text(render(), encoding="utf-8")
