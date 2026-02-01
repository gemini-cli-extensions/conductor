import json


def test_sync_skills_updates_vscode_package_json(tmp_path, monkeypatch):
    """Verifies that syncing skills updates the VS Code package.json with commands."""
    # Setup mock repo structure in tmp_path
    repo_root = tmp_path
    (repo_root / "skills").mkdir()
    (repo_root / "conductor-vscode").mkdir()

    # Mock manifest
    manifest_data = {
        "manifest_version": 1,
        "tools": {},
        "extensions": {},
        "skills": [
            {
                "id": "test-skill",
                "name": "conductor-test",
                "description": "Test",
                "commands": {"vscode": "@conductor /test"},
                "enabled": {"vscode": True},
                "template": "setup",
            }
        ],
    }
    manifest_path = repo_root / "skills" / "manifest.json"
    manifest_path.write_text(json.dumps(manifest_data))

    # Mock package.json
    package_json_path = repo_root / "conductor-vscode" / "package.json"
    package_json_data = {"name": "conductor-vscode", "contributes": {"commands": []}}
    package_json_path.write_text(json.dumps(package_json_data))

    # Mock templates
    templates_dir = repo_root / "conductor-core" / "src" / "conductor_core" / "templates"
    templates_dir.mkdir(parents=True)
    (templates_dir / "setup.j2").write_text("Mock template")
    (templates_dir / "SKILL.md.j2").write_text("Mock skill template")
    # Patch script variables
    import scripts.sync_skills as sync_module

    monkeypatch.setattr(sync_module, "ROOT", repo_root)
    monkeypatch.setattr(sync_module, "MANIFEST_PATH", manifest_path)
    monkeypatch.setattr(sync_module, "VSCODE_SKILLS_DIR", repo_root / "conductor-vscode" / "skills")
    monkeypatch.setattr(sync_module, "TEMPLATES_DIR", templates_dir)
    monkeypatch.setattr(sync_module, "load_manifest", lambda _path: manifest_data)
    monkeypatch.setattr(sync_module, "iter_skills", lambda manifest: manifest.get("skills", []))
    monkeypatch.setattr(sync_module, "validate_manifest", lambda *args, **kwargs: None)

    # This should now pass
    sync_module.sync_skills()

    updated_pkg = json.loads(package_json_path.read_text())
    commands = [cmd["command"] for cmd in updated_pkg["contributes"]["commands"]]

    assert "conductor.test-skill" in commands
