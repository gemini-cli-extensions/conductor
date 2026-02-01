from scripts.check_skills_sync import _check_antigravity_workflows, _check_vsix_artifact
from scripts.skills_manifest import render_antigravity_workflow_content


def test_check_antigravity_workflows_match(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "setup.j2").write_text("Template body")

    skill = {"name": "conductor-setup", "description": "Setup", "template": "setup"}
    target_dir = tmp_path / "workflows"
    target_dir.mkdir()

    expected = render_antigravity_workflow_content(skill, templates_dir)
    (target_dir / "conductor-setup.md").write_text(expected)

    mismatches = _check_antigravity_workflows([skill], templates_dir, target_dir, fix=False, optional=False)
    assert mismatches == []


def test_check_antigravity_workflows_missing(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "setup.j2").write_text("Template body")

    skill = {"name": "conductor-setup", "description": "Setup", "template": "setup"}
    target_dir = tmp_path / "workflows"
    target_dir.mkdir()

    mismatches = _check_antigravity_workflows([skill], templates_dir, target_dir, fix=False, optional=False)
    assert any("Missing:" in item for item in mismatches)


def test_check_vsix_missing(tmp_path):
    vsix_path = tmp_path / "conductor.vsix"
    mismatches = _check_vsix_artifact(vsix_path, require=True)
    assert any("Missing VSIX" in item for item in mismatches)
