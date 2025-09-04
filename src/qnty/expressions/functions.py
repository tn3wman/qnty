"""
Expression Helper Functions
==========================

Convenience functions for creating mathematical expressions.
"""

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..quantities.core import FastQuantity, TypeSafeVariable
    from .nodes import Expression, BinaryOperation

from .nodes import Expression, UnaryFunction, ConditionalExpression


# Convenience functions for mathematical operations
def sin(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Sine function."""
    return UnaryFunction('sin', Expression._wrap_operand(expr))


def cos(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Cosine function."""
    return UnaryFunction('cos', Expression._wrap_operand(expr))


def tan(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Tangent function."""
    return UnaryFunction('tan', Expression._wrap_operand(expr))


def sqrt(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Square root function."""
    return UnaryFunction('sqrt', Expression._wrap_operand(expr))


def abs_expr(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Absolute value function."""
    return UnaryFunction('abs', Expression._wrap_operand(expr))


def ln(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Natural logarithm function."""
    return UnaryFunction('ln', Expression._wrap_operand(expr))


def log10(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Base-10 logarithm function."""
    return UnaryFunction('log10', Expression._wrap_operand(expr))


def exp(expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> UnaryFunction:
    """Exponential function."""
    return UnaryFunction('exp', Expression._wrap_operand(expr))


def cond_expr(condition: Union['Expression', 'BinaryOperation'],
              true_expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float],
              false_expr: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> ConditionalExpression:
    """Conditional expression: if condition then true_expr else false_expr."""
    return ConditionalExpression(
        condition if isinstance(condition, Expression) else condition,
        Expression._wrap_operand(true_expr),
        Expression._wrap_operand(false_expr)
    )


def min_expr(*expressions: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> 'Expression':
    """Minimum of multiple expressions."""
    if len(expressions) < 2:
        raise ValueError("min_expr requires at least 2 arguments")
    
    wrapped_expressions = [Expression._wrap_operand(expr) for expr in expressions]
    result = wrapped_expressions[0]
    
    for expr in wrapped_expressions[1:]:
        # min(a, b) = if(a < b, a, b)
        result = cond_expr(result < expr, result, expr)
    
    return result


def max_expr(*expressions: Union['Expression', 'TypeSafeVariable', 'FastQuantity', int, float]) -> 'Expression':
    """Maximum of multiple expressions."""
    if len(expressions) < 2:
        raise ValueError("max_expr requires at least 2 arguments")
    
    wrapped_expressions = [Expression._wrap_operand(expr) for expr in expressions]
    result = wrapped_expressions[0]
    
    for expr in wrapped_expressions[1:]:
        # max(a, b) = if(a > b, a, b)
        result = cond_expr(result > expr, result, expr)
    
    return result