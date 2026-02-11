import json

import pytest
from conductor_core.project_manager import ProjectManager


@pytest.fixture()
def pm(tmp_path):
    return ProjectManager(tmp_path)


def test_initialize_project_already_exists(pm, tmp_path):
    (tmp_path / "conductor").mkdir()
    pm.initialize_project("Test Goal")
    assert (tmp_path / "conductor" / "product.md").exists()


def test_get_status_report_basic(pm):
    pm.initialize_project("Goal")
    report = pm.get_status_report()
    assert "Active Tracks" in report
    assert "No active tracks" in report


def test_get_status_report_with_active_track(pm, tmp_path):
    pm.initialize_project("Goal")
    track_id = pm.create_track("My Track")
    # Add a task to plan.md
    plan_file = tmp_path / "conductor" / "tracks" / track_id / "plan.md"
    plan_file.write_text("- [ ] Task 1")

    report = pm.get_status_report()
    assert "My Track" in report
    assert "0/1 tasks completed" in report


def test_get_status_report_with_archived_track(pm, tmp_path):
    pm.initialize_project("Goal")
    archive_dir = tmp_path / "conductor" / "archive" / "old_track"
    archive_dir.mkdir(parents=True)
    (archive_dir / "metadata.json").write_text(json.dumps({"description": "Old Track"}))
    (archive_dir / "plan.md").write_text("- [x] Done")

    report = pm.get_status_report()
    assert "Archived Tracks" in report
    assert "Old Track" in report
    assert "1/1 tasks completed" in report


def test_get_archived_tracks_invalid_json(pm, tmp_path):
    archive_dir = tmp_path / "conductor" / "archive" / "bad_track"
    archive_dir.mkdir(parents=True)
    (archive_dir / "metadata.json").write_text("invalid json")

    archived = pm._get_archived_tracks()  # noqa: SLF001
    assert archived[0][1] == "bad_track"


def test_get_track_summary_no_plan(pm):
    pm.initialize_project("Goal")
    track_id = pm.create_track("No Plan Track")
    # Remove the automatically created plan.md if it existed (wait, create_track doesn't create plan.md)
    summary, tasks, completed = pm._get_track_summary(track_id, "No Plan Track")  # noqa: SLF001
    assert "No plan.md found" in summary
    assert tasks == 0
    assert completed == 0


def test_get_track_summary_different_statuses(pm, tmp_path):
    pm.initialize_project("Goal")
    track_id = pm.create_track("Statuses")
    plan_file = tmp_path / "conductor" / "tracks" / track_id / "plan.md"
    plan_file.write_text("- [x] Done\n- [~] Doing\n- [ ] Todo")

    summary, tasks, completed = pm._get_track_summary(track_id, "Statuses")  # noqa: SLF001
    assert "2/3 tasks completed" in summary
    assert tasks == 3
    assert completed == 2


def test_get_track_summary_with_status_char(pm, tmp_path):
    pm.initialize_project("Goal")
    track_id = pm.create_track("Status Char")
    plan_file = tmp_path / "conductor" / "tracks" / track_id / "plan.md"
    plan_file.write_text("- [ ] Task")

    summary, _, _ = pm._get_track_summary(track_id, "Status Char", status_char="x")  # noqa: SLF001
    assert "[COMPLETED]" in summary

    summary, _, _ = pm._get_track_summary(track_id, "Status Char", status_char="~")  # noqa: SLF001
    assert "[IN_PROGRESS]" in summary


def test_initialize_project_missing_tracks_file(pm, tmp_path):
    # Setup without tracks.md
    (tmp_path / "conductor").mkdir()
    pm.initialize_project("Goal")
    assert (tmp_path / "conductor" / "tracks.md").exists()


def test_create_track_ensure_metadata_written(pm, tmp_path):
    track_id = pm.create_track("Metadata Test")
    assert (tmp_path / "conductor" / "tracks" / track_id / "metadata.json").exists()


def test_get_status_report_missing_tracks_file(pm):
    with pytest.raises(FileNotFoundError, match="Project tracks file not found"):
        pm.get_status_report()


def test_update_track_metadata(pm, tmp_path):
    track_id = pm.create_track("Metadata Update")
    updated = pm.update_track_metadata(track_id, {"vcs": {"enabled": True}})
    assert updated["vcs"]["enabled"] is True
    metadata = json.loads((tmp_path / "conductor" / "tracks" / track_id / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["vcs"]["enabled"] is True
