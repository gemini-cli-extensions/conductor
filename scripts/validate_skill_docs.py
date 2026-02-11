import re
import sys
from pathlib import Path

import yaml


def validate_skill_md(file_path: Path) -> None:
    content = file_path.read_text(encoding="utf-8")

    # Check for YAML frontmatter
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter in {file_path}")

    frontmatter = yaml.safe_load(match.group(1))
    required_keys = ["name", "description", "triggers", "version", "engine_compatibility"]
    for key in required_keys:
        if key not in frontmatter:
            raise ValueError(f"Missing key '{key}' in frontmatter of {file_path}")

    # Check for header
    if f"# {frontmatter['name']}" not in content:
        raise ValueError(f"Missing main header '# {frontmatter['name']}' in {file_path}")

    # Check for required sections
    required_sections = ["## Triggers", "## Usage"]
    for section in required_sections:
        if section not in content:
            raise ValueError(f"Missing required section '{section}' in {file_path}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    skills_dir = repo_root / "skills"

    success = True
    for skill_path in skills_dir.glob("**/SKILL.md"):
        try:
            validate_skill_md(skill_path)
        except Exception:
            success = False

    if not success:
        sys.exit(1)
