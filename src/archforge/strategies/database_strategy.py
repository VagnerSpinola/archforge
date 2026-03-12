from __future__ import annotations

from abc import ABC, abstractmethod

from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile


class DatabaseStrategy(ABC):
    @abstractmethod
    def build_context(self, config: ProjectConfig) -> dict[str, object]:
        raise NotImplementedError

    @abstractmethod
    def template_files(self, config: ProjectConfig) -> list[TemplateFile]:
        raise NotImplementedError


class InMemoryDatabaseStrategy(DatabaseStrategy):
    def build_context(self, config: ProjectConfig) -> dict[str, object]:
        return {"database_strategy": config.database}

    def template_files(self, config: ProjectConfig) -> list[TemplateFile]:
        return []