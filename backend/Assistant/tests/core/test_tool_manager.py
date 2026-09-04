"""
Tests for core.tool_manager.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from tools.tool_manager import ToolManager
from tools.calculator.calculator_tool import CalculatorTool
from core.models import ToolRequest


class TestToolManager(unittest.TestCase):

    def setUp(self):
        self.manager = ToolManager()
        self.manager.register("calculator", CalculatorTool())

    def test_tool_manager_registration(self):
        self.assertTrue(self.manager.has_tool("calculator"))
        self.assertIn("calculator", self.manager.list_tools())

    def test_tool_manager_execution(self):
        request = ToolRequest(
            tool="calculator",
            action="calculate",
            parameters={"expression": "2 + 2"},
        )
        result = self.manager.execute(request)
        self.assertTrue(result.success)
        self.assertEqual(result.data, 4)

    def test_tool_manager_missing_tool(self):
        request = ToolRequest(
            tool="non_existent",
            action="do_something",
            parameters={},
        )
        result = self.manager.execute(request)
        self.assertFalse(result.success)


if __name__ == "__main__":
    unittest.main()