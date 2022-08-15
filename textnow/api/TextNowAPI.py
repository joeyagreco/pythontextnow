import json
from datetime import datetime

import cloudscraper

from textnow.enum import MessageType, MessageDirection, ContactType, ReadStatus
from textnow.model.Client import Client, ClientConfig
from textnow.model.Message import Message
from textnow.util.ConfigReader import ConfigReader


class TextNowAPI:
    def __init__(self):
        self.__scraper = cloudscraper.create_scraper()

        self.__BASE_URL = ConfigReader.get("api", "textnow_base_url")
        self.__API_ROUTE = ConfigReader.get("api", "api_route")
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

        messages = json.loads(response.content)
        messages = [
            Message(msg) if not msg["message"].startswith("http") else None for msg in messages["messages"]]
        return messages
