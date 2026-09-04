"""
Calculator tool: evaluates arithmetic/mathematical expressions.
"""
from core.results import success, failure
from tools.calculator.calculator import Calculator


class CalculatorTool:

    def __init__(self):
        self.calculator = Calculator()

    def execute(self, request):

        if request.action != "calculate":
            return failure(
                "Unsupported calculator action.",
                tool="calculator",
                action=request.action,
            )

        try:
            expression = request.parameters["expression"]

            result = self.calculator.calculate(
                expression
            )

            return success(
                str(result),
                data=result,
                tool="calculator",
                action="calculate",
            )

        except ZeroDivisionError:
            return failure(
                "Division by zero is not allowed.",
                tool="calculator",
                action="calculate",
            )

        except Exception as exc:
            return failure(
                f"Invalid calculation: {exc}",
                tool="calculator",
                action="calculate",
            )