from __future__ import annotations

from dataclasses import dataclass


@dataclass(kw_only=True)
class User:
    user_id: int
    username: str
    email: str
    phone_number: str

    @classmethod
    def from_dict(cls, user_dict: dict) -> User:
        return User(
            user_id=user_dict["user_id"],
            username=user_dict["username"],
            email=user_dict["email"],
            phone_number=user_dict["phone_number"],
        )
