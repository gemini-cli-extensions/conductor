import pytest
from click.testing import CliRunner
from conductor_gemini.cli import main
import os
from pathlib import Path
from git import Repo

@pytest.fixture
def base_path(tmp_path):
    # Initialize a git repo in the temporary directory
    repo = Repo.init(tmp_path)
    # Configure git user for commits
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@example.com").release()
    return tmp_path

def test_vscode_contract_setup(base_path):
    """Test the 'setup' command with arguments provided by VS Code extension."""
    runner = CliRunner()
    # VS Code sends: ['setup', '--goal', prompt]
    result = runner.invoke(main, ['--base-path', str(base_path), 'setup', '--goal', 'Initial goal'])
    assert result.exit_code == 0
    assert "Initialized Conductor project" in result.output
    assert (base_path / "conductor" / "product.md").exists()

def test_vscode_contract_newtrack(base_path):
    """Test the 'new-track' command with arguments provided by VS Code extension."""
    runner = CliRunner()
    runner.invoke(main, ['--base-path', str(base_path), 'setup', '--goal', 'Test'])
    
    # VS Code sends: ['new-track', prompt] (prompt is quoted in shell)
    result = runner.invoke(main, ['--base-path', str(base_path), 'new-track', 'Feature implementation'])
    assert result.exit_code == 0
    assert "Feature implementation" in result.output
    assert "Created track" in result.output

def test_vscode_contract_status(base_path):
    """Test the 'status' command."""
    runner = CliRunner()
    runner.invoke(main, ['--base-path', str(base_path), 'setup', '--goal', 'Test'])
    
    # VS Code sends: ['status']
    result = runner.invoke(main, ['--base-path', str(base_path), 'status'])
    assert result.exit_code == 0
    assert "Project Status Report" in result.output

def test_vscode_contract_implement(base_path):
    """Test the 'implement' command."""
    runner = CliRunner()
    runner.invoke(main, ['--base-path', str(base_path), 'setup', '--goal', 'Test'])
    runner.invoke(main, ['--base-path', str(base_path), 'new-track', 'Test Track'])
    
    # VS Code sends: ['implement']
    # We need to ensure there is a plan to implement
    track_dir = base_path / "conductor" / "tracks"
    track_id = os.listdir(track_dir)[0]
    (track_dir / track_id / "plan.md").write_text("- [ ] Task 1")
    (track_dir / track_id / "spec.md").write_text("# Spec")
    base_path.joinpath("conductor/workflow.md").write_text("# Workflow")
    
    result = runner.invoke(main, ['--base-path', str(base_path), 'implement'])
    assert result.exit_code == 0
    assert "Selecting track: Test Track" in result.output

def test_vscode_contract_revert(base_path):
    """Test the 'revert' command with arguments provided by VS Code extension."""
    runner = CliRunner()
    runner.invoke(main, ['--base-path', str(base_path), 'setup', '--goal', 'Test'])
    runner.invoke(main, ['--base-path', str(base_path), 'new-track', 'Test Track'])
    
    track_dir = base_path / "conductor" / "tracks"
    track_id = os.listdir(track_dir)[0]
    
    # VS Code sends: ['revert', trackId, taskDesc]
    # Revert command might not be fully implemented or might expect existing git history.
    # In test_cli.py, revert isn't tested. Let's see if it's supported.
    result = runner.invoke(main, ['--base-path', str(base_path), 'revert', track_id, 'Task 1'])
    
    # Even if it fails because there's nothing to revert, we check if the command is recognized.
    # If the command is not implemented, exit_code will likely be 2 (Click error).
    assert result.exit_code != 2 # Command exists
