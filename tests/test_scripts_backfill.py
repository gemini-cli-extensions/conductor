import importlib
import json
import runpy
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from scripts.install_local import _resolve_locations, install_antigravity_vsix, install_vsix
from scripts.skills_manifest import (
    load_manifest,
    render_skill,
)
from scripts.sync_skills import (
    _clean_antigravity_global,
    update_vscode_package_json,
)


@pytest.fixture()
def mock_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "skills").mkdir()
    (repo / "conductor-vscode").mkdir()
    (repo / "conductor-core" / "src" / "conductor_core" / "templates").mkdir(parents=True)

    manifest = {
        "manifest_version": 1,
        "tools": {"gemini": {"name": "G"}},
        "extensions": {"gemini": {"id": "ext"}},
        "skills": [
            {
                "id": "s1",
                "name": "c1",
                "description": "D",
                "enabled": {"vscode": True, "gemini": True},
                "template": "setup",
                "commands": {"claude": "/c", "codex": "/cx"},
            }
        ],
    }
    (repo / "skills" / "manifest.json").write_text(json.dumps(manifest))
    (repo / "conductor-core" / "src" / "conductor_core" / "templates" / "setup.j2").write_text("T")
    (repo / "conductor-core" / "src" / "conductor_core" / "templates" / "SKILL.md.j2").write_text("{{ skill.name }}")

    return repo


def test_skills_manifest_all(mock_repo):
    manifest_path = mock_repo / "skills" / "manifest.json"
    templates_dir = mock_repo / "conductor-core" / "src" / "conductor_core" / "templates"

    content = render_skill(manifest_path, templates_dir, "s1")
    assert "c1" in content

    v2_path = mock_repo / "v2.json"
    v2_path.write_text(json.dumps({"manifest_version": 2}))
    with pytest.raises(ValueError, match="Unsupported manifest_version"):
        load_manifest(v2_path)


def test_sync_skills_all(mock_repo, monkeypatch):
    sync_module = importlib.import_module("scripts.sync_skills")

    monkeypatch.setattr(sync_module, "ROOT", mock_repo)
    monkeypatch.setattr(sync_module, "MANIFEST_PATH", mock_repo / "skills" / "manifest.json")
    monkeypatch.setattr(
        sync_module, "TEMPLATES_DIR", mock_repo / "conductor-core" / "src" / "conductor_core" / "templates"
    )
    monkeypatch.setattr(sync_module, "SKILLS_DIR", mock_repo / "skills")
    monkeypatch.setattr(sync_module, "VSCODE_SKILLS_DIR", mock_repo / "conductor-vscode" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_DIR", mock_repo / ".antigravity" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_WORKSPACE_DIR", mock_repo / ".agent" / "workflows")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_SKILLS_WORKSPACE_DIR", mock_repo / ".agent" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_SKILLS_GLOBAL_DIR", mock_repo / ".gemini" / "antigravity" / "skills")
    monkeypatch.setattr(sync_module, "validate_manifest", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(sync_module, "iter_skills", lambda manifest: manifest.get("skills", []))

    # Missing package.json
    update_vscode_package_json([])

    # Clean non-existent dir
    _clean_antigravity_global(mock_repo / "none", [])

    # Clean with unlink
    target = mock_repo / "clean"
    target.mkdir()
    (target / "conductor-old.md").write_text("old")
    _clean_antigravity_global(target, [])
    assert not (target / "conductor-old.md").exists()

    skills = [
        {"id": "s1", "name": "c1", "description": "d", "enabled": {"vscode": False}},
        {"id": "s2", "name": "c2", "description": "d", "enabled": {"vscode": True}, "template": "setup"},
    ]

    monkeypatch.setenv("CONDUCTOR_SYNC_REPO_ONLY", "1")
    with (
        patch("scripts.sync_skills.load_manifest", return_value={"manifest_version": 1, "skills": skills}),
        patch("scripts.sync_skills.validate_manifest"),
        patch("scripts.sync_skills.print"),
    ):
        runpy.run_module("scripts.sync_skills", run_name="__main__")


def test_sync_skills_antigravity_skills_output(mock_repo, monkeypatch):
    sync_module = importlib.import_module("scripts.sync_skills")

    monkeypatch.setattr(sync_module, "ROOT", mock_repo)
    monkeypatch.setattr(sync_module, "MANIFEST_PATH", mock_repo / "skills" / "manifest.json")
    monkeypatch.setattr(
        sync_module, "TEMPLATES_DIR", mock_repo / "conductor-core" / "src" / "conductor_core" / "templates"
    )
    monkeypatch.setattr(sync_module, "SKILLS_DIR", mock_repo / "skills")
    monkeypatch.setattr(sync_module, "VSCODE_SKILLS_DIR", mock_repo / "conductor-vscode" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_DIR", mock_repo / ".antigravity" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_WORKSPACE_DIR", mock_repo / ".agent" / "workflows")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_SKILLS_WORKSPACE_DIR", mock_repo / ".agent" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_SKILLS_GLOBAL_DIR", mock_repo / ".gemini" / "antigravity" / "skills")
    monkeypatch.setattr(sync_module, "validate_manifest", lambda *_args, **_kwargs: None)

    skills = [
        {"id": "s1", "name": "c1", "description": "d", "enabled": {"vscode": False}, "template": "setup"},
    ]

    sync_module.sync_antigravity_skills(skills, repo_only=False)

    assert (mock_repo / ".agent" / "skills" / "c1" / "SKILL.md").exists()
    assert (mock_repo / ".gemini" / "antigravity" / "skills" / "c1" / "SKILL.md").exists()


