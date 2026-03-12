from __future__ import annotations

from archforge.core.contracts.plugin import ArchforgePlugin
from archforge.core.models.plugin import GeneratorContribution
from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile
from archforge.services.filesystem_service import FileSystemService
from archforge.services.plugin_registry import PluginRegistry
from archforge.strategies.database_strategy import InMemoryDatabaseStrategy
from archforge.strategies.framework_strategy import FastAPIFrameworkStrategy
from archforge.strategies.project_template_strategy import (
    ApiServiceTemplateStrategy,
    EventDrivenServiceTemplateStrategy,
    WorkerServiceTemplateStrategy,
)


class CorePlugin(ArchforgePlugin):
    @property
    def name(self) -> str:
        return "core"

    def register(self, registry: PluginRegistry) -> None:
        registry.register_framework_strategy("fastapi", FastAPIFrameworkStrategy)
        registry.register_database_strategy("in_memory", InMemoryDatabaseStrategy)
        registry.register_project_template("api-service", ApiServiceTemplateStrategy)
        registry.register_project_template("worker-service", WorkerServiceTemplateStrategy)
        registry.register_project_template(
            "event-driven-service",
            EventDrivenServiceTemplateStrategy,
        )
        registry.register_generator(
            GeneratorContribution(kind="entity", build_templates=self._entity_templates)
        )
        registry.register_generator(
            GeneratorContribution(kind="use_case", build_templates=self._use_case_templates)
        )
        registry.register_generator(
            GeneratorContribution(kind="repository", build_templates=self._repository_templates)
        )
        registry.register_generator(
            GeneratorContribution(
                kind="endpoint",
                build_templates=self._endpoint_templates,
                after_generate=self._register_endpoint_router,
            )
        )

    def _entity_templates(
        self,
        config: ProjectConfig,
        context: dict[str, object],
    ) -> list[TemplateFile]:
        return [
            TemplateFile(
                "common/entity.py.j2",
                config.source_root / "domain" / "entities" / f"{context['module_name']}.py",
                context,
            )
        ]

    def _use_case_templates(
        self,
        config: ProjectConfig,
        context: dict[str, object],
    ) -> list[TemplateFile]:
        return [
            TemplateFile(
                "common/use_case.py.j2",
                config.source_root / "application" / "use_cases" / f"{context['module_name']}.py",
                context,
            )
        ]

    def _repository_templates(
        self,
        config: ProjectConfig,
        context: dict[str, object],
    ) -> list[TemplateFile]:
        return [
            TemplateFile(
                "common/repository_interface.py.j2",
                config.source_root
                / "domain"
                / "repositories"
                / f"{context['module_name']}_repository.py",
                context,
            ),
            TemplateFile(
                "common/repository_implementation.py.j2",
                config.source_root
                / "infrastructure"
                / "repositories"
                / f"in_memory_{context['module_name']}_repository.py",
                context,
            ),
        ]

    def _endpoint_templates(
        self,
        config: ProjectConfig,
        context: dict[str, object],
    ) -> list[TemplateFile]:
        return [
            TemplateFile(
                "common/schema.py.j2",
                config.source_root / "presentation" / "schemas" / f"{context['module_name']}.py",
                context,
            ),
            TemplateFile(
                "common/endpoint.py.j2",
                config.source_root / "presentation" / "api" / f"{context['collection_name']}.py",
                context,
            ),
        ]

    def _register_endpoint_router(
        self,
        file_system: FileSystemService,
        config: ProjectConfig,
        context: dict[str, object],
    ) -> None:
        router_path = config.source_root / "presentation" / "api" / "router.py"
        collection_name = str(context["collection_name"])
        block = (
            f"from presentation.api.{collection_name} import router as {collection_name}_router\n"
            f"api_router.include_router({collection_name}_router)"
        )
        file_system.append_unique_block(router_path, block)
