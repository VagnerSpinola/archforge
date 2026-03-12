from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from archforge.core.exceptions import PluginError, ValidationError
from archforge.core.models.plugin import (
    CliCommandRegistrar,
    DatabaseStrategyFactory,
    FrameworkStrategyFactory,
    GeneratorContribution,
    PluginConfigOption,
    ProjectTemplateStrategyFactory,
)

if TYPE_CHECKING:
    from archforge.strategies.database_strategy import DatabaseStrategy
    from archforge.strategies.framework_strategy import FrameworkStrategy
    from archforge.strategies.project_template_strategy import ProjectTemplateStrategy


class PluginRegistry:
    def __init__(self) -> None:
        self._plugin_names: set[str] = set()
        self._template_directories: list[Path] = []
        self._cli_registrars: list[CliCommandRegistrar] = []
        self._generators: dict[str, GeneratorContribution] = {}
        self._config_options: dict[str, PluginConfigOption] = {}
        self._framework_strategies: dict[str, FrameworkStrategyFactory] = {}
        self._database_strategies: dict[str, DatabaseStrategyFactory] = {}
        self._project_templates: dict[str, ProjectTemplateStrategyFactory] = {}

    @property
    def template_directories(self) -> tuple[Path, ...]:
        return tuple(self._template_directories)

    @property
    def cli_registrars(self) -> tuple[CliCommandRegistrar, ...]:
        return tuple(self._cli_registrars)

    @property
    def config_options(self) -> tuple[PluginConfigOption, ...]:
        return tuple(self._config_options.values())

    @property
    def plugin_names(self) -> tuple[str, ...]:
        return tuple(sorted(self._plugin_names))

    def register_plugin(self, name: str) -> None:
        if name in self._plugin_names:
            raise PluginError(f"Plugin '{name}' has already been registered.")
        self._plugin_names.add(name)

    def register_template_directory(self, directory: Path) -> None:
        resolved_directory = directory.resolve()
        if not resolved_directory.exists():
            raise PluginError(f"Plugin template directory does not exist: {resolved_directory}")
        if resolved_directory not in self._template_directories:
            self._template_directories.append(resolved_directory)

    def register_cli_command(self, registrar: CliCommandRegistrar) -> None:
        self._cli_registrars.append(registrar)

    def register_generator(self, contribution: GeneratorContribution) -> None:
        if contribution.kind in self._generators:
            raise PluginError(f"Generator '{contribution.kind}' has already been registered.")
        self._generators[contribution.kind] = contribution

    def register_config_option(self, option: PluginConfigOption) -> None:
        if option.name in self._config_options:
            raise PluginError(f"Configuration option '{option.name}' has already been registered.")
        self._config_options[option.name] = option

    def register_framework_strategy(self, name: str, factory: FrameworkStrategyFactory) -> None:
        if name in self._framework_strategies:
            raise PluginError(f"Framework strategy '{name}' has already been registered.")
        self._framework_strategies[name] = factory

    def register_database_strategy(self, name: str, factory: DatabaseStrategyFactory) -> None:
        if name in self._database_strategies:
            raise PluginError(f"Database strategy '{name}' has already been registered.")
        self._database_strategies[name] = factory

    def register_project_template(self, name: str, factory: ProjectTemplateStrategyFactory) -> None:
        if name in self._project_templates:
            raise PluginError(f"Project template '{name}' has already been registered.")
        self._project_templates[name] = factory

    def create_framework_strategy(self, name: str) -> FrameworkStrategy:
        if name not in self._framework_strategies:
            raise ValidationError(f"Unsupported framework: {name}")
        return self._framework_strategies[name]()

    def create_database_strategy(self, name: str) -> DatabaseStrategy:
        if name not in self._database_strategies:
            raise ValidationError(f"Unsupported database strategy: {name}")
        return self._database_strategies[name]()

    def create_project_template(self, name: str) -> ProjectTemplateStrategy:
        if name not in self._project_templates:
            raise ValidationError(f"Unsupported project template: {name}")
        return self._project_templates[name]()

    def get_generator(self, kind: str) -> GeneratorContribution:
        if kind not in self._generators:
            raise ValidationError(f"Unsupported module type: {kind}")
        return self._generators[kind]

    def default_option_values(self) -> dict[str, str]:
        defaults: dict[str, str] = {}
        for option in self._config_options.values():
            if option.default is not None:
                defaults[option.name] = option.default
        return defaults

    def validate_option_names(self, options: dict[str, str]) -> None:
        unknown = sorted(set(options) - set(self._config_options))
        if unknown:
            formatted = ", ".join(unknown)
            raise ValidationError(f"Unsupported configuration option(s): {formatted}")

        missing = sorted(
            option.name
            for option in self._config_options.values()
            if option.required and option.name not in options
        )
        if missing:
            formatted = ", ".join(missing)
            raise ValidationError(f"Missing required configuration option(s): {formatted}")