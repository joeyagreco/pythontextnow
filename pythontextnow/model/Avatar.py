from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class Avatar:
    background_color: str
    picture: Optional[str]
    initials: Optional[str]

    @classmethod
    def from_dict(cls, avatar_dict: dict) -> Avatar:
        return Avatar(
            background_color=avatar_dict["background_colour"],
            picture=avatar_dict["picture"],
            initials=avatar_dict["initials"],
        )

    @classmethod
    def to_dict(cls, avatar: Avatar) -> dict:
        return {
            "background_colour": avatar.background_color,
            "picture": avatar.picture,
            "initials": avatar.initials,
        }
