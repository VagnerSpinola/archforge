from __future__ import annotations

import re


def slug_to_snake_case(value: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    collapsed = sanitized.replace("-", "_")
    return re.sub(r"_+", "_", collapsed).strip("_").lower()


def pascal_case(value: str) -> str:
    parts = re.split(r"[_\-\s]+", value.strip())
    return "".join(part.capitalize() for part in parts if part)


def pluralize(value: str) -> str:
    if value.endswith("y") and not value.endswith(("ay", "ey", "iy", "oy", "uy")):
        return f"{value[:-1]}ies"
    if value.endswith("s"):
        return f"{value}es"
    return f"{value}s"


def kebab_case(value: str) -> str:
    return slug_to_snake_case(value).replace("_", "-")