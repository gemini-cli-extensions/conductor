from pathlib import Path

from scripts import sync_skills


def test_sync_skills_constants_exist():
    assert hasattr(sync_skills, "AIX_DIR")
    assert hasattr(sync_skills, "SKILLSHARE_DIR")
    assert isinstance(sync_skills.AIX_DIR, Path)
    assert isinstance(sync_skills.SKILLSHARE_DIR, Path)
