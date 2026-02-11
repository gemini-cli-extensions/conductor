import sys
from pathlib import Path

from conductor_core.models import PlatformCapability, SkillManifest


def _repo_root():
    return Path(__file__).resolve().parents[2]


def test_valid_skill_manifest():
    manifest = SkillManifest(
        id="test-skill",
        name="Test Skill",
        description="A test skill",
        version="1.0.0",
        engine_compatibility=">=0.1.0",
        triggers=["test", "demo"],
        commands={"claude": "/test-skill", "vscode": "@conductor /test"},
        capabilities=[PlatformCapability.UI_PROMPT, PlatformCapability.FILE_SYSTEM],
    )
    assert manifest.id == "test-skill"
    assert "test" in manifest.triggers
    assert manifest.commands["claude"] == "/test-skill"


def test_rendered_skill_matches_repo_output():
    repo_root = _repo_root()
    sys.path.insert(0, str(repo_root))
    from scripts.skills_manifest import render_skill

    manifest_path = repo_root / "skills" / "manifest.json"
    templates_dir = repo_root / "conductor-core" / "src" / "conductor_core" / "templates"
    skill_dir = repo_root / "skills" / "conductor-setup" / "SKILL.md"

    rendered = render_skill(manifest_path, templates_dir, "setup").strip()
    expected = skill_dir.read_text(encoding="utf-8").strip()

    assert rendered == expected
