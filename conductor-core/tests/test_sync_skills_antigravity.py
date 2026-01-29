import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def test_sync_to_antigravity():
    repo_root = _repo_root()
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    # Force unload of any existing 'scripts' module to avoid conflict with external packages
    if 'scripts' in sys.modules:
        del sys.modules['scripts']
    if 'scripts.skills_manifest' in sys.modules:
        del sys.modules['scripts.skills_manifest']

    # Ensure module is loaded to avoid AttributeError in patch with namespace packages
    import scripts.skills_manifest
    
    # Verify we got the right one
    assert str(repo_root) in str(scripts.skills_manifest.__file__), f"Wrong scripts module loaded: {scripts.skills_manifest.__file__}"

    # We need to mock BEFORE importing the module if we want to mock constants, 
    # but here we want to mock the behavior of functions called BY sync_skills.
    
    with patch('scripts.skills_manifest.load_manifest') as mock_load, \
         patch('scripts.skills_manifest.iter_skills') as mock_iter, \
         patch('scripts.skills_manifest.render_skill_content') as mock_render, \
         patch('builtins.print') as mock_print, \
         patch('builtins.open', new_callable=MagicMock) as mock_open, \
         patch('pathlib.Path.mkdir') as mock_mkdir:

        # Import inside the patch context to ensure clean slate if needed, 
        # though standard import caching applies.
        from scripts.sync_skills import sync_skills, ANTIGRAVITY_DIR, ANTIGRAVITY_GLOBAL_DIR

        # Setup Test Data
        fake_skill = {"name": "conductor-test", "template": "test_template"}
        mock_load.return_value = {} # content doesn't matter as we mock iter_skills
        mock_iter.return_value = [fake_skill]
        mock_render.return_value = "# Test Content"

        # Execute
        sync_skills()

        # Verification 1: Check Local Antigravity Sync (.antigravity/skills/conductor-test/SKILL.md)
        expected_local_file = ANTIGRAVITY_DIR / "conductor-test" / "SKILL.md"
        
        # We need to find if open was called with this path.
        # Note: Paths might be absolute.
        opened_files = [str(call.args[0]) for call in mock_open.call_args_list]
        
        assert str(expected_local_file) in opened_files, f"Did not attempt to write to {expected_local_file}"

        # Verification 2: Check Global Antigravity Sync (Flat structure)
        # Assuming CONDUCTOR_SYNC_REPO_ONLY is not set or handling default
        # The script checks env var. We should mock os.environ or ensure it's not set.
        
        expected_global_file = ANTIGRAVITY_GLOBAL_DIR / "conductor-test.md"
        assert str(expected_global_file) in opened_files, f"Did not attempt to write to {expected_global_file}"