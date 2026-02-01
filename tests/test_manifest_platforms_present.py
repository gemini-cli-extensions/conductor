import json
from pathlib import Path


def test_manifest_platforms_present():
    manifest_path = Path("skills/manifest.json")
    with manifest_path.open(encoding="utf-8") as f:
        manifest = json.load(f)

    tools = manifest.get("tools", {})
    assert "aix" in tools
    assert "skillshare" in tools

    for skill in manifest.get("skills", []):
        assert "aix" in skill["commands"]
        assert "skillshare" in skill["commands"]
        assert "aix" in skill["enabled"]
        assert "skillshare" in skill["enabled"]
