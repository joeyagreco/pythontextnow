from datetime import datetime


class Message:
    __MESSAGE_TYPE = 0

    def __init__(self, message_dict):
        self.content = message_dict["message"]
        self.number = message_dict["contact_value"]
        self.date = datetime.fromisoformat(message_dict["date"].replace("Z", "+00:00"))
        self.first_contact = message_dict["conversation_filtering"]["first_time_contact"]
        self.type = self.__MESSAGE_TYPE
        self.read = message_dict["read"]
        self.id = message_dict["id"]
        self.direction = message_dict["message_direction"]
        self.raw = message_dict

    def mark_as_read(self):
        from textnow.model.Client import Client
        Client.patch(Client.get_client_config(), self, {"read": True})