def test_sync_skills_emits_antigravity_skills(mock_repo, monkeypatch):
    sync_module = importlib.import_module("scripts.sync_skills")

    monkeypatch.setattr(sync_module, "ROOT", mock_repo)
    monkeypatch.setattr(sync_module, "MANIFEST_PATH", mock_repo / "skills" / "manifest.json")
    monkeypatch.setattr(
        sync_module, "TEMPLATES_DIR", mock_repo / "conductor-core" / "src" / "conductor_core" / "templates"
    )
    monkeypatch.setattr(sync_module, "SKILLS_DIR", mock_repo / "skills")
    monkeypatch.setattr(sync_module, "VSCODE_SKILLS_DIR", mock_repo / "conductor-vscode" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_DIR", mock_repo / ".antigravity" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_WORKSPACE_DIR", mock_repo / ".agent" / "workflows")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_SKILLS_WORKSPACE_DIR", mock_repo / ".agent" / "skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_SKILLS_GLOBAL_DIR", mock_repo / ".gemini" / "antigravity" / "skills")
    monkeypatch.setattr(sync_module, "validate_manifest", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(sync_module, "iter_skills", lambda manifest: manifest.get("skills", []))

    skills = [
        {"id": "s1", "name": "c1", "description": "d", "enabled": {"vscode": False}, "template": "setup"},
    ]

    monkeypatch.setenv("CONDUCTOR_ANTIGRAVITY_SKILLS", "1")
    monkeypatch.setenv("CONDUCTOR_SYNC_REPO_ONLY", "1")
    with (
        patch("scripts.sync_skills.load_manifest", return_value={"manifest_version": 1, "skills": skills}),
        patch("scripts.sync_skills.validate_manifest"),
        patch("scripts.sync_skills.sync_antigravity_skills") as mock_sync,
        patch("scripts.sync_skills.print"),
    ):
        sync_module.sync_skills()

    mock_sync.assert_called_once_with(skills, repo_only=True)


def test_install_local_all():
    with (
        patch("scripts.install_local.Path.exists", return_value=False),
        patch("scripts.sync_skills.sync_skills"),
        patch("scripts.sync_skills.validate_manifest"),
        patch("scripts.install_local.sync_antigravity_global_workflows"),
        patch("scripts.install_local.sync_antigravity_workspace_workflows"),
        patch("scripts.install_local.print"),
        pytest.raises(SystemExit) as e,
    ):
        runpy.run_module("scripts.install_local", run_name="__main__")
    assert e.value.code == 1


def test_install_local_functions_fail(capsys):
    with patch("subprocess.run", side_effect=FileNotFoundError):
        install_vsix(Path("test.vsix"), dry_run=False)
        install_antigravity_vsix(Path("test.vsix"), dry_run=False)
    captured = capsys.readouterr()
    assert "not found or failed" in captured.out


def test_resolve_locations_posix():
    repo_root = PurePosixPath("/repo")
    home = PurePosixPath("/home/user")
    locations = _resolve_locations(repo_root, home)
    assert str(locations["antigravity-global"]) == "/home/user/.gemini/antigravity/global_workflows"
    assert str(locations["copilot"]) == "/home/user/.config/github-copilot/conductor.md"
    assert str(locations["vsix"]) == "/repo/conductor.vsix"


def test_resolve_locations_windows():
    repo_root = PureWindowsPath("C:/repo")
    home = PureWindowsPath("C:/Users/Alice")
    locations = _resolve_locations(repo_root, home)
    assert str(locations["antigravity-global"]) == r"C:\Users\Alice\.gemini\antigravity\global_workflows"
    assert str(locations["copilot"]) == r"C:\Users\Alice\.config\github-copilot\conductor.md"


def test_validate_artifacts_runs_checks(monkeypatch):
    validate_artifacts = importlib.import_module("scripts.validate_artifacts")
    calls: list[list[str]] = []

    def fake_run(cmd, **_kwargs):
        calls.append(cmd)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(validate_artifacts, "ROOT", Path("repo"))
    monkeypatch.setattr(validate_artifacts.subprocess, "run", fake_run)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validate_artifacts.py",
            "--require-vsix",
            "--check-global",
            "--check-antigravity-skills",
            "--fix",
        ],
    )

    assert validate_artifacts.main() == 0
    assert any("scripts/check_skills_sync.py" in " ".join(cmd) for cmd in calls)
    assert any("scripts/validate_platforms.py" in " ".join(cmd) for cmd in calls)
