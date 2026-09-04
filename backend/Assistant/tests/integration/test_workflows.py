import unittest
from agent.agent import Agent
from tools.tool_manager import ToolManager


class TestWorkflows(unittest.TestCase):
    def test_system_health_workflow(self):
        result = Agent(ToolManager(), llm_client=None).run("Check my system health and tell me if anything needs attention")
        self.assertIn("TASK:", result)
        self.assertIn("Metrics collected", result)

    def test_travel_never_fabricates_integrations(self):
        result = Agent(ToolManager(), llm_client=None).run("Plan a trip to Hyderabad")
        self.assertIn("not configured", result.lower())
