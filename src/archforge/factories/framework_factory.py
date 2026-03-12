from __future__ import annotations

from archforge.core.models.project_config import ProjectConfig
from archforge.services.plugin_registry import PluginRegistry
from archforge.strategies.database_strategy import DatabaseStrategy
from archforge.strategies.framework_strategy import FrameworkStrategy
from archforge.strategies.project_template_strategy import ProjectTemplateStrategy


class FrameworkFactory:
    def __init__(self, plugin_registry: PluginRegistry) -> None:
        self._plugin_registry = plugin_registry

    def create_framework_strategy(self, config: ProjectConfig) -> FrameworkStrategy:
        return self._plugin_registry.create_framework_strategy(config.framework)

    def create_database_strategy(self, config: ProjectConfig) -> DatabaseStrategy:
        return self._plugin_registry.create_database_strategy(config.database)

    def create_project_template_strategy(self, config: ProjectConfig) -> ProjectTemplateStrategy:
        return self._plugin_registry.create_project_template(config.project_template)