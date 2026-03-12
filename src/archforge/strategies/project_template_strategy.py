from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

from archforge.core.models.project_config import ProjectConfig
from archforge.core.models.template_file import TemplateFile

TemplatePathBuilder = Callable[..., TemplateFile]


class ProjectTemplateStrategy(ABC):
    @abstractmethod
    def build_context(self, config: ProjectConfig) -> dict[str, object]:
        raise NotImplementedError

    @abstractmethod
    def template_files(self, config: ProjectConfig) -> list[TemplateFile]:
        raise NotImplementedError


class BaseProjectTemplateStrategy(ProjectTemplateStrategy):
    template_name: str

    def build_context(self, config: ProjectConfig) -> dict[str, object]:
        return {"project_template": self.template_name}

    def template_files(self, config: ProjectConfig) -> list[TemplateFile]:
        root = config.service_root
        src_root = config.source_root

        def root_template(name: str, *parts: str) -> TemplateFile:
            return TemplateFile(name, root.joinpath(*parts))

        def src_template(name: str, *parts: str) -> TemplateFile:
            return TemplateFile(name, src_root.joinpath(*parts))

        return [
            root_template("project/shared/README.md.j2", "README.md"),
            root_template("project/shared/pyproject.toml.j2", "pyproject.toml"),
            root_template("project/shared/.env.example.j2", ".env.example"),
            root_template("project/shared/Dockerfile.j2", "Dockerfile"),
            root_template("project/shared/docker-compose.yml.j2", "docker-compose.yml"),
            root_template("project/shared/pytest.ini.j2", "pytest.ini"),
            src_template(
                "project/shared/src/infrastructure/observability/bootstrap.py.j2",
                "infrastructure",
                "observability",
                "bootstrap.py",
            ),
            src_template(
                "project/shared/src/infrastructure/observability/metrics.py.j2",
                "infrastructure",
                "observability",
                "metrics.py",
            ),
            src_template(
                "project/shared/src/infrastructure/observability/middleware.py.j2",
                "infrastructure",
                "observability",
                "middleware.py",
            ),
            src_template(
                "project/shared/src/infrastructure/observability/request_context.py.j2",
                "infrastructure",
                "observability",
                "request_context.py",
            ),
            src_template(
                "project/shared/src/infrastructure/observability/tracing.py.j2",
                "infrastructure",
                "observability",
                "tracing.py",
            ),
            src_template(
                "project/shared/src/presentation/api/metrics.py.j2",
                "presentation",
                "api",
                "metrics.py",
            ),
            src_template(
                "project/shared/src/presentation/api/readiness.py.j2",
                "presentation",
                "api",
                "readiness.py",
            ),
            root_template(
                "project/shared/tests/integration/test_readiness.py.j2",
                "tests",
                "integration",
                "test_readiness.py",
            ),
            *self._service_templates(src_template=src_template, root_template=root_template),
        ]

    @abstractmethod
    def _service_templates(
        self,
        src_template: TemplatePathBuilder,
        root_template: TemplatePathBuilder,
    ) -> list[TemplateFile]:
        raise NotImplementedError


