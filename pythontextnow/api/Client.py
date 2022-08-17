from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Optional


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
    def set_client_config(cls, *, username: str, sid_cookie: str, csrf_cookie: str) -> None:
        from pythontextnow.api.TextNowAPI import TextNowAPI
        text_now_api = TextNowAPI()
        cookies = {
            "connect.sid": sid_cookie,
            "_csrf": csrf_cookie,
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36 ",
            "x-csrf-token": text_now_api.get_csrf_token(cookies)
        }

        client_config = ClientConfig(username=username,
                                     headers=headers,
                                     cookies=cookies,
                                     last_call_time=datetime.datetime.now())
        cls.client_config = client_config

    @classmethod
    def get_client_config(cls) -> ClientConfig:
        return cls.client_config

    @classmethod
    def update(cls, **kwargs) -> None:
        new_last_call_time = kwargs.pop("last_call_time", None)
        if new_last_call_time is not None:
            cls.client_config.last_call_time = new_last_call_time
