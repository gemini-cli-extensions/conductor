from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum

class TaskStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TrackStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(BaseModel):
    description: str
    status: TaskStatus = TaskStatus.NEW
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
    status: TrackStatus = TrackStatus.NEW
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
