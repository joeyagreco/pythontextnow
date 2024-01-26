from __future__ import annotations

from dataclasses import dataclass

from pythontextnow.model.Message import Message


@dataclass
class MultiMediaMessage(Message):
    media: str

    @classmethod
    def from_dict(cls, message_dict: dict) -> MultiMediaMessage:
        message = Message.from_dict(message_dict)
        return MultiMediaMessage(
            number=message.number,
            datetime_=message.datetime_,
            first_contact=message.first_contact,
            message_type=message.message_type,
            read=message.read,
            id_=message.id_,
            message_direction=message.message_direction,
            raw=message.raw,
            media=message_dict["message"],
        )
