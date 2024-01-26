from __future__ import annotations

from dataclasses import dataclass

from pythontextnow.model.Message import Message


@dataclass
class TextMessage(Message):
    text: str

    @classmethod
    def from_dict(cls, message_dict: dict) -> TextMessage:
        message = Message.from_dict(message_dict)
        return TextMessage(
            number=message.number,
            datetime_=message.datetime_,
            first_contact=message.first_contact,
            message_type=message.message_type,
            read=message.read,
            id_=message.id_,
            message_direction=message.message_direction,
            raw=message.raw,
            text=message_dict["message"],
        )
