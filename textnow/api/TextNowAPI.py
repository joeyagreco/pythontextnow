import json
from datetime import datetime

import cloudscraper

from textnow.enum import MessageType, MessageDirection, ContactType, ReadStatus
from textnow.model.Client import Client


class TextNowAPI:
    def __init__(self):
        self.__scraper = cloudscraper.create_scraper()

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

        response = self.__scraper.post(f"https://www.textnow.com/api/users/{client_config.username}/messages",
                                       headers=client_config.headers,
                                       cookies=client_config.cookies,
                                       data=data)
        response.raise_for_status()
