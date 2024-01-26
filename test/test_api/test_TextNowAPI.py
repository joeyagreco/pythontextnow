import datetime
import os
from test.helper.helper_classes import MockResponse
from unittest import TestCase, mock

from pythontextnow.api.Client import Client
from pythontextnow.api.TextNowAPI import TextNowAPI
from pythontextnow.enum import ContactType, MessageDirection, MessageType
from pythontextnow.model.Group import Group
from pythontextnow.model.MultiMediaMessage import MultiMediaMessage
from pythontextnow.model.TextMessage import TextMessage
from pythontextnow.model.User import User


class TestTextNowAPI(TestCase):
    PATH_TO_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

    @classmethod
    @mock.patch("requests.get")
    def setUpClass(cls, mock_requests_get):
        # get dummy messaging page as a string
        with open(os.path.join(cls.PATH_TO_DATA_DIR, "dummy_messaging_page.html")) as f:
            dummy_messaging_page_lines = f.readlines()
        dummy_messaging_page_str = "\n".join(dummy_messaging_page_lines)

        mock_response = MockResponse(dict(), 200, text=dummy_messaging_page_str)
        mock_requests_get.return_value = mock_response
        Client.set_client_config(username="dummy_username", sid_cookie="dummy_sid_cookie")

    @mock.patch("requests.post")
    def test_send_message_happy_path(self, mock_requests_post):
        mock_response = MockResponse(dict(), 200)
        mock_requests_post.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.send_message.__wrapped__(
            text_now_api, message="hello world", send_to="5555555555"
        )

        self.assertIsNone(response)

    @mock.patch("requests.get")
    def test_get_messages_text_message_happy_path(self, mock_requests_get):
        mock_message_dict = {
            "id": "id",
            "username": "username",
            "contact_value": "contact_value",
            "message_direction": 2,
            "message_type": 1,
            "message": "hello world",
            "read": True,
            "date": "2000-01-01T01:01:00Z",
            "conversation_filtering": {"first_time_contact": True},
        }
        mock_response_dict = {"status": {}, "messages": [mock_message_dict]}
        mock_response = MockResponse(mock_response_dict, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_messages.__wrapped__(
            text_now_api, conversation_phone_number="1111111111", page_size=10, get_archived=True
        )

        message = response[0]
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertIsInstance(message, TextMessage)
        self.assertEqual("id", message.id_)
        self.assertEqual("contact_value", message.number)
        self.assertEqual(
            datetime.datetime(2000, 1, 1, 1, 1, tzinfo=datetime.timezone.utc), message.datetime_
        )
        self.assertTrue(message.first_contact)
        self.assertEqual(MessageType.TEXT, message.message_type)
        self.assertTrue(message.read)
        self.assertEqual(MessageDirection.INCOMING, message.message_direction)
        self.assertEqual(mock_message_dict, message.raw)
        self.assertEqual("hello world", message.text)

    @mock.patch("requests.get")
    def test_get_messages_multi_media_message_happy_path(self, mock_requests_get):
        mock_message_dict = {
            "id": "id",
            "username": "username",
            "contact_value": "contact_value",
            "message_direction": 2,
            "message_type": 2,
            "message": "https://test",
            "read": True,
            "date": "2000-01-01T01:01:00Z",
            "conversation_filtering": {"first_time_contact": True},
        }
        mock_response_dict = {"status": {}, "messages": [mock_message_dict]}
        mock_response = MockResponse(mock_response_dict, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_messages.__wrapped__(
            text_now_api, conversation_phone_number="1111111111", page_size=10, get_archived=True
        )

        message = response[0]
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertIsInstance(message, MultiMediaMessage)
        self.assertEqual("id", message.id_)
        self.assertEqual("contact_value", message.number)
        self.assertEqual(
            datetime.datetime(2000, 1, 1, 1, 1, tzinfo=datetime.timezone.utc), message.datetime_
        )
        self.assertTrue(message.first_contact)
        self.assertEqual(MessageType.IMAGE, message.message_type)
        self.assertTrue(message.read)
        self.assertEqual(MessageDirection.INCOMING, message.message_direction)
        self.assertEqual(mock_message_dict, message.raw)
        self.assertEqual("https://test", message.media)

    @mock.patch("requests.patch")
    def test_mark_message_as_read_happy_path(self, mock_requests_patch):
        mock_response = MockResponse(dict(), 200)
        mock_requests_patch.return_value = mock_response
        text_now_api = TextNowAPI()
        dummy_message = TextMessage(
            text=None,
            number="1111111111",
            datetime_=None,
            first_contact=None,
            message_type=None,
            read=None,
            id_="12345",
            message_direction=None,
            raw=None,
        )
        response = text_now_api.mark_message_as_read.__wrapped__(
            text_now_api, message=dummy_message
        )

        self.assertIsNone(response)

    @mock.patch("requests.delete")
    def test_delete_message_happy_path(self, mock_requests_delete):
        mock_response = MockResponse(dict(), 200)
        mock_requests_delete.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.delete_message.__wrapped__(text_now_api, message_id="12345")

        self.assertIsNone(response)

    @mock.patch("requests.get")
    def test_get_attachment_url_happy_path(self, mock_requests_get):
        mock_response_dict = {"result": "https://test"}
        mock_response = MockResponse(mock_response_dict, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_attachment_url.__wrapped__(
            text_now_api, message_type=MessageType.IMAGE
        )

        self.assertIsInstance(response, str)
        self.assertEqual("https://test", response)

    @mock.patch("requests.put")
    def test_upload_raw_media_happy_path(self, mock_requests_put):
        mock_response = MockResponse(dict(), 200)
        mock_requests_put.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.upload_raw_media.__wrapped__(
            text_now_api,
            attachment_url="https://test",
            raw_media=bytes("some_image_bytes", "utf-8"),
            media_type="image/png",
        )

        self.assertIsNone(response)

    @mock.patch("requests.post")
    def test_send_attachment_happy_path(self, mock_requests_post):
        mock_response = MockResponse(dict(), 200)
        mock_requests_post.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.send_attachment.__wrapped__(
            text_now_api,
            conversation_phone_number="1111111111",
            message_type=MessageType.IMAGE,
            file_type="image",
            is_video=False,
            attachment_url="https://test",
        )

        self.assertIsNone(response)

    @mock.patch("requests.get")
    def test_get_groups_happy_path(self, mock_requests_get):
        dummy_group = {
            "title": "group",
            "avatar": {
                "background_colour": "#000000",
                "picture": "https://test",
                "initials": "initials",
            },
            "members": [
                {
                    "contact_name": "name",
                    "contact_type": ContactType.DEFAULT.value,
                    "contact_value": "2222222222",
                    "e164_contact_value": "+2222222222",
                    "display_value": "display",
                    "avatar": {
                        "background_colour": "#111111",
                        "picture": "https://test",
                        "initials": "initials",
                    },
                }
            ],
            "contact_value": "1111111111",
            "e164_contact_value": "+1111111111",
        }
        mock_response = MockResponse([dummy_group], 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_groups.__wrapped__(text_now_api)

        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertEqual("group", response[0].title)
        self.assertEqual("#000000", response[0].avatar.background_color)
        self.assertEqual("https://test", response[0].avatar.picture)
        self.assertEqual("initials", response[0].avatar.initials)
        self.assertIsInstance(response[0].members, list)
        self.assertEqual(1, len(response[0].members))
        self.assertEqual(ContactType.DEFAULT, response[0].members[0].contact_type)
        self.assertEqual("2222222222", response[0].members[0].contact_value)
        self.assertEqual("+2222222222", response[0].members[0].e164_contact_value)
        self.assertEqual("display", response[0].members[0].display_value),
        self.assertEqual("#111111", response[0].members[0].avatar.background_color)
        self.assertEqual("https://test", response[0].members[0].avatar.picture)
        self.assertEqual("initials", response[0].members[0].avatar.initials)
        self.assertEqual("name", response[0].members[0].contact_name)
        self.assertEqual("1111111111", response[0].contact_value)
        self.assertEqual("+1111111111", response[0].e164_contact_value)

    @mock.patch("requests.get")
    def test_get_user_happy_path(self, mock_requests_get):
        dummy_user = {
            "user_id": 123,
            "username": "user",
            "email": "123@email.com",
            "phone_number": "1111111111",
        }
        mock_response = MockResponse(dummy_user, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_user.__wrapped__(text_now_api)

        self.assertIsInstance(response, User)
        self.assertEqual(123, response.user_id)
        self.assertEqual("user", response.username)
        self.assertEqual("123@email.com", response.email)
        self.assertEqual("1111111111", response.phone_number)

    @mock.patch("requests.post")
    def test_create_group_happy_path(self, mock_requests_post):
        dummy_group = {
            "title": "group",
            "avatar": {
                "background_colour": "#000000",
                "picture": "https://test",
                "initials": "initials",
            },
            "members": [
                {
                    "contact_name": "name",
                    "contact_type": ContactType.DEFAULT.value,
                    "contact_value": "2222222222",
                    "e164_contact_value": "+2222222222",
                    "display_value": "display",
                    "avatar": {
                        "background_colour": "#111111",
                        "picture": "https://test",
                        "initials": "initials",
                    },
                }
            ],
            "contact_value": "1111111111",
            "e164_contact_value": "+1111111111",
        }
        mock_response = MockResponse(dummy_group, 200)
        mock_requests_post.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.create_group.__wrapped__(text_now_api, phone_numbers=["1111111111"])

        self.assertIsInstance(response, Group)
        self.assertEqual("group", response.title)
        self.assertEqual("#000000", response.avatar.background_color)
        self.assertEqual("https://test", response.avatar.picture)
        self.assertEqual("initials", response.avatar.initials)
        self.assertIsInstance(response.members, list)
        self.assertEqual(1, len(response.members))
        self.assertEqual(ContactType.DEFAULT, response.members[0].contact_type)
        self.assertEqual("2222222222", response.members[0].contact_value)
        self.assertEqual("+2222222222", response.members[0].e164_contact_value)
        self.assertEqual("display", response.members[0].display_value),
        self.assertEqual("#111111", response.members[0].avatar.background_color)
        self.assertEqual("https://test", response.members[0].avatar.picture)
        self.assertEqual("initials", response.members[0].avatar.initials)
        self.assertEqual("name", response.members[0].contact_name)
        self.assertEqual("1111111111", response.contact_value)
        self.assertEqual("+1111111111", response.e164_contact_value)

    @mock.patch("requests.delete")
    def test_delete_conversation_happy_path(self, mock_requests_delete):
        mock_response = MockResponse(dict(), 200)
        mock_requests_delete.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.delete_conversation.__wrapped__(
            text_now_api, conversation_phone_number="+1111111111"
        )

        self.assertIsNone(response)