class ApiServiceTemplateStrategy(BaseProjectTemplateStrategy):
    template_name = "api-service"

    def _service_templates(
        self,
        src_template: TemplatePathBuilder,
        root_template: TemplatePathBuilder,
    ) -> list[TemplateFile]:
        return [
            src_template("project/api_service/src/main.py.j2", "main.py"),
            src_template(
                "project/api_service/src/domain/entities/user.py.j2",
                "domain",
                "entities",
                "user.py",
            ),
            src_template(
                "project/api_service/src/domain/repositories/user_repository.py.j2",
                "domain",
                "repositories",
                "user_repository.py",
            ),
            src_template(
                "project/api_service/src/application/dto/user_dto.py.j2",
                "application",
                "dto",
                "user_dto.py",
            ),
            src_template(
                "project/api_service/src/application/interfaces/unit_of_work.py.j2",
                "application",
                "interfaces",
                "unit_of_work.py",
            ),
            src_template(
                "project/api_service/src/application/use_cases/get_user.py.j2",
                "application",
                "use_cases",
                "get_user.py",
            ),
            src_template(
                "project/api_service/src/infrastructure/config/settings.py.j2",
                "infrastructure",
                "config",
                "settings.py",
            ),
            src_template(
                "project/api_service/src/infrastructure/logging/logging_config.py.j2",
                "infrastructure",
                "logging",
                "logging_config.py",
            ),
            src_template(
                "project/api_service/src/infrastructure/persistence/unit_of_work.py.j2",
                "infrastructure",
                "persistence",
                "unit_of_work.py",
            ),
            src_template(
                "project/api_service/src/infrastructure/repositories/in_memory_user_repository.py.j2",
                "infrastructure",
                "repositories",
                "in_memory_user_repository.py",
            ),
            src_template(
                "project/api_service/src/presentation/api/router.py.j2",
                "presentation",
                "api",
                "router.py",
            ),
            src_template(
                "project/api_service/src/presentation/api/health.py.j2",
                "presentation",
                "api",
                "health.py",
            ),
            src_template(
                "project/api_service/src/presentation/api/users.py.j2",
                "presentation",
                "api",
                "users.py",
            ),
            src_template(
                "project/api_service/src/presentation/dependencies/providers.py.j2",
                "presentation",
                "dependencies",
                "providers.py",
            ),
            src_template(
                "project/api_service/src/presentation/schemas/user.py.j2",
                "presentation",
                "schemas",
                "user.py",
            ),
            root_template(
                "project/api_service/tests/unit/test_get_user.py.j2",
                "tests",
                "unit",
                "test_get_user.py",
            ),
            root_template(
                "project/api_service/tests/integration/test_health.py.j2",
                "tests",
                "integration",
                "test_health.py",
            ),
            root_template(
                "project/api_service/tests/e2e/test_user_endpoint.py.j2",
                "tests",
                "e2e",
                "test_user_endpoint.py",
            ),
        ]


class WorkerServiceTemplateStrategy(BaseProjectTemplateStrategy):
    template_name = "worker-service"

    def _service_templates(
        self,
        src_template: TemplatePathBuilder,
        root_template: TemplatePathBuilder,
    ) -> list[TemplateFile]:
        return [
            src_template("project/worker_service/src/main.py.j2", "main.py"),
            src_template(
                "project/worker_service/src/domain/entities/job.py.j2",
                "domain",
                "entities",
                "job.py",
            ),
            src_template(
                "project/worker_service/src/domain/repositories/job_repository.py.j2",
                "domain",
                "repositories",
                "job_repository.py",
            ),
            src_template(
                "project/worker_service/src/application/interfaces/unit_of_work.py.j2",
                "application",
                "interfaces",
                "unit_of_work.py",
            ),
            src_template(
                "project/worker_service/src/application/use_cases/run_job_batch.py.j2",
                "application",
                "use_cases",
                "run_job_batch.py",
            ),
            src_template(
                "project/worker_service/src/infrastructure/config/settings.py.j2",
                "infrastructure",
                "config",
                "settings.py",
            ),
            src_template(
                "project/worker_service/src/infrastructure/logging/logging_config.py.j2",
                "infrastructure",
                "logging",
                "logging_config.py",
            ),
            src_template(
                "project/worker_service/src/infrastructure/persistence/unit_of_work.py.j2",
                "infrastructure",
                "persistence",
                "unit_of_work.py",
            ),
            src_template(
                "project/worker_service/src/infrastructure/repositories/in_memory_job_repository.py.j2",
                "infrastructure",
                "repositories",
                "in_memory_job_repository.py",
            ),
            src_template(
                "project/worker_service/src/presentation/api/router.py.j2",
                "presentation",
                "api",
                "router.py",
            ),
            src_template(
                "project/worker_service/src/presentation/api/health.py.j2",
                "presentation",
                "api",
                "health.py",
            ),
            src_template(
                "project/worker_service/src/presentation/api/jobs.py.j2",
                "presentation",
                "api",
                "jobs.py",
            ),
            src_template(
                "project/worker_service/src/presentation/dependencies/providers.py.j2",
                "presentation",
                "dependencies",
                "providers.py",
            ),
            root_template(
                "project/worker_service/tests/unit/test_run_job_batch.py.j2",
                "tests",
                "unit",
                "test_run_job_batch.py",
            ),
            root_template(
                "project/worker_service/tests/integration/test_health.py.j2",
                "tests",
                "integration",
                "test_health.py",
            ),
            root_template(
                "project/worker_service/tests/e2e/test_run_jobs_endpoint.py.j2",
                "tests",
                "e2e",
                "test_run_jobs_endpoint.py",
            ),
        ]


