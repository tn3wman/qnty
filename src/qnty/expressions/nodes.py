"""
Expression AST Nodes
===================

Core abstract syntax tree nodes for mathematical expressions.
"""

import math
from abc import ABC, abstractmethod

from ..constants import CONDITION_EVALUATION_THRESHOLD, DIVISION_BY_ZERO_THRESHOLD, FLOAT_EQUALITY_TOLERANCE
from ..quantities import FieldQnty, Quantity
from ..units.field_units import DimensionlessUnits
from ..utils.caching.manager import get_cache_manager
from ..utils.scope_discovery import ScopeDiscoveryService
from .formatter import ExpressionFormatter


class Expression(ABC):
    """Abstract base class for mathematical expressions."""

    # Class-level optimization settings
    _auto_eval_enabled = False  # Disabled by default for performance

    @abstractmethod
    def evaluate(self, variable_values: dict[str, "FieldQnty"]) -> "Quantity":
        """Evaluate the expression given variable values."""
        pass

    @abstractmethod
    def get_variables(self) -> set[str]:
        """Get all variable symbols used in this expression."""
        pass

    @abstractmethod
    def simplify(self) -> "Expression":
        """Simplify the expression."""
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    def _discover_variables_from_scope(self) -> dict[str, "FieldQnty"]:
        """Automatically discover variables from the calling scope using centralized service."""
        # Skip if auto-evaluation is disabled
        if not self._auto_eval_enabled:
            return {}

        # Get required variables first to optimize search
        required_vars = self.get_variables()
        if not required_vars:
            return {}

        # Use centralized scope discovery service
        return ScopeDiscoveryService.discover_variables(required_vars, enable_caching=True)

    def _can_auto_evaluate(self) -> tuple[bool, dict[str, "FieldQnty"]]:
        """Check if expression can be auto-evaluated from scope using centralized service."""
        # Use centralized scope discovery service
        return ScopeDiscoveryService.can_auto_evaluate(self)

    def __add__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("+", self, wrap_operand(other))

    def __radd__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("+", wrap_operand(other), self)

    def __sub__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("-", self, wrap_operand(other))

    def __rsub__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("-", wrap_operand(other), self)

    def __mul__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("*", self, wrap_operand(other))

    def __rmul__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("*", wrap_operand(other), self)

    def __truediv__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("/", self, wrap_operand(other))

    def __rtruediv__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("/", wrap_operand(other), self)

    def __pow__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("**", self, wrap_operand(other))

    def __rpow__(self, other: "OperandType") -> "Expression":
        return BinaryOperation("**", wrap_operand(other), self)

    def __abs__(self) -> "Expression":
        """Absolute value of the expression."""
        return UnaryFunction("abs", self)

    # Comparison operators for conditional expressions (consolidated)
    def _make_comparison(self, operator: str, other) -> "BinaryOperation":
        """Helper method to create comparison operations."""
        return BinaryOperation(operator, self, wrap_operand(other))

    def __lt__(self, other: "OperandType") -> "BinaryOperation":
        return self._make_comparison("<", other)

    def __le__(self, other: "OperandType") -> "BinaryOperation":
        return self._make_comparison("<=", other)

    def __gt__(self, other: "OperandType") -> "BinaryOperation":
        return self._make_comparison(">", other)

    def __ge__(self, other: "OperandType") -> "BinaryOperation":
        return self._make_comparison(">=", other)


# Type aliases to reduce repetition
OperandType = Expression | FieldQnty | Quantity | int | float


class VariableReference(Expression):
    """Reference to a variable in an expression with performance optimizations."""

    __slots__ = ("variable", "_cached_name", "_last_symbol")

    def __init__(self, variable: "FieldQnty"):
        self.variable = variable
        # Cache the name resolution to avoid repeated lookups
        self._cached_name = None
        self._last_symbol = None

    @property
    def name(self) -> str:
        """Get variable name with caching for performance."""
        current_symbol = self.variable.symbol
        if self._cached_name is None or self._last_symbol != current_symbol:
            # Use symbol for optinova compatibility, fall back to name if symbol not set
            self._cached_name = current_symbol if current_symbol else self.variable.name
            self._last_symbol = current_symbol
        return self._cached_name

    def evaluate(self, variable_values: dict[str, "FieldQnty"]) -> "Quantity":
        try:
            if self.name in variable_values:
                var = variable_values[self.name]
                if var.quantity is not None:
                    return var.quantity
            elif self.variable.quantity is not None:
                return self.variable.quantity

            # If we reach here, no valid quantity was found
            available_vars = list(variable_values.keys()) if variable_values else []
            raise ValueError(f"Cannot evaluate variable '{self.name}' without value. Available variables: {available_vars}")
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Error evaluating variable '{self.name}': {e}") from e

    def get_variables(self) -> set[str]:
        return {self.name}

    def simplify(self) -> "Expression":
        return self

    def __str__(self) -> str:
        return ExpressionFormatter.format_variable_reference(self)


