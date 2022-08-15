from pythontextnow.api.TextNowAPI import TextNowAPI
from pythontextnow.enum import MessageDirection
from pythontextnow.model.Message import Message
from pythontextnow.util import general


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


def get_all_incoming_messages() -> list[Message]:
    """
    Gets all incoming messages.
    """
    all_messages = get_all_messages()
    return [message for message in all_messages if message.direction == MessageDirection.INCOMING]


def get_all_outgoing_messages() -> list[Message]:
    """
    This all messages sent by your account.
    """
    all_messages = get_all_messages()
    return [message for message in all_messages if message.direction == MessageDirection.OUTGOING]


def get_all_unread_messages():
    """
    Gets all unread messages.
    """
    all_messages = get_all_messages()
    return [message for message in all_messages if not message.read]


def mark_as_read(*, message: Message = None, messages: list[Message] = None) -> None:
    """
    Marks the given message/s as read.
    """
    if message is None and messages is None:
        raise ValueError("'message' and 'messages' cannot both be None.")
    all_messages = messages
    if all_messages is None:
        all_messages = [message]
    text_now_api = TextNowAPI()
    for message in all_messages:
        text_now_api.mark_message_as_read(message)
