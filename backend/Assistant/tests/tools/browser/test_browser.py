"""
Tests for Browser tool.
"""
import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.browser.parser import BrowserParser
from tools.browser.browser_tool import BrowserTool
from core.models import ToolRequest


class TestBrowser(unittest.TestCase):

    def setUp(self):
        self.parser = BrowserParser()
        self.tool = BrowserTool()

    def test_parse_open_site(self):
        parsed = self.parser.parse("open google")
        self.assertEqual(parsed["action"], "open")
        self.assertEqual(parsed["url"], "https://www.google.com")

    def test_parse_search_query(self):
        parsed = self.parser.parse("search python asyncio")
        self.assertEqual(parsed["action"], "search")
        self.assertIn("python+asyncio", parsed["url"])

    @patch("tools.browser.operations.BrowserOperations.open", return_value=True)
    def test_tool_execution(self, mock_open):
        req = ToolRequest(tool="browser", action="parse_and_execute", parameters={"command": "open github"})
        res = self.tool.execute(req)
        self.assertTrue(res.success)
        mock_open.assert_called_once()


if __name__ == "__main__":
    unittest.main()
