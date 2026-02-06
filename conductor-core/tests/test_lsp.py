from conductor_core.lsp import completions
from lsprotocol.types import CompletionParams, Position, TextDocumentIdentifier


def test_lsp_completions_exists():
    assert callable(completions)


def test_completions_returns_list():
    params = CompletionParams(
        text_document=TextDocumentIdentifier(uri="file://test"), position=Position(line=0, character=0)
    )
    result = completions(params)
    assert len(result.items) > 0
    assert result.items[0].label.startswith("/conductor")
