import json

import pytest
from conductor_core.models import TrackStatus
from conductor_core.project_manager import ProjectManager


@pytest.fixture()
def workspace(tmp_path):
    return tmp_path


def test_initialize_project(workspace):
    manager = ProjectManager(base_path=str(workspace))
    manager.initialize_project(goal="Test project goal")

    conductor_dir = workspace / "conductor"
    assert conductor_dir.exists()
    assert (conductor_dir / "setup_state.json").exists()
    assert (conductor_dir / "product.md").exists()

    product_content = (conductor_dir / "product.md").read_text()
    assert "Test project goal" in product_content


def test_create_track(workspace):
    manager = ProjectManager(base_path=str(workspace))
    manager.initialize_project(goal="Test goal")

    track_id = manager.create_track(description="Test track description")

    track_dir = workspace / "conductor" / "tracks" / track_id
    assert track_dir.exists()
    assert (track_dir / "metadata.json").exists()

    with (track_dir / "metadata.json").open() as f:
        metadata = json.load(f)
        assert metadata["description"] == "Test track description"
        assert metadata["status"] == TrackStatus.NEW


def test_create_track_metadata_fields(workspace):
    manager = ProjectManager(base_path=str(workspace))
    manager.initialize_project(goal="Test goal")

    track_id = manager.create_track(description="Metadata fields")
    track_dir = workspace / "conductor" / "tracks" / track_id
    metadata = json.loads((track_dir / "metadata.json").read_text())

    assert metadata["track_id"] == track_id
    assert metadata["status"] == TrackStatus.NEW
    assert "created_at" in metadata
    assert "updated_at" in metadata

    tracks_md = (workspace / "conductor" / "tracks.md").read_text()
    assert f"/{track_id}/" in tracks_md
