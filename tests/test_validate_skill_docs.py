import pytest

from scripts.validate_skill_docs import validate_skill_md


def test_validate_skill_md_valid(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    f = d / "SKILL.md"
    f.write_text(
        """---
name: Test Skill
description: A test skill
triggers: ["test"]
version: 1.0.0
engine_compatibility: ">=0.1.0"
---

# Test Skill

## Triggers
- test

## Usage
Ask to test.
""",
        encoding="utf-8",
    )

    # Should not raise
    validate_skill_md(f)


def test_validate_skill_md_invalid(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    f = d / "SKILL.md"
    f.write_text(
        """---
name: Test Skill
---
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing key 'description'"):
        validate_skill_md(f)
