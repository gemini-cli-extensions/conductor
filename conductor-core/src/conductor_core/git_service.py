from __future__ import annotations
from typing import Protocol, runtime_checkable
from pathlib import Path

@runtime_checkable
class VCSService(Protocol):
    def get_status(self) -> str: ...
    def commit(self, message: str, stage_all: bool = True) -> str: ...
    def get_latest_hash(self) -> str: ...
    def add_note(self, message: str, commit_hash: str) -> None: ...

class GitService:
    def __init__(self, repo_path: str):
        self.path = repo_path
        # Real implementation would use GitPython
        pass

    def get_status(self) -> str:
        return "git status placeholder"

    def commit(self, message: str, stage_all: bool = True) -> str:
        return "abcdef1234567"

    def get_latest_hash(self) -> str:
        return "abcdef1234567"

    def add_note(self, message: str, commit_hash: str) -> None:
        pass