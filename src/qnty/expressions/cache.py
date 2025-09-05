"""
Expression Caching System
========================

Caching infrastructure for optimized expression evaluation and type checking.
"""

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..quantities.quantity import Quantity, TypeSafeVariable
    from .nodes import Expression

# Import here to avoid circular imports - delayed imports
from ..cache_manager import get_cache_manager
from ..generated.units import DimensionlessUnits
from ..quantities.quantity import Quantity, TypeSafeVariable

# Cache for common types to avoid repeated type checks
_NUMERIC_TYPES = (int, float)
_DIMENSIONLESS_CONSTANT = None


def _get_cached_dimensionless():
    """Get cached dimensionless constant for numeric values."""
    global _DIMENSIONLESS_CONSTANT
    if _DIMENSIONLESS_CONSTANT is None:
        _DIMENSIONLESS_CONSTANT = DimensionlessUnits.dimensionless
    return _DIMENSIONLESS_CONSTANT


def _get_dimensionless_quantity(value: float) -> "Quantity":
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


def wrap_operand(operand: Union["Expression", "TypeSafeVariable", "Quantity", int, float]) -> "Expression":
    """
    Optimized operand wrapping with cached type checks.

    This function uses cached type checks for maximum performance.
    """
    # Import Expression classes to avoid circular imports
    from .nodes import Constant, Expression, VariableReference

    # Fast path: check most common cases first using cached type check
    if _is_numeric_type(operand):
        # operand is guaranteed to be int or float at this point
        return Constant(_get_dimensionless_quantity(float(operand)))  # type: ignore[arg-type]

    # Check if already an Expression (using isinstance for speed)
    if isinstance(operand, Expression):
        return operand

    # Check for FastQuantity
    if isinstance(operand, Quantity):
        return Constant(operand)

    # Check for TypeSafeVariable
    if isinstance(operand, TypeSafeVariable):
        return VariableReference(operand)

    # Check for ConfigurableVariable (from composition system)
    if hasattr(operand, "_variable"):
        var = getattr(operand, "_variable", None)
        if isinstance(var, TypeSafeVariable):
            return VariableReference(var)

    # No duck typing - fail fast for unknown types
    raise TypeError(f"Cannot convert {type(operand)} to Expression")
