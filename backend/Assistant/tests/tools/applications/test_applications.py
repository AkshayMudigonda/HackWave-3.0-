"""
Tests for Applications tool.
"""
import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.applications.parser import ApplicationParser
from tools.applications.registry import ApplicationRegistry
from tools.applications.applications_tool import ApplicationsTool
from core.models import ToolRequest


class TestApplications(unittest.TestCase):

    def setUp(self):
        self.parser = ApplicationParser()
        self.registry = ApplicationRegistry()
        self.tool = ApplicationsTool()

    def test_parse_open(self):
        parsed = self.parser.parse("open notepad")
        self.assertEqual(parsed["action"], "open")
        self.assertEqual(parsed["application"], "notepad")

    def test_registry_lookup(self):
        app = self.registry.find("notepad")
        self.assertIsNotNone(app)
        self.assertEqual(app["name"], "Notepad")

    @patch("tools.applications.process_manager.ProcessManager.open", return_value=True)
    def test_tool_execution(self, mock_open):
        req = ToolRequest(tool="applications", action="parse_and_execute", parameters={"command": "open notepad"}, original_input="open notepad")
        res = self.tool.execute(req)
        self.assertTrue(res.success)
        mock_open.assert_called_once()


if __name__ == "__main__":
    unittest.main()
