from pathlib import Path
import sys

import pytest


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_load_manifest_has_expected_skills():
    repo_root = _repo_root()
    sys.path.insert(0, str(repo_root))
    from scripts.skills_manifest import load_manifest

    manifest = load_manifest(repo_root / "skills" / "manifest.json")
    skill_names = {skill["name"] for skill in manifest["skills"]}

    assert "conductor-setup" in skill_names
    assert "conductor-implement" in skill_names


def test_rendered_skill_matches_repo_output():
    repo_root = _repo_root()
    sys.path.insert(0, str(repo_root))
    from scripts.skills_manifest import render_skill

    manifest_path = repo_root / "skills" / "manifest.json"
    templates_dir = repo_root / "conductor-core" / "src" / "conductor_core" / "templates"
    skill_dir = repo_root / "skills" / "conductor-setup" / "SKILL.md"

    rendered = render_skill(manifest_path, templates_dir, "setup")
    expected = skill_dir.read_text(encoding="utf-8")

    assert rendered == expected
