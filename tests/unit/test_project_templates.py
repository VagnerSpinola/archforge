from pathlib import Path

from archforge.core.models.project_config import ProjectConfig
from archforge.services.plugin_loader import load_plugin_registry


def test_plugin_registry_creates_api_project_template(tmp_path: Path) -> None:
    registry = load_plugin_registry(plugin_directories=[])
    config = ProjectConfig(project_name="billing-service", destination_root=tmp_path)

    strategy = registry.create_project_template(config.project_template)
    template_files = strategy.template_files(config)

    assert any(template.output_path.name == "users.py" for template in template_files)


def test_plugin_registry_creates_worker_project_template(tmp_path: Path) -> None:
    registry = load_plugin_registry(plugin_directories=[])

    strategy = registry.create_project_template("worker-service")
    template_files = strategy.template_files(
        ProjectConfig(
            project_name="job-runner",
            destination_root=tmp_path,
            project_template="worker-service",
        )
    )

    assert any(template.output_path.name == "jobs.py" for template in template_files)


def test_plugin_registry_creates_event_driven_project_template(tmp_path: Path) -> None:
    registry = load_plugin_registry(plugin_directories=[])

    strategy = registry.create_project_template("event-driven-service")
    template_files = strategy.template_files(
        ProjectConfig(
            project_name="order-events",
            destination_root=tmp_path,
            project_template="event-driven-service",
        )
    )

    assert any(template.output_path.name == "events.py" for template in template_files)