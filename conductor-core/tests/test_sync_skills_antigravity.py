import importlib
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_sync_to_antigravity():
    repo_root = _repo_root()
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    # Force unload of any existing 'scripts' module to avoid conflict with external packages
    if "scripts" in sys.modules:
        del sys.modules["scripts"]
    if "scripts.skills_manifest" in sys.modules:
        del sys.modules["scripts.skills_manifest"]
    if "scripts.sync_skills" in sys.modules:
        del sys.modules["scripts.sync_skills"]

    # Ensure module is loaded to avoid AttributeError in patch with namespace packages
    skills_manifest = importlib.import_module("scripts.skills_manifest")

    # Verify we got the right one
    assert str(repo_root) in str(skills_manifest.__file__), f"Wrong scripts module loaded: {skills_manifest.__file__}"

    # We need to mock BEFORE importing the module if we want to mock constants,
    # but here we want to mock the behavior of functions called BY sync_skills.

    with (
        patch("scripts.skills_manifest.load_manifest") as mock_load,
        patch("scripts.skills_manifest.iter_skills") as mock_iter,
        patch("scripts.skills_manifest.render_skill_content") as mock_render,
        patch("scripts.skills_manifest.render_antigravity_workflow_content") as mock_workflow_render,
        patch("scripts.sync_skills.load_manifest") as mock_sync_load,
        patch("scripts.sync_skills.validate_manifest"),
        patch("builtins.print"),
        patch("builtins.open", new_callable=MagicMock) as mock_open,
        patch("pathlib.Path.mkdir"),
        patch("pathlib.Path.write_text", autospec=True) as mock_write_text,
    ):
        # Import inside the patch context to ensure clean slate if needed,
        # though standard import caching applies.
        sync_skills_module = importlib.import_module("scripts.sync_skills")
        antigravity_dir = sync_skills_module.ANTIGRAVITY_DIR
        antigravity_global_dir = sync_skills_module.ANTIGRAVITY_GLOBAL_DIR

        # Setup Test Data
        fake_skill = {"name": "conductor-test", "template": "test_template", "id": "test"}
        mock_load.return_value = {}  # content doesn't matter as we mock iter_skills
        mock_sync_load.return_value = {"manifest_version": 1}
        mock_iter.return_value = [fake_skill]
        mock_render.return_value = "# Test Content"
        mock_workflow_render.return_value = "# Workflow Content"

        # Configure mock_open to handle json.load(f)
        # We need a context manager mock that returns a string on .read()
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.read.return_value = '{"contributes": {"commands": []}}'

        # Execute
        sync_skills_module.sync_skills()

        # Verification 1: Check Local Antigravity Sync (.antigravity/skills/conductor-test/SKILL.md)
        expected_local_file = antigravity_dir / "conductor-test" / "SKILL.md"

        # We need to find if write_text was called with this path.
        # Note: Paths might be absolute.
        written_files = [str(call.args[0]) for call in mock_write_text.call_args_list]

        assert str(expected_local_file) in written_files, f"Did not attempt to write to {expected_local_file}"

        # Verification 2: Check Global Antigravity Sync (Flat structure)
        # Assuming CONDUCTOR_SYNC_REPO_ONLY is not set or handling default
        # The script checks env var. We should mock os.environ or ensure it's not set.

        expected_global_file = antigravity_global_dir / "conductor-test.md"
        assert str(expected_global_file) in written_files, f"Did not attempt to write to {expected_global_file}"
