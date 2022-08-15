from __future__ import annotations

from enum import Enum, unique


@unique
class MessageType(Enum):
    MULTIMEDIA = 2
    TEXT = 1

    @classmethod
    def from_value(cls, v: str | int) -> MessageType:
        if v == "1" or v == 1:
            return MessageType.TEXT
        if v == "2" or v == 2:
            return MessageType.MULTIMEDIA
        else:
            raise ValueError(f"Value '{v}' is unknown for MessageType.")
