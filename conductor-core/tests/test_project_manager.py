import pytest
import os
import json
from pathlib import Path
from conductor_core.project_manager import ProjectManager
from conductor_core.models import TaskStatus, TrackStatus

@pytest.fixture
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
    
    with open(track_dir / "metadata.json") as f:
        metadata = json.load(f)
        assert metadata["description"] == "Test track description"
        assert metadata["status"] == TrackStatus.NEW
