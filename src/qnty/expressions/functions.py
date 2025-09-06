"""
Expression Helper Functions
==========================

Convenience functions for creating mathematical expressions.
"""

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..quantities import FieldQnty, Quantity
    from .nodes import BinaryOperation, Expression

from .nodes import ConditionalExpression, Expression, UnaryFunction, wrap_operand


# Convenience functions for mathematical operations
def sin(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Sine function."""
    return UnaryFunction("sin", wrap_operand(expr))


def cos(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Cosine function."""
    return UnaryFunction("cos", wrap_operand(expr))


def tan(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Tangent function."""
    return UnaryFunction("tan", wrap_operand(expr))


def sqrt(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Square root function."""
    return UnaryFunction("sqrt", wrap_operand(expr))


def abs_expr(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Absolute value function."""
    return UnaryFunction("abs", wrap_operand(expr))


def ln(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Natural logarithm function."""
    return UnaryFunction("ln", wrap_operand(expr))


def log10(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Base-10 logarithm function."""
    return UnaryFunction("log10", wrap_operand(expr))


def exp(expr: Union["Expression", "FieldQnty", "Quantity", int, float]) -> UnaryFunction:
    """Exponential function."""
    return UnaryFunction("exp", wrap_operand(expr))


def cond_expr(
    condition: Union["Expression", "BinaryOperation"],
    true_expr: Union["Expression", "FieldQnty", "Quantity", int, float],
    false_expr: Union["Expression", "FieldQnty", "Quantity", int, float],
) -> ConditionalExpression:
    """Conditional expression: if condition then true_expr else false_expr."""
    return ConditionalExpression(condition if isinstance(condition, Expression) else condition, wrap_operand(true_expr), wrap_operand(false_expr))


def min_expr(*expressions: Union["Expression", "FieldQnty", "Quantity", int, float]) -> "Expression":
    """Minimum of multiple expressions."""
    if len(expressions) < 2:
        raise ValueError("min_expr requires at least 2 arguments")

    wrapped_expressions = [wrap_operand(expr) for expr in expressions]
    result = wrapped_expressions[0]

    for expr in wrapped_expressions[1:]:
        # min(a, b) = if(a < b, a, b)
        result = cond_expr(result < expr, result, expr)

    return result


def max_expr(*expressions: Union["Expression", "FieldQnty", "Quantity", int, float]) -> "Expression":
    """Maximum of multiple expressions."""
    if len(expressions) < 2:
        raise ValueError("max_expr requires at least 2 arguments")

    wrapped_expressions = [wrap_operand(expr) for expr in expressions]
    result = wrapped_expressions[0]

    for expr in wrapped_expressions[1:]:
        # max(a, b) = if(a > b, a, b)
        result = cond_expr(result > expr, result, expr)

    return result
