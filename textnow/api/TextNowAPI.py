import json
from datetime import datetime

import cloudscraper

from textnow.enum import MessageType, MessageDirection, ContactType, ReadStatus
from textnow.model.Client import Client
from textnow.util.ConfigReader import ConfigReader


class TextNowAPI:
    def __init__(self):
        self.__scraper = cloudscraper.create_scraper()

        self.__BASE_URL = ConfigReader.get("api", "textnow_base_url")
        self.__API_ROUTE = ConfigReader.get("api", "api_route")
        self.__MESSAGES_ROUTE = ConfigReader.get("api", "messages_route")
        self.__USERS_ROUTE = ConfigReader.get("api", "users_route")

    def send_message(self, message: str, send_to: str) -> None:
        client_config = Client.get_client_config()

        json_data = {"contact_value": send_to,
                     "contact_type": ContactType.DEFAULT.value,
                     "message": message,
                     "read": ReadStatus.READ.value,
                     "message_direction": MessageDirection.OUTGOING.value,
                     "message_type": MessageType.MULTIMEDIA.value,
                     "from_name": client_config.username,
                     "has_video": False,
                     "new": True,
                     "date": datetime.now().isoformat()}

        data = {"json": json.dumps(json_data)}

        response = self.__scraper.post(
            f"{self.__BASE_URL}{self.__API_ROUTE}{self.__USERS_ROUTE}/{client_config.username}{self.__MESSAGES_ROUTE}",
            headers=client_config.headers,
            cookies=client_config.cookies,
            data=data)
        response.raise_for_status()
