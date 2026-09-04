"""
Tests for agent.planner.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.reasoning import Reasoning
from agent.planner import Planner
from tools.tool_manager import ToolManager


class TestPlanner(unittest.TestCase):

    def setUp(self):
        self.reasoning = Reasoning(ToolManager())
        self.planner = Planner(self.reasoning)

    def test_create_plan_calculator(self):
        plan = self.planner.create_plan("2 + 2")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.tool, "calculator")
        self.assertEqual(plan.action, "calculate")
        self.assertEqual(plan.parameters["expression"], "2 + 2")

    def test_create_plan_datetime(self):
        plan = self.planner.create_plan("today")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.tool, "datetime")
        self.assertEqual(plan.action, "get")

    def test_create_plan_browser(self):
        plan = self.planner.create_plan("search python")
        self.assertIsNotNone(plan)
        self.assertEqual(plan.tool, "browser")
        self.assertEqual(plan.parameters["command"], "search python")

    def test_create_multi_plan_compound(self):
        plans = self.planner.create_multi_plan("calculate 10 * 5 and what date is it today")
        self.assertEqual(len(plans), 2)
        self.assertEqual(plans[0].tool, "calculator")
        self.assertEqual(plans[1].tool, "datetime")

    def test_create_multi_plan_three_tasks(self):
        plans = self.planner.create_multi_plan("2 + 2, open google, and today")
        self.assertEqual(len(plans), 3)
        self.assertEqual(plans[0].tool, "calculator")
        self.assertEqual(plans[1].tool, "browser")
        self.assertEqual(plans[2].tool, "datetime")

    def test_create_plan_unknown(self):
        plan = self.planner.create_plan("asdf1234unknowncommandxyz")
        self.assertIsNone(plan)


if __name__ == "__main__":
    unittest.main()
