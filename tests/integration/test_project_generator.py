from pathlib import Path

from archforge.builders.project_builder import ProjectBuilder
from archforge.core.models.project_config import ProjectConfig
from archforge.factories.framework_factory import FrameworkFactory
from archforge.generators.file_generator import FileGenerator
from archforge.generators.project_generator import ProjectGenerator
from archforge.services.filesystem_service import FileSystemService
from archforge.services.plugin_loader import load_plugin_registry
from archforge.services.template_renderer import TemplateRenderer
from archforge.services.validation_service import ValidationService


def test_project_generator_creates_expected_directories(tmp_path: Path) -> None:
    plugin_registry = load_plugin_registry(plugin_directories=[])
    file_system = FileSystemService()
    validation = ValidationService(file_system=file_system)
    generator = ProjectGenerator(
        builder=ProjectBuilder(framework_factory=FrameworkFactory(plugin_registry=plugin_registry)),
        file_generator=FileGenerator(
            renderer=TemplateRenderer(template_directories=plugin_registry.template_directories),
            file_system=file_system,
        ),
        file_system=file_system,
        validation=validation,
    )

    project_root = generator.generate(
        ProjectConfig(project_name="payment-service", destination_root=tmp_path)
    )

    assert (project_root / "src" / "domain").exists()
    assert (project_root / "src" / "application").exists()
    assert (project_root / "src" / "infrastructure").exists()
    assert (project_root / "src" / "presentation").exists()
    assert (project_root / "tests" / "e2e").exists()
    assert (project_root / "src" / "infrastructure" / "observability" / "bootstrap.py").exists()
    assert (project_root / "src" / "presentation" / "api" / "readiness.py").exists()

    settings_file = project_root / "src" / "infrastructure" / "config" / "settings.py"
    assert "request_id_enabled" in settings_file.read_text(encoding="utf-8")

    main_file = project_root / "src" / "main.py"
    assert "configure_observability" in main_file.read_text(encoding="utf-8")


def test_project_generator_creates_worker_service_files(tmp_path: Path) -> None:
    plugin_registry = load_plugin_registry(plugin_directories=[])
    file_system = FileSystemService()
    validation = ValidationService(file_system=file_system)
    generator = ProjectGenerator(
        builder=ProjectBuilder(framework_factory=FrameworkFactory(plugin_registry=plugin_registry)),
        file_generator=FileGenerator(
            renderer=TemplateRenderer(template_directories=plugin_registry.template_directories),
            file_system=file_system,
        ),
        file_system=file_system,
        validation=validation,
    )

    project_root = generator.generate(
        ProjectConfig(
            project_name="job-runner",
            destination_root=tmp_path,
            project_template="worker-service",
        )
    )

    jobs_endpoint = project_root / "src" / "presentation" / "api" / "jobs.py"
    assert jobs_endpoint.exists()
    assert "processed_jobs" in jobs_endpoint.read_text(encoding="utf-8")
    assert (project_root / "src" / "presentation" / "api" / "metrics.py").exists()


def test_project_generator_creates_event_driven_service_files(tmp_path: Path) -> None:
    plugin_registry = load_plugin_registry(plugin_directories=[])
    file_system = FileSystemService()
    validation = ValidationService(file_system=file_system)
    generator = ProjectGenerator(
        builder=ProjectBuilder(framework_factory=FrameworkFactory(plugin_registry=plugin_registry)),
        file_generator=FileGenerator(
            renderer=TemplateRenderer(template_directories=plugin_registry.template_directories),
            file_system=file_system,
        ),
        file_system=file_system,
        validation=validation,
    )

    project_root = generator.generate(
        ProjectConfig(
            project_name="order-events",
            destination_root=tmp_path,
            project_template="event-driven-service",
        )
    )

    events_endpoint = project_root / "src" / "presentation" / "api" / "events.py"
    assert events_endpoint.exists()
    assert "order-created" in events_endpoint.read_text(encoding="utf-8")
    observability_readme = project_root / "README.md"
    assert "OBSERVABILITY" in observability_readme.read_text(encoding="utf-8").upper()