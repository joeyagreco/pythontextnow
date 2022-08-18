from __future__ import annotations

from dataclasses import dataclass

from pythontextnow.model.Member import Member


@dataclass(kw_only=True)
class Group:
    title: str
    members: list[Member]
    contact_value: str

    @classmethod
    def from_dict(cls, group_dict: dict) -> Group:
        members = list()
        for member_dict in group_dict["members"]:
            members.append(Member.from_dict(member_dict))
        return Group(title=group_dict["title"],
                     members=members,
                     contact_value=group_dict["contact_value"])
