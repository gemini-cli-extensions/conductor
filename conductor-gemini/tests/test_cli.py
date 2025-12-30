import pytest
from click.testing import CliRunner
from conductor_gemini.cli import main

def test_cli_setup():
    runner = CliRunner()
    result = runner.invoke(main, ['setup', '--project-goal', 'Build a tool'])
    assert result.exit_code == 0
    assert "Setting up project with goal: Build a tool" in result.output

def test_cli_new_track():
    runner = CliRunner()
    result = runner.invoke(main, ['new-track', 'Add a feature'])
    assert result.exit_code == 0
    assert "Creating new track: Add a feature" in result.output

def test_cli_implement():
    runner = CliRunner()
    result = runner.invoke(main, ['implement'])
    assert result.exit_code == 0
    assert "Implementing current track..." in result.output
