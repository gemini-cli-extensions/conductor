import json
import os
from pathlib import Path
from datetime import datetime, timezone
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

    def create_track(self, description: str) -> str:
        """Initializes a new track directory and metadata."""
        if not self.conductor_path.exists():
            self.conductor_path.mkdir(parents=True)
            
        tracks_file = self.conductor_path / "tracks.md"
        if not tracks_file.exists():
            tracks_file.write_text("# Project Tracks\n\n")
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        # Simple ID generation for now
        short_name = description.lower().replace(" ", "_")[:20]
        track_id = f"{short_name}_{timestamp}"
        
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
        
        return track_id
