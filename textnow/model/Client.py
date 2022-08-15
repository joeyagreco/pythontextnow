from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cloudscraper


@dataclass(kw_only=True, frozen=True)
class ClientConfig:
    """
    Used to hold the Client config.
    """
    username: str
    events: list
    scraper: Any
    headers: dict
    cookies: dict


class Client:
    """
    This class is used to store and set up initial Client configuration.
    """
    client_config = None
    __RECEIVED_MESSAGE_TYPE = 1
    __ALLOWED_EVENTS = ["message"]

    @classmethod
    def set_client_config(cls, username: str, sid_cookie: str, csrf_cookie: str) -> None:
        from textnow.api.TextNowAPI import TextNowAPI
        text_now_api = TextNowAPI()
        scraper = cloudscraper.create_scraper()
        cookies = {
            'connect.sid': sid_cookie,
            '_csrf': csrf_cookie,
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.104 Safari/537.36 ',
            'x-csrf-token': text_now_api.get_csrf_token(cookies)
        }

        client_config = ClientConfig(username=username,
                                     events=list(),
                                     scraper=scraper,
                                     headers=headers,
                                     cookies=cookies)
        cls.client_config = client_config

    @classmethod
    def get_client_config(cls) -> ClientConfig:
        return cls.client_config
