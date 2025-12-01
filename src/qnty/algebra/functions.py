"""
Expression Helper Functions
==========================

Convenience functions for creating mathematical expressions.
"""

from collections.abc import Callable

from ..core.quantity import FieldQuantity, Quantity
from ..utils.shared_utilities import ContextDetectionHelper
from .nodes import BinaryOperation, ConditionalExpression, Expression, UnaryFunction, wrap_operand

# Type aliases for better maintainability
ExpressionOperand = Expression | FieldQuantity | Quantity | int | float
ConditionalOperand = Expression | BinaryOperation


# Use shared context detection
_should_preserve_symbolic_expression = ContextDetectionHelper.should_preserve_symbolic_expression


def _create_unary_function(name: str, docstring: str) -> "Callable[[ExpressionOperand], Expression | Quantity | float]":
    """Factory function for creating unary mathematical functions."""

    def func(expr: ExpressionOperand) -> Expression | Quantity | float:
        # Check if we should preserve symbolic expressions (in class definition context)
        if _should_preserve_symbolic_expression():
            from ..problems.composition import DelayedFunction

            return DelayedFunction(name, expr)

        wrapped_expr = wrap_operand(expr)

        # For known quantities (FieldQnty with known values), check context before auto-evaluating
        should_auto_evaluate = False
        if hasattr(expr, "quantity") and getattr(expr, "quantity", None) is not None:
            should_auto_evaluate = True
        # Also auto-evaluate for Quantity objects with values
        elif hasattr(expr, "value") and hasattr(expr, "dim") and getattr(expr, "value", None) is not None:
            should_auto_evaluate = True

        if should_auto_evaluate:
            # No Problem class context found, safe to auto-evaluate
            try:
                unary_func = UnaryFunction(name, wrapped_expr)
                # Use an empty variable dict since we have the quantity directly
                result = unary_func.evaluate({})
                return result
            except (ValueError, TypeError, AttributeError):
                # Fall back to expression if evaluation fails
                pass

        # For unknown variables or expressions, return the UnaryFunction
        return UnaryFunction(name, wrapped_expr)

    func.__name__ = name
    func.__doc__ = docstring
    return func


def _create_comparison_expr(expressions: tuple[ExpressionOperand, ...], comparator: str) -> Expression:
    """Create min/max expression using specified comparator."""
    if len(expressions) < 2:
        raise ValueError(f"{comparator}_expr requires at least 2 arguments")

    wrapped_expressions = [wrap_operand(expr) for expr in expressions]
    result = wrapped_expressions[0]

    for expr in wrapped_expressions[1:]:
        if comparator == "min":
            # min(a, b) = if(a < b, a, b)
            result = cond_expr(result < expr, result, expr)
        else:  # max
            # max(a, b) = if(a > b, a, b)
            result = cond_expr(result > expr, result, expr)

    return result


# Mathematical functions (generated via factory)
sin = _create_unary_function("sin", "Sine function.")
cos = _create_unary_function("cos", "Cosine function.")
tan = _create_unary_function("tan", "Tangent function.")
sqrt = _create_unary_function("sqrt", "Square root function.")
abs_expr = _create_unary_function("abs", "Absolute value function.")
ln = _create_unary_function("ln", "Natural logarithm function.")
log10 = _create_unary_function("log10", "Base-10 logarithm function.")
exp = _create_unary_function("exp", "Exponential function.")


def cond_expr(
    condition: ConditionalOperand,
    true_expr: ExpressionOperand,
    false_expr: ExpressionOperand,
) -> ConditionalExpression | Expression:
    """Conditional expression: if condition then true_expr else false_expr."""
    # Check if we should preserve symbolic expressions (in class definition context)
    if _should_preserve_symbolic_expression():
        from ..problems.composition import DelayedFunction

        return DelayedFunction("cond_expr", condition, true_expr, false_expr)
    wrapped_condition = condition if isinstance(condition, Expression) else condition
    return ConditionalExpression(wrapped_condition, wrap_operand(true_expr), wrap_operand(false_expr))


