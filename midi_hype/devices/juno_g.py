from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices.base import choice_param, int_param, with_checksum


PATCH_GROUPS = {
    0: (0x57, 0x00),
    1: (0x57, 0x40),
    2: (0x57, 0x41),
    3: (0x57, 0x42),
    4: (0x57, 0x43),
    5: (0x57, 0x44),
    6: (0x57, 0x45),
    7: (0x79, 0x00),
    8: (0x57, 0x20),
}


def _header(device_id: int) -> list[int]:
    return [0xF0, 0x41, device_id - 1, 0x00, 0x00, 0x15, 0x12]


def _msg(header: list[int], address: list[int], value: int) -> list[int]:
    return with_checksum(header, address[:-1] + [value])


def generate(params: dict[str, int]) -> list[list[int]]:
    header = _header(params["device_id"])
    mode = params["mode"]
    messages = [_msg(header, [1, 0, 0, 0, 0], mode)]

    if mode == 0:
        group = params["patch_group"]
        patch_number = params["patch_number"]
        msb, lsb = PATCH_GROUPS.get(group, (0x57, 0x00))
        if group in (0, 8) and patch_number > 128:
            lsb += 1
        if group == 9:
            msb = 93
            lsb = params["srx_board"] - 1
        messages.append(_msg(header, [1, 0, 0, 4, 0], msb))
        messages.append(_msg(header, [1, 0, 0, 5, 0], lsb))
        messages.append(_msg(header, [1, 0, 0, 6, 0], (patch_number - 1) % 128))
    else:
        bank_map = {0: 0, 1: 32, 2: 64}
        messages.append(_msg(header, [1, 0, 0, 1, 0], 85))
        messages.append(_msg(header, [1, 0, 0, 2, 0], bank_map[params["performance_group"]]))
        messages.append(_msg(header, [1, 0, 0, 3, 0], params["performance_number"] - 1))

    messages.append(_msg(header, [1, 0, 0, 0x13, 0], 64 + params["octave"]))
    return messages


SPEC = DeviceSpec(
    key="juno_g",
    name="Roland JUNO-G",
    parameters=(
        int_param("device_id", "Device ID", 20, 1, 32),
        choice_param("mode", "Режим", 0, [("Patch", 0), ("Performance", 1)]),
        choice_param("patch_group", "Patch group", 0, [("User", 0), ("PR-A", 1), ("PR-B", 2), ("PR-C", 3), ("PR-D", 4), ("PR-E", 5), ("PR-F", 6), ("GM", 7), ("Card", 8), ("SRX", 9)]),
        int_param("patch_number", "Номер патча", 1, 1, 256),
        int_param("srx_board", "Номер платы SRX", 1, 1, 12),
        choice_param("performance_group", "Performance group", 0, [("User", 0), ("Card", 1), ("PRST", 2)]),
        int_param("performance_number", "Номер перформанса", 1, 1, 64),
        int_param("octave", "Октава", 0, -3, 3),
    ),
    generator=generate,
)

