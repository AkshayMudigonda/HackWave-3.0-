"""
Tests for Calculator tool.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from tools.calculator.calculator import Calculator
from tools.calculator.calculator_tool import CalculatorTool
from core.models import ToolRequest


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()
        self.tool = CalculatorTool()

    def test_basic_arithmetic(self):
        self.assertEqual(self.calculator.calculate("2 + 2"), 4)
        self.assertEqual(self.calculator.calculate("10 - 3"), 7)
        self.assertEqual(self.calculator.calculate("6 * 7"), 42)
        self.assertEqual(self.calculator.calculate("100 / 5"), 20.0)
        self.assertEqual(self.calculator.calculate("2 ^ 3"), 8)

    def test_tool_execution(self):
        req = ToolRequest(tool="calculator", action="calculate", parameters={"expression": "5 * 5"})
        res = self.tool.execute(req)
        self.assertTrue(res.success)
        self.assertEqual(res.data, 25)

    def test_division_by_zero(self):
        req = ToolRequest(tool="calculator", action="calculate", parameters={"expression": "1 / 0"})
        res = self.tool.execute(req)
        self.assertFalse(res.success)
        self.assertIn("Division by zero", res.message)


if __name__ == "__main__":
    unittest.main()
