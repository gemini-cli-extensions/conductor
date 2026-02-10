import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

class TelemetryLogger:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_implementation_attempt(self, track_id: str, data: dict[str, Any]):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        log_file = self.log_dir / f"implement_{track_id}_{timestamp}.json"
        
        entry = {
            "track_id": track_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
        
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(entry, f, indent=2)
        
        return log_file
