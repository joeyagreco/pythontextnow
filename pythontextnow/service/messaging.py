from typing import Optional, Generator

from pythontextnow.api.TextNowAPI import TextNowAPI
from pythontextnow.enum import MessageDirection
from pythontextnow.model.Message import Message
from pythontextnow.util import general


def send_sms(*, message: str, send_to: str):
    """
    Sends an sms text message to this number.
    """
    message = general.replace_newlines(message)
    text_now_api = TextNowAPI()
    text_now_api.send_message(message=message, send_to=send_to)


def get_all_messages() -> list[Message]:
    """
    This gets the last 30 sent and received messages.
    """
    text_now_api = TextNowAPI()
    return text_now_api.get_all_messages()


def get_messages(*, conversation_phone_number: str,
                 num_messages: int = None,
                 include_archived: bool = True) -> Generator[list[Message], None, None]:
    """
    This yields the last n messages in the conversation with the given phone number.
    Where: n = 30 or response_size if given.

    THINGS TO NOTE:
        - num_messages is the number of messages to return before stopping iteration
        - if num_messages is not given, this generator will keep yielding until there are no more messages found
        - The returned message list will be ordered most recent -> least recent
    """
    text_now_api = TextNowAPI()
    start_message_id: Optional[str] = None

    messages_yielded = 0
    page_size = num_messages

    while num_messages is None or messages_yielded < num_messages:
        messages = text_now_api.get_messages(conversation_phone_number,
                                             start_message_id=start_message_id,
                                             get_archived=include_archived,
                                             page_size=page_size)
        if len(messages) > 0:
            start_message_id = messages[-1].id_
            messages_yielded += len(messages)
            page_size -= messages_yielded
            yield messages
        else:
            return


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
