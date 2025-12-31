import os
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
from .project_manager import ProjectManager
from .git_service import GitService
from .models import TaskStatus, TrackStatus

class TaskRunner:
    def __init__(self, project_manager: ProjectManager, git_service: Optional[GitService] = None):
        self.pm = project_manager
        self.git = git_service or GitService(str(self.pm.base_path))

    def get_track_to_implement(self, description: Optional[str] = None) -> Tuple[str, str, str]:
        """Selects a track to implement, either by description or the next pending one."""
        tracks_file = self.pm.conductor_path / "tracks.md"
        if not tracks_file.exists():
            raise FileNotFoundError("tracks.md not found")

        active_tracks = self.pm._parse_tracks_file(tracks_file)
        if not active_tracks:
            raise ValueError("No active tracks found in tracks.md")

        if description:
            # Try to match by description
            for track_id, desc, status_char in active_tracks:
                if description.lower() in desc.lower():
                    return track_id, desc, status_char
            raise ValueError(f"No track found matching description: {description}")
        else:
            # Return the first one (assuming it's pending/next)
            return active_tracks[0]

    def update_track_status(self, track_id: str, status: str):
        """Updates the status of a track in tracks.md (e.g., [ ], [~], [x])."""
        tracks_file = self.pm.conductor_path / "tracks.md"
        content = tracks_file.read_text()
        
        import re
        # We need to find the specific track by its link and update the preceding checkbox
        # Using a more robust multi-step approach if regex is tricky
        escaped_id = re.escape(track_id)
        # Match from ## [ ] Track: ... until the link with track_id
        # We use a non-greedy match for the track description
        pattern = rf"(##\s*\[)[ xX~]?(\]\s*Track:.*?\r?\n\*Link:\s*\[.*?/tracks/{escaped_id}/\]\(.*?\)\*)"
        
        new_content, count = re.subn(pattern, rf"\1{status}\2", content, flags=re.MULTILINE)
        if count == 0:
            raise ValueError(f"Could not find track {track_id} in tracks.md to update status")
            
        tracks_file.write_text(new_content)

    def archive_track(self, track_id: str):
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
        
        # Pattern to match the track section (starting with --- if present, or just the heading)
        # Note: This is a bit simplified, might need refinement for exact matching
        import re
        pattern = rf"(?m)^---\n\n##\s*\[.*?]\s*Track:.*?\n\*Link:\s*\[.*?/tracks/{track_id}/].*?\n?"
        new_content, count = re.subn(pattern, "", content)
        
        if count == 0:
            # Try without the separator
            pattern = rf"(?m)^##\s*\[.*?]\s*Track:.*?\n\*Link:\s*\[.*?/tracks/{track_id}/].*?\n?"
            new_content, count = re.subn(pattern, "", content)

        tracks_file.write_text(new_content)
