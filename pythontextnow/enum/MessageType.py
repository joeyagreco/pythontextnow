from __future__ import annotations

from enum import Enum, unique


@unique
class MessageType(Enum):
    TEXT = 1
    IMAGE = 2
    VIDEO = 4
    UNKNOWN_MEDIA = 6  # TODO: Figure out what this represents

    @classmethod
    def from_value(cls, v: str | int) -> MessageType:
        if v == "1" or v == 1:
            return MessageType.TEXT
        if v == "2" or v == 2:
            return MessageType.IMAGE
        if v == "4" or v == 4:
            return MessageType.VIDEO
        if v == "6" or v == 6:
            return MessageType.UNKNOWN_MEDIA
        else:
            raise ValueError(f"Value '{v}' is unknown for MessageType.")
