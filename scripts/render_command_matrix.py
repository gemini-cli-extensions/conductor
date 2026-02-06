import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
MANIFEST_PATH = ROOT / "skills" / "manifest.json"
TARGET_PATH = ROOT / "docs" / "skill-command-syntax.md"
START = "<!-- BEGIN: TOOL-MATRIX -->"
END = "<!-- END: TOOL-MATRIX -->"


def render_table(manifest: dict) -> str:
    lines = [
        START,
        "| Tool | Artifact Type / Location | Command Style | Example |",
        "| --- | --- | --- | --- |",
    ]
    for tool_name, tool in manifest.get("tools", {}).items():
        artifact = tool.get("artifact", "")
        style = tool.get("command_style", "")
        example = tool.get("example", "")
        lines.append(f"| {tool_name} | `{artifact}` | `{style}` | `{example}` |")
    lines.append(END)
    return "\n".join(lines)


def update_doc(content: str, table: str) -> str:
    if START not in content or END not in content:
        raise ValueError("Missing tool matrix markers in docs/skill-command-syntax.md")
    before, rest = content.split(START, 1)
    _current, after = rest.split(END, 1)
    return before.rstrip() + "\n\n" + table + "\n" + after.lstrip()


if __name__ == "__main__":
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    table = render_table(manifest)
    updated = update_doc(TARGET_PATH.read_text(encoding="utf-8"), table)
    TARGET_PATH.write_text(updated, encoding="utf-8")