from __future__ import annotations

from pathlib import Path
from typing import Protocol


class RendersTemplates(Protocol):
    def render(self, template_name: str, context: dict[str, object]) -> str:
        ...


class SupportsFileOperations(Protocol):
    def create_directory(self, directory: Path) -> Path:
        ...

    def create_project_root(self, project_root: Path) -> Path:
        ...

    def write_text(self, file_path: Path, content: str, *, overwrite: bool = False) -> Path:
        ...

    def append_unique_block(self, file_path: Path, block: str) -> Path:
        ...


class ValidatesProjects(Protocol):
    def validate_project_config(self, config: object) -> None:
        ...

    def validate_existing_project(self, project_root: Path) -> None:
        ...

    def validate_module_name(self, name: str) -> str:
        ...