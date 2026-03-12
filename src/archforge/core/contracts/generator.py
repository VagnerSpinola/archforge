from __future__ import annotations

from pathlib import Path
from typing import Protocol

from archforge.core.models.project_config import ProjectConfig


class GeneratesFiles(Protocol):
    def generate(self, config: ProjectConfig) -> Path:
        ...