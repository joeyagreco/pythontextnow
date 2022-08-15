from enum import unique, Enum


@unique
class MessageDirection(Enum):
    OUTGOING = 1
