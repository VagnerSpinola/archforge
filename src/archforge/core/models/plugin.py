from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from archforge.core.models.template_file import TemplateFile

if TYPE_CHECKING:
    import typer

    from archforge.core.models.project_config import ProjectConfig
    from archforge.services.filesystem_service import FileSystemService
    from archforge.services.plugin_registry import PluginRegistry
    from archforge.strategies.database_strategy import DatabaseStrategy
    from archforge.strategies.framework_strategy import FrameworkStrategy
    from archforge.strategies.project_template_strategy import ProjectTemplateStrategy

FrameworkStrategyFactory = Callable[[], "FrameworkStrategy"]
DatabaseStrategyFactory = Callable[[], "DatabaseStrategy"]
ProjectTemplateStrategyFactory = Callable[[], "ProjectTemplateStrategy"]
CliCommandRegistrar = Callable[["typer.Typer", "typer.Typer", "PluginRegistry"], None]
TemplateBuilder = Callable[["ProjectConfig", dict[str, object]], list[TemplateFile]]
PostGenerateHook = Callable[["FileSystemService", "ProjectConfig", dict[str, object]], None]


@dataclass(frozen=True, slots=True)
class PluginConfigOption:
    name: str
    description: str
    default: str | None = None
    required: bool = False


@dataclass(frozen=True, slots=True)
class GeneratorContribution:
    kind: str
    build_templates: TemplateBuilder
    after_generate: PostGenerateHook | None = None