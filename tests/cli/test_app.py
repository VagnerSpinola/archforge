from pathlib import Path

import typer
from typer.testing import CliRunner

from archforge.cli.app import app, create_app
from archforge.core.models.plugin import PluginConfigOption
from archforge.services.plugin_loader import load_plugin_registry
from archforge.services.plugin_registry import PluginRegistry

runner = CliRunner()


def test_new_command_generates_service_layout(tmp_path: Path) -> None:
    result = runner.invoke(app, ["new", "billing-service", "--destination", str(tmp_path)])

    assert result.exit_code == 0
    project_root = tmp_path / "billing-service"
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "src" / "main.py").exists()
    assert (project_root / "src" / "domain" / "entities" / "user.py").exists()
    assert (project_root / "src" / "presentation" / "api" / "users.py").exists()


def test_new_command_supports_worker_service_template(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "new",
            "job-runner",
            "--destination",
            str(tmp_path),
            "--template",
            "worker-service",
        ],
    )

    assert result.exit_code == 0
    project_root = tmp_path / "job-runner"
    assert (project_root / "src" / "domain" / "entities" / "job.py").exists()
    assert (project_root / "src" / "presentation" / "api" / "jobs.py").exists()


def test_new_command_supports_event_driven_service_template(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "new",
            "order-events",
            "--destination",
            str(tmp_path),
            "--template",
            "event-driven-service",
        ],
    )

    assert result.exit_code == 0
    project_root = tmp_path / "order-events"
    assert (project_root / "src" / "domain" / "entities" / "order_created.py").exists()
    assert (project_root / "src" / "presentation" / "api" / "events.py").exists()


def test_add_endpoint_command_creates_endpoint_files(tmp_path: Path) -> None:
    runner.invoke(app, ["new", "billing-service", "--destination", str(tmp_path)])
    project_root = tmp_path / "billing-service"

    result = runner.invoke(
        app,
        ["add", "endpoint", "invoices", "--project-root", str(project_root)],
    )

    assert result.exit_code == 0
    assert (project_root / "src" / "presentation" / "api" / "invoices.py").exists()
    assert (project_root / "src" / "presentation" / "schemas" / "invoices.py").exists()


def test_plugin_cli_commands_are_registered() -> None:
    registry = load_plugin_registry(plugin_directories=[])

    def register_plugin_command(
        main_app: typer.Typer,
        _add_app: typer.Typer,
        current_registry: PluginRegistry,
    ) -> None:
        @main_app.command("plugins")
        def plugins() -> None:
            typer.echo(",".join(current_registry.plugin_names))

    registry.register_cli_command(register_plugin_command)
    plugin_app = create_app(registry)

    result = runner.invoke(plugin_app, ["plugins"])

    assert result.exit_code == 0
    assert result.output.strip() == "core"


def test_new_command_accepts_registered_plugin_options(tmp_path: Path) -> None:
    registry = load_plugin_registry(plugin_directories=[])
    registry.register_config_option(
        PluginConfigOption(
            name="region",
            description="Deployment region.",
            default="us-east-1",
        )
    )
    plugin_app = create_app(registry)

    result = runner.invoke(
        plugin_app,
        [
            "new",
            "billing-service",
            "--destination",
            str(tmp_path),
            "--option",
            "region=eu-west-1",
        ],
    )

    assert result.exit_code == 0
    assert (tmp_path / "billing-service" / "pyproject.toml").exists()