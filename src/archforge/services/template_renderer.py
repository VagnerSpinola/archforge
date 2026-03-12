from __future__ import annotations

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from archforge.core.exceptions import TemplateError
from archforge.utils.naming import kebab_case, pascal_case, pluralize, slug_to_snake_case


class TemplateRenderer:
    def __init__(self, template_directories: Iterable[Path] | None = None) -> None:
        template_root = Path(str(files("archforge").joinpath("templates")))
        search_paths = [str(template_root)]
        if template_directories is not None:
            search_paths.extend(str(directory) for directory in template_directories)
        environment = Environment(
            loader=FileSystemLoader(search_paths),
            autoescape=False,
            keep_trailing_newline=True,
            lstrip_blocks=True,
            trim_blocks=True,
            undefined=StrictUndefined,
        )
        environment.filters["snake_case"] = slug_to_snake_case
        environment.filters["pascal_case"] = pascal_case
        environment.filters["pluralize"] = pluralize
        environment.filters["kebab_case"] = kebab_case
        self._environment = environment

    def render(self, template_name: str, context: dict[str, object]) -> str:
        try:
            template = self._environment.get_template(template_name)
            return template.render(**context)
        except Exception as exc:  # noqa: BLE001
            raise TemplateError(f"Unable to render template '{template_name}': {exc}") from exc