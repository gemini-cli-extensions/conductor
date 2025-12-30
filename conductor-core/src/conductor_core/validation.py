import os
import re
from typing import Dict, List, Tuple
from .prompts import PromptProvider

class ValidationService:
    def __init__(self, core_templates_dir: str):
        self.provider = PromptProvider(core_templates_dir)

    def validate_gemini_toml(self, toml_path: str, template_name: str) -> Tuple[bool, str]:
        """
        Validates that the 'prompt' field in a Gemini TOML matches the core template.
        """
        if not os.path.exists(toml_path):
            return False, f"File not found: {toml_path}"
        
        with open(toml_path, 'r') as f:
            toml_content = f.read()
        
        # Simple regex to extract prompt string from TOML
        match = re.search(r'prompt\s*=\s*"""(.*?)"""', toml_content, re.DOTALL)
        if not match:
            return False, f"Could not find prompt field in {toml_path}"
        
        toml_prompt = match.group(1).strip()
        core_prompt = self.provider.get_template_text(template_name).strip()
        
        if toml_prompt == core_prompt:
            return True, "Matches core template"
        else:
            return False, "Content mismatch"

    def validate_claude_md(self, md_path: str, template_name: str) -> Tuple[bool, str]:
        """
        Validates that a Claude Markdown skill/command matches the core template.
        """
        if not os.path.exists(md_path):
            return False, f"File not found: {md_path}"
        
        with open(md_path, 'r') as f:
            md_content = f.read().strip()
        
        core_prompt = self.provider.get_template_text(template_name).strip()
        
        if md_content == core_prompt:
            return True, "Matches core template"
        else:
            # Claude files might have frontmatter or extra headers
            # For now, we assume exact match or look for the protocol headers
            if core_prompt in md_content:
                return True, "Core protocol found in file"
            return False, "Content mismatch"

    def synchronize_gemini_toml(self, toml_path: str, template_name: str) -> Tuple[bool, str]:
        """
        Overwrites the 'prompt' field in a Gemini TOML with the core template content.
        """
        if not os.path.exists(toml_path):
            return False, f"File not found: {toml_path}"
        
        with open(toml_path, 'r') as f:
            content = f.read()
        
        core_prompt = self.provider.get_template_text(template_name).strip()
        # Regex to find and replace the prompt block
        new_content = re.sub(r'prompt\s*=\s*""".*?"""', f'prompt = """\n{core_prompt}\n"""', content, flags=re.DOTALL)
        
        with open(toml_path, 'w') as f:
            f.write(new_content)
        
        return True, "Successfully synchronized Gemini TOML"

    def synchronize_claude_md(self, md_path: str, template_name: str) -> Tuple[bool, str]:
        """
        Overwrites a Claude Markdown file with the core template content.
        """
        # For now, we overwrite the entire file as these are strictly prompt files
        core_prompt = self.provider.get_template_text(template_name).strip()
        
        with open(md_path, 'w') as f:
            f.write(core_prompt)
            
        return True, "Successfully synchronized Claude MD"
