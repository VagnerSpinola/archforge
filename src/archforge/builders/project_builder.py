from __future__ import annotations

from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile
from archforge.factories.framework_factory import FrameworkFactory


class ProjectBuilder:
    def __init__(self, framework_factory: FrameworkFactory) -> None:
        self._framework_factory = framework_factory

    def build(self, config: ProjectConfig) -> list[TemplateFile]:
        project_template = self._framework_factory.create_project_template_strategy(config)
        framework_strategy = self._framework_factory.create_framework_strategy(config)
        database_strategy = self._framework_factory.create_database_strategy(config)
        context = project_template.build_context(config)
        context.update(framework_strategy.build_context(config))
        context.update(database_strategy.build_context(config))
        context["config_options"] = config.options

        template_files = project_template.template_files(config)
        template_files.extend(framework_strategy.template_files(config))
        template_files.extend(database_strategy.template_files(config))

        return [
            TemplateFile(
                template_name=template_file.template_name,
                output_path=template_file.output_path,
                context={**context, **template_file.context},
            )
            for template_file in template_files
        ]