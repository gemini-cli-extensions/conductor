from unittest.mock import MagicMock

import pytest
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner


@pytest.fixture()
def tr(tmp_path):
    pm = ProjectManager(tmp_path)
    pm.initialize_project("Goal")
    git_mock = MagicMock()
    return TaskRunner(pm, git_service=git_mock)


def test_get_track_to_implement_no_tracks_file(tr, tmp_path):
    (tmp_path / "conductor" / "tracks.md").unlink()
    with pytest.raises(FileNotFoundError, match="tracks.md not found"):
        tr.get_track_to_implement()


def test_get_track_to_implement_empty_tracks(tr, tmp_path):
    (tmp_path / "conductor" / "tracks.md").write_text("# Tracks")
    with pytest.raises(ValueError, match="No active tracks found"):
        tr.get_track_to_implement()


def test_get_track_to_implement_not_found(tr, tmp_path):
    tr.pm.create_track("Real Track")
    with pytest.raises(ValueError, match="No track found matching description"):
        tr.get_track_to_implement("Fake Track")


def test_update_track_status_not_found(tr):
    with pytest.raises(ValueError, match="Could not find track"):
        tr.update_track_status("missing_id", "~")


def test_update_task_status_missing_plan(tr):
    with pytest.raises(FileNotFoundError, match="plan.md not found"):
        tr.update_task_status("any_id", "task", "x")


def test_update_task_status_not_found(tr, tmp_path):
    track_id = tr.pm.create_track("Task Test")
    plan_file = tmp_path / "conductor" / "tracks" / track_id / "plan.md"
    plan_file.write_text("- [ ] Real Task")
    with pytest.raises(ValueError, match="Could not find task 'Fake Task'"):
        tr.update_task_status(track_id, "Fake Task", "x")


def test_checkpoint_phase_not_found(tr, tmp_path):
    track_id = tr.pm.create_track("Phase Test")
    plan_file = tmp_path / "conductor" / "tracks" / track_id / "plan.md"
    plan_file.write_text("## Phase 1: Real")
    with pytest.raises(ValueError, match="Could not find phase 'Fake'"):
        tr.checkpoint_phase(track_id, "Fake", "1234567")


def test_checkpoint_phase_missing_plan(tr):
    with pytest.raises(FileNotFoundError, match="plan.md not found"):
        tr.checkpoint_phase("any_id", "Phase 1", "1234567")


def test_archive_track_not_found(tr):
    with pytest.raises(FileNotFoundError, match="Track directory .* not found"):
        tr.archive_track("missing_id")


def test_archive_track_already_archived(tr, tmp_path):
    track_id = tr.pm.create_track("Archive Test")
    tr.archive_track(track_id)
    # Try archiving again
    with pytest.raises(FileNotFoundError):
        tr.archive_track(track_id)


def test_archive_track_target_exists(tr, tmp_path):
    track_id = tr.pm.create_track("Collision")
    # Manually create a directory in archive with same name
    (tmp_path / "conductor" / "archive" / track_id).mkdir(parents=True)
    tr.archive_track(track_id)  # Should overwrite via shutil.rmtree
    assert not (tmp_path / "conductor" / "tracks" / track_id).exists()
    assert (tmp_path / "conductor" / "archive" / track_id).exists()


def test_archive_track_without_separator(tr, tmp_path):
    track_id = "manual_id_456"
    tracks_file = tmp_path / "conductor" / "tracks.md"
    (tmp_path / "conductor" / "tracks" / track_id).mkdir(parents=True)

    # Construct a track without leading separator
    content = chr(10).join(
        [
            "# Project Tracks",
            "",
            "- [ ] **Track: Test**",
            f"*Link: [./conductor/tracks/{track_id}/](./conductor/tracks/{track_id}/)*",
        ]
    )
    tracks_file.write_text(content)

    tr.archive_track(track_id)
    assert track_id not in tracks_file.read_text()
