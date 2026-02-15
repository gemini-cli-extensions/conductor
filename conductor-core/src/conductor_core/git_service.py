from __future__ import annotations

import os
from typing import Protocol, runtime_checkable

from git import InvalidGitRepositoryError, Repo


@runtime_checkable
class VCSService(Protocol):
    def get_status(self) -> str:
        ...

    def commit(self, message: str, stage_all: bool = True) -> str:
        ...

    def get_latest_hash(self) -> str:
        ...

    def add_note(self, commit_hash: str, message: str) -> None:
        ...

    def add(self, file_path: str) -> None:
        ...

    def is_dirty(self) -> bool:
        ...

    def checkout_and_merge(self, branch_name: str) -> None:
        ...

    def create_branch(self, branch_name: str) -> None:
        ...

    def create_worktree(self, path: str, branch: str) -> None:
        ...

    def get_head_sha(self) -> str:
        ...

    def checkout(self, branch_name: str, create: bool = False) -> None:
        ...

    def merge(self, branch_name: str) -> None:
        ...

    def get_log(self, n: int = 10) -> str:
        ...

    @property
    def repo(self) -> Repo:
        ...


class GitService:
    def __init__(self, repo_path: str):
        try:
            self.repo = Repo(repo_path, search_parent_directories=True)
            self.path = repo_path
        except InvalidGitRepositoryError:
            raise InvalidGitRepositoryError(f"Not a git repository: {repo_path}")

    def get_status(self) -> str:
        return self.repo.git.status()

    def commit(self, message: str, stage_all: bool = True) -> str:
        if stage_all:
            self.repo.git.add(A=True)
        self.repo.index.commit(message)
        return self.repo.head.commit.hexsha

    def get_latest_hash(self) -> str:
        return self.repo.head.commit.hexsha

    def get_head_sha(self) -> str:
        return self.repo.head.commit.hexsha

    def add(self, file_path: str) -> None:
        abs_path = os.path.join(self.path, file_path)
        rel_path = os.path.relpath(abs_path, self.repo.working_dir)
        self.repo.index.add(rel_path)

    def is_dirty(self) -> bool:
        return self.repo.is_dirty() or len(self.repo.untracked_files) > 0

    def checkout(self, branch_name: str, create: bool = False) -> None:
        if create:
            self.repo.git.checkout("-b", branch_name)
        else:
            self.repo.git.checkout(branch_name)

    def checkout_and_merge(self, branch_name: str) -> None:
        # Checkout the branch and merge it into current branch
        current_branch = self.repo.active_branch.name
        self.repo.git.checkout(branch_name)
        self.repo.git.checkout(current_branch)
        self.repo.git.merge(branch_name)

    def create_branch(self, branch_name: str) -> None:
        self.repo.git.branch(branch_name)

    def create_worktree(self, path: str, branch: str) -> None:
        # Create a new branch if it doesn't exist
        if branch not in self.repo.branches:
            self.repo.git.branch(branch)

        # Use git worktree command to create worktree
        self.repo.git.worktree("add", path, branch)

    def merge(self, branch_name: str) -> None:
        self.repo.git.merge(branch_name)

    def get_log(self, n: int = 10) -> str:
        return self.repo.git.log("-n", str(n))

    def add_note(self, commit_hash: str, message: str) -> None:
        self.repo.git.notes("add", "-m", message, commit_hash)
