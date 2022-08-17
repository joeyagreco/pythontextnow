import json
import urllib
from datetime import datetime
from typing import Optional
from urllib import parse
from urllib.parse import quote

import requests

from pythontextnow.api.Client import Client, ClientConfig
from pythontextnow.enum import MessageType, MessageDirection, ContactType, ReadStatus
from pythontextnow.model.Message import Message
from pythontextnow.model.MultiMediaMessage import MultiMediaMessage
from pythontextnow.model.TextMessage import TextMessage
from pythontextnow.util.ConfigReader import ConfigReader


class TextNowAPI:
    def __init__(self):
        self.__BASE_URL = ConfigReader.get("api", "textnow_base_url")
        self.__VERSION = ConfigReader.get("api", "version")
        self.__API_ROUTE = ConfigReader.get("api", "api_route")
        self.__ATTACHMENT_URL_ROUTE = ConfigReader.get("api", "attachment_url_route")
        self.__CONVERSATIONS_ROUTE = ConfigReader.get("api", "conversations_route")
        self.__MESSAGES_ROUTE = ConfigReader.get("api", "messages_route")
        self.__MESSAGING_ROUTE = ConfigReader.get("api", "messaging_route")
        self.__SEND_ATTACHMENT_ROUTE = ConfigReader.get("api", "send_attachment_route")
        self.__USERS_ROUTE = ConfigReader.get("api", "users_route")

        self.__MAX_MESSAGE_RESPONSE_SIZE = 30

    @property
    def __client_config(self) -> ClientConfig:
        return Client.get_client_config()

    def get_csrf_token(self, cookies: dict) -> str:
        response = requests.get(f"{self.__BASE_URL}{self.__MESSAGING_ROUTE}",
                                cookies=cookies)

        response.raise_for_status()

        resp = response.text
        needle = 'csrf-token" content="'
        needle_index = resp.find(needle)
        token_start = needle_index + len(needle)
        token_end = resp.find('"', token_start)
        csrf_token = resp[token_start:token_end]
        return csrf_token

    def send_message(self, *, message: str, send_to: str) -> None:
        json_data = {"contact_value": send_to,
                     "contact_type": ContactType.DEFAULT.value,
                     "message": message,
                     "read": ReadStatus.READ.value,
                     "message_direction": MessageDirection.OUTGOING.value,
                     "message_type": MessageType.MULTIMEDIA.value,
                     "from_name": self.__client_config.username,
                     "has_video": False,
                     "new": True,
                     "date": datetime.now().isoformat()}

        data = {"json": json.dumps(json_data)}

        response = requests.post(
            f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{self.__client_config.username}{self.__MESSAGES_ROUTE}",
            headers=self.__client_config.headers,
            cookies=self.__client_config.cookies,
            data=data)
        response.raise_for_status()

    def get_messages(self, conversation_phone_number: str,
                     *,
                     start_message_id: Optional[str] = None,
                     page_size: Optional[int],
                     get_archived: Optional[bool]) -> list[Message]:
        """
        This gets messages from the conversation with the given phone number.

        This will get all messages before (but not including) the message with the given start_message_id.
        If the given page_size is greater than the max allowed (30), will default to 30.
        """
        page_size = page_size if page_size <= self.__MAX_MESSAGE_RESPONSE_SIZE else self.__MAX_MESSAGE_RESPONSE_SIZE
        params = {
            "contact_value": f"+{conversation_phone_number}",
            "direction": "past",
            "page_size": page_size,
            "get_archived": 1 if get_archived else 0
        }
        if start_message_id is not None:
            params["start_message_id"] = start_message_id
        base_url = f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{self.__client_config.username}{self.__MESSAGES_ROUTE}"
        url_with_params = f"{base_url}?{urllib.parse.urlencode(params)}"

        response = requests.get(
            url_with_params,
            headers=self.__client_config.headers,
            cookies=self.__client_config.cookies)
        response.raise_for_status()

        message_dicts = json.loads(response.content)["messages"]

        all_messages = list()
        # sort into Text and MultiMedia messages
        for message_dict in message_dicts:
            message_type = MessageType.from_value(message_dict["message_type"])
            if message_type == MessageType.TEXT:
                all_messages.append(TextMessage.from_dict(message_dict))
            elif message_type == MessageType.MULTIMEDIA:
                all_messages.append(MultiMediaMessage.from_dict(message_dict))
        return all_messages

    def mark_message_as_read(self, message: Message) -> None:

        clean_number = quote(message.number)
        url = f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{self.__client_config.username}{self.__CONVERSATIONS_ROUTE}/{clean_number}"

        params = {
            "latest_message_id": message.id_,
            "http_method": "PATCH"
        }

        data = {"read": True}

        response = requests.post(url,
                                 params=params,
                                 data=data,
                                 cookies=self.__client_config.cookies,
                                 headers=self.__client_config.headers)
        response.raise_for_status()

    def delete_message(self, *, message: Optional[Message] = None, message_id: Optional[str] = None) -> None:
        """
        Deletes the given message or message with the given ID.
        """
        if message is None and message_id is None:
            raise ValueError("'message' and 'message_id' cannot both be None.")

        message_id = message_id if message_id is not None else message.id_

        url = f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{self.__client_config.username}{self.__MESSAGES_ROUTE}/{message_id}"
        response = requests.delete(url,
                                   cookies=self.__client_config.cookies,
                                   headers=self.__client_config.headers)
        response.raise_for_status()

    def get_attachment_url(self) -> str:
        """
        Gets the URL that a file can be uploaded to.
        """
        url = f"{self.__BASE_URL}{self.__API_ROUTE}/{self.__VERSION}{self.__ATTACHMENT_URL_ROUTE}"
        params = {"message_type": 2}
        url_with_params = f"{url}&{parse.urlencode(params)}"

        response = requests.get(
            url_with_params,
            headers=self.__client_config.headers,
            cookies=self.__client_config.cookies)
        response.raise_for_status()

        return response.json()["result"]

    def upload_raw_media(self, *, attachment_url: str, raw_media: bytearray, content_type: tuple) -> None:
        """
        Uploads the given raw_media to the given URL.
        """
        headers = {
            'accept': '*/*',
            'content-type': content_type,
            'accept-language': 'en-US,en;q=0.9',
            "mode": "cors",
            "method": "PUT",
            "credentials": 'omit'
        }

        response = requests.put(attachment_url,
                                data=raw_media,
                                headers=headers,
                                cookies=self.__client_config.cookies)
        response.raise_for_status()

    def send_attachment(self, *,
                        conversation_phone_number: str,
                        message_type: MessageType,
                        file_type: str,
                        has_video: bool,
                        attachment_url: str) -> None:

        data = {
            "contact_value": conversation_phone_number,
            "contact_type": ContactType.MEDIA.value,
            "read": 1,
            "message_direction": MessageDirection.OUTGOING.value,
            "message_type": message_type.value,
            "from_name": self.__client_config.username,
            "has_video": has_video,
            "new": True,
            "date": datetime.now().isoformat(),
            "attachment_url": attachment_url,
            "media_type": file_type
        }

        url = f"{self.__BASE_URL}{self.__API_ROUTE}/{self.__VERSION}{self.__SEND_ATTACHMENT_ROUTE}"

        response = requests.post(url,
                                 data=data,
                                 headers=self.__client_config.headers,
                                 cookies=self.__client_config.cookies)
