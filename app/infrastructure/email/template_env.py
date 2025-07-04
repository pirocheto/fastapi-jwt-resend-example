from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.config import settings

base_dir = Path(settings.app_dir)

envs = {
    "html": Environment(
        loader=FileSystemLoader(str(base_dir / "infrastructure/email/templates/html")),
        autoescape=True,
    ),
    "raw": Environment(
        loader=FileSystemLoader(str(base_dir / "infrastructure/email/templates/raw")),
        autoescape=False,
    ),
}