def _create_expr_function(func_name: str, comparator: str):
    """Factory function to create min/max expression functions."""

    def expr_func(*expressions: ExpressionOperand) -> Expression:
        # Check if we should preserve symbolic expressions (in class definition context)
        if _should_preserve_symbolic_expression():
            from ..problems.composition import DelayedFunction

            return DelayedFunction(func_name, *expressions)
        return _create_comparison_expr(expressions, comparator)

    expr_func.__name__ = func_name
    expr_func.__doc__ = f"{comparator.title()} of multiple expressions."
    return expr_func


min_expr = _create_expr_function("min_expr", "min")
max_expr = _create_expr_function("max_expr", "max")


def sum_expr(*expressions: ExpressionOperand) -> Expression:
    """
    Sum of multiple expressions.

    Accepts either individual expressions as arguments, or a single iterable of expressions.

    Args:
        *expressions: Variable number of expressions to sum, or a single iterable of expressions

    Returns:
        Expression representing the sum of all input expressions

    Examples:
        >>> from qnty import Length, sum_expr
        >>> x = Length("x")
        >>> y = Length("y")
        >>> z = Length("z")
        >>> total = sum_expr(x, y, z)  # equivalent to x + y + z

        >>> # Using with a list or generator
        >>> terms = [x * i for i in range(3)]
        >>> result = sum_expr(terms)  # sum of list elements
    """
    # Handle case where a single iterable is passed
    if len(expressions) == 1:
        try:
            # Check if it's iterable (but not a string or Quantity)
            from collections.abc import Iterable

            if isinstance(expressions[0], Iterable) and not isinstance(expressions[0], str | Quantity | FieldQuantity):
                expressions = tuple(expressions[0])
        except (TypeError, ImportError):
            pass

    if len(expressions) == 0:
        raise ValueError("sum_expr requires at least 1 argument")

    # Check if we should preserve symbolic expressions (in class definition context)
    if _should_preserve_symbolic_expression():
        from ..problems.composition import DelayedFunction

        return DelayedFunction("sum_expr", *expressions)

    # Build the sum expression
    wrapped_expressions = [wrap_operand(expr) for expr in expressions]
    result = wrapped_expressions[0]

    for expr in wrapped_expressions[1:]:
        result = result + expr

    return result


def summation(term_generator, *range_specs, **kwargs):
    """
    Create a generic summation expression using a lambda/callable to generate terms.

    This function defers term generation until after Problem class initialization,
    allowing you to write clean summation expressions without manual expansion.

    Args:
        term_generator: A callable that takes (indices..., **captured_vars) and returns an expression.
                       For example: lambda i, j, M, x, y: M[i,j] * x**i * y**j
        *range_specs: Variable number of range specifications. Each can be:
                     - An integer (creates range(n))
                     - A tuple (start, stop) or (start, stop, step)
                     - A range object
        **kwargs: Variables to pass to term_generator. This makes linters happy by
                 explicitly passing captured variables.

    Returns:
        Expression representing the summation

    Examples:
        >>> import numpy as np
        >>> from qnty import Dimensionless, summation
        >>> M = np.array([[1, 2, 3], [4, 5, 6]])
        >>> x = Dimensionless("x")
        >>> y = Dimensionless("y")
        >>>
        >>> # Example 1: 2D summation with coefficient matrix (explicit variables)
        >>> # Σ_ij M[i,j] * x^i * y^j for i=0,1 and j=0,1,2
        >>> result = summation(lambda i, j, M, x, y: M[i,j] * x**i * y**j, 2, 3, M=M, x=x, y=y)
        >>>
        >>> # Example 2: Using closure (simpler but linter warnings)
        >>> result = summation(lambda i, j: M[i,j] * x**i * y**j, 2, 3)
        >>>
        >>> # Example 3: 1D summation
        >>> # Σ_i i * x^i for i=0 to 4
        >>> result = summation(lambda i, x: i * x**i, 5, x=x)
    """
    # Check if we should preserve symbolic expressions (in class definition context)
    if _should_preserve_symbolic_expression():
        from ..problems.composition import DelayedFunction

        return DelayedFunction("summation", term_generator, range_specs, kwargs)

    # Convert range_specs to actual ranges and generate terms using shared utilities
    from ..utils.shared_utilities import generate_terms_from_product, normalize_range_specs

    ranges = normalize_range_specs(range_specs)
    terms = generate_terms_from_product(ranges, term_generator, kwargs if kwargs else None)

    # Use sum_expr to combine all terms
    return sum_expr(*terms)


