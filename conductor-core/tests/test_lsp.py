import sys
from unittest.mock import MagicMock

# Mock pygls and lsprotocol for the feasibility study
mock_pygls = MagicMock()
mock_lsprotocol = MagicMock()
sys.modules["pygls"] = mock_pygls
sys.modules["pygls.server"] = mock_pygls.server
sys.modules["lsprotocol"] = mock_lsprotocol
sys.modules["lsprotocol.types"] = mock_lsprotocol.types

import pytest
from conductor_core.lsp import completions

def test_lsp_completions_exists():
    assert callable(completions)
