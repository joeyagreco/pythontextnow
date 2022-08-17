import datetime
import os
import unittest
from unittest import mock

from pythontextnow.api.Client import Client
from pythontextnow.api.TextNowAPI import TextNowAPI
from pythontextnow.enum import MessageType, MessageDirection
from pythontextnow.model.MultiMediaMessage import MultiMediaMessage
from pythontextnow.model.TextMessage import TextMessage
from test.helper.helper_classes import MockResponse


class TestTextNowAPI(unittest.TestCase):
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
        Client.set_client_config(username="dummy_username",
                                 csrf_cookie="dummy_csrf_cookie",
                                 sid_cookie="dummy_sid_cookie")

    @mock.patch("requests.get")
    def test_get_csrf_token_happy_path(self, mock_requests_get):
        # get dummy messaging page as a string
        with open(os.path.join(self.PATH_TO_DATA_DIR, "dummy_messaging_page.html")) as f:
            dummy_messaging_page_lines = f.readlines()
        dummy_messaging_page_str = "\n".join(dummy_messaging_page_lines)

        mock_response = MockResponse(dict(), 200, text=dummy_messaging_page_str)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_csrf_token(dict())

        self.assertIsInstance(response, str)
        self.assertEqual("dummy_csrf_token", response)

    @mock.patch("requests.post")
    def test_send_message_happy_path(self, mock_requests_post):
        mock_response = MockResponse(dict(), 200)
        mock_requests_post.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.send_message(message="hello world", send_to="5555555555")

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
            "conversation_filtering": {
                "first_time_contact": True
            }
        }
        mock_response_dict = {
            "status": {},
            "messages": [
                mock_message_dict
            ]
        }
        mock_response = MockResponse(mock_response_dict, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_messages(conversation_phone_number="1111111111", page_size=10, get_archived=True)

        message = response[0]
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertIsInstance(message, TextMessage)
        self.assertEqual("id", message.id_)
        self.assertEqual("contact_value", message.number)
        self.assertEqual(datetime.datetime(2000, 1, 1, 1, 1, tzinfo=datetime.timezone.utc), message.datetime_)
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
            "conversation_filtering": {
                "first_time_contact": True
            }
        }
        mock_response_dict = {
            "status": {},
            "messages": [
                mock_message_dict
            ]
        }
        mock_response = MockResponse(mock_response_dict, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_messages(conversation_phone_number="1111111111", page_size=10, get_archived=True)

        message = response[0]
        self.assertIsInstance(response, list)
        self.assertEqual(1, len(response))
        self.assertIsInstance(message, MultiMediaMessage)
        self.assertEqual("id", message.id_)
        self.assertEqual("contact_value", message.number)
        self.assertEqual(datetime.datetime(2000, 1, 1, 1, 1, tzinfo=datetime.timezone.utc), message.datetime_)
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
        dummy_message = TextMessage(text=None,
                                    number="1111111111",
                                    datetime_=None,
                                    first_contact=None,
                                    message_type=None,
                                    read=None,
                                    id_="12345",
                                    message_direction=None,
                                    raw=None)
        response = text_now_api.mark_message_as_read(message=dummy_message)

        self.assertIsNone(response)

    @mock.patch("requests.delete")
    def test_delete_message_happy_path(self, mock_requests_delete):
        mock_response = MockResponse(dict(), 200)
        mock_requests_delete.return_value = mock_response
        text_now_api = TextNowAPI()
        dummy_message = TextMessage(text=None,
                                    number=None,
                                    datetime_=None,
                                    first_contact=None,
                                    message_type=None,
                                    read=None,
                                    id_="12345",
                                    message_direction=None,
                                    raw=None)
        response = text_now_api.delete_message(message=dummy_message)

        self.assertIsNone(response)

    @mock.patch("requests.get")
    def test_get_attachment_url_happy_path(self, mock_requests_get):
        mock_response_dict = {
            "result": "https://test"
        }
        mock_response = MockResponse(mock_response_dict, 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.get_attachment_url(message_type=MessageType.IMAGE)

        self.assertIsInstance(response, str)
        self.assertEqual("https://test", response)
