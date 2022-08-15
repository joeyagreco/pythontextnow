from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from textnow.enum import MessageType, MessageDirection


@dataclass(kw_only=True)
class Message:
    number: str
    date: datetime
    first_contact: bool
    type_: MessageType
    read: bool
    id_: str
    direction: MessageDirection
    raw: dict

    @classmethod
    def from_dict(cls, message_dict: dict) -> Message:
        number = message_dict["contact_value"]
        date = datetime.fromisoformat(message_dict["date"].replace("Z", "+00:00"))
        first_contact = message_dict["conversation_filtering"]["first_time_contact"]
        type_ = MessageType.from_value(message_dict["message_type"])
        read = message_dict["read"]
        id_ = message_dict["id"]
        direction = MessageDirection.from_value(message_dict["message_direction"])
        raw = message_dict
        return Message(number=number,
                       date=date,
                       first_contact=first_contact,
                       type_=type_,
                       read=read,
                       id_=id_,
                       direction=direction,
                       raw=raw)
