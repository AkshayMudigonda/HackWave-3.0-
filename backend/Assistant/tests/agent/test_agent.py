"""
Tests for agent.agent.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.agent import Agent
from tools.tool_manager import ToolManager
from tools.calculator.calculator_tool import CalculatorTool
from tools.datetime.datetime_tool import DateTimeTool


class TestAgent(unittest.TestCase):

    def setUp(self):
        manager = ToolManager()
        manager.register("calculator", CalculatorTool())
        manager.register("datetime", DateTimeTool())
        self.agent = Agent(manager)

    def test_calculator(self):
        result = self.agent.run("2 + 2")
        self.assertIn("4", result)

    def test_datetime(self):
        result = self.agent.run("today")
        self.assertTrue(len(result) > 0)

    def test_empty_input(self):
        result = self.agent.run("")
        self.assertEqual(result, "Please enter a command.")

    def test_unknown_command_with_llm(self):
        result = self.agent.run("xyzunknown123")
        self.assertTrue(len(result) > 0)

    def test_unknown_command_without_llm(self):
        agent_no_llm = Agent(self.agent.tool_manager, llm_client=None)
        agent_no_llm.llm_client = None
        result = agent_no_llm.run("xyzunknown123")
        self.assertEqual(result, "I couldn't understand that request.")



if __name__ == "__main__":
    unittest.main()