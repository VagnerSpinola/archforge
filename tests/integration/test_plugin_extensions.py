from __future__ import annotations

from pathlib import Path

from archforge.builders.project_builder import ProjectBuilder
from archforge.core.models.plugin import GeneratorContribution
from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile
from archforge.factories.framework_factory import FrameworkFactory
from archforge.generators.file_generator import FileGenerator
from archforge.generators.module_generator import ModuleGenerator
from archforge.generators.project_generator import ProjectGenerator
from archforge.services.filesystem_service import FileSystemService
from archforge.services.plugin_loader import load_plugin_registry
from archforge.services.plugin_registry import PluginRegistry
from archforge.services.template_renderer import TemplateRenderer
from archforge.services.validation_service import ValidationService


def test_module_generator_supports_plugin_generators(tmp_path: Path) -> None:
    plugin_registry = load_plugin_registry(plugin_directories=[])
    template_directory = tmp_path / "plugin_templates"
    template_directory.mkdir()
    generator_directory = template_directory / "plugin"
    generator_directory.mkdir()
    (generator_directory / "job.py.j2").write_text(
        "job={{ module_name }} region={{ config_options['region'] }}\n",
        encoding="utf-8",
    )
    plugin_registry.register_template_directory(template_directory)
    plugin_registry.register_generator(
        GeneratorContribution(kind="job", build_templates=_build_job_templates)
    )

    project_root = _create_project_generator(plugin_registry).generate(
        ProjectConfig(project_name="billing-service", destination_root=tmp_path)
    )
    file_system = FileSystemService()
    config = ProjectConfig.from_existing_project(project_root).model_copy(
        update={"options": {"region": "eu-west-1"}}
    )
    module_generator = ModuleGenerator(
        renderer=TemplateRenderer(template_directories=plugin_registry.template_directories),
        file_system=file_system,
        validation=ValidationService(file_system=file_system),
        plugin_registry=plugin_registry,
    )

    created_files = module_generator.generate(kind="job", name="fraud-check", config=config)

    created_file = project_root / "src" / "application" / "jobs" / "fraud_check.py"
    assert created_files == [created_file]
    assert created_file.read_text(encoding="utf-8") == "job=fraud_check region=eu-west-1\n"


def _create_project_generator(plugin_registry: PluginRegistry) -> ProjectGenerator:
    file_system = FileSystemService()
    return ProjectGenerator(
        builder=ProjectBuilder(framework_factory=FrameworkFactory(plugin_registry=plugin_registry)),
        file_generator=FileGenerator(
            renderer=TemplateRenderer(template_directories=plugin_registry.template_directories),
            file_system=file_system,
        ),
        file_system=file_system,
        validation=ValidationService(file_system=file_system),
    )


def _build_job_templates(
    config: ProjectConfig,
    context: dict[str, object],
) -> list[TemplateFile]:
    return [
        TemplateFile(
            template_name="plugin/job.py.j2",
            output_path=(
                config.source_root / "application" / "jobs" / f"{context['module_name']}.py"
            ),
            context=context,
        )
    ]