from __future__ import annotations

import re
from pathlib import Path

from .prompts import PromptProvider


class ValidationService:
    def __init__(self, core_templates_dir: str | Path) -> None:
        self.provider = PromptProvider(core_templates_dir)

    def validate_gemini_toml(self, toml_path: str | Path, template_name: str) -> tuple[bool, str]:
        """
        Validates that the 'prompt' field in a Gemini TOML matches the core template.
        """
        path = Path(toml_path)
        if not path.exists():
            return False, f"File not found: {toml_path}"

        toml_content = path.read_text(encoding="utf-8")

        # Simple regex to extract prompt string from TOML
        match = re.search(r'prompt\s*=\s*"""(.*?)"""', toml_content, re.DOTALL)
        if not match:
            return False, f"Could not find prompt field in {toml_path}"

        toml_prompt = match.group(1).strip()
        core_prompt = self.provider.get_template_text(template_name).strip()

        if toml_prompt == core_prompt:
            return True, "Matches core template"

        return False, "Content mismatch"

    def validate_claude_md(self, md_path: str | Path, template_name: str) -> tuple[bool, str]:
        """
        Validates that a Claude Markdown skill/command matches the core template.
        """
        path = Path(md_path)
        if not path.exists():
            return False, f"File not found: {md_path}"

        md_content = path.read_text(encoding="utf-8").strip()

        core_prompt = self.provider.get_template_text(template_name).strip()

        if md_content == core_prompt:
            return True, "Matches core template"

        # Claude files might have frontmatter or extra headers
        # For now, we assume exact match or look for the protocol headers
        if core_prompt in md_content:
            return True, "Core protocol found in file"

        return False, "Content mismatch"

    def synchronize_gemini_toml(self, toml_path: str | Path, template_name: str) -> tuple[bool, str]:
        """
        Overwrites the 'prompt' field in a Gemini TOML with the core template content.
        """
        path = Path(toml_path)
        if not path.exists():
            return False, f"File not found: {toml_path}"

        content = path.read_text(encoding="utf-8")

        core_prompt = self.provider.get_template_text(template_name).strip()
        prompt_block = f'prompt = """\n{core_prompt}\n"""'
        if re.search(r'prompt\s*=\s*""".*?"""', content, flags=re.DOTALL):
            new_content = re.sub(
                r'prompt\s*=\s*""".*?"""',
                prompt_block,
                content,
                flags=re.DOTALL,
            )
        elif re.search(r'prompt\s*=\s*""', content):
            new_content = re.sub(r'prompt\s*=\s*""', prompt_block, content)
        else:
            new_content = content.rstrip() + "\n" + prompt_block + "\n"

        path.write_text(new_content, encoding="utf-8")

        return True, "Successfully synchronized Gemini TOML"

    def synchronize_claude_md(self, md_path: str | Path, template_name: str) -> tuple[bool, str]:
        """
        Overwrites a Claude Markdown file with the core template content.
        """
        # For now, we overwrite the entire file as these are strictly prompt files
        core_prompt = self.provider.get_template_text(template_name).strip()

        path = Path(md_path)
        path.write_text(core_prompt, encoding="utf-8")

        return True, "Successfully synchronized Claude MD"
