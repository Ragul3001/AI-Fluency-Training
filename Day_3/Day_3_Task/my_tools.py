"""A simple calculator tool for the Day 3 task."""

import ast
import operator

# Only allow basic arithmetic operations.
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):
    """Safely evaluate a basic arithmetic expression."""

    if isinstance(node, ast.Constant) and isinstance(
        node.value, (int, float)
    ):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_evaluate(node.operand))

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Calculate a basic arithmetic expression."""

    try:
        result = _evaluate(ast.parse(expression, mode="eval").body)
        return str(result)
    except Exception as error:
        return f"Calculator error: {error}"


if __name__ == "__main__":
    print("Fee calculation:", calculator("18000 * 0.85"))
    print("Fee difference:", calculator("18000 - 12000"))