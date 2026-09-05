from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices.base import choice_param, int_param, with_checksum


def _header(device_id: int) -> list[int]:
    return [0xF0, 0x41, device_id - 1, 0x6A, 0x12]


def generate(params: dict[str, int]) -> list[list[int]]:
    header = _header(params["device_id"])
    mode = params["mode"]
    messages = [with_checksum(header, [0, 0, 0, 0, mode])]

    if mode == 0:
        bank = params["perform_bank"]
        number = params["perform_number"]
        base = {0: 0, 1: 64, 2: 96, 3: 32}[bank]
        messages.append(with_checksum(header, [0, 0, 0, 1, base + number - 1]))
    elif mode == 1:
        patch_number = params["patch_number"] - 1
        messages.append(with_checksum(header, [0, 0, 0, 2, params["patch_type"]]))
        messages.append(with_checksum(header, [0, 0, 0, 3, params["patch_group"]]))
        messages.append(with_checksum(header, [0, 0, 0, 4, patch_number // 16, patch_number % 16]))

    messages.append(with_checksum(header, [0, 0, 0, 0x2D, params["octave"] + 3]))
    return messages


SPEC = DeviceSpec(
    key="xp60",
    name="Roland XP-60",
    parameters=(
        int_param("device_id", "Device ID", 18, 1, 32),
        choice_param("mode", "Режим", 0, [("Performance", 0), ("Patch", 1), ("GM", 2)]),
        choice_param("perform_bank", "Performance bank", 0, [("User", 0), ("PR-A", 1), ("PR-B", 2), ("Card", 3)]),
        int_param("perform_number", "Номер перформанса", 1, 1, 32),
        choice_param("patch_type", "Patch type", 0, [("User/Preset", 0), ("PCM", 1), ("EXP", 2)]),
        int_param("patch_group", "Patch group id", 1, 1, 6),
        int_param("patch_number", "Номер патча", 1, 1, 128),
        int_param("octave", "Октава", 0, -3, 3),
    ),
    generator=generate,
)

