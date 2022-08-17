import os
import unittest
from unittest import mock

from pythontextnow.api.Client import Client
from pythontextnow.api.TextNowAPI import TextNowAPI
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
    def test_send_message_happy_path(self, mock_requests_get):
        mock_response = MockResponse(dict(), 200)
        mock_requests_get.return_value = mock_response
        text_now_api = TextNowAPI()
        response = text_now_api.send_message(message="hello world", send_to="5555555555")

        self.assertIsNone(response)
