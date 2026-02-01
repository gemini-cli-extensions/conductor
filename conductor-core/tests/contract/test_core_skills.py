from unittest.mock import MagicMock

import pytest
from conductor_core.models import CapabilityContext, PlatformCapability
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner


@pytest.fixture()
def mock_pm(tmp_path):
    pm = ProjectManager(tmp_path)
    # Create necessary files for PM to be considered "set up"
    (tmp_path / "conductor").mkdir()
    (tmp_path / "conductor" / "product.md").write_text("# Product")
    (tmp_path / "conductor" / "workflow.md").write_text("# Workflow")
    (tmp_path / "conductor" / "tracks.md").write_text("# Tracks")
    return pm


def test_contract_new_track_logic(mock_pm):
    """Verifies that the core logic for selecting a track works with abstract inputs."""
    # Mocking tracks.md content for parsing
    tracks_file = mock_pm.conductor_path / "tracks.md"
    tracks_file.write_text(
        """# Project Tracks
---
## [ ] Track: Test Track
*Link: [./conductor/tracks/test_20260101/](./conductor/tracks/test_20260101/)*
"""
    )

    git_mock = MagicMock()
    runner = TaskRunner(mock_pm, git_service=git_mock)

    track_id, desc, status = runner.get_track_to_implement("Test Track")

    assert track_id == "test_20260101"
    assert "Test Track" in desc
    assert status == ""


def test_contract_capability_gate(mock_pm):
    """Verifies that the core respects platform capabilities."""
    git_mock = MagicMock()
    # Host platform with NO terminal capability
    ctx = CapabilityContext(available_capabilities=[PlatformCapability.UI_PROMPT])
    runner = TaskRunner(mock_pm, git_service=git_mock, capability_context=ctx)

    assert runner.capabilities.has_capability(PlatformCapability.TERMINAL) is False
