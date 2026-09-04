"""
Tests for core.task.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.task import Task


class TestTask(unittest.TestCase):

    def test_task_lifecycle(self):
        task = Task(query="2 + 2")
        self.assertEqual(task.status, "CREATED")
        self.assertIsNone(task.result)

        task.tool = "calculator"
        task.status = "completed"
        task.result = 4
        self.assertEqual(task.result, 4)
        self.assertEqual(task.status, "completed")


if __name__ == "__main__":
    unittest.main()
