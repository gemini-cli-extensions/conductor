from __future__ import annotations

import re
import shutil
from typing import TYPE_CHECKING

from .git_service import GitService
from .models import CapabilityContext, PlatformCapability

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
        self.git: GitService | None
        if git_service is not None:
            self.git = git_service
        elif capability_context is not None and not self.capabilities.has_capability(PlatformCapability.VCS):
            self.git = None
        else:
            self.git = GitService(str(self.pm.base_path))

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

        # Escape description for regex
        escaped_desc = re.escape(task_description)
        # Match - [ ] Task description ...
        pattern = rf"(^\s*-\s*\[)[ xX~]?(\]\s*(?:Task:\s*)?{escaped_desc}.*?)(?:\s*\[[0-9a-f]{{7,}}\])?$"

        replacement = rf"\1{status}\2"
        if commit_sha:
            short_sha = commit_sha[:7]
            replacement += f" [{short_sha}]"

        new_content, count = re.subn(pattern, replacement, content, flags=re.MULTILINE)
        if count == 0:
            raise ValueError(f"Could not find task '{task_description}' in plan.md")

        plan_file.write_text(new_content)

    def checkpoint_phase(self, track_id: str, phase_name: str, commit_sha: str) -> None:
        """Updates a phase with a checkpoint SHA in plan.md."""
        plan_file = self.pm.conductor_path / "tracks" / track_id / "plan.md"
        if not plan_file.exists():
            raise FileNotFoundError(f"plan.md not found for track {track_id}")

        content = plan_file.read_text()

        escaped_phase = re.escape(phase_name)
        short_sha = commit_sha[:7]
        pattern = rf"(##\s*(?:Phase\s*\d+:\s*)?{escaped_phase})(?:\s*\[checkpoint:\s*[0-9a-f]+\])?"
        replacement = rf"\1 [checkpoint: {short_sha}]"

        new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE | re.MULTILINE)
        if count == 0:
            raise ValueError(f"Could not find phase '{phase_name}' in plan.md")

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
