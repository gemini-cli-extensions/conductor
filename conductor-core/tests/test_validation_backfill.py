import pytest
from conductor_core.validation import ValidationService


@pytest.fixture()
def validation_setup(tmp_path):
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "test.md").write_text("Hello World")

    vs = ValidationService(str(templates_dir))
    return vs, templates_dir


def test_validate_gemini_toml_success(validation_setup, tmp_path):
    vs, _ = validation_setup
    toml_file = tmp_path / "test.toml"
    content = chr(10).join(['prompt = """', "Hello World", '"""'])
    toml_file.write_text(content)

    valid, msg = vs.validate_gemini_toml(str(toml_file), "test.md")
    assert valid
    assert msg == "Matches core template"


def test_validate_gemini_toml_missing_file(validation_setup):
    vs, _ = validation_setup
    valid, msg = vs.validate_gemini_toml("missing.toml", "test.md")
    assert not valid
    assert "File not found" in msg


def test_validate_gemini_toml_no_prompt_field(validation_setup, tmp_path):
    vs, _ = validation_setup
    toml_file = tmp_path / "bad.toml"
    toml_file.write_text('key = "value"')

    valid, msg = vs.validate_gemini_toml(str(toml_file), "test.md")
    assert not valid
    assert "Could not find prompt field" in msg


def test_validate_gemini_toml_mismatch(validation_setup, tmp_path):
    vs, _ = validation_setup
    toml_file = tmp_path / "mismatch.toml"
    content = chr(10).join(['prompt = """', "Goodbye", '"""'])
    toml_file.write_text(content)

    valid, msg = vs.validate_gemini_toml(str(toml_file), "test.md")
    assert not valid
    assert "Content mismatch" in msg


def test_validate_claude_md_success(validation_setup, tmp_path):
    vs, _ = validation_setup
    md_file = tmp_path / "test.md"
    md_file.write_text("Hello World")

    valid, msg = vs.validate_claude_md(str(md_file), "test.md")
    assert valid
    assert "Matches core template" in msg


def test_validate_claude_md_missing_file(validation_setup):
    vs, _ = validation_setup
    valid, _msg = vs.validate_claude_md("missing.md", "test.md")
    assert not valid


def test_validate_claude_md_contains(validation_setup, tmp_path):
    vs, _ = validation_setup
    md_file = tmp_path / "contains.md"
    content = chr(10).join(["---", "title: test", "---", "Hello World"])
    md_file.write_text(content)

    valid, msg = vs.validate_claude_md(str(md_file), "test.md")
    assert valid
    assert "Core protocol found" in msg


def test_validate_claude_md_mismatch(validation_setup, tmp_path):
    vs, _ = validation_setup
    md_file = tmp_path / "mismatch.md"
    md_file.write_text("Goodbye")

    valid, msg = vs.validate_claude_md(str(md_file), "test.md")
    assert not valid
    assert "Content mismatch" in msg


def test_synchronize_gemini_toml(validation_setup, tmp_path):
    vs, _ = validation_setup
    toml_file = tmp_path / "sync.toml"
    content = chr(10).join(['prompt = """', "Old", '"""'])
    toml_file.write_text(content)

    valid, _msg = vs.synchronize_gemini_toml(str(toml_file), "test.md")
    assert valid
    expected = chr(10).join(['prompt = """', "Hello World", '"""'])
    assert expected in toml_file.read_text()


def test_synchronize_gemini_toml_missing(validation_setup):
    vs, _ = validation_setup
    valid, _msg = vs.synchronize_gemini_toml("missing.toml", "test.md")
    assert not valid


def test_synchronize_claude_md(validation_setup, tmp_path):
    vs, _ = validation_setup
    md_file = tmp_path / "sync.md"
    md_file.write_text("Old")

    valid, _msg = vs.synchronize_claude_md(str(md_file), "test.md")
    assert valid
    assert md_file.read_text() == "Hello World"
