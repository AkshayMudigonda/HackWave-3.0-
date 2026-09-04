"""
Tests for Terminal tool.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.terminal.parser import TerminalParser
from tools.terminal.safety import TerminalSafety
from tools.terminal.terminal_tool import TerminalTool
from core.models import ToolRequest


class TestTerminal(unittest.TestCase):

    def setUp(self):
        self.parser = TerminalParser()
        self.safety = TerminalSafety()
        self.tool = TerminalTool()

    def test_parse_command(self):
        parsed = self.parser.parse("run dir")
        self.assertEqual(parsed["action"], "run")
        self.assertEqual(parsed["program"], "dir")

    def test_safety_blocked(self):
        self.assertFalse(self.safety.is_allowed("shutdown"))
        self.assertFalse(self.safety.is_allowed("format"))
        self.assertTrue(self.safety.is_allowed("echo"))

    def test_tool_execution(self):
        req = ToolRequest(tool="terminal", action="run", parameters={"command": "run echo Hello"})
        res = self.tool.execute(req)
        self.assertTrue(res.success)
        self.assertIn("Hello", res.message)


if __name__ == "__main__":
    unittest.main()
