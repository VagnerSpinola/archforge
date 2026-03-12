from pathlib import Path

import pytest

from archforge.core.exceptions import FileConflictError
from archforge.services.filesystem_service import FileSystemService


def test_write_text_creates_parent_directories(tmp_path: Path) -> None:
    file_system = FileSystemService()

    target = file_system.write_text(tmp_path / "nested" / "file.txt", "content")

    assert target.exists()
    assert target.read_text(encoding="utf-8") == "content"


def test_write_text_raises_on_conflict(tmp_path: Path) -> None:
    file_system = FileSystemService()
    target = tmp_path / "file.txt"
    target.write_text("existing", encoding="utf-8")

    with pytest.raises(FileConflictError):
        file_system.write_text(target, "new")