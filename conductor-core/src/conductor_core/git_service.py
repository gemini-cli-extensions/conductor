from git import Repo
import os

class GitService:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.repo = Repo(self.repo_path)

    def is_dirty(self) -> bool:
        return self.repo.is_dirty(untracked_files=True)

    def add(self, files):
        if isinstance(files, str):
            files = [files]
        self.repo.index.add(files)

    def commit(self, message: str) -> str:
        commit = self.repo.index.commit(message)
        return commit.hexsha

    def get_head_sha(self) -> str:
        return self.repo.head.commit.hexsha

    def checkout(self, branch_name: str, create: bool = False):
        if create:
            self.repo.create_head(branch_name)
        self.repo.git.checkout(branch_name)

    def merge(self, branch_name: str):
        self.repo.git.merge(branch_name)
