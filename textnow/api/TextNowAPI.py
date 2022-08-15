import json
from datetime import datetime
from urllib.parse import quote

import cloudscraper

from textnow.enum import MessageType, MessageDirection, ContactType, ReadStatus
from textnow.model.Client import Client, ClientConfig
from textnow.model.Message import Message
from textnow.model.MultiMediaMessage import MultiMediaMessage
from textnow.model.TextMessage import TextMessage
from textnow.util.ConfigReader import ConfigReader


class TextNowAPI:
    def __init__(self):
        self.__scraper = cloudscraper.create_scraper()

        self.__BASE_URL = ConfigReader.get("api", "textnow_base_url")
        self.__API_ROUTE = ConfigReader.get("api", "api_route")
        self.__CONVERSATIONS_ROUTE = ConfigReader.get("api", "conversations_route")
        self.__MESSAGES_ROUTE = ConfigReader.get("api", "messages_route")
        self.__USERS_ROUTE = ConfigReader.get("api", "users_route")

    @property
    def __client_config(self) -> ClientConfig:
        return Client.get_client_config()

    def send_message(self, message: str, send_to: str) -> None:
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

        response = self.__scraper.post(
            f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{self.__client_config.username}{self.__MESSAGES_ROUTE}",
            headers=self.__client_config.headers,
            cookies=self.__client_config.cookies,
            data=data)
        response.raise_for_status()

    def get_all_messages(self) -> list[Message]:
        response = self.__scraper.get(
            f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{self.__client_config.username}{self.__MESSAGES_ROUTE}",
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

        response = self.__scraper.post(url,
                                       params=params,
                                       data=data,
                                       cookies=self.__client_config.cookies,
                                       headers=self.__client_config.headers)
        response.raise_for_status()
