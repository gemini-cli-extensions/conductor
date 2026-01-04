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

def test_git_service_checkout_and_merge(temp_repo):
    service = GitService(repo_path=str(temp_repo))
    # Create first commit on main
    (temp_repo / "main.txt").write_text("main")
    service.add("main.txt")
    service.commit("feat: Main commit")
    
    # Create and checkout new branch
    service.checkout("feature", create=True)
    (temp_repo / "feat.txt").write_text("feat")
    service.add("feat.txt")
    service.commit("feat: Feature commit")
    
    # Checkout main and merge feature
    default_branch = service.repo.active_branch.name
    service.checkout("feature") # Just to make sure we move away
    service.checkout(default_branch) 
    service.merge("feature")
    assert os.path.exists(os.path.join(temp_repo, "feat.txt"))

def test_git_service_missing_repo(tmp_path):
    # Pass a path that is not a git repo
    with pytest.raises(Exception): # git.exc.InvalidGitRepositoryError
        GitService(repo_path=str(tmp_path))