class EventDrivenServiceTemplateStrategy(BaseProjectTemplateStrategy):
    template_name = "event-driven-service"

    def _service_templates(
        self,
        src_template: TemplatePathBuilder,
        root_template: TemplatePathBuilder,
    ) -> list[TemplateFile]:
        return [
            src_template("project/event_driven_service/src/main.py.j2", "main.py"),
            src_template(
                "project/event_driven_service/src/domain/entities/order_created.py.j2",
                "domain",
                "entities",
                "order_created.py",
            ),
            src_template(
                "project/event_driven_service/src/domain/repositories/event_repository.py.j2",
                "domain",
                "repositories",
                "event_repository.py",
            ),
            src_template(
                "project/event_driven_service/src/application/interfaces/unit_of_work.py.j2",
                "application",
                "interfaces",
                "unit_of_work.py",
            ),
            src_template(
                "project/event_driven_service/src/application/use_cases/process_order_created.py.j2",
                "application",
                "use_cases",
                "process_order_created.py",
            ),
            src_template(
                "project/event_driven_service/src/infrastructure/config/settings.py.j2",
                "infrastructure",
                "config",
                "settings.py",
            ),
            src_template(
                "project/event_driven_service/src/infrastructure/logging/logging_config.py.j2",
                "infrastructure",
                "logging",
                "logging_config.py",
            ),
            src_template(
                "project/event_driven_service/src/infrastructure/persistence/unit_of_work.py.j2",
                "infrastructure",
                "persistence",
                "unit_of_work.py",
            ),
            src_template(
                "project/event_driven_service/src/infrastructure/repositories/in_memory_event_repository.py.j2",
                "infrastructure",
                "repositories",
                "in_memory_event_repository.py",
            ),
            src_template(
                "project/event_driven_service/src/presentation/api/router.py.j2",
                "presentation",
                "api",
                "router.py",
            ),
            src_template(
                "project/event_driven_service/src/presentation/api/health.py.j2",
                "presentation",
                "api",
                "health.py",
            ),
            src_template(
                "project/event_driven_service/src/presentation/api/events.py.j2",
                "presentation",
                "api",
                "events.py",
            ),
            src_template(
                "project/event_driven_service/src/presentation/dependencies/providers.py.j2",
                "presentation",
                "dependencies",
                "providers.py",
            ),
            src_template(
                "project/event_driven_service/src/presentation/schemas/order_created.py.j2",
                "presentation",
                "schemas",
                "order_created.py",
            ),
            root_template(
                "project/event_driven_service/tests/unit/test_process_order_created.py.j2",
                "tests",
                "unit",
                "test_process_order_created.py",
            ),
            root_template(
                "project/event_driven_service/tests/integration/test_health.py.j2",
                "tests",
                "integration",
                "test_health.py",
            ),
            root_template(
                "project/event_driven_service/tests/e2e/test_order_created_event.py.j2",
                "tests",
                "e2e",
                "test_order_created_event.py",
            ),
        ]