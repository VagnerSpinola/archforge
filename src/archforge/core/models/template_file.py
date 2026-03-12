from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TemplateFile:
    template_name: str
    output_path: Path
    context: dict[str, object] = field(default_factory=dict)