from __future__ import annotations

from midi_hype.core.models import DeviceSpec
from midi_hype.devices import boss_ve500, juno_g, tr, vk7, x3, xp60


DEVICES: tuple[DeviceSpec, ...] = (
    juno_g.SPEC,
    xp60.SPEC,
    vk7.SPEC,
    tr.SPEC,
    x3.SPEC,
    boss_ve500.SPEC,
)

DEVICE_REGISTRY: dict[str, DeviceSpec] = {device.key: device for device in DEVICES}

