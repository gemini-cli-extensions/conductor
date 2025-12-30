from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class Task(BaseModel):
    description: str
    status: str = "new"  # new, in_progress, completed, cancelled
    commit_sha: Optional[str] = None

class Phase(BaseModel):
    name: str
    tasks: List[Task] = Field(default_factory=list)
    checkpoint_sha: Optional[str] = None

class Plan(BaseModel):
    phases: List[Phase] = Field(default_factory=list)

class Track(BaseModel):
    track_id: str
    description: str
    status: str = "new"  # new, in_progress, completed, cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
