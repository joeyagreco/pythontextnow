from __future__ import annotations

from enum import Enum, unique


@unique
class MessageDirection(Enum):
    INCOMING = 2
    OUTGOING = 1

    @classmethod
    def from_value(cls, v: str | int) -> MessageDirection:
        if v == "1" or v == 1:
            return MessageDirection.OUTGOING
        if v == "2" or v == 2:
            return MessageDirection.INCOMING
        else:
            raise ValueError(f"Value '{v}' is unknown for MessageDirection.")
