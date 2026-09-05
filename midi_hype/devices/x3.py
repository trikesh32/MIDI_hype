from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices.base import choice_param, int_param


def generate(params: dict[str, int]) -> list[list[int]]:
    midi_channel = params["midi_channel"] - 1
    mode = params["mode"]
    messages = [[0xF0, 0x42, 0x30 + midi_channel, 0x35, 0x4E, 0 if mode == 1 else 2, 0, 0xF7]]

    if mode == 1:
        bank = params["combi_bank"] - 1
        patch = params["patch"]
        messages.append([0xF0, 0x42, 0x30 + midi_channel, 0xB0 + midi_channel, 0, 0, 0xB0 + midi_channel, 32, bank, 0xC0 + midi_channel, patch, 0xF7])
        return messages

    bank_map = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (0, 3),
        5: (0x38, 0),
        6: (0x3E, 0),
    }
    first_byte, second_byte = bank_map[params["prog_bank"]]
    patch = params["patch"]
    if params["prog_bank"] == 5:
        patch -= 1
    elif params["prog_bank"] == 6:
        patch = {129: 0, 130: 16, 131: 25, 132: 32, 133: 40, 134: 64, 135: 24, 136: 48}.get(patch, patch)
    messages.append([0xF0, 0x42, 0x30 + midi_channel, 0xB0 + midi_channel, 0, first_byte, 0xB0 + midi_channel, 32, second_byte, 0xC0 + midi_channel, patch, 0xF7])
    return messages


SPEC = DeviceSpec(
    key="x3",
    name="Korg X3",
    parameters=(
        int_param("midi_channel", "MIDI канал", 1, 1, 16),
        choice_param("mode", "Режим", 1, [("Combi", 1), ("Prog", 2)]),
        int_param("combi_bank", "Combi bank A/B", 1, 1, 2),
        int_param("prog_bank", "Prog bank A/B/C/D/GM/GM drum", 1, 1, 6),
        int_param("patch", "Номер патча", 0, 0, 136),
    ),
    generator=generate,
)

