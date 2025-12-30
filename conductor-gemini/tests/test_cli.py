import pytest
from click.testing import CliRunner
from conductor_gemini.cli import main
import os

def test_cli_setup(tmp_path):
    runner = CliRunner()
    # Pass base-path to avoid git issues in test environment
    result = runner.invoke(main, ['--base-path', str(tmp_path), 'setup', '--goal', 'Build a tool'])
    assert result.exit_code == 0
    assert "Initialized Conductor project" in result.output
    assert os.path.exists(tmp_path / "conductor" / "product.md")

def test_cli_new_track(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ['--base-path', str(tmp_path), 'new-track', 'Add a feature'])
    assert result.exit_code == 0
    assert "Created track" in result.output
    assert "Add a feature" in result.output

def test_cli_implement():
    runner = CliRunner()
    result = runner.invoke(main, ['implement'])
    assert result.exit_code == 0
    assert "Implementing current track..." in result.output