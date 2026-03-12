from __future__ import annotations

from pathlib import Path

from archforge.core.models.template_file import TemplateFile
from archforge.services.filesystem_service import FileSystemService
from archforge.services.template_renderer import TemplateRenderer


class FileGenerator:
    def __init__(self, renderer: TemplateRenderer, file_system: FileSystemService) -> None:
        self._renderer = renderer
        self._file_system = file_system

    def generate(self, template_file: TemplateFile) -> Path:
        content = self._renderer.render(template_file.template_name, template_file.context)
        return self._file_system.write_text(template_file.output_path, content)