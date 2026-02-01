import git
import pytest
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner


@pytest.fixture()
def project(tmp_path):
    pm = ProjectManager(tmp_path)
    pm.initialize_project("Test")
    git.Repo.init(tmp_path)
    return pm


def test_update_task_status_with_commit_sha(project):
    runner = TaskRunner(project)
    track_id = project.create_track("Commit Test")

    plan_file = project.conductor_path / "tracks" / track_id / "plan.md"
    plan_file.write_text("- [ ] Task A")

    runner.update_task_status(track_id, "Task A", "x", commit_sha="1234567890")

    content = plan_file.read_text()
    assert "- [x] Task A [1234567]" in content


def test_checkpoint_phase_success(project):
    runner = TaskRunner(project)
    track_id = project.create_track("Phase Success")
    plan_file = project.conductor_path / "tracks" / track_id / "plan.md"
    plan_file.write_text("## Phase 1: Test")
    runner.checkpoint_phase(track_id, "Test", "abcdef123456")
    assert "[checkpoint: abcdef1]" in plan_file.read_text()


def test_checkpoint_phase_not_found_regex(project):
    runner = TaskRunner(project)
    track_id = project.create_track("Phase Regex Test")

    plan_file = project.conductor_path / "tracks" / track_id / "plan.md"
    plan_file.write_text("## Phase X")

    with pytest.raises(ValueError, match="Could not find phase 'Missing'"):
        runner.checkpoint_phase(track_id, "Missing", "123")


def test_revert_task(project):
    runner = TaskRunner(project)
    track_id = project.create_track("Revert Test")
    plan_file = project.conductor_path / "tracks" / track_id / "plan.md"
    plan_file.write_text("- [x] Task A")

    runner.revert_task(track_id, "Task A")
    assert "- [ ] Task A" in plan_file.read_text()