class Constant(Expression):
    """Constant value in an expression."""

    __slots__ = ("value",)

    def __init__(self, value: "Quantity"):
        self.value = value

    def evaluate(self, variable_values: dict[str, "FieldQnty"]) -> "Quantity":
        del variable_values  # Suppress unused variable warning
        return self.value

    def get_variables(self) -> set[str]:
        return set()

    def simplify(self) -> "Expression":
        return self

    def __str__(self) -> str:
        return ExpressionFormatter.format_constant(self)


class BinaryOperation(Expression):
    """Binary operation between two expressions."""

    __slots__ = ("operator", "left", "right")

    # Operator dispatch table for better performance
    _ARITHMETIC_OPS = {"+", "-", "*", "/", "**"}
    _COMPARISON_OPS = {"<", "<=", ">", ">=", "==", "!="}

    def __init__(self, operator: str, left: Expression, right: Expression):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, variable_values: dict[str, "FieldQnty"]) -> "Quantity":
        """Evaluate the binary operation with caching and error handling."""
        try:
            # Check cache for constant expressions
            cached_result = self._try_get_cached_result()
            if cached_result is not None:
                return cached_result

            # Evaluate operands
            left_val = self.left.evaluate(variable_values)
            right_val = self.right.evaluate(variable_values)

            # Dispatch operation
            result = self._dispatch_operation(left_val, right_val)

            # Cache result for constant expressions
            self._try_cache_result(result)

            return result
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Error evaluating binary operation '{self}': {e}") from e

    def _try_get_cached_result(self) -> "Quantity | None":
        """Attempt to retrieve a cached result for constant expressions."""
        if not self._is_constant_expression():
            return None

        cache_manager = get_cache_manager()
        cache_key = self._generate_cache_key()
        return cache_manager.get_expression_result(cache_key)

    def _try_cache_result(self, result: "Quantity") -> None:
        """Attempt to cache the result for constant expressions."""
        if not self._is_constant_expression():
            return

        cache_manager = get_cache_manager()
        cache_key = self._generate_cache_key()
        cache_manager.cache_expression_result(cache_key, result)

    def _is_constant_expression(self) -> bool:
        """Check if both operands are constants."""
        return isinstance(self.left, Constant) and isinstance(self.right, Constant)

    def _generate_cache_key(self) -> str:
        """Generate a cache key for constant expressions."""
        # Safe to cast since _is_constant_expression() already verified types
        left_const = self.left
        right_const = self.right
        assert isinstance(left_const, Constant) and isinstance(right_const, Constant)
        return f"{id(self)}_{self.operator}_{id(left_const.value)}_{id(right_const.value)}"

    def _dispatch_operation(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Dispatch to the appropriate operation handler."""
        if self.operator in self._ARITHMETIC_OPS:
            return self._evaluate_arithmetic(left_val, right_val)
        elif self.operator in self._COMPARISON_OPS:
            return self._evaluate_comparison(left_val, right_val)
        else:
            raise ValueError(f"Unknown operator: {self.operator}")

    def _evaluate_arithmetic(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Evaluate arithmetic operations using operation-specific handlers."""
        operation_map = {"*": self._multiply, "+": self._add, "-": self._subtract, "/": self._divide, "**": self._power}

        handler = operation_map.get(self.operator)
        if handler:
            return handler(left_val, right_val)
        else:
            raise ValueError(f"Unknown arithmetic operator: {self.operator}")

    def _multiply(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Handle multiplication with fast path optimizations."""
        if right_val.value == 1.0:
            return left_val
        elif left_val.value == 1.0:
            return right_val
        elif right_val.value == 0.0:
            return Quantity(0.0, right_val.unit)
        elif left_val.value == 0.0:
            return Quantity(0.0, left_val.unit)
        return left_val * right_val

    def _add(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Handle addition with fast path optimizations."""
        if right_val.value == 0.0:
            return left_val
        elif left_val.value == 0.0:
            return right_val
        return left_val + right_val

    def _subtract(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Handle subtraction with fast path optimizations."""
        if right_val.value == 0.0:
            return left_val
        return left_val - right_val

    def _divide(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Handle division with zero checking and optimizations."""
        if abs(right_val.value) < DIVISION_BY_ZERO_THRESHOLD:
            raise ValueError(f"Division by zero in expression: {self}")
        if right_val.value == 1.0:
            return left_val
        return left_val / right_val

    def _power(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Handle power operations with special cases."""
        if not isinstance(right_val.value, int | float):
            raise ValueError("Exponent must be dimensionless number")

        # Fast paths for common exponents
        if right_val.value == 1.0:
            return left_val
        elif right_val.value == 0.0:
            return Quantity(1.0, DimensionlessUnits.dimensionless)
        elif right_val.value == 2.0:
            return left_val * left_val  # Use multiplication for squaring

        if right_val.value < 0 and left_val.value < 0:
            raise ValueError(f"Negative base with negative exponent: {left_val.value}^{right_val.value}")

        result_value = left_val.value**right_val.value
        return Quantity(result_value, left_val.unit)

    def _evaluate_comparison(self, left_val: "Quantity", right_val: "Quantity") -> "Quantity":
        """Evaluate comparison operations."""
        # Convert to same units for comparison if possible
        try:
            if left_val._dimension_sig == right_val._dimension_sig and left_val.unit != right_val.unit:
                right_val = right_val.to(left_val.unit)
        except (ValueError, TypeError, AttributeError):
            pass

        # Use dispatch dictionary for comparisons
        ops = {
            "<": lambda left, right: left < right,
            "<=": lambda left, right: left <= right,
            ">": lambda left, right: left > right,
            ">=": lambda left, right: left >= right,
            "==": lambda left, right: abs(left - right) < FLOAT_EQUALITY_TOLERANCE,
            "!=": lambda left, right: abs(left - right) >= FLOAT_EQUALITY_TOLERANCE,
        }

        result = ops[self.operator](left_val.value, right_val.value)
        return Quantity(1.0 if result else 0.0, DimensionlessUnits.dimensionless)

    def get_variables(self) -> set[str]:
        return self.left.get_variables() | self.right.get_variables()

    def simplify(self) -> Expression:
        left_simplified = self.left.simplify()
        right_simplified = self.right.simplify()

        # Basic simplification rules
        if isinstance(left_simplified, Constant) and isinstance(right_simplified, Constant):
            # Evaluate constant expressions
            dummy_vars = {}
            try:
                result = BinaryOperation(self.operator, left_simplified, right_simplified).evaluate(dummy_vars)
                return Constant(result)
            except (ValueError, TypeError, ArithmeticError):
                pass

        return BinaryOperation(self.operator, left_simplified, right_simplified)

    def __str__(self) -> str:
        # Delegate to centralized formatter
        can_eval, variables = self._can_auto_evaluate()
        return ExpressionFormatter.format_binary_operation(self, can_auto_evaluate=can_eval, auto_eval_variables=variables)


class UnaryFunction(Expression):
    """Unary mathematical function expression."""

    __slots__ = ("function_name", "operand")

    def __init__(self, function_name: str, operand: Expression):
        self.function_name = function_name
        self.operand = operand

    def evaluate(self, variable_values: dict[str, "FieldQnty"]) -> "Quantity":
        operand_val = self.operand.evaluate(variable_values)

        # Function dispatch table for better performance and maintainability
        functions = {
            "sin": lambda x: Quantity(math.sin(x.value), DimensionlessUnits.dimensionless),
            "cos": lambda x: Quantity(math.cos(x.value), DimensionlessUnits.dimensionless),
            "tan": lambda x: Quantity(math.tan(x.value), DimensionlessUnits.dimensionless),
            "sqrt": lambda x: Quantity(math.sqrt(x.value), x.unit),
            "abs": lambda x: Quantity(abs(x.value), x.unit),
            "ln": lambda x: Quantity(math.log(x.value), DimensionlessUnits.dimensionless),
            "log10": lambda x: Quantity(math.log10(x.value), DimensionlessUnits.dimensionless),
            "exp": lambda x: Quantity(math.exp(x.value), DimensionlessUnits.dimensionless),
        }

        func = functions.get(self.function_name)
        if func:
            return func(operand_val)
        else:
            raise ValueError(f"Unknown function: {self.function_name}")

    def get_variables(self) -> set[str]:
        return self.operand.get_variables()

    def simplify(self) -> Expression:
        simplified_operand = self.operand.simplify()
        if isinstance(simplified_operand, Constant):
            # Evaluate constant functions at compile time
            try:
                dummy_vars = {}
                result = UnaryFunction(self.function_name, simplified_operand).evaluate(dummy_vars)
                return Constant(result)
            except (ValueError, TypeError, ArithmeticError):
                pass
        return UnaryFunction(self.function_name, simplified_operand)

    def __str__(self) -> str:
        return ExpressionFormatter.format_unary_function(self)


class ConditionalExpression(Expression):
    """Conditional expression: if condition then true_expr else false_expr."""

    __slots__ = ("condition", "true_expr", "false_expr")

    def __init__(self, condition: Expression, true_expr: Expression, false_expr: Expression):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def evaluate(self, variable_values: dict[str, "FieldQnty"]) -> "Quantity":
        condition_val = self.condition.evaluate(variable_values)
        # Consider non-zero as True
        if abs(condition_val.value) > CONDITION_EVALUATION_THRESHOLD:
            return self.true_expr.evaluate(variable_values)
        else:
            return self.false_expr.evaluate(variable_values)

    def get_variables(self) -> set[str]:
        return self.condition.get_variables() | self.true_expr.get_variables() | self.false_expr.get_variables()

    def simplify(self) -> Expression:
        simplified_condition = self.condition.simplify()
        simplified_true = self.true_expr.simplify()
        simplified_false = self.false_expr.simplify()

        # If condition is constant, choose the appropriate branch
        if isinstance(simplified_condition, Constant):
            try:
                dummy_vars = {}
                condition_val = simplified_condition.evaluate(dummy_vars)
                if abs(condition_val.value) > CONDITION_EVALUATION_THRESHOLD:
                    return simplified_true
                else:
                    return simplified_false
            except (ValueError, TypeError, ArithmeticError):
                pass

        return ConditionalExpression(simplified_condition, simplified_true, simplified_false)

    def __str__(self) -> str:
        return ExpressionFormatter.format_conditional_expression(self)


# Utility functions for expression creation

# Cache for common types to avoid repeated type checks
_NUMERIC_TYPES = (int, float)
_DIMENSIONLESS_CONSTANT = None


def _get_cached_dimensionless():
    """Get cached dimensionless constant for numeric values."""
    global _DIMENSIONLESS_CONSTANT
    if _DIMENSIONLESS_CONSTANT is None:
        _DIMENSIONLESS_CONSTANT = DimensionlessUnits.dimensionless
    return _DIMENSIONLESS_CONSTANT


def _get_dimensionless_quantity(value: float) -> Quantity:
    """Get cached dimensionless quantity for common numeric values."""
    cache_manager = get_cache_manager()

    # Check unified cache first
    cached_qty = cache_manager.get_dimensionless_quantity(value)
    if cached_qty is not None:
        return cached_qty

    # Create new quantity
    qty = Quantity(value, _get_cached_dimensionless())

    # Cache if appropriate
    cache_manager.cache_dimensionless_quantity(value, qty)

    return qty


def _is_numeric_type(obj) -> bool:
    """Cached type check for numeric types."""
    obj_type = type(obj)
    cache_manager = get_cache_manager()

    # Check unified cache
    cached_result = cache_manager.get_type_check(obj_type)
    if cached_result is not None:
        return cached_result

    # Compute and cache result
    result = obj_type in _NUMERIC_TYPES
    cache_manager.cache_type_check(obj_type, result)
    return result


def wrap_operand(operand: "OperandType") -> Expression:
    """
    Convert various types to Expression objects.

    This function uses cached type checks from the unified cache manager
    for maximum performance.

    Args:
        operand: Value to wrap as an Expression

    Returns:
        Expression object representing the operand

    Raises:
        TypeError: If operand type cannot be converted to Expression
    """
    # Fast path: check most common cases first using cached type check
    if _is_numeric_type(operand):
        # operand is guaranteed to be int or float at this point
        return Constant(_get_dimensionless_quantity(float(operand)))  # type: ignore[arg-type]

    # Check if already an Expression (using isinstance for speed)
    if isinstance(operand, Expression):
        return operand

    # Check for Quantity
    if isinstance(operand, Quantity):
        return Constant(operand)

    # Check for FieldQnty
    if isinstance(operand, FieldQnty):
        return VariableReference(operand)

    # Check for ConfigurableVariable (from composition system)
    if hasattr(operand, "_variable"):
        var = getattr(operand, "_variable", None)
        if isinstance(var, FieldQnty):
            return VariableReference(var)

    # No duck typing - fail fast for unknown types
    raise TypeError(f"Cannot convert {type(operand)} to Expression")


# Register expression types with the TypeRegistry for optimal performance
from ..utils.protocols import register_expression_type

register_expression_type(Expression)
register_expression_type(BinaryOperation)
register_expression_type(VariableReference)
register_expression_type(Constant)
register_expression_type(UnaryFunction)
register_expression_type(ConditionalExpression)
