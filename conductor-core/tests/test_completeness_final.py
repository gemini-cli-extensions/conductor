import git
import pytest
from conductor_core.errors import ErrorCategory, ProjectError, VCSError
from conductor_core.git_service import GitService
from conductor_core.prompts import PromptProvider


def test_vcs_error():
    e = VCSError("vcs", details={"x": 1})
    assert e.category == ErrorCategory.VCS
    assert e.to_dict()["error"]["category"] == "vcs"


def test_project_error():
    e = ProjectError("sys")
    assert e.category == ErrorCategory.SYSTEM


def test_git_service_more(tmp_path):
    git.Repo.init(tmp_path)
    gs = GitService(str(tmp_path))
    (tmp_path / "f").write_text("c")
    gs.add("f")
    commit_sha = gs.commit("initial")
    sha = gs.get_head_sha()
    assert sha == commit_sha

    gs.add_note(commit_sha, "note")
    log = gs.get_log(n=1)
    assert "initial" in log


def test_prompt_provider_errors(tmp_path):
    pp = PromptProvider(str(tmp_path))
    with pytest.raises(RuntimeError, match="Failed to render template"):
        pp.render("missing.md")

    with pytest.raises(RuntimeError, match="Failed to render string"):
        # Trigger exception during render
        pp.render_string("{{ 1/0 }}")


def test_prompt_provider_read_error(tmp_path):
    pp = PromptProvider(str(tmp_path))
    # Passing a directory name to get_template_text will fail during open() or read()
    with pytest.raises(RuntimeError, match="Failed to read template"):
        pp.get_template_text("")  # Current dir or just empty string depending on OS


def test_lsp_placeholder():
    from conductor_core.lsp import start_lsp

    start_lsp()
