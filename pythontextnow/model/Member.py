from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class Member:
    contact_value: str
    display_value: str
    contact_name: str

    @classmethod
    def from_dict(cls, member_dict: dict) -> Member:
        return Member(contact_value=member_dict["contact_value"],
                      display_value=member_dict["display_value"],
                      contact_name=member_dict["contact_name"])
