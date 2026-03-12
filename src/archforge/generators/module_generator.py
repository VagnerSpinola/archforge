from __future__ import annotations

from pathlib import Path

from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile
from archforge.services.filesystem_service import FileSystemService
from archforge.services.plugin_registry import PluginRegistry
from archforge.services.template_renderer import TemplateRenderer
from archforge.services.validation_service import ValidationService
from archforge.utils.naming import kebab_case, pascal_case, pluralize, slug_to_snake_case


class ModuleGenerator:
    def __init__(
        self,
        renderer: TemplateRenderer,
        file_system: FileSystemService,
        validation: ValidationService,
        plugin_registry: PluginRegistry,
    ) -> None:
        self._renderer = renderer
        self._file_system = file_system
        self._validation = validation
        self._plugin_registry = plugin_registry

    def generate(self, kind: str, name: str, config: ProjectConfig) -> list[Path]:
        self._validation.validate_existing_project(config.service_root)
        self._validation.validate_module_name(name)
        normalized_name = slug_to_snake_case(name)
        context = self._build_context(config=config, name=normalized_name)
        contribution = self._plugin_registry.get_generator(kind)
        template_files = contribution.build_templates(config, context)
        created_files = [self._write_template(template_file) for template_file in template_files]

        if contribution.after_generate is not None:
            contribution.after_generate(self._file_system, config, context)

        return created_files

    def _write_template(self, template_file: TemplateFile) -> Path:
        content = self._renderer.render(template_file.template_name, template_file.context)
        return self._file_system.write_text(template_file.output_path, content)

    def _build_context(self, config: ProjectConfig, name: str) -> dict[str, object]:
        collection_name = pluralize(name) if not name.endswith("s") else name
        return {
            "project_name": config.project_name,
            "module_name": name,
            "class_name": pascal_case(name),
            "collection_name": collection_name,
            "route_name": kebab_case(collection_name),
            "config_options": config.options,
        }