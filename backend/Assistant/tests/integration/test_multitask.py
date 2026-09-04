"""
Integration tests for multitasking text input execution.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.agent import Agent
from tools.tool_manager import ToolManager
from tools.calculator.calculator_tool import CalculatorTool
from tools.datetime.datetime_tool import DateTimeTool
from tools.terminal.terminal_tool import TerminalTool


class TestMultitaskIntegration(unittest.TestCase):

    def setUp(self):
        manager = ToolManager()
        manager.register("calculator", CalculatorTool())
        manager.register("datetime", DateTimeTool())
        manager.register("terminal", TerminalTool())
        # Provide agent with llm_client=None to test deterministic decomposition
        self.agent = Agent(manager, llm_client=None)

    def test_dual_task_math_and_date(self):
        response = self.agent.run("25 * 4 and today")
        self.assertIn("1. 100", response)
        self.assertIn("2.", response)

    def test_triple_task_execution(self):
        response = self.agent.run("10 + 5, 20 * 2, and run echo Multitask Done")
        self.assertIn("1. 15", response)
        self.assertIn("2. 40", response)
        self.assertIn("3. Multitask Done", response)


if __name__ == "__main__":
    unittest.main()
