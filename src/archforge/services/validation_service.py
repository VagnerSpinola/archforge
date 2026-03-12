from __future__ import annotations

import re
from pathlib import Path

from archforge.core.constants.layout import REQUIRED_PROJECT_MARKERS
from archforge.core.exceptions import InvalidProjectError, ValidationError
from archforge.core.models.project_config import ProjectConfig
from archforge.services.filesystem_service import FileSystemService
from archforge.utils.naming import kebab_case


class ValidationService:
    _name_pattern = re.compile(r"^[a-z][a-z0-9_-]*$")

    def __init__(self, file_system: FileSystemService) -> None:
        self._file_system = file_system

    def validate_project_config(self, config: ProjectConfig) -> None:
        normalized_name = self.validate_project_name(config.project_name)
        if normalized_name != config.project_name:
            raise ValidationError(
                f"Project name '{config.project_name}' must use lowercase kebab-case."
            )

        if config.service_root.exists():
            raise ValidationError(f"Destination already exists: {config.service_root}")

    def validate_project_name(self, name: str) -> str:
        return self._validate_name(name=name, subject="project")

    def validate_module_name(self, name: str) -> str:
        return self._validate_name(name=name, subject="module")

    def validate_existing_project(self, project_root: Path) -> None:
        missing_markers = [
            marker for marker in REQUIRED_PROJECT_MARKERS if not (project_root / marker).exists()
        ]
        if missing_markers:
            formatted_markers = ", ".join(str(marker) for marker in missing_markers)
            raise InvalidProjectError(
                f"{project_root} is not a supported ArchForge project. "
                f"Missing: {formatted_markers}."
            )

    def _validate_name(self, name: str, subject: str) -> str:
        candidate = name.strip()
        if not candidate:
            raise ValidationError(f"{subject.capitalize()} name cannot be empty.")
        if not self._name_pattern.match(candidate):
            raise ValidationError(
                f"{subject.capitalize()} name '{candidate}' must start with a lowercase "
                f"letter and contain only lowercase letters, numbers, or '-'."
            )
        return kebab_case(candidate)