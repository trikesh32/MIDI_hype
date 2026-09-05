from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices.base import choice_param, int_param


def generate(params: dict[str, int]) -> list[list[int]]:
    midi_channel = params["midi_channel"] - 1
    bank_mode = 1 if params["bank"] == 1 else 0
    program = params["program"] - 1
    return [[0xB0 + midi_channel, 0, bank_mode, 0xB0 + midi_channel, 0x20, 0, 0xC0 + midi_channel, program]]


SPEC = DeviceSpec(
    key="boss_ve500",
    name="BOSS VE-500",
    parameters=(
        int_param("midi_channel", "MIDI канал", 13, 1, 16),
        choice_param("bank", "Банк", 1, [("Factory patches", 1), ("User patches", 2)]),
        int_param("program", "Номер программы", 1, 1, 99),
    ),
    generator=generate,
)

