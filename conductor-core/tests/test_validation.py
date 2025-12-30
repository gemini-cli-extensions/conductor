import pytest
import os
from conductor_core.validation import ValidationService

def test_validate_gemini_toml(tmp_path):
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "setup.j2").write_text("CORE PROMPT")
    
    commands = tmp_path / "commands"
    commands.mkdir()
    toml = commands / "setup.toml"
    # Use raw string or careful escaping for multi-line
    content = 'description = "test"\nprompt = """CORE PROMPT"""'
    toml.write_text(content)
    
    service = ValidationService(str(templates))
    valid, msg = service.validate_gemini_toml(str(toml), "setup.j2")
    assert valid is True
    assert msg == "Matches core template"

def test_validate_gemini_toml_mismatch(tmp_path):
    templates = tmp_path / "templates"
    templates.mkdir()
    (templates / "setup.j2").write_text("CORE PROMPT")
    
    commands = tmp_path / "commands"
    commands.mkdir()
    toml = commands / "setup.toml"
    content = 'description = "test"\nprompt = """DIFFERENT PROMPT"""'
    toml.write_text(content)
    
    service = ValidationService(str(templates))
    valid, msg = service.validate_gemini_toml(str(toml), "setup.j2")
    assert valid is False
    assert msg == "Content mismatch"