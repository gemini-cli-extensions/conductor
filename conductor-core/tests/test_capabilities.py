from pathlib import Path
from unittest.mock import MagicMock

import git
from conductor_core.models import CapabilityContext, PlatformCapability
from conductor_core.project_manager import ProjectManager
from conductor_core.task_runner import TaskRunner


def test_task_runner_capabilities():
    pm = ProjectManager(Path())
    git_mock = MagicMock()
    ctx = CapabilityContext(available_capabilities=[PlatformCapability.UI_PROMPT])
    runner = TaskRunner(pm, git_service=git_mock, capability_context=ctx)

    assert runner.capabilities.has_capability(PlatformCapability.UI_PROMPT) is True
    assert runner.capabilities.has_capability(PlatformCapability.FILE_SYSTEM) is False


def test_default_capabilities():
    pm = ProjectManager(Path())
    git_mock = MagicMock()
    runner = TaskRunner(pm, git_service=git_mock)
    assert runner.capabilities.available_capabilities == []


def test_task_runner_git_disabled(tmp_path):
    pm = ProjectManager(tmp_path)
    pm.initialize_project("Goal")
    ctx = CapabilityContext(available_capabilities=[])
    runner = TaskRunner(pm, capability_context=ctx)
    assert runner.git is None


def test_task_runner_git_enabled(tmp_path):
    pm = ProjectManager(tmp_path)
    pm.initialize_project("Goal")
    git.Repo.init(tmp_path)
    ctx = CapabilityContext(available_capabilities=[PlatformCapability.VCS])
    runner = TaskRunner(pm, capability_context=ctx)
    assert runner.git is not None
