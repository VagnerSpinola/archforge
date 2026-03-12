from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

from archforge.core.models.project_config import ProjectConfig

ArtifactT = TypeVar("ArtifactT")


class BaseGenerator[ArtifactT](ABC):
    def generate(self, config: ProjectConfig) -> Path:
        self.validate(config)
        project_root = self.prepare(config)
        artifacts = self.collect_artifacts(config)
        self.persist(artifacts)
        self.finalize(config)
        return project_root

    @abstractmethod
    def validate(self, config: ProjectConfig) -> None:
        raise NotImplementedError

    @abstractmethod
    def prepare(self, config: ProjectConfig) -> Path:
        raise NotImplementedError

    @abstractmethod
    def collect_artifacts(self, config: ProjectConfig) -> list[ArtifactT]:
        raise NotImplementedError

    @abstractmethod
    def persist(self, artifacts: list[ArtifactT]) -> None:
        raise NotImplementedError

    def finalize(self, config: ProjectConfig) -> None:
        return None