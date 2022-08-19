import mimetypes
from typing import Optional, Generator

from pythontextnow.api.TextNowAPI import TextNowAPI
from pythontextnow.enum import MessageType, ContactType
from pythontextnow.model.Avatar import Avatar
from pythontextnow.model.Group import Group
from pythontextnow.model.Member import Member
from pythontextnow.model.Message import Message
from pythontextnow.util import general


class ConversationService:

    def __init__(self, *, conversation_phone_numbers: list[str]):
        # check that given phone numbers are well-formed
        for phone_number in conversation_phone_numbers:
            self.__validate_well_formed_phone_number(phone_number)
        self.__conversation_phone_numbers = conversation_phone_numbers
        if len(self.__conversation_phone_numbers) == 0:
            raise ValueError("'conversation_phone_numbers' cannot be empty.")
        self.__cached_conversation_number: Optional[str] = None

        self.__DEFAULT_PAGE_SIZE = 30
        self.__BANNED_MEDIA_TYPES = ["audio"]
        self.__text_now_api = TextNowAPI()

    @property
    def __conversation_number(self) -> str:
        """
        Returns the conversation number for this conversation.
        """
        if self.__cached_conversation_number is None:
            if len(self.__conversation_phone_numbers) == 1:
                # this is a single contact conversation
                self.__cached_conversation_number = self.__conversation_phone_numbers[0]
            else:
                # this is a group chat
                conversation_number = self.__get_conversation_number()
                self.__cached_conversation_number = conversation_number
        return self.__cached_conversation_number

    @staticmethod
    def __validate_well_formed_phone_number(phone_number: str) -> None:
        """
        Checks that the given phone number is well-formed.
        If it is not well-formed, will raise an appropriate exception.
        """
        VALID_CHARACTERS = ["+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        VALID_PHONE_NUMBER_LENGTHS = [10, 11]
        for char in phone_number:
            if char not in VALID_CHARACTERS:
                raise ValueError(f"'{char}' is not a valid character for a phone number.")
        if phone_number.count("+") > 1 or phone_number.find("+") not in (0, -1):
            raise ValueError(f"Phone number can only have 1 '+' at the start of the number.")
        if len(phone_number.replace("+", "")) not in VALID_PHONE_NUMBER_LENGTHS:
            raise ValueError(f"Phone number does not have a valid length.")

    @staticmethod
    def __numbers_match(number_1: str, number_2: str) -> bool:
        """
        This is a helper method to see if 2 numbers match.
        It accounts for country codes.
        If one number has a country code and the other does not but the "core" number matches, it is counted as a match.

        Examples:
            - "+01112223333", "+01112223333" -> True
            - "1112223333", "1112223333" -> True
            - "+01112223333", "01112223333" -> True
            - "+01112223333", "1112223333" -> True
            - "1112223333", "4445556666" -> False
        """
        if number_1.startswith("+"):
            # only keep core number (keep last 10 digits)
            number_1 = number_1[-10:]
        if number_2.startswith("+"):
            # only keep core number (keep last 10 digits)
            number_2 = number_2[-10:]
        return number_1[-10:] == number_2[-10:]

    def __get_conversation_number(self) -> str:
        """
        For a chat with a single number, returns the only conversation_phone_number.
        For interfacing with group chats, a single phone number is used that is assigned by TextNow.
        This retrieves the group phone number for this group chat.
        This will not be needed or used if this is not a group chat.
        """
        # check if this is a chat with a single number
        if len(self.__conversation_phone_numbers) == 1:
            return self.__conversation_phone_numbers[0]
        # get this user
        user = self.__text_now_api.get_user()
        # get this user's groups
        groups = self.__text_now_api.get_groups()

        # find the group that contains exactly all conversation_phone_numbers + this user's TextNow number
        for group in groups:
            # keep track of all numbers that should be in the group we are looking for
            all_needed_group_numbers = [user.phone_number] + self.__conversation_phone_numbers
            # keep track of all numbers that have are a match
            matching_numbers = list()
            if len(group.members) == len(all_needed_group_numbers):
                # correct amount of members, see if all the numbers match
                for member in group.members:
                    # some numbers will have a "+" at the start
                    member_number = member.contact_value.replace("+", "")
                    for needed_number in all_needed_group_numbers:
                        if self.__numbers_match(member_number, needed_number):
                            # in the group we are looking for
                            matching_numbers.append(member_number)
            if len(matching_numbers) == len(all_needed_group_numbers):
                return group.contact_value

        # unable to find a group that matched all conversation phone numbers
        # create a new group
        # create a Member for each number
        members = list()
        for number in self.__conversation_phone_numbers:
            # create a default avatar
            avatar = Avatar(background_color="#DD7C00",
                            picture=None,
                            initials=None)
            members.append(
                Member(contact_name="",
                       contact_value=number,
                       contact_type=ContactType.ALTERNATE,
                       display_value="",
                       avatar=avatar)
            )
        group_avatar = Avatar(background_color="#DD7C00",
                              picture=None,
                              initials=None)
        new_group_obj = Group(title=None,
                              avatar=group_avatar,
                              members=members,
                              contact_value=None)
        new_group = self.__text_now_api.create_group(group=new_group_obj)
        return new_group.contact_value

    def send_message(self, *, message: str):
        """
        Sends a text message to this instance's conversation_phone_number.
        """
        message = general.replace_newlines(message)
        self.__text_now_api.send_message(message=message, send_to=self.__conversation_number)

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

        messages_yielded = 0
        page_size = num_messages if num_messages is not None else self.__DEFAULT_PAGE_SIZE

        while num_messages is None or messages_yielded < num_messages and page_size > 0:
            messages = self.__text_now_api.get_messages(self.__conversation_number,
                                                        start_message_id=start_message_id,
                                                        get_archived=include_archived,
                                                        page_size=page_size)
            if len(messages) > 0:
                start_message_id = messages[-1].id_
                messages_yielded += len(messages)
                if num_messages:
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

    def delete_message(self, *, message: Optional[Message] = None, message_id: Optional[str] = None) -> None:
        """
        Deletes the given message or message with the given ID.
        """
        if message is None and message_id is None:
            raise ValueError("'message' and 'message_id' cannot both be None.")

        message_id = message_id if message_id is not None else message.id_
        self.__text_now_api.delete_message(message_id=message_id)

    def send_media(self, *, file_path: str):
        """
        Sends the given media to this instance's conversation_phone_number.
        Supports sending:
            - Images
            - Videos
            - GIFs
        """

        mime_type = mimetypes.guess_type(file_path)
        if mime_type is None:
            raise ValueError("Cannot get media type from media at 'file_path'.")
        media_type = mime_type[0]  # will be something like "video/mp4" or "image/png"
        file_type = media_type[0].split("/")[0]  # will be something like "video" or "image" or "gif"
        if file_type in self.__BANNED_MEDIA_TYPES:
            raise ValueError(f"'{file_type} is not an allowed media type.'")
        is_video = file_type == "video"
        message_type = MessageType.IMAGE if file_type == "image" else MessageType.VIDEO

        with open(file_path, mode="rb") as media:
            raw_media = media.read()

        attachment_url = self.__text_now_api.get_attachment_url(message_type=message_type)

        self.__text_now_api.upload_raw_media(attachment_url=attachment_url,
                                             raw_media=raw_media,
                                             media_type=media_type)

        self.__text_now_api.send_attachment(conversation_phone_number=self.__conversation_number,
                                            message_type=message_type,
                                            file_type=file_type,
                                            is_video=is_video,
                                            attachment_url=attachment_url)

    def delete_conversation(self) -> None:
        """
        Deletes this conversation.
        """
        conversation_number = self.__conversation_number
        self.__text_now_api.delete_conversation(conversation_phone_number=conversation_number)
