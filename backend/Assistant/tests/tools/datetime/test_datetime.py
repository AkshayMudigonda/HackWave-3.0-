"""
Tests for DateTime tool.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.datetime.datetime import DateTime
from tools.datetime.datetime_tool import DateTimeTool
from core.models import ToolRequest


class TestDateTime(unittest.TestCase):

    def setUp(self):
        self.dt = DateTime()
        self.tool = DateTimeTool()

    def test_get_today(self):
        result = self.dt.get("today")
        self.assertTrue(len(result) > 0)

    def test_get_time(self):
        result = self.dt.get("time")
        self.assertTrue(":" in result)

    def test_tool_execution(self):
        req = ToolRequest(tool="datetime", action="get", parameters={"query": "date"})
        res = self.tool.execute(req)
        self.assertTrue(res.success)
        self.assertIsNotNone(res.data)


if __name__ == "__main__":
    unittest.main()
