from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from archforge.services.plugin_registry import PluginRegistry


class ArchforgePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def register(self, registry: PluginRegistry) -> None:
        raise NotImplementedError