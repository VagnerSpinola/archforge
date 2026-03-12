from __future__ import annotations

from pathlib import Path

from archforge.services.plugin_loader import load_plugin_registry


def test_plugin_loader_registers_external_plugin_contributions(tmp_path: Path) -> None:
    template_directory = tmp_path / "templates"
    template_directory.mkdir()
    plugin_templates = template_directory / "plugin"
    plugin_templates.mkdir()
    (plugin_templates / "job.py.j2").write_text("job={{ module_name }}\n", encoding="utf-8")

    plugin_directory = tmp_path / "plugins"
    plugin_directory.mkdir()
    plugin_file = plugin_directory / "demo_plugin.py"
    plugin_file.write_text(
        f'''
from pathlib import Path

from archforge.core.contracts.plugin import ArchforgePlugin
from archforge.core.models.plugin import GeneratorContribution, PluginConfigOption
from archforge.core.models.template_file import TemplateFile
from archforge.services.plugin_registry import PluginRegistry


class DemoPlugin(ArchforgePlugin):
    @property
    def name(self) -> str:
        return "demo"

    def register(self, registry: PluginRegistry) -> None:
        registry.register_template_directory(Path(r"{template_directory}"))
        registry.register_config_option(
            PluginConfigOption(name="region", description="Deployment region.", default="us")
        )
        registry.register_generator(
            GeneratorContribution(kind="job", build_templates=self._build_templates)
        )

    def _build_templates(self, config, context):
        return [
            TemplateFile(
                "plugin/job.py.j2",
                config.source_root / "application" / "jobs" / f"{{context['module_name']}}.py",
                context,
            )
        ]


plugin = DemoPlugin()
'''.strip(),
        encoding="utf-8",
    )

    registry = load_plugin_registry(plugin_directories=[plugin_directory])

    assert registry.plugin_names == ("core", "demo")
    assert template_directory.resolve() in registry.template_directories
    assert registry.get_generator("job").kind == "job"
    assert registry.default_option_values()["region"] == "us"