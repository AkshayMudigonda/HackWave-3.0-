"""
Tests for core.models.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.models import ToolRequest, ToolResult, AgentObservation, AgentResponse
from core.results import success, failure, success_result, failure_result


class TestModels(unittest.TestCase):

    def test_tool_request(self):
        req = ToolRequest(tool="calculator", action="calculate", parameters={"expression": "2+2"})
        self.assertEqual(req.tool, "calculator")
        self.assertEqual(req.action, "calculate")
        self.assertEqual(req.parameters["expression"], "2+2")

    def test_tool_result_success(self):
        res = success("Calculation done", data=4)
        self.assertTrue(res.success)
        self.assertEqual(res.data, 4)
        self.assertEqual(res.message, "Calculation done")

    def test_tool_result_failure(self):
        res = failure("Division by zero", error="ZeroDivisionError")
        self.assertFalse(res.success)
        self.assertEqual(res.message, "Division by zero")
        self.assertEqual(res.error, "ZeroDivisionError")

    def test_agent_observation(self):
        obs = AgentObservation(tool="datetime", success=True, data="Friday", message="Today is Friday")
        self.assertEqual(obs.tool, "datetime")
        self.assertTrue(obs.success)
        self.assertEqual(obs.data, "Friday")

    def test_agent_response(self):
        resp = AgentResponse(success=True, message="Result is 4")
        self.assertTrue(resp.success)
        self.assertEqual(resp.message, "Result is 4")


if __name__ == "__main__":
    unittest.main()
