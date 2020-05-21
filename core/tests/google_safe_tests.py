import unittest
from core.google_safe_browsing import GoogleSafeBrowsing
from unittest.mock import patch, MagicMock
import json
import requests


class GoogleSafeBrowsingTests(unittest.TestCase):

    TEST_KEY = "ducks123"
    EXAMPLE_RESPONSE = {"test": "test response"}

    def setUp(self) -> None:
        self.g_safe = GoogleSafeBrowsing(api_key=self.TEST_KEY)

    @patch('requests.post')
    def test_api_call(self, post_mock):
        response = MagicMock
        response.status_code = 200
        response.text = json.dumps(self.EXAMPLE_RESPONSE)
        post_mock.return_value = response

        is_safe, details = self.g_safe.api_call(['test_url'])
        post_mock.assert_called()
        self.assertFalse(is_safe)
        self.assertDictEqual(self.EXAMPLE_RESPONSE, details)

        response.status_code = 404
        with self.assertRaises(requests.HTTPError):
            self.g_safe.api_call(['test'])
