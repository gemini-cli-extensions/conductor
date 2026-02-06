from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template


class PromptProvider:
    def __init__(self, template_dir: str | Path) -> None:
        self.template_dir = Path(template_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)), autoescape=True, trim_blocks=True, lstrip_blocks=True
        )

    def render(self, template_name: str, **kwargs: object) -> str:
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs)
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Failed to render template '{template_name}': {e}") from e

    def render_string(self, source: str, **kwargs: object) -> str:
        try:
            template = Template(source)
            return template.render(**kwargs)
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Failed to render string template: {e}") from e

    def get_template_text(self, template_name: str) -> str:
        """Returns the raw text of a template file."""
        template_path = self.template_dir / template_name
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found at {template_path}")
        try:
            with template_path.open("r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Failed to read template '{template_name}': {e}") from e
