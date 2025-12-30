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
        template = self.env.get_template(template_name)
        return template.render(**kwargs)

    def render_string(self, source: str, **kwargs) -> str:
        template = Template(source)
        return template.render(**kwargs)
