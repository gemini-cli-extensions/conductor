import os
import subprocess
from pathlib import Path
import sys


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_install_script_list():
    repo_root = _repo_root()
    script_path = repo_root / "skill" / "scripts" / "install.sh"

    result = subprocess.run(
        [str(script_path), "--list"],
        capture_output=True,
        text=True,
        env={**os.environ, "HOME": str(repo_root / ".tmp_home")},
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
