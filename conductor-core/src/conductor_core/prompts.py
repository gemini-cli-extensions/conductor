import os
from jinja2 import Environment, FileSystemLoader, Template

class PromptProvider:
    def __init__(self, template_dir: str):
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True
        )

    def render(self, template_name: str, **kwargs) -> str:
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to render template '{template_name}': {e}")

    def render_string(self, source: str, **kwargs) -> str:
        try:
            template = Template(source)
            return template.render(**kwargs)
        except Exception as e:
            raise RuntimeError(f"Failed to render string template: {e}")

    def get_template_text(self, template_name: str) -> str:
        """Returns the raw text of a template file."""
        template_path = os.path.join(self.template_dir, template_name)
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template '{template_name}' not found at {template_path}")
        try:
            with open(template_path, 'r') as f:
                return f.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read template '{template_name}': {e}")
