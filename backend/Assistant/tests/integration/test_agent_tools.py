"""
Integration tests covering the agent's interaction with individual tools.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.agent import Agent
from tools.tool_manager import ToolManager
from tools.calculator.calculator_tool import CalculatorTool
from tools.datetime.datetime_tool import DateTimeTool
from tools.filesystem.filesystem_tool import FilesystemTool
from tools.terminal.terminal_tool import TerminalTool


class TestAgentToolsIntegration(unittest.TestCase):

    def setUp(self):
        manager = ToolManager()
        manager.register("calculator", CalculatorTool())
        manager.register("datetime", DateTimeTool())
        manager.register("filesystem", FilesystemTool())
        manager.register("terminal", TerminalTool())
        self.agent = Agent(manager)

    def test_calculator_execution(self):
        result = self.agent.run("15 * 3")
        self.assertEqual(result, "45")

    def test_datetime_execution(self):
        result = self.agent.run("current time")
        self.assertTrue(len(result) > 0)

    def test_terminal_allowed_execution(self):
        result = self.agent.run("run echo Hello World")
        self.assertIn("Hello World", result)


if __name__ == "__main__":
    unittest.main()
