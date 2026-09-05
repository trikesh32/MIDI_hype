from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices.base import int_param


def generate(params: dict[str, int]) -> list[list[int]]:
    midi_channel = params["midi_channel"] - 1
    bank = params["bank"]
    patch = params["patch"]
    return [[0xC0 + midi_channel, (bank - 1) * 8 + patch - 1]]


SPEC = DeviceSpec(
    key="vk7",
    name="VK7",
    parameters=(
        int_param("midi_channel", "MIDI канал", 6, 1, 16),
        int_param("bank", "Банк", 1, 1, 8),
        int_param("patch", "Патч", 1, 1, 8),
    ),
    generator=generate,
)

