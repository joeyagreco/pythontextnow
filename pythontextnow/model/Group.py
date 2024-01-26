from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pythontextnow.model.Avatar import Avatar
from pythontextnow.model.Member import Member


@dataclass(kw_only=True)
class Group:
    title: Optional[str]
    avatar: Avatar
    members: list[Member]
    contact_value: str
    e164_contact_value: str

    @classmethod
    def from_dict(cls, group_dict: dict) -> Group:
        members = list()
        for member_dict in group_dict["members"]:
            members.append(Member.from_dict(member_dict))
        avatar = Avatar.from_dict(group_dict["avatar"])
        return Group(
            title=group_dict["title"],
            avatar=avatar,
            members=members,
            contact_value=group_dict["contact_value"],
            e164_contact_value=group_dict["e164_contact_value"],
        )

    @classmethod
    def to_dict(cls, group: Group) -> dict:
        return {
            "title": group.title,
            "avatar": Avatar.to_dict(group.avatar),
            "members": [Member.to_dict(member) for member in group.members],
            "contact_value": group.contact_value,
        }
