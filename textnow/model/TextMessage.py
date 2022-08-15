from __future__ import annotations

from dataclasses import dataclass

from textnow.model.Message import Message


@dataclass
class TextMessage(Message):
    text: str

    @classmethod
    def from_dict(cls, message_dict: dict) -> TextMessage:
        message = Message.from_dict(message_dict)
        return TextMessage(number=message.number,
                           date=message.date,
                           first_contact=message.first_contact,
                           type_=message.type_,
                           read=message.read,
                           id_=message.id_,
                           direction=message.direction,
                           raw=message.raw,
                           text=message_dict["message"])
