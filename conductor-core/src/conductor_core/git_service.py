from __future__ import annotations

from git import Repo


class GitService:
    def __init__(self, repo_path: str = ".") -> None:
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)

    def is_dirty(self) -> bool:
        return self.repo.is_dirty(untracked_files=True)

    def add(self, files: str | list[str]) -> None:
        if isinstance(files, str):
            files = [files]
        self.repo.index.add(files)

    def commit(self, message: str) -> str:
        commit = self.repo.index.commit(message)
        return commit.hexsha

    def add_note(self, commit_sha: str, note: str, namespace: str = "commits") -> None:
        """Adds a git note to a specific commit."""
        self.repo.git.notes("--ref", namespace, "add", "-m", note, commit_sha)

    def get_log(self, n: int = 5) -> str:
        """Returns recent commit log."""
        return self.repo.git.log(n=n, oneline=True)

    def get_head_sha(self) -> str:
        return self.repo.head.commit.hexsha

    def checkout(self, branch_name: str, *, create: bool = False) -> None:
        if create:
            self.repo.create_head(branch_name)
        self.repo.git.checkout(branch_name)

    def merge(self, branch_name: str) -> None:
        self.repo.git.merge(branch_name)

    def create_branch(self, branch_name: str, base: str | None = None) -> None:
        if branch_name in [head.name for head in self.repo.heads]:
            return
        if base:
            self.repo.git.branch(branch_name, base)
        else:
            self.repo.create_head(branch_name)

    def create_worktree(self, worktree_path: str, branch_name: str, base: str | None = None) -> None:
        path = str(worktree_path)
        if base:
            self.repo.git.worktree("add", path, "-b", branch_name, base)
        else:
            self.repo.git.worktree("add", path, "-b", branch_name)
