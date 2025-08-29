"""
Type Definitions and Utilities
===============================

Shared type definitions and utility functions to avoid circular imports.
This module contains core type definitions used across the system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar

if TYPE_CHECKING:
    from .expression import Constant, Expression, VariableReference
    from .setters import LengthSetter, PressureSetter, TypeSafeSetter
    from .variable import FastQuantity

# TypeVar for generic dimensional types
DimensionType = TypeVar('DimensionType', bound='FastQuantity')


def is_variable_like(obj: Any) -> bool:
    """Check if object is a TypeSafeVariable using duck typing."""
    return hasattr(obj, 'name') and hasattr(obj, 'quantity') and hasattr(obj, 'is_known')


def is_quantity_like(obj: Any) -> bool:
    """Check if object is a FastQuantity using duck typing."""
    return hasattr(obj, 'value') and hasattr(obj, 'unit') and hasattr(obj, '_dimension_sig')


def is_expression_like(obj: Any) -> bool:
    """Check if object is an Expression using duck typing."""
    return hasattr(obj, 'evaluate') and hasattr(obj, 'get_variables') and hasattr(obj, 'simplify')


class ExpressionFactory:
    """Factory for creating expression objects without circular imports."""
    
    @staticmethod
    def create_variable_reference(variable: TypeSafeVariable) -> Expression:
        """Create a VariableReference without importing expression module."""
        # Delayed import to avoid circular dependency
        from .expression import VariableReference
        return VariableReference(variable)
    
    @staticmethod
    def create_constant(quantity: FastQuantity) -> Expression:
        """Create a Constant without importing expression module."""
        # Delayed import to avoid circular dependency
        from .expression import Constant
        return Constant(quantity)
    
    @staticmethod
    def create_constant_from_number(value: float) -> Expression:
        """Create a Constant from a number without importing modules."""
        # Delayed imports to avoid circular dependency
        from .expression import Constant
        from .units import DimensionlessUnits
        from .variable import FastQuantity
        return Constant(FastQuantity(value, DimensionlessUnits.dimensionless))


def wrap_operand(operand: Expression | TypeSafeVariable | FastQuantity | int | float) -> Expression:
    """
    Wrap non-Expression operands in appropriate Expression subclasses.
    
    This is the central function that handles type conversion without circular imports.
    Uses factory pattern to avoid importing expression classes directly.
    """
    if is_expression_like(operand):
        return operand
    elif is_variable_like(operand):
        return ExpressionFactory.create_variable_reference(operand)
    elif is_quantity_like(operand):
        return ExpressionFactory.create_constant(operand)
    elif isinstance(operand, int | float):
        return ExpressionFactory.create_constant_from_number(float(operand))
    else:
        raise TypeError(f"Cannot convert {type(operand)} to Expression")


class TypeSafeVariable(Generic[DimensionType]):
    """Type-safe variable with compile-time dimensional checking."""
    
    def __init__(self, name: str, expected_dimension, is_known: bool = True):
        self.name = name
        self.symbol: str | None = None  # Will be set by EngineeringProblem to attribute name
        self.expected_dimension = expected_dimension
        self.quantity: FastQuantity | None = None
        self.is_known = is_known
    
    def set(self, value: float) -> TypeSafeSetter | LengthSetter | PressureSetter:
        # Delayed import to avoid circular dependency
        from .setters import TypeSafeSetter
        return TypeSafeSetter(self, value)
    
    @property
    def unknown(self) -> Self:
        """Mark this variable as unknown using fluent API."""
        self.is_known = False
        return self
    
    @property
    def known(self) -> Self:
        """Mark this variable as known using fluent API."""
        self.is_known = True
        return self
    
    def equals(self, expression: Expression | TypeSafeVariable | FastQuantity | int | float):
        """Create an equation: self = expression."""
        # Delayed import to avoid circular dependency
        from .equation import Equation
        
        # Wrap the expression in proper Expression type
        rhs_expr = wrap_operand(expression)
        return Equation(f"{self.name}_eq", self, rhs_expr)
    
    def __add__(self, other: TypeSafeVariable | FastQuantity | int | float) -> Expression:
        """Add this variable to another operand, returning an Expression."""
        return wrap_operand(self) + wrap_operand(other)

    def __radd__(self, other: FastQuantity | int | float) -> Expression:
        """Reverse add for this variable."""
        return wrap_operand(other) + wrap_operand(self)
    
    def __sub__(self, other: TypeSafeVariable | FastQuantity | int | float) -> Expression:
        """Subtract another operand from this variable, returning an Expression."""
        return wrap_operand(self) - wrap_operand(other)
    
    def __rsub__(self, other: FastQuantity | int | float) -> Expression:
        """Reverse subtract for this variable."""
        return wrap_operand(other) - wrap_operand(self)
    
    def __mul__(self, other: TypeSafeVariable | FastQuantity | int | float) -> Expression:
        """Multiply this variable by another operand, returning an Expression."""
        return wrap_operand(self) * wrap_operand(other)
    
    def __rmul__(self, other: FastQuantity | int | float) -> Expression:
        """Reverse multiply for this variable."""
        return wrap_operand(other) * wrap_operand(self)
    
    def __truediv__(self, other: TypeSafeVariable | FastQuantity | int | float) -> Expression:
        """Divide this variable by another operand, returning an Expression."""
        return wrap_operand(self) / wrap_operand(other)

    def __rtruediv__(self, other: FastQuantity | int | float) -> Expression:
        """Reverse divide for this variable."""
        return wrap_operand(other) / wrap_operand(self)
    
    def __pow__(self, other: TypeSafeVariable | FastQuantity | int | float) -> Expression:
        """Raise this variable to a power, returning an Expression."""
        return wrap_operand(self) ** wrap_operand(other)

    def __rpow__(self, other: FastQuantity | int | float) -> Expression:
        """Reverse power for this variable."""
        return wrap_operand(other) ** wrap_operand(self)
    
    def __str__(self):
        return f"{self.name}: {self.quantity}" if self.quantity else f"{self.name}: unset"