class When:
    """
    Helper class for creating range conditions in range_expr with readable syntax.

    Supports chaining comparisons to create range conditions:
    - When.between(0.1, 0.5) creates 0.1 <= x <= 0.5
    - When.gt(0.5).and_leq(2.0) creates 0.5 < x <= 2.0
    - When.geq(0.1).and_lt(0.25) creates 0.1 <= x < 0.25
    - When.lt(0.1) creates x < 0.1
    - When.gt(1.0) creates x > 1.0
    """

    def __init__(self, lower=None, upper=None, lower_inclusive=True, upper_inclusive=True):
        """Initialize a range condition."""
        self.lower = lower
        self.upper = upper
        self.lower_inclusive = lower_inclusive
        self.upper_inclusive = upper_inclusive

    @classmethod
    def between(cls, lower, upper):
        """Create an inclusive range: lower <= x <= upper."""
        return cls(lower=lower, upper=upper, lower_inclusive=True, upper_inclusive=True)

    @classmethod
    def geq(cls, value):
        """Create a greater-than-or-equal condition: x >= value."""
        return cls(lower=value, lower_inclusive=True)

    @classmethod
    def gt(cls, value):
        """Create a greater-than condition: x > value."""
        return cls(lower=value, lower_inclusive=False)

    @classmethod
    def leq(cls, value):
        """Create a less-than-or-equal condition: x <= value."""
        return cls(upper=value, upper_inclusive=True)

    @classmethod
    def lt(cls, value):
        """Create a less-than condition: x < value."""
        return cls(upper=value, upper_inclusive=False)

    def and_leq(self, value):
        """Chain an upper bound (inclusive): ... and x <= value."""
        if self.upper is not None:
            raise ValueError("Upper bound already set")
        self.upper = value
        self.upper_inclusive = True
        return self

    def and_lt(self, value):
        """Chain an upper bound (exclusive): ... and x < value."""
        if self.upper is not None:
            raise ValueError("Upper bound already set")
        self.upper = value
        self.upper_inclusive = False
        return self

    def and_geq(self, value):
        """Chain a lower bound (inclusive): ... and x >= value."""
        if self.lower is not None:
            raise ValueError("Lower bound already set")
        self.lower = value
        self.lower_inclusive = True
        return self

    def and_gt(self, value):
        """Chain a lower bound (exclusive): ... and x > value."""
        if self.lower is not None:
            raise ValueError("Lower bound already set")
        self.lower = value
        self.lower_inclusive = False
        return self

    def then(self, expression):
        """Attach an expression to this range condition."""
        return (self, expression)

    def build_lower_condition(self, wrapped_var: Expression) -> BinaryOperation:
        """Build the lower bound condition for this When.

        Args:
            wrapped_var: The wrapped variable to compare against

        Returns:
            BinaryOperation representing the lower bound check

        Note:
            Caller must ensure self.lower is not None before calling.
        """
        assert self.lower is not None, "Lower bound must be set to build lower condition"
        if self.lower_inclusive:
            return wrapped_var >= wrap_operand(self.lower)
        else:
            return wrapped_var > wrap_operand(self.lower)

    def build_upper_condition(self, wrapped_var: Expression) -> BinaryOperation:
        """Build the upper bound condition for this When.

        Args:
            wrapped_var: The wrapped variable to compare against

        Returns:
            BinaryOperation representing the upper bound check

        Note:
            Caller must ensure self.upper is not None before calling.
        """
        assert self.upper is not None, "Upper bound must be set to build upper condition"
        if self.upper_inclusive:
            return wrapped_var <= wrap_operand(self.upper)
        else:
            return wrapped_var < wrap_operand(self.upper)


