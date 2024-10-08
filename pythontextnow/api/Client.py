from __future__ import annotations

import datetime
import hashlib
from dataclasses import dataclass
from typing import Optional

from pythontextnow.util.general import get_random_user_agent


@dataclass(kw_only=True)
class ClientConfig:
    """
    Used to hold the Client config.
    """

    username: str
    headers: dict
    cookies: dict
    last_call_time: datetime


class Client:
    """
    This class is used to store and set up initial Client configuration.
    """

    client_config: Optional[ClientConfig] = None

    @classmethod
    def set_client_config(cls, *, username: str, sid_cookie: str) -> None:
        # use the same user agent for the same username + sid cookie combo
        # we do this by creating a hash of them and then using it as a seed
        hash: int = int(
            hashlib.sha256(f"{username}+{sid_cookie}".encode()).hexdigest(), 16
        )
        headers = {
            "user-agent": get_random_user_agent(hash),
            "Cookie": f"connect.sid={sid_cookie};",
        }

        client_config = ClientConfig(
            username=username,
            headers=headers,
            cookies=dict(),  # for now, no cookies are needed
            last_call_time=datetime.datetime.now(),
        )
        cls.client_config = client_config

    @classmethod
    def get_client_config(cls) -> ClientConfig:
        return cls.client_config

    @classmethod
    def update(cls, **kwargs) -> None:
        new_last_call_time = kwargs.pop("last_call_time", None)
        if new_last_call_time is not None:
            cls.client_config.last_call_time = new_last_call_time
