from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from archforge.core.constants.layout import REQUIRED_PROJECT_MARKERS
from archforge.core.exceptions import InvalidProjectError
from archforge.utils.naming import slug_to_snake_case


class ProjectConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    project_name: str = Field(min_length=1)
    destination_root: Path
    project_template: str = "api-service"
    framework: str = "fastapi"
    database: str = "in_memory"
    options: dict[str, str] = Field(default_factory=dict)

    @property
    def service_slug(self) -> str:
        return slug_to_snake_case(self.project_name)

    @property
    def service_root(self) -> Path:
        return self.destination_root / self.project_name

    @property
    def source_root(self) -> Path:
        return self.service_root / "src"

    @classmethod
    def from_existing_project(cls, project_root: Path) -> ProjectConfig:
        missing_markers = [
            marker for marker in REQUIRED_PROJECT_MARKERS if not (project_root / marker).exists()
        ]
        if missing_markers:
            formatted_markers = ", ".join(str(marker) for marker in missing_markers)
            raise InvalidProjectError(
                f"{project_root} is not a supported ArchForge project. "
                f"Missing: {formatted_markers}."
            )

        return cls(project_name=project_root.name, destination_root=project_root.parent)