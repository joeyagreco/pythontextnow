from textnow.api.TextNowAPI import TextNowAPI
from textnow.enum import MessageDirection
from textnow.model.Message import Message
from textnow.util import general


def send_sms(message: str, send_to: str):
    """
    Sends an sms text message to this number.
    """
    message = general.replace_newlines(message)
    text_now_api = TextNowAPI()
    text_now_api.send_message(message, send_to)


def get_all_messages() -> list[Message]:
    """
    This gets the last 30 sent and received messages.
    """
    text_now_api = TextNowAPI()
    return text_now_api.get_all_messages()


def get_sent_messages():
    """
    This gets the last 30 messages sent by your account.
    """
    all_messages = get_all_messages()
    return [message for message in all_messages if
            MessageDirection.from_value(message.direction) == MessageDirection.OUTGOING]
