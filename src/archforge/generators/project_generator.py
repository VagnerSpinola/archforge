from __future__ import annotations

from pathlib import Path

from archforge.builders.project_builder import ProjectBuilder
from archforge.core.constants.layout import GENERATED_SOURCE_DIRECTORIES
from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile
from archforge.generators.base import BaseGenerator
from archforge.generators.file_generator import FileGenerator
from archforge.services.filesystem_service import FileSystemService
from archforge.services.validation_service import ValidationService


class ProjectGenerator(BaseGenerator[TemplateFile]):
    def __init__(
        self,
        builder: ProjectBuilder,
        file_generator: FileGenerator,
        file_system: FileSystemService,
        validation: ValidationService,
    ) -> None:
        self._builder = builder
        self._file_generator = file_generator
        self._file_system = file_system
        self._validation = validation

    def validate(self, config: ProjectConfig) -> None:
        self._validation.validate_project_config(config)

    def prepare(self, config: ProjectConfig) -> Path:
        project_root = self._file_system.create_project_root(config.service_root)
        for relative_directory in GENERATED_SOURCE_DIRECTORIES:
            self._file_system.create_directory(project_root / relative_directory)
        self._file_system.create_directory(project_root / "tests" / "unit")
        self._file_system.create_directory(project_root / "tests" / "integration")
        self._file_system.create_directory(project_root / "tests" / "e2e")
        return project_root

    def collect_artifacts(self, config: ProjectConfig) -> list[TemplateFile]:
        return self._builder.build(config)

    def persist(self, artifacts: list[TemplateFile]) -> None:
        for artifact in artifacts:
            self._file_generator.generate(artifact)