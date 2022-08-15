from enum import unique, Enum


@unique
class ReadStatus(Enum):
    READ = 1
    UNREAD = 0
