from pathlib import Path

from archforge.core.models.project_config import ProjectConfig
from archforge.factories.framework_factory import FrameworkFactory
from archforge.services.plugin_loader import load_plugin_registry
from archforge.strategies.database_strategy import InMemoryDatabaseStrategy
from archforge.strategies.framework_strategy import FastAPIFrameworkStrategy


def test_framework_factory_returns_fastapi_strategy(tmp_path: Path) -> None:
    factory = FrameworkFactory(plugin_registry=load_plugin_registry(plugin_directories=[]))
    config = ProjectConfig(project_name="orders-service", destination_root=tmp_path)

    strategy = factory.create_framework_strategy(config)

    assert isinstance(strategy, FastAPIFrameworkStrategy)


def test_framework_factory_returns_in_memory_database_strategy(tmp_path: Path) -> None:
    factory = FrameworkFactory(plugin_registry=load_plugin_registry(plugin_directories=[]))
    config = ProjectConfig(project_name="orders-service", destination_root=tmp_path)

    strategy = factory.create_database_strategy(config)

    assert isinstance(strategy, InMemoryDatabaseStrategy)