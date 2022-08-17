import os
import unittest
from unittest import mock

from pythontextnow.api.TextNowAPI import TextNowAPI
from test.helper.helper_classes import MockResponse


class TestTextNowAPI(unittest.TestCase):
    PATH_TO_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))

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
