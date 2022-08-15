from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import cloudscraper

from textnow.model.Message import Message


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
        scraper = cloudscraper.create_scraper()
        cookies = {
            'connect.sid': sid_cookie,
            '_csrf': csrf_cookie,
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.104 Safari/537.36 ',
            'x-csrf-token': cls.__get_initial_csrf_token(scraper, cookies)
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

    @classmethod
    def __get_initial_csrf_token(cls, scraper, cookies: dict):
        response = scraper.get('https://www.textnow.com/messaging', cookies=cookies)
        response.raise_for_status()

        resp = response.text
        needle = 'csrf-token" content="'
        needle_index = resp.find(needle)
        token_start = needle_index + len(needle)
        token_end = resp.find('"', token_start)
        csrf_token = resp[token_start:token_end]
        return csrf_token

    # def __on_exit(self):
    #     if len(self.events) == 0:
    #         return
    #
    #     while True:
    #         for event, func in self.events:
    #             if event == "message":
    #                 unread_msgs = self.__get_unread_messages()
    #                 for msg in unread_msgs:
    #                     msg.mark_as_read()
    #                     func(msg)
    #         time.sleep(1)

    @classmethod
    def __get_unread_messages(cls):
        new_messages = cls.__get_received_messages()
        new_messages = [msg for msg in new_messages if not msg.read]
        time.sleep(1)
        return new_messages

    @classmethod
    def __get_received_messages(cls) -> list[Message]:
        """
            Gets inbound messages
        """
        messages = cls.get_messages()
        messages = [Message(msg) for msg in messages if msg.direction == cls.__RECEIVED_MESSAGE_TYPE]
        time.sleep(1)
        return messages

    @classmethod
    def get_received_messages(cls) -> list[Message]:
        """
        Gets inbound messages
        """
        messages = cls.get_messages()
        messages = [msg for msg in messages if msg.direction == cls.__RECEIVED_MESSAGE_TYPE]
        time.sleep(1)
        return messages
