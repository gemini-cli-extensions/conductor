from pathlib import Path


def test_docs_matrix_updated():
    docs_path = Path("docs/skill-command-syntax.md")
    content = docs_path.read_text(encoding="utf-8")
    assert "| aix |" in content
    assert "| skillshare |" in content
