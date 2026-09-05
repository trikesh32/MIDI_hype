from __future__ import annotations

from midi_hype.core.models import ChoiceOption, ParameterSpec


def int_param(key: str, label: str, default: int, minimum: int, maximum: int) -> ParameterSpec:
    return ParameterSpec(key=key, label=label, field_type="int", default=default, minimum=minimum, maximum=maximum)


def choice_param(key: str, label: str, default: int, choices: list[tuple[str, int]]) -> ParameterSpec:
    return ParameterSpec(
        key=key,
        label=label,
        field_type="choice",
        default=default,
        options=tuple(ChoiceOption(label=label, value=value) for label, value in choices),
    )


def roland_checksum(message: list[int]) -> int:
    return (128 - (sum(message) % 128)) % 128


def with_checksum(header: list[int], payload: list[int]) -> list[int]:
    return header + payload + [roland_checksum(payload), 0xF7]