def range_expr(variable: ExpressionOperand, *cases, otherwise=None) -> ConditionalExpression | Expression:
    """
    Create a piecewise function based on value ranges.

    This provides a cleaner way to express equations that have different formulas
    for different ranges of a variable, common in engineering standards and codes.

    Args:
        variable: The variable to check ranges against
        *cases: Tuples of (When condition, expression) created using When.xxx(...).then(expr)
        otherwise: Optional default expression when no range matches

    Returns:
        ConditionalExpression representing the piecewise function

    Examples:
        >>> from qnty import Dimensionless
        >>> from qnty.algebra import range_expr, When
        >>> X_h = Dimensionless("X_h")
        >>>
        >>> # Example 1: Two ranges with natural syntax
        >>> # For 0.1 <= X_h <= 0.5: use v_1_expr
        >>> # For 0.5 < X_h <= 2.0: use v_2_expr
        >>> V = range_expr(
        ...     X_h,
        ...     When.between(0.1, 0.5).then(v_1_expr),
        ...     When.gt(0.5).and_leq(2.0).then(v_2_expr)
        ... )
        >>>
        >>> # Example 2: Four ranges with default
        >>> # For 0.1 <= X_h <= 0.25: use expr1
        >>> # For 0.25 < X_h <= 0.5: use expr2
        >>> # For 0.5 < X_h <= 1.0: use expr3
        >>> # For 1.0 < X_h <= 2.0: use expr4
        >>> # Otherwise: use default_expr
        >>> V_L = range_expr(
        ...     X_h,
        ...     When.between(0.1, 0.25).then(expr1),
        ...     When.gt(0.25).and_leq(0.5).then(expr2),
        ...     When.gt(0.5).and_leq(1.0).then(expr3),
        ...     When.gt(1.0).and_leq(2.0).then(expr4),
        ...     otherwise=default_expr
        ... )
        >>>
        >>> # Example 3: One-sided conditions
        >>> result = range_expr(
        ...     X_h,
        ...     When.lt(0.1).then(expr_small),
        ...     When.geq(0.1).and_lt(1.0).then(expr_medium),
        ...     When.geq(1.0).then(expr_large)
        ... )
    """
    # Check if we should preserve symbolic expressions (in class definition context)
    if _should_preserve_symbolic_expression():
        from ..problems.composition import DelayedFunction

        return DelayedFunction("range_expr", variable, cases, otherwise)

    if len(cases) == 0:
        if otherwise is not None:
            return wrap_operand(otherwise)
        raise ValueError("range_expr requires at least one case")

    # Parse cases
    range_cases = []
    for case in cases:
        if not isinstance(case, tuple) or len(case) != 2:
            raise ValueError(f"Each case must be created using When.xxx(...).then(expression), got: {case}")

        condition, expression = case
        if not isinstance(condition, When):
            raise ValueError(f"First element of case must be a When object, got: {type(condition)}")

        range_cases.append((condition, expression))

    # Build the nested conditional expression from right to left
    wrapped_var = wrap_operand(variable)

    # Start with the otherwise/default case or the last case
    if otherwise is not None:
        result = wrap_operand(otherwise)
    elif range_cases:
        # Use the last range case as the implicit default
        _, last_expr = range_cases[-1]
        result = wrap_operand(last_expr)
        range_cases = range_cases[:-1]
    else:
        raise ValueError("range_expr requires at least one case or an otherwise clause")

    # Build nested conditionals from right to left
    for condition, expression in reversed(range_cases):
        # Build the condition based on When specification
        wrapped_expression = wrap_operand(expression)

        if condition.lower is not None and condition.upper is not None:
            # Both bounds: create nested conditionals to implement AND logic
            lower_cond = condition.build_lower_condition(wrapped_var)
            upper_cond = condition.build_upper_condition(wrapped_var)

            # Nest the conditions: if lower_cond then (if upper_cond then expr else result) else result
            inner_cond = cond_expr(upper_cond, wrapped_expression, result)
            result = cond_expr(lower_cond, inner_cond, result)

        elif condition.lower is not None:
            # Only lower bound
            combined_cond = condition.build_lower_condition(wrapped_var)
            result = cond_expr(combined_cond, wrapped_expression, result)

        elif condition.upper is not None:
            # Only upper bound
            combined_cond = condition.build_upper_condition(wrapped_var)
            result = cond_expr(combined_cond, wrapped_expression, result)

        else:
            raise ValueError("When condition must have at least one bound")

    return result
