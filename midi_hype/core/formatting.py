from __future__ import annotations


def format_message(message: list[int] | tuple[int, ...]) -> str:
    return " ".join(f"{byte:02X}" for byte in message)


def format_dump(messages: list[list[int]] | tuple[tuple[int, ...], ...]) -> str:
    return "\n".join(format_message(message) for message in messages)

