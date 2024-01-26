from __future__ import annotations

from enum import Enum, unique


@unique
class ContactType(Enum):
    # TODO: Find out what these values stand for
    DEFAULT = 1
    ALTERNATE = 2

    @classmethod
    def from_value(cls, v: str | int) -> ContactType:
        if v == "1" or v == 1:
            return ContactType.DEFAULT
        if v == "2" or v == 2:
            return ContactType.ALTERNATE
        else:
            raise ValueError(f"Value '{v}' is unknown for ContactType.")
