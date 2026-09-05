from __future__ import annotations

from pathlib import Path

from midi_hype.core.models import DeviceConfig, DumpResult
from midi_hype.devices.registry import DEVICE_REGISTRY


class DumpSession:
    def __init__(self) -> None:
        self._configs: list[DeviceConfig] = []

    @property
    def configs(self) -> tuple[DeviceConfig, ...]:
        return tuple(self._configs)

    def add_config(self, config: DeviceConfig) -> None:
        self._configs.append(config)

    def remove_config(self, index: int) -> None:
        del self._configs[index]

    def move_config(self, index: int, direction: int) -> None:
        new_index = index + direction
        if not 0 <= new_index < len(self._configs):
            return
        self._configs[index], self._configs[new_index] = self._configs[new_index], self._configs[index]

    def clear(self) -> None:
        self._configs.clear()

    def build(self) -> DumpResult:
        messages: list[tuple[int, ...]] = []
        for config in self._configs:
            spec = DEVICE_REGISTRY[config.device_key]
            for message in spec.generator(config.parameters):
                messages.append(tuple(message))
        return DumpResult(configs=self.configs, messages=tuple(messages))


def write_dump(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")

