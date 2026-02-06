import pytest
from conductor_core.prompts import PromptProvider


def test_prompt_rendering():
    provider = PromptProvider(template_dir="templates")
    # For now, we'll mock or use a dummy template
    template_content = "Hello {{ name }}!"
    rendered = provider.render_string(template_content, name="Conductor")
    assert rendered == "Hello Conductor!"


def test_prompt_from_file(tmp_path):
    # Create a temporary template file
    d = tmp_path / "templates"
    d.mkdir()
    p = d / "test.j2"
    p.write_text("Context: {{ project_name }}")

    provider = PromptProvider(template_dir=str(d))
    rendered = provider.render("test.j2", project_name="Conductor")
    assert rendered == "Context: Conductor"


def test_get_template_text(tmp_path):
    d = tmp_path / "templates"
    d.mkdir()
    p = d / "test.j2"
    p.write_text("Raw Template Content")

    provider = PromptProvider(template_dir=str(d))
    assert provider.get_template_text("test.j2") == "Raw Template Content"


def test_render_missing_template():
    provider = PromptProvider(template_dir="non_existent")
    with pytest.raises(RuntimeError):
        provider.render("missing.j2")


def test_get_template_text_missing():
    provider = PromptProvider(template_dir="non_existent")
    with pytest.raises(FileNotFoundError):
        provider.get_template_text("missing.j2")
