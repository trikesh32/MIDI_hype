from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices.base import choice_param, int_param


def generate(params: dict[str, int]) -> list[list[int]]:
    midi_channel = params["midi_channel"] - 1
    mode = params["mode"]
    mode_byte = 0 if mode == 1 else 2
    messages = [[0xF0, 0x42, 0x30 + midi_channel, 0x63, 0x4E, mode_byte, 0xF7]]

    if mode == 1:
        bank = params["combi_bank"] - 1
        patch = params["patch"]
        messages.append([0xF0, 0x42, 0x63, 0xB0 + midi_channel, 0, 0, 0xB0 + midi_channel, 32, bank, 0xC0 + midi_channel, patch, 0xF7])
    else:
        bank_map = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            4: (0, 3),
            5: (0x79, 0),
            6: (0x78, 0),
        }
        first_byte, second_byte = bank_map[params["prog_bank"]]
        patch = params["patch"] - 1 if params["prog_bank"] in (5, 6) else params["patch"]
        messages.append([0xF0, 0x42, 0x63, 0xB0 + midi_channel, 0, first_byte, 0xB0 + midi_channel, 32, second_byte, 0xC0 + midi_channel, patch, 0xF7])

    arp_on = params["arp"] == 1
    messages.append([0xF0, 0x42, 0x63, 0xB0 + midi_channel, 0x63, 0, 0xB0 + midi_channel, 0x62, 0x2, 0xB0 + midi_channel, 6, 0x7F if arp_on else 0, 0xF7])
    if arp_on:
        messages.append([0xF0, 0x42, 0x63, 0xB0 + midi_channel, 0x63, 0, 0xB0 + midi_channel, 0x62, 0xA, 0xB0 + midi_channel, 6, params["arp_gate"], 0xF7])
        messages.append([0xF0, 0x42, 0x63, 0xB0 + midi_channel, 0x63, 0, 0xB0 + midi_channel, 0x62, 0xB, 0xB0 + midi_channel, 6, params["arp_velocity"], 0xF7])
    return messages


SPEC = DeviceSpec(
    key="tr",
    name="Korg TR",
    parameters=(
        int_param("midi_channel", "MIDI канал", 7, 1, 16),
        choice_param("mode", "Режим", 1, [("Combi", 1), ("Prog", 2)]),
        int_param("combi_bank", "Combi bank A/B/C", 1, 1, 3),
        int_param("prog_bank", "Prog bank A/B/C/D/GM/GM drum", 1, 1, 6),
        int_param("patch", "Номер патча", 0, 0, 128),
        choice_param("arp", "ARP", 0, [("Off", 0), ("On", 1)]),
        int_param("arp_gate", "ARP gate", 64, 0, 127),
        int_param("arp_velocity", "ARP velocity", 64, 0, 127),
    ),
    generator=generate,
)

