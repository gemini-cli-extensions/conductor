import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Optional
from .models import Track, Plan, Task, Phase, TaskStatus, TrackStatus

class ProjectManager:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.conductor_path = self.base_path / "conductor"

    def initialize_project(self, goal: str):
        """Initializes the conductor directory and base files."""
        if not self.conductor_path.exists():
            self.conductor_path.mkdir(parents=True)
        
        state_file = self.conductor_path / "setup_state.json"
        if not state_file.exists():
            state_file.write_text(json.dumps({"last_successful_step": ""}))
        
        product_file = self.conductor_path / "product.md"
        if not product_file.exists():
            product_file.write_text(f"# Product Context\n\n## Initial Concept\n{goal}\n")

        tracks_file = self.conductor_path / "tracks.md"
        if not tracks_file.exists():
            tracks_file.write_text("# Project Tracks\n\nThis file tracks all major tracks for the project.\n")

        # Create basic placeholders for other required files if they don't exist
        for filename in ["tech-stack.md", "workflow.md"]:
            f = self.conductor_path / filename
            if not f.exists():
                f.write_text(f"# {filename.split('.')[0].replace('-', ' ').title()}\n")

    def create_track(self, description: str) -> str:
        """Initializes a new track directory and metadata."""
        if not self.conductor_path.exists():
            self.conductor_path.mkdir(parents=True)
            
        tracks_file = self.conductor_path / "tracks.md"
        if not tracks_file.exists():
            tracks_file.write_text("# Project Tracks\n\nThis file tracks all major tracks for the project.\n")
        
        # Robust ID generation: sanitized description + short hash of desc and timestamp
        import hashlib
        import re
        sanitized = re.sub(r'[^a-z0-9]', '_', description.lower())[:30].strip('_')
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        hash_input = f"{description}{timestamp}".encode()
        short_hash = hashlib.md5(hash_input).hexdigest()[:8]
        
        track_id = f"{sanitized}_{short_hash}"
        
        track_dir = self.conductor_path / "tracks" / track_id
        track_dir.mkdir(parents=True, exist_ok=True)
        
        track = Track(
            track_id=track_id,
            description=description,
            status=TrackStatus.NEW,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        (track_dir / "metadata.json").write_text(track.model_dump_json(indent=2))
        
        # Append to tracks.md
        with open(tracks_file, "a") as f:
            f.write(f"\n## [ ] Track: {description}\n*Link: [./conductor/tracks/{track_id}/](./conductor/tracks/{track_id}/)*\n")
        
        return track_id

    def get_status_report(self) -> str:
        """Generates a detailed status report of all tracks."""
        tracks_file = self.conductor_path / "tracks.md"
        if not tracks_file.exists():
            raise FileNotFoundError("Project tracks file not found.")

        active_tracks = self._parse_tracks_file(tracks_file)
        archived_tracks = self._get_archived_tracks()

        report = [
            "## Project Status Report",
            f"Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC",
            "",
            "### Active Tracks"
        ]

        total_tasks = 0
        completed_tasks = 0

        if not active_tracks:
            report.append("No active tracks.")
        for track_id, desc, status_char in active_tracks:
            track_report, t, c = self._get_track_summary(track_id, desc, is_archived=False, status_char=status_char)
            report.append(track_report)
            total_tasks += t
            completed_tasks += c

        report.append("\n### Archived Tracks")
        if not archived_tracks:
            report.append("No archived tracks.")
        for track_id, desc in archived_tracks:
            track_report, t, c = self._get_track_summary(track_id, desc, is_archived=True)
            report.append(track_report)
            total_tasks += t
            completed_tasks += c

        percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        summary_header = [
            "\n---",
            "### Overall Progress",
            f"Tasks: {completed_tasks}/{total_tasks} ({percentage:.1f}%)",
            ""
        ]
        
        return "\n".join(report + summary_header)

    def _parse_tracks_file(self, tracks_file: Path) -> List[tuple]:
        """Parses tracks.md for active tracks."""
        import re
        content = tracks_file.read_text()
        tracks = []
        # Flexible pattern for ## [ ] Track: Description and the following Link line
        # Link line format: *Link: [./conductor/tracks/track_id/](./conductor/tracks/track_id/)*
        pattern = r"##\s*\[\s*([ xX~]?)\s*\]\s*Track:\s*(.*?)\r?\n\*Link:\s*\[.*?/tracks/(.*?)/\]\(.*?\)\*"
        for match in re.finditer(pattern, content):
            status_char, desc, track_id = match.groups()
            tracks.append((track_id.strip(), desc.strip(), status_char.strip()))
        return tracks

    def _get_archived_tracks(self) -> List[tuple]:
        """Lists tracks in the archive directory."""
        archive_dir = self.conductor_path / "archive"
        if not archive_dir.exists():
            return []
        
        archived = []
        for d in archive_dir.iterdir():
            if d.is_dir():
                metadata_file = d / "metadata.json"
                if metadata_file.exists():
                    try:
                        import json
                        meta = json.loads(metadata_file.read_text())
                        archived.append((d.name, meta.get("description", d.name)))
                    except:
                        archived.append((d.name, d.name))
        return archived

    def _get_track_summary(self, track_id: str, description: str, is_archived: bool = False, status_char: Optional[str] = None) -> tuple:
        """Returns (formatted_string, total_tasks, completed_tasks) for a track."""
        base = "archive" if is_archived else "tracks"
        plan_file = self.conductor_path / base / track_id / "plan.md"
        
        if not plan_file.exists():
            return f"- **{description}** ({track_id}): No plan.md found", 0, 0

        content = plan_file.read_text()
        tasks = 0
        completed = 0
        
        import re
        # Match - [ ] or - [x] or - [~]
        for line in content.splitlines():
            if re.match(r"^\s*-\s*\[.\]", line):
                tasks += 1
                if "[x]" in line or "[X]" in line or "[~]" in line:
                    completed += 1
        
        percent = (completed / tasks * 100) if tasks > 0 else 0
        
        if status_char:
            status = "COMPLETED" if status_char.lower() == "x" else "IN_PROGRESS" if status_char == "~" else "PENDING"
        else:
            status = "COMPLETED" if percent == 100 else "IN_PROGRESS" if completed > 0 else "PENDING"
        
        return f"- **{description}** ({track_id}): {completed}/{tasks} tasks completed ({percent:.1f}%) [{status}]", tasks, completed
