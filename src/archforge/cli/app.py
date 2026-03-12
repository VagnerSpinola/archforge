from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Annotated

import typer

from archforge.builders.project_builder import ProjectBuilder
from archforge.core.exceptions import ArchforgeError
from archforge.core.models.project_config import ProjectConfig
from archforge.factories.framework_factory import FrameworkFactory
from archforge.generators.file_generator import FileGenerator
from archforge.generators.module_generator import ModuleGenerator
from archforge.generators.project_generator import ProjectGenerator
from archforge.services.filesystem_service import FileSystemService
from archforge.services.plugin_loader import load_plugin_registry
from archforge.services.plugin_registry import PluginRegistry
from archforge.services.template_renderer import TemplateRenderer
from archforge.services.validation_service import ValidationService

ProjectNameArgument = Annotated[str, typer.Argument(help="Name of the service to create.")]
ModuleNameArgument = Annotated[str, typer.Argument(help="Name of the module to create.")]
DestinationOption = Annotated[
    Path | None,
    typer.Option(
        "--destination",
        "-d",
        resolve_path=True,
        file_okay=False,
        help="Base directory where the new project will be created.",
    ),
]
ProjectRootOption = Annotated[
    Path | None,
    typer.Option(
        "--project-root",
        resolve_path=True,
        file_okay=False,
        help="Path to an existing ArchForge-generated project.",
    ),
]
FrameworkOption = Annotated[
    str,
    typer.Option("--framework", help="Framework strategy to use for the generated project."),
]
DatabaseOption = Annotated[
    str,
    typer.Option("--database", help="Database strategy to use for the generated project."),
]
ProjectTemplateOption = Annotated[
    str,
    typer.Option(
        "--template",
        help="Project template to use for the generated service.",
    ),
]
ConfigOption = Annotated[
    list[str] | None,
    typer.Option(
        "--option",
        "-o",
        help="Plugin configuration option in the form key=value. Can be passed multiple times.",
    ),
]


@lru_cache(maxsize=1)
def get_plugin_registry() -> PluginRegistry:
    return load_plugin_registry()


def _build_project_generator(plugin_registry: PluginRegistry) -> ProjectGenerator:
    template_renderer = TemplateRenderer(template_directories=plugin_registry.template_directories)
    file_system = FileSystemService()
    validation = ValidationService(file_system=file_system)
    project_builder = ProjectBuilder(
        framework_factory=FrameworkFactory(plugin_registry=plugin_registry)
    )
    file_generator = FileGenerator(renderer=template_renderer, file_system=file_system)
    return ProjectGenerator(
        builder=project_builder,
        file_generator=file_generator,
        file_system=file_system,
        validation=validation,
    )


def _build_module_generator(plugin_registry: PluginRegistry) -> ModuleGenerator:
    template_renderer = TemplateRenderer(template_directories=plugin_registry.template_directories)
    file_system = FileSystemService()
    validation = ValidationService(file_system=file_system)
    return ModuleGenerator(
        renderer=template_renderer,
        file_system=file_system,
        validation=validation,
        plugin_registry=plugin_registry,
    )


def _parse_config_options(
    raw_options: list[str] | None,
    plugin_registry: PluginRegistry,
) -> dict[str, str]:
    parsed_options = plugin_registry.default_option_values()
    for raw_option in raw_options or []:
        if "=" not in raw_option:
            raise typer.BadParameter(
                f"Invalid configuration option '{raw_option}'. Expected key=value.",
                param_hint="--option",
            )
        key, value = raw_option.split("=", maxsplit=1)
        parsed_options[key.strip()] = value.strip()

    plugin_registry.validate_option_names(parsed_options)
    return parsed_options


def create_app(plugin_registry: PluginRegistry | None = None) -> typer.Typer:
    registry = plugin_registry or get_plugin_registry()
    app = typer.Typer(help="Scaffold and extend production-ready backend services.")
    add_app = typer.Typer(help="Add architectural modules to an existing service.")
    app.add_typer(add_app, name="add")

    @app.command()
    def new(
        project_name: ProjectNameArgument,
        destination: DestinationOption = None,
        project_template: ProjectTemplateOption = "api-service",
        framework: FrameworkOption = "fastapi",
        database: DatabaseOption = "in_memory",
        option: ConfigOption = None,
    ) -> None:
        """Create a new backend service."""
        generator = _build_project_generator(registry)
        config = ProjectConfig(
            project_name=project_name,
            destination_root=destination or Path.cwd(),
            project_template=project_template,
            framework=framework,
            database=database,
            options=_parse_config_options(option, registry),
        )

        try:
            typer.secho(f"Validating project '{project_name}'...", fg=typer.colors.BLUE)
            project_root = generator.generate(config)
        except ArchforgeError as exc:
            typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc

        typer.secho(f"Created project at {project_root}", fg=typer.colors.GREEN)

    @add_app.command("entity")
    def add_entity(name: ModuleNameArgument, project_root: ProjectRootOption = None) -> None:
        _run_add_command(
            kind="entity",
            name=name,
            project_root=project_root,
            plugin_registry=registry,
        )

    @add_app.command("use-case")
    def add_use_case(name: ModuleNameArgument, project_root: ProjectRootOption = None) -> None:
        _run_add_command(
            kind="use_case",
            name=name,
            project_root=project_root,
            plugin_registry=registry,
        )

    @add_app.command("repository")
    def add_repository(name: ModuleNameArgument, project_root: ProjectRootOption = None) -> None:
        _run_add_command(
            kind="repository",
            name=name,
            project_root=project_root,
            plugin_registry=registry,
        )

    @add_app.command("endpoint")
    def add_endpoint(name: ModuleNameArgument, project_root: ProjectRootOption = None) -> None:
        _run_add_command(
            kind="endpoint",
            name=name,
            project_root=project_root,
            plugin_registry=registry,
        )

    for registrar in registry.cli_registrars:
        registrar(app, add_app, registry)

    return app


def _run_add_command(
    kind: str,
    name: str,
    project_root: Path | None,
    plugin_registry: PluginRegistry,
) -> None:
    generator = _build_module_generator(plugin_registry)
    root = project_root or Path.cwd()

    try:
        config = ProjectConfig.from_existing_project(root)
        created_files = generator.generate(kind=kind, name=name, config=config)
    except ArchforgeError as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    typer.secho(f"Created {kind.replace('_', '-')} modules:", fg=typer.colors.GREEN)
    for created_file in created_files:
        typer.echo(f" - {created_file}")


app = create_app()


def run() -> None:
    app()