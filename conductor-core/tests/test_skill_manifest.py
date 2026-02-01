import pytest
from conductor_core.models import PlatformCapability, SkillManifest
from pydantic import ValidationError


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


def test_invalid_skill_manifest_missing_fields():
    with pytest.raises(ValidationError):
        # Missing required fields like id, name, version
        SkillManifest(description="Missing fields")


def test_invalid_version_format():
    with pytest.raises(ValidationError):
        SkillManifest(
            id="test", name="Test", version="invalid-version", engine_compatibility=">=0.1.0", triggers=["test"]
        )
