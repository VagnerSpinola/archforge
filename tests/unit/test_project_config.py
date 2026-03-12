from pathlib import Path

import pytest

from archforge.core.exceptions import InvalidProjectError
from archforge.core.models.project_config import ProjectConfig


def test_project_config_builds_service_paths(tmp_path: Path) -> None:
    config = ProjectConfig(project_name="billing-service", destination_root=tmp_path)

    assert config.service_slug == "billing_service"
    assert config.service_root == tmp_path / "billing-service"


def test_project_config_requires_existing_project_markers(tmp_path: Path) -> None:
    with pytest.raises(InvalidProjectError):
        ProjectConfig.from_existing_project(tmp_path)