from __future__ import annotations

from dataclasses import dataclass

from pythontextnow.enum import ContactType
from pythontextnow.model.Avatar import Avatar


@dataclass(kw_only=True)
class Member:
    contact_name: str
    contact_type: ContactType
    contact_value: str
    e164_contact_value: str
    display_value: str
    avatar: Avatar

    @classmethod
    def from_dict(cls, member_dict: dict) -> Member:
        avatar = Avatar.from_dict(member_dict["avatar"])
        return Member(
            contact_value=member_dict["contact_value"],
            e164_contact_value=member_dict["e164_contact_value"],
            contact_type=ContactType.from_value(member_dict["contact_type"]),
            display_value=member_dict["display_value"],
            contact_name=member_dict["contact_name"],
            avatar=avatar,
        )

    @classmethod
    def to_dict(cls, member: Member) -> dict:
        avatar_dict = Avatar.to_dict(member.avatar)
        return {
            "contact_type": member.contact_type.value,
            "contact_value": member.contact_value,
            "contact_name": member.contact_name,
            "display_value": member.display_value,
            "avatar": avatar_dict,
        }
