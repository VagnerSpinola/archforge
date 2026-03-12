from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType

from archforge.core.contracts.plugin import ArchforgePlugin
from archforge.core.exceptions import PluginError
from archforge.plugins.core_plugin import CorePlugin
from archforge.services.plugin_registry import PluginRegistry


class PluginLoader:
    def __init__(self, plugin_directories: list[Path] | None = None) -> None:
        self._plugin_directories = plugin_directories or self._default_plugin_directories()

    def load_into(self, registry: PluginRegistry) -> None:
        for plugin_path in self._discover_plugin_files():
            plugin = self._load_plugin(plugin_path)
            registry.register_plugin(plugin.name)
            plugin.register(registry)

    def _discover_plugin_files(self) -> list[Path]:
        plugin_files: list[Path] = []
        for directory in self._plugin_directories:
            if not directory.exists():
                continue
            plugin_files.extend(
                path for path in sorted(directory.glob("*.py")) if path.name != "__init__.py"
            )
        return plugin_files

    def _load_plugin(self, plugin_path: Path) -> ArchforgePlugin:
        module_name = f"archforge_external_plugin_{plugin_path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_path)
        if spec is None or spec.loader is None:
            raise PluginError(f"Unable to create import spec for plugin: {plugin_path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return self._resolve_plugin(module=module, plugin_path=plugin_path)

    def _resolve_plugin(self, module: ModuleType, plugin_path: Path) -> ArchforgePlugin:
        if hasattr(module, "plugin") and isinstance(module.plugin, ArchforgePlugin):
            return module.plugin
        if hasattr(module, "get_plugin"):
            plugin = module.get_plugin()
            if isinstance(plugin, ArchforgePlugin):
                return plugin
        raise PluginError(
            "Plugin module "
            f"'{plugin_path}' must expose 'plugin' or 'get_plugin()' returning an "
            "ArchforgePlugin."
        )

    def _default_plugin_directories(self) -> list[Path]:
        directories = [Path.cwd() / "plugins", Path(__file__).resolve().parents[3] / "plugins"]
        environment_value = os.getenv("ARCHFORGE_PLUGIN_DIRS")
        if environment_value:
            directories.extend(Path(path) for path in environment_value.split(os.pathsep) if path)
        return directories


def load_plugin_registry(plugin_directories: list[Path] | None = None) -> PluginRegistry:
    registry = PluginRegistry()
    core_plugin = CorePlugin()
    registry.register_plugin(core_plugin.name)
    core_plugin.register(registry)
    PluginLoader(plugin_directories=plugin_directories).load_into(registry)
    return registry