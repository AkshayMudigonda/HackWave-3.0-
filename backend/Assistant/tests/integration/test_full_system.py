"""
End-to-end integration tests exercising the full assistant pipeline.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.agent import Agent
from tools.tool_manager import ToolManager
from tools.calculator.calculator_tool import CalculatorTool
from tools.datetime.datetime_tool import DateTimeTool
from tools.browser.browser_tool import BrowserTool
from tools.applications.applications_tool import ApplicationsTool
from tools.filesystem.filesystem_tool import FilesystemTool
from tools.terminal.terminal_tool import TerminalTool


def create_system():
    manager = ToolManager()
    manager.register("calculator", CalculatorTool())
    manager.register("datetime", DateTimeTool())
    manager.register("browser", BrowserTool())
    manager.register("applications", ApplicationsTool())
    manager.register("filesystem", FilesystemTool())
    manager.register("terminal", TerminalTool())
    return Agent(manager)


class TestFullSystem(unittest.TestCase):

    def setUp(self):
        self.agent = create_system()

    def test_calculator_commands(self):
        response = self.agent.run("2 + 2")
        self.assertEqual(response, "4")

    def test_datetime_commands(self):
        response = self.agent.run("today")
        self.assertTrue(len(response) > 0)

    def test_unknown_command(self):
        agent_no_llm = create_system()
        agent_no_llm.llm_client = None
        response = agent_no_llm.run("gibberish nonexistent query 12345")
        self.assertEqual(response, "I couldn't understand that request.")



if __name__ == "__main__":
    unittest.main()