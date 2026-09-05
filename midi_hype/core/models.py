from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Literal


FieldType = Literal["int", "choice"]


@dataclass(frozen=True)
class ChoiceOption:
    label: str
    value: int


@dataclass(frozen=True)
class ParameterSpec:
    key: str
    label: str
    field_type: FieldType
    default: int
    minimum: int | None = None
    maximum: int | None = None
    options: tuple[ChoiceOption, ...] = ()


@dataclass(frozen=True)
class DeviceSpec:
    key: str
    name: str
    parameters: tuple[ParameterSpec, ...]
    generator: Callable[[dict[str, int]], list[list[int]]]


@dataclass(frozen=True)
class DeviceConfig:
    device_key: str
    label: str
    parameters: dict[str, int]


@dataclass(frozen=True)
class DumpResult:
    configs: tuple[DeviceConfig, ...]
    messages: tuple[tuple[int, ...], ...]


def flatten_messages(message_groups: Iterable[Iterable[Iterable[int]]]) -> list[list[int]]:
    messages: list[list[int]] = []
    for group in message_groups:
        for message in group:
            messages.append(list(message))
    return messages

