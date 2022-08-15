import json
from datetime import datetime

import cloudscraper

from textnow.model.Client import Client


class TextNowAPI:
    def __init__(self):
        self.__scraper = cloudscraper.create_scraper()

    def send_message(self, message: str, send_to: str) -> None:
        client_config = Client.get_client_config()

        json_data = {"contact_value": send_to,
                     "contact_type": 2,
                     "message": message,
                     "read": 1,
                     "message_direction": 1,
                     "message_type": 1,
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
