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
