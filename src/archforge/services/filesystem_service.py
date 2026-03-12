from __future__ import annotations

from pathlib import Path

from archforge.core.exceptions import FileConflictError


class FileSystemService:
    def create_directory(self, directory: Path) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def create_project_root(self, project_root: Path) -> Path:
        if project_root.exists():
            raise FileConflictError(f"Destination already exists: {project_root}")

        project_root.mkdir(parents=True, exist_ok=False)
        return project_root

    def write_text(self, file_path: Path, content: str, *, overwrite: bool = False) -> Path:
        if file_path.exists() and not overwrite:
            raise FileConflictError(f"Refusing to overwrite existing file: {file_path}")

        self.create_directory(file_path.parent)
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def append_unique_block(self, file_path: Path, block: str) -> Path:
        if not file_path.exists():
            raise FileNotFoundError(file_path)

        current = file_path.read_text(encoding="utf-8")
        if block in current:
            return file_path

        separator = "" if current.endswith("\n") else "\n"
        file_path.write_text(f"{current}{separator}{block}\n", encoding="utf-8")
        return file_path