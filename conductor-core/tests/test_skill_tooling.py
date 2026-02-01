import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_script_list():
    if not shutil.which("sh") and not shutil.which("bash"):
        pytest.skip("Shell not found, skipping install.sh test")

    repo_root = _repo_root()
    script_path = repo_root / "skill" / "scripts" / "install.sh"

    # On Windows, we need to invoke via sh/bash explicitly
    shell = shutil.which("bash") or shutil.which("sh")

    result = subprocess.run(
        [shell, str(script_path), "--list"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(repo_root / ".tmp_home")},
        check=False,
    )

    assert result.returncode == 0
    assert "Codex" in result.stdout


def test_manifest_validation_passes():
    repo_root = _repo_root()
    sys.path.insert(0, str(repo_root))
    from scripts.skills_validator import validate_manifest

    manifest_path = repo_root / "skills" / "manifest.json"
    schema_path = repo_root / "skills" / "manifest.schema.json"

    validate_manifest(manifest_path, schema_path)
