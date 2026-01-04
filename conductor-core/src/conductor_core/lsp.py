from pygls.server import LanguageServer
from lsprotocol.types import (
    TEXT_DOCUMENT_COMPLETION,
    CompletionItem,
    CompletionList,
    CompletionParams,
)

server = LanguageServer("conductor-lsp", "v0.1.0")

@server.feature(TEXT_DOCUMENT_COMPLETION)
def completions(params: CompletionParams = None) -> CompletionList:
    """Returns completion items for Conductor commands."""
    items = [
        CompletionItem(label="/conductor:setup"),
        CompletionItem(label="/conductor:newTrack"),
        CompletionItem(label="/conductor:implement"),
        CompletionItem(label="/conductor:status"),
        CompletionItem(label="/conductor:revert"),
    ]
    return CompletionList(is_incomplete=False, items=items)

def start_lsp():
    # In a real scenario, this would be invoked by the VS Code extension
    # starting the Python process with the LSP feature enabled.
    print("Conductor LSP prototype ready.")
    # server.start_io()
