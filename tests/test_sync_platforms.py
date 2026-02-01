import json
import os
from pathlib import Path
import scripts.sync_skills as sync_module

def test_sync_aix_and_skillshare(tmp_path, monkeypatch):
    repo_root = tmp_path
    (repo_root / "skills").mkdir()
    (repo_root / "conductor-vscode").mkdir()
    
    aix_dir = tmp_path / "aix"
    skillshare_dir = tmp_path / "skillshare"
    copilot_dir = tmp_path / "copilot"
    
    manifest_data = {
        "manifest_version": 1,
        "tools": {},
        "extensions": {},
        "skills": [
            {
                "id": "test",
                "template": "test",
                "name": "conductor-test",
                "description": "Test skill",
                "commands": {"aix": "/conductor-test", "skillshare": "/conductor-test"},
                "enabled": {"aix": True, "skillshare": True}
            }
        ],
    }
    
    manifest_path = repo_root / "skills" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest_data))
    
    templates_dir = repo_root / "conductor-core" / "src" / "conductor_core" / "templates"
    templates_dir.mkdir(parents=True)
    (templates_dir / "test.j2").write_text("Test template content")
    (templates_dir / "SKILL.md.j2").write_text("Skill content")

    monkeypatch.setattr(sync_module, "ROOT", repo_root)
    monkeypatch.setattr(sync_module, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(sync_module, "TEMPLATES_DIR", templates_dir)
    monkeypatch.setattr(sync_module, "AIX_DIR", aix_dir)
    monkeypatch.setattr(sync_module, "SKILLSHARE_DIR", skillshare_dir)
    monkeypatch.setattr(sync_module, "COPILOT_DIR", copilot_dir)
    monkeypatch.setattr(sync_module, "SKILLS_DIR", tmp_path / "repo_skills")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_DIR", tmp_path / "antigravity")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_WORKSPACE_DIR", tmp_path / "workspace_workflows")
    monkeypatch.setattr(sync_module, "ANTIGRAVITY_GLOBAL_DIR", tmp_path / "global_workflows")
    monkeypatch.setattr(sync_module, "CODEX_DIR", tmp_path / "codex")
    monkeypatch.setattr(sync_module, "CLAUDE_DIR", tmp_path / "claude")
    monkeypatch.setattr(sync_module, "OPENCODE_DIR", tmp_path / "opencode")
    monkeypatch.setattr(sync_module, "validate_manifest", lambda *args, **kwargs: None)
    
    # Ensure env var is set to avoid repo-only mode
    monkeypatch.setenv("CONDUCTOR_SYNC_REPO_ONLY", "0")
    
    sync_module.sync_skills()
    
    # Check SkillShare output
    assert (skillshare_dir / "conductor-test" / "SKILL.md").exists()
    
    # Check AIX output
    assert (aix_dir / "conductor.md").exists()
    aix_content = (aix_dir / "conductor.md").read_text()
    assert "## Command: /conductor-test" in aix_content
    assert "Test template content" in aix_content
