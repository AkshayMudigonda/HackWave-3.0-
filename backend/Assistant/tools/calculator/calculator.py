"""
Core calculator logic for evaluating mathematical expressions.
"""
import ast
import operator


class Calculator:

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression: str):

        expression = expression.lower()

        for prefix in [
            "what is",
            "calculate",
            "compute",
        ]:
            if expression.startswith(prefix):
                expression = expression[len(prefix):].strip()

        expression = expression.replace("^", "**")

        tree = ast.parse(
            expression,
            mode="eval",
        )

        return self._evaluate(tree.body)

    def _evaluate(self, node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

        if isinstance(node, ast.BinOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator.")

            return operation(
                self._evaluate(node.operand)
            )

        raise ValueError("Invalid mathematical expression.")