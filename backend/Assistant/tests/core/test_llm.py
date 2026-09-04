"""
Tests for Featherless AI client and configuration.
"""
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.llm import FeatherlessClient
from core import config


class TestFeatherlessClient(unittest.TestCase):

    def test_config_loaded(self):
        self.assertIsInstance(config.FEATHERLESS_API_KEY, str)
        self.assertIn("featherless.ai", config.FEATHERLESS_BASE_URL)

    @patch("urllib.request.urlopen")
    def test_chat_completion_mock(self, mock_urlopen):
        mock_resp = MagicMock()
        mock_resp.read.return_value = b'{"choices": [{"message": {"content": "Hello there!"}}]}'
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        client = FeatherlessClient(api_key="test_key")
        result = client.ask("Hi")
        self.assertEqual(result, "Hello there!")


if __name__ == "__main__":
    unittest.main()
