import os
import runpy
from unittest.mock import patch

import git
import pytest
from click.testing import CliRunner
from conductor_core.errors import ValidationError
from conductor_gemini.cli import main


@pytest.fixture()
def repo_dir(tmp_path):
    git.Repo.init(tmp_path)
    return tmp_path


def test_handle_conductor_error_with_details(repo_dir):
    runner = CliRunner()
    with patch(
        "conductor_core.project_manager.ProjectManager.create_track",
        side_effect=ValidationError("Msg", details={"info": "extra"}),
    ):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "new-track", "test"])
        assert result.exit_code == 1
        assert "[VALIDATION] ERROR: Msg" in result.output
        assert "Details: {'info': 'extra'}" in result.output


def test_status_not_setup(repo_dir):
    runner = CliRunner()
    result = runner.invoke(main, ["--base-path", str(repo_dir), "status"])
    assert result.exit_code == 1
    assert "Error: Project not set up" in result.output


def test_status_exception(repo_dir):
    runner = CliRunner()
    runner.invoke(main, ["--base-path", str(repo_dir), "setup", "--goal", "test"])
    with patch("conductor_core.project_manager.ProjectManager.get_status_report", side_effect=Exception("Unexpected")):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "status"])
        assert result.exit_code == 1
        assert "UNEXPECTED ERROR: Unexpected" in result.output


def test_setup_exception(repo_dir):
    runner = CliRunner()
    with patch("conductor_core.project_manager.ProjectManager.initialize_project", side_effect=Exception("Boom")):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "setup", "--goal", "test"])
        assert result.exit_code == 1
        assert "UNEXPECTED ERROR: Boom" in result.output


def test_implement_exception(repo_dir):
    runner = CliRunner()
    runner.invoke(main, ["--base-path", str(repo_dir), "setup", "--goal", "test"])
    with patch("conductor_core.task_runner.TaskRunner.get_track_to_implement", side_effect=Exception("Fail")):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "implement"])
        assert result.exit_code == 1
        assert "UNEXPECTED ERROR: Fail" in result.output


def test_revert_success(repo_dir):
    runner = CliRunner()
    runner.invoke(main, ["--base-path", str(repo_dir), "setup", "--goal", "test"])
    with patch("conductor_core.task_runner.TaskRunner.revert_task"):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "revert", "t1", "task1"])
        assert result.exit_code == 0
        assert "reset to pending" in result.output


def test_archive_success(repo_dir):
    runner = CliRunner()
    runner.invoke(main, ["--base-path", str(repo_dir), "setup", "--goal", "test"])
    with patch("conductor_core.task_runner.TaskRunner.archive_track"):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "archive", "t1"])
        assert result.exit_code == 0
        assert "archived successfully" in result.output


def test_archive_exception(repo_dir):
    runner = CliRunner()
    runner.invoke(main, ["--base-path", str(repo_dir), "setup", "--goal", "test"])
    with patch("conductor_core.task_runner.TaskRunner.archive_track", side_effect=Exception("Err")):
        result = runner.invoke(main, ["--base-path", str(repo_dir), "archive", "t1"])
        assert result.exit_code == 1


def test_main_invocation_help():
    with patch("sys.argv", ["conductor", "--help"]):
        with pytest.raises(SystemExit) as e:
            from conductor_gemini import cli

            cli.main()
        assert e.value.code == 0


def test_cli_run_main_block(repo_dir):
    # Using runpy to execute the file as __main__
    cli_path = os.path.join("conductor-gemini", "src", "conductor_gemini", "cli.py")
    with patch("sys.argv", ["conductor", "--help"]):
        with pytest.raises(SystemExit) as e:
            runpy.run_path(cli_path, run_name="__main__")
        assert e.value.code == 0
