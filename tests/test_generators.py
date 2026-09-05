from midi_hype.core.formatting import format_dump, format_message
from midi_hype.devices.base import roland_checksum
from midi_hype.devices.boss_ve500 import generate as generate_boss_ve500
from midi_hype.devices.vk7 import generate as generate_vk7
from midi_hype.devices.xp60 import generate as generate_xp60


def test_format_message() -> None:
    assert format_message([0, 15, 16, 255]) == "00 0F 10 FF"


def test_format_dump() -> None:
    assert format_dump([[0xC0, 0x01], [0xF0, 0xF7]]) == "C0 01\nF0 F7"


def test_roland_checksum() -> None:
    assert roland_checksum([1, 0, 0, 0, 1]) == 126


def test_boss_ve500_factory_program() -> None:
    assert generate_boss_ve500({"midi_channel": 13, "bank": 1, "program": 1}) == [
        [0xBC, 0, 1, 0xBC, 0x20, 0, 0xCC, 0]
    ]


def test_vk7_program_number() -> None:
    assert generate_vk7({"midi_channel": 6, "bank": 2, "patch": 3}) == [[0xC5, 10]]


def test_xp60_patch_messages_have_sysex_boundaries() -> None:
    messages = generate_xp60(
        {
            "device_id": 18,
            "mode": 1,
            "perform_bank": 0,
            "perform_number": 1,
            "patch_type": 0,
            "patch_group": 1,
            "patch_number": 1,
            "octave": 0,
        }
    )
    assert len(messages) == 5
    assert all(message[0] == 0xF0 and message[-1] == 0xF7 for message in messages)

