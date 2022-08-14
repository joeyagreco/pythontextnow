from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from urllib.parse import quote

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
        messages = cls.__get_messages()
        messages = [Message(msg) for msg in messages if msg.direction == cls.__RECEIVED_MESSAGE_TYPE]
        time.sleep(1)
        return messages

    @classmethod
    def __get_messages(cls) -> list[Message]:
        """
        This gets most of the messages both sent and received. However, it won't get all of them just the past 10-15
        """
        client_config = cls.get_client_config()
        response = cls.client_config.scraper.get(
            "https://www.textnow.com/api/users/" + client_config.username + "/messages",
            headers=client_config.headers,
            cookies=client_config.cookies)
        response.raise_for_status()

        messages = json.loads(response.content)
        messages = [
            Message(msg) if not msg["message"].startswith("http") else None for msg in messages["messages"]]
        time.sleep(1)
        return messages

    @staticmethod
    def __replace_newlines(text):
        return re.sub(r'(?<!\\)\n', r'\\n', text)

    @classmethod
    def send_sms(cls, to, text):
        """
        Sends an sms text message to this number
        """
        client_config = cls.get_client_config()
        text = cls.__replace_newlines(text)

        data = \
            {
                'json': '{"contact_value":"' + to + '","contact_type":2,"message":"' + text + '","read":1,'
                                                                                              '"message_direction":2,'
                                                                                              '"message_type":1,'
                                                                                              '"from_name":"' +
                        client_config.username + '","has_video":false,"new":true,"date":"' + datetime.now().isoformat() + '"} '
            }

        response = client_config.scraper.post(
            'https://www.textnow.com/api/users/' + client_config.username + '/messages',
            headers=client_config.headers, cookies=client_config.cookies, data=data)

        response.raise_for_status()

        for cookie in response.cookies:
            if cookie.name == 'XSRF-TOKEN':
                client_config.cookies['XSRF-TOKEN'] = cookie.value

        time.sleep(1)
        return response

    @classmethod
    def get_unread_messages(cls):
        """
        Gets unread messages
        """
        new_messages = cls.get_received_messages()
        new_messages = [msg for msg in new_messages if not msg.read]
        time.sleep(1)
        # return MessageContainer(new_messages, self)
        return new_messages

    @classmethod
    def get_received_messages(cls) -> list[Message]:
        """
        Gets inbound messages
        """
        messages = cls.__get_messages()
        messages = [msg for msg in messages if msg.direction == cls.__RECEIVED_MESSAGE_TYPE]
        time.sleep(1)
        return messages

    @staticmethod
    def patch(client_config: ClientConfig, message: Message, data):
        if not all(key in message.raw for key in data):
            return

        base_url = "https://www.textnow.com/api/users/" + client_config.username + "/conversations/"
        url = base_url + quote(message.number)

        params = {
            "latest_message_id": message.id,
            "http_method": "PATCH"
        }

        res = client_config.scraper.post(url, params=params, data=data, cookies=client_config.cookies,
                                         headers=client_config.headers)
        time.sleep(1)
        return res
