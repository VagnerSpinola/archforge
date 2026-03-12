from __future__ import annotations

from abc import ABC, abstractmethod

from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile
from archforge.utils.naming import kebab_case, pascal_case


class FrameworkStrategy(ABC):
    @abstractmethod
    def build_context(self, config: ProjectConfig) -> dict[str, object]:
        raise NotImplementedError

    @abstractmethod
    def template_files(self, config: ProjectConfig) -> list[TemplateFile]:
        raise NotImplementedError


class FastAPIFrameworkStrategy(FrameworkStrategy):
    def build_context(self, config: ProjectConfig) -> dict[str, object]:
        bounded_context = pascal_case(config.service_slug.replace("_service", ""))
        return {
            "project_name": config.project_name,
            "framework": config.framework,
            "service_slug": config.service_slug,
            "service_title": config.project_name.replace("-", " ").title(),
            "bounded_context": bounded_context,
            "docker_service_name": kebab_case(config.project_name),
        }

    def template_files(self, config: ProjectConfig) -> list[TemplateFile]:
        return []