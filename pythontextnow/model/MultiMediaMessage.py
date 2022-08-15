from __future__ import annotations

from dataclasses import dataclass

from pythontextnow.model.Message import Message


@dataclass
class MultiMediaMessage(Message):
    media: str

    @classmethod
    def from_dict(cls, message_dict: dict) -> MultiMediaMessage:
        message = Message.from_dict(message_dict)
        return MultiMediaMessage(number=message.number,
                                 date=message.date,
                                 first_contact=message.first_contact,
                                 type_=message.type_,
                                 read=message.read,
                                 id_=message.id_,
                                 direction=message.direction,
                                 raw=message.raw,
                                 media=message_dict["message"])
