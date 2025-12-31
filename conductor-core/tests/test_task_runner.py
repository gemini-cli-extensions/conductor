import pytest
import os
from pathlib import Path
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner
from git import Repo

@pytest.fixture
def project(tmp_path):
    pm = ProjectManager(tmp_path)
    pm.initialize_project("Test project")
    Repo.init(tmp_path)
    return pm

def test_select_next_track(project):
    project.create_track("Track 1")
    project.create_track("Track 2")
    
    runner = TaskRunner(project)
    track_id, desc, status = runner.get_track_to_implement()
    
    assert desc == "Track 1"
    assert status == "" # Empty because it's [ ]

def test_select_specific_track(project):
    project.create_track("Feature A")
    project.create_track("Feature B")
    
    runner = TaskRunner(project)
    track_id, desc, status = runner.get_track_to_implement("Feature B")
    
    assert desc == "Feature B"

def test_update_track_status(project):
    track_id = project.create_track("Track to update")
    runner = TaskRunner(project)
    
    runner.update_track_status(track_id, "~")
    
    tracks_file = project.conductor_path / "tracks.md"
    assert "## [~] Track: Track to update" in tracks_file.read_text()

def test_archive_track(project, tmp_path):
    track_id = project.create_track("Track to archive")
    track_dir = project.conductor_path / "tracks" / track_id
    (track_dir / "plan.md").write_text("# Plan")
    
    runner = TaskRunner(project)
    runner.archive_track(track_id)
    
    assert not track_dir.exists()
    assert (project.conductor_path / "archive" / track_id).exists()
    assert (project.conductor_path / "archive" / track_id / "plan.md").exists()
    assert "Track to archive" not in (project.conductor_path / "tracks.md").read_text()
