import pytest
import os
import subprocess
from conductor_core.git_service import GitService

@pytest.fixture
def temp_repo(tmp_path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo_dir, check=True)
    return repo_dir

def test_git_service_status(temp_repo):
    service = GitService(repo_path=str(temp_repo))
    # Initially no changes
    assert service.is_dirty() == False
    
    # Add a file
    (temp_repo / "test.txt").write_text("hello")
    assert service.is_dirty() == True

def test_git_service_commit(temp_repo):
    service = GitService(repo_path=str(temp_repo))
    (temp_repo / "test.txt").write_text("hello")
    service.add("test.txt")
    sha = service.commit("feat: Test commit")
    assert len(sha) == 40
    assert service.is_dirty() == False

def test_git_service_get_head_sha(temp_repo):
    service = GitService(repo_path=str(temp_repo))
    (temp_repo / "test.txt").write_text("hello")
    service.add("test.txt")
    sha = service.commit("feat: Test commit")
    assert service.get_head_sha() == sha
