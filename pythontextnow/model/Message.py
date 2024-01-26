from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from pythontextnow.enum import MessageDirection, MessageType


@dataclass(kw_only=True)
class Message:
    number: str
    datetime_: datetime
    first_contact: bool
    message_type: MessageType
    read: bool
    id_: str
    message_direction: MessageDirection
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
        return Message(
            number=number,
            datetime_=date,
            first_contact=first_contact,
            message_type=type_,
            read=read,
            id_=id_,
            message_direction=direction,
            raw=raw,
        )
