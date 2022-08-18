from enum import unique, Enum


@unique
class ContactType(Enum):
    # TODO: Find out what these values stand for
    DEFAULT = 1
    ALTERNATE = 2
