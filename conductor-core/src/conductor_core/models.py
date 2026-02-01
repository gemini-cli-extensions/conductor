from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = " "
    IN_PROGRESS = "~"
    COMPLETED = "x"


class TrackStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Task(BaseModel):
    description: str
    status: TaskStatus = TaskStatus.PENDING
    commit_sha: str | None = None


class Phase(BaseModel):
    name: str
    tasks: list[Task] = Field(default_factory=list)
    checkpoint_sha: str | None = None


class Plan(BaseModel):
    track_id: str = ""
    phases: list[Phase] = Field(default_factory=list)


class Track(BaseModel):
    track_id: str
    description: str
    status: TrackStatus = TrackStatus.NEW
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PlatformCapability(str, Enum):
    TERMINAL = "terminal"
    FILE_SYSTEM = "file_system"
    VCS = "vcs"
    NETWORK = "network"
    BROWSER = "browser"
    UI_PROMPT = "ui_prompt"


class CapabilityContext(BaseModel):
    available_capabilities: list[PlatformCapability] = Field(default_factory=list)

    def has_capability(self, capability: PlatformCapability) -> bool:
        return capability in self.available_capabilities


class SkillManifest(BaseModel):
    id: str
    name: str
    version: str
    description: str
    engine_compatibility: str
    triggers: list[str] = Field(default_factory=list)
    commands: dict[str, str] = Field(default_factory=dict)
    capabilities: list[PlatformCapability] = Field(default_factory=list)
