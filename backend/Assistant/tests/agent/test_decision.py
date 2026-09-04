"""
Tests for agent.decision.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.decision import Decision
from core.models import AgentObservation, ToolResult


class TestDecision(unittest.TestCase):

    def setUp(self):
        self.decision = Decision()

    def test_format_response_success_message(self):
        obs = AgentObservation(tool="browser", success=True, message="Opening google.")
        self.assertEqual(self.decision.format_response(obs), "Opening google.")

    def test_format_response_success_data(self):
        obs = AgentObservation(tool="calculator", success=True, data=4, message="")
        self.assertEqual(self.decision.format_response(obs), "4")

    def test_format_response_failure(self):
        obs = AgentObservation(tool="calculator", success=False, message="Division by zero", error="ZeroDivisionError")
        self.assertEqual(self.decision.format_response(obs), "Division by zero")

    def test_format_response_none(self):
        self.assertEqual(self.decision.format_response(None), "I couldn't understand that request.")


if __name__ == "__main__":
    unittest.main()
