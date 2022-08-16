import time
from typing import Optional, Generator

from pythontextnow.api.TextNowAPI import TextNowAPI
from pythontextnow.model.Message import Message
from pythontextnow.util import general


class MessageService:

    def __init__(self, *, conversation_phone_number: str):
        self.__conversation_phone_number = conversation_phone_number

        self.__text_now_api = TextNowAPI()
        self.__API_CALL_COOLDOWN_SECONDS = 1
        self.__DEFAULT_PAGE_SIZE = 30

    def send_message(self, *, message: str):
        """
        Sends a text message to this instance's conversation_phone_number.
        """
        message = general.replace_newlines(message)
        self.__text_now_api.send_message(message=message, send_to=self.__conversation_phone_number)

    def get_messages(self,
                     *,
                     num_messages: Optional[int] = None,
                     include_archived: bool = True) -> Generator[list[Message], None, None]:
        """
        This yields the last n messages in the conversation with this instance's conversation_phone_number.
        Where: n = 30 or response_size if given.

        THINGS TO NOTE:
            - num_messages is the number of messages to return before stopping iteration
            - if num_messages is not given, this generator will keep yielding until there are no more messages found
            - The returned message list will be ordered most recent -> least recent
            - This enforces a cooldown time between each call
        """
        start_message_id: Optional[str] = None

        last_call_time = None
        messages_yielded = 0
        num_messages = num_messages if num_messages is not None else self.__DEFAULT_PAGE_SIZE
        page_size = num_messages

        while num_messages is None or messages_yielded < num_messages and page_size > 0:
            if last_call_time is not None:
                time_since_last_call = last_call_time - time.time()
                if time_since_last_call < self.__API_CALL_COOLDOWN_SECONDS:
                    # cooldown
                    time.sleep(self.__API_CALL_COOLDOWN_SECONDS)
            messages = self.__text_now_api.get_messages(self.__conversation_phone_number,
                                                        start_message_id=start_message_id,
                                                        get_archived=include_archived,
                                                        page_size=page_size)
            last_call_time = time.time()
            if len(messages) > 0:
                start_message_id = messages[-1].id_
                messages_yielded += len(messages)
                page_size -= messages_yielded
                yield messages
            else:
                return

    def mark_as_read(self, *, message: Message = None, messages: list[Message] = None) -> None:
        """
        Marks the given message/s as read.
        This enforces a cooldown time between each call.
        """
        if message is None and messages is None:
            raise ValueError("'message' and 'messages' cannot both be None.")
        all_messages = messages
        if all_messages is None:
            all_messages = [message]
        for message in all_messages:
            self.__text_now_api.mark_message_as_read(message)
            time.sleep(self.__API_CALL_COOLDOWN_SECONDS)

    def delete_message(self, *, message: Optional[Message] = None, message_id: Optional[str] = None) -> None:
        """
        Deletes the given message or message with the given ID.
        """
        self.__text_now_api.delete_message(message=message, message_id=message_id)
