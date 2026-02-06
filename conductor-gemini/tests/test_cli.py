import os

import pytest
from click.testing import CliRunner
from conductor_gemini.cli import main
from git import Repo


@pytest.fixture()
def base_path(tmp_path):
    # Initialize a git repo in the temporary directory
    Repo.init(tmp_path)
    return tmp_path


def test_cli_setup(base_path):
    runner = CliRunner()
    result = runner.invoke(main, ["--base-path", str(base_path), "setup", "--goal", "Build a tool"])
    assert result.exit_code == 0
    assert "Initialized Conductor project" in result.output
    assert os.path.exists(base_path / "conductor" / "product.md")


def test_cli_new_track(base_path):
    runner = CliRunner()
    result = runner.invoke(main, ["--base-path", str(base_path), "new-track", "Add a feature"])
    assert result.exit_code == 0
    assert "Created track" in result.output
    assert "Add a feature" in result.output


def test_cli_implement(base_path):
    runner = CliRunner()
    # Need to setup and create track first
    runner.invoke(main, ["--base-path", str(base_path), "setup", "--goal", "Test"])
    runner.invoke(main, ["--base-path", str(base_path), "new-track", "Test Track"])
    # Mocking files for implement
    track_dir = base_path / "conductor" / "tracks"
    track_id = os.listdir(track_dir)[0]
    (track_dir / track_id / "plan.md").write_text("- [ ] Task 1")
    (track_dir / track_id / "spec.md").write_text("# Spec")
    base_path.joinpath("conductor/workflow.md").write_text("# Workflow")

    result = runner.invoke(main, ["--base-path", str(base_path), "implement"])
    if result.exit_code != 0:
        pass
    assert result.exit_code == 0
    assert "Selecting track: Test Track" in result.output


def test_cli_status(base_path):
    runner = CliRunner()
    # Setup first
    runner.invoke(main, ["--base-path", str(base_path), "setup", "--goal", "Test"])
    # Check status
    result = runner.invoke(main, ["--base-path", str(base_path), "status"])
    assert result.exit_code == 0
    assert "Project Status Report" in result.output
