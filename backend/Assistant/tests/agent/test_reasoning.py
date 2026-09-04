"""
Tests for agent.reasoning.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from agent.reasoning import Reasoning
from tools.tool_manager import ToolManager


class TestReasoning(unittest.TestCase):

    def setUp(self):
        self.reasoning = Reasoning(ToolManager())

    def test_classify_calculator(self):
        self.assertEqual(self.reasoning.classify("2 + 2"), "calculator")
        self.assertEqual(self.reasoning.classify("calculate 10 * 5"), "calculator")
        self.assertEqual(self.reasoning.classify("100 / 4"), "calculator")

    def test_classify_datetime(self):
        self.assertEqual(self.reasoning.classify("today"), "datetime")
        self.assertEqual(self.reasoning.classify("what time is it"), "datetime")
        self.assertEqual(self.reasoning.classify("current date"), "datetime")

    def test_classify_browser(self):
        self.assertEqual(self.reasoning.classify("open google"), "browser")
        self.assertEqual(self.reasoning.classify("search python tutorials"), "browser")
        self.assertEqual(self.reasoning.classify("youtube lofi music"), "browser")
        self.assertEqual(self.reasoning.classify("github whisper"), "browser")
        self.assertEqual(self.reasoning.classify("wikipedia alan turing"), "browser")
        self.assertEqual(self.reasoning.classify("maps hyderabad"), "browser")

    def test_classify_applications(self):
        self.assertEqual(self.reasoning.classify("open notepad"), "applications")
        self.assertEqual(self.reasoning.classify("launch vscode"), "applications")
        self.assertEqual(self.reasoning.classify("close chrome"), "applications")

    def test_classify_filesystem(self):
        self.assertEqual(self.reasoning.classify("create folder my_test"), "filesystem")
        self.assertEqual(self.reasoning.classify("create file hello.txt"), "filesystem")
        self.assertEqual(self.reasoning.classify("list ."), "filesystem")

    def test_classify_terminal(self):
        self.assertEqual(self.reasoning.classify("run dir"), "terminal")
        self.assertEqual(self.reasoning.classify("execute whoami"), "terminal")


if __name__ == "__main__":
    unittest.main()
