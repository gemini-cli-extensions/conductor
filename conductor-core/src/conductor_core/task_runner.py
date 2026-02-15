from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from .git_service import GitService
from .models import CapabilityContext, PlatformCapability, TaskStatus
from .parser import MarkdownParser
from .vcs_adapters import JujutsuService

if TYPE_CHECKING:
    from .project_manager import ProjectManager


class TaskRunner:
    def __init__(
        self,
        project_manager: ProjectManager,
        git_service: GitService | None = None,
        capability_context: CapabilityContext | None = None,
    ) -> None:
        self.pm = project_manager
        self.capabilities = capability_context or CapabilityContext()
        self.vcs: GitService | JujutsuService | None

        if git_service is not None:
            self.vcs = git_service
        elif capability_context is not None and not self.capabilities.has_capability(PlatformCapability.VCS):
            self.vcs = None
        else:
            # Discover which VCS system is in use and select appropriate adapter
            self.vcs = self._discover_and_select_vcs_adapter(str(self.pm.base_path))

    @property
    def git(self):
        """Backward compatibility property for git attribute."""
        return self.vcs

    @git.setter
    def git(self, value):
        """Backward compatibility setter for git attribute."""
        self.vcs = value

    def _discover_and_select_vcs_adapter(self, repo_path: str):
        """Discover the VCS system in use and return the appropriate adapter."""
        repo_path_obj = Path(repo_path)

        # Check for Jujutsu first (JJ repo)
        jj_config = repo_path_obj / ".jj"
        if jj_config.exists():
            return JujutsuService(repo_path)

        # Check for Git (standard .git directory or file)
        git_indicator = repo_path_obj / ".git"
        if git_indicator.exists():
            return GitService(repo_path)

        # If no VCS detected, try to initialize Git as default
        return GitService(repo_path)

    def get_track_to_implement(self, description: str | None = None) -> tuple[str, str, str]:
        """Selects a track to implement, either by description or the next pending one."""
        tracks_file = self.pm.conductor_path / "tracks.md"
        if not tracks_file.exists():
            raise FileNotFoundError("tracks.md not found")

        # Accessing protected member for parsing logic
        active_tracks = self.pm._parse_tracks_file(tracks_file)  # noqa: SLF001
        if not active_tracks:
            raise ValueError("No active tracks found in tracks.md")

        if description:
            # Try to match by description
            for track_id, desc, status_char in active_tracks:
                if description.lower() in desc.lower():
                    return track_id, desc, status_char
            raise ValueError(f"No track found matching description: {description}")

        # Return the first one (assuming it's pending/next)
        return active_tracks[0]

    def update_track_status(self, track_id: str, status: str) -> None:
        """Updates the status of a track in tracks.md (e.g., [ ], [~], [x])."""
        tracks_file = self.pm.conductor_path / "tracks.md"
        content = tracks_file.read_text()

        # We need to find the specific track by its link and update the preceding checkbox
        escaped_id = re.escape(track_id)
        # Match from (##|[-]) [ ] (**)Track: ... until the link with track_id
        pattern = rf"((?:##|[-])\s*\[)[ xX~]?(\]\s*(?:\*\*)?Track:.*?\r?\n\*Link:\s*\[.*?/tracks/{escaped_id}/\].*?\*)"

        new_content, count = re.subn(pattern, rf"\1{status}\2", content, flags=re.MULTILINE)
        if count == 0:
            raise ValueError(f"Could not find track {track_id} in tracks.md to update status")

        tracks_file.write_text(new_content)

    def update_task_status(
        self, track_id: str, task_description: str, status: str, commit_sha: str | None = None
    ) -> None:
        """Updates a specific task's status in the track's plan.md."""
        plan_file = self.pm.conductor_path / "tracks" / track_id / "plan.md"
        if not plan_file.exists():
            raise FileNotFoundError(f"plan.md not found for track {track_id}")

        content = plan_file.read_text()

        # Parse the plan using structured parsing
        plan = MarkdownParser.parse_plan(content)

        # Find and update the task
        task_updated = False
        for phase in plan.phases:
            for task in phase.tasks:
                if task_description.lower() in task.description.lower():
                    # Map status string to TaskStatus enum
                    if status == "x":
                        task.status = TaskStatus.COMPLETED
                    elif status == "~":
                        task.status = TaskStatus.IN_PROGRESS
                    elif status == " ":
                        task.status = TaskStatus.PENDING

                    if commit_sha:
                        task.commit_sha = commit_sha
                    task_updated = True
                    break
            if task_updated:
                break

        if not task_updated:
            raise ValueError(f"Could not find task '{task_description}' in plan.md")

        # Serialize back to markdown
        new_content = MarkdownParser.serialize_plan(plan)
        plan_file.write_text(new_content)

    def checkpoint_phase(self, track_id: str, phase_name: str, commit_sha: str) -> None:
        """Updates a phase with a checkpoint SHA in plan.md."""
        plan_file = self.pm.conductor_path / "tracks" / track_id / "plan.md"
        if not plan_file.exists():
            raise FileNotFoundError(f"plan.md not found for track {track_id}")

        content = plan_file.read_text()

        # Parse the plan using structured parsing
        plan = MarkdownParser.parse_plan(content)

        # Find and update the phase
        phase_updated = False
        for phase in plan.phases:
            if phase_name.lower() in phase.name.lower():
                phase.checkpoint_sha = commit_sha
                phase_updated = True
                break

        if not phase_updated:
            raise ValueError(f"Could not find phase '{phase_name}' in plan.md")

        # Serialize back to markdown
        new_content = MarkdownParser.serialize_plan(plan)
        plan_file.write_text(new_content)

    def revert_task(self, track_id: str, task_description: str) -> None:
        """Resets a task status to pending in plan.md."""
        self.update_task_status(track_id, task_description, " ")

    def archive_track(self, track_id: str) -> None:
        """Moves a track from tracks/ to archive/ and removes it from tracks.md."""
        track_dir = self.pm.conductor_path / "tracks" / track_id
        archive_dir = self.pm.conductor_path / "archive"

        if not track_dir.exists():
            raise FileNotFoundError(f"Track directory {track_dir} not found")

        archive_dir.mkdir(parents=True, exist_ok=True)
        target_dir = archive_dir / track_id

        if target_dir.exists():
            shutil.rmtree(target_dir)

        shutil.move(str(track_dir), str(target_dir))

        # Remove from tracks.md
        tracks_file = self.pm.conductor_path / "tracks.md"
        content = tracks_file.read_text()

        # Support both legacy (## [ ] Track:) and modern (- [ ] **Track:) formats
        # and handle optional separator (---)
        p1 = r"(?ms)^---\r?\n\n\s*(?:##|[-])\s*(\[.*?]\s*(?:\*\*)?Track:.*?)"
        p2 = rf"\r?\n\*Link:\s*\[.*?/tracks/{track_id}/.*?\)[\*]*\r?\n?"
        pattern = p1 + p2
        new_content, count = re.subn(pattern, "", content)

        if count == 0:
            # Try without the separator
            p1 = r"(?ms)^\s*(?:##|[-])\s*(\[.*?]\s*(?:\*\*)?Track:.*?)"
            pattern = p1 + p2
            new_content, count = re.subn(pattern, "", content)

        tracks_file.write_text(new_content)
