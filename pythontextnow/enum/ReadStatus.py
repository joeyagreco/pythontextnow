from enum import Enum, unique


@unique
class ReadStatus(Enum):
    READ = 1
    UNREAD = 0
