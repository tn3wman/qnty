"""
Consistent Error Handling System for Qnty Library.

This module provides a unified approach to error handling across the library,
with consistent exception types, error messages, and logging patterns.

This is now a compatibility facade that imports from the infrastructure package.
"""

# Import everything from the new infrastructure location for backward compatibility
from .infrastructure.error_handling import *

# Maintain the same __all__ exports
__all__ = [
    # Exception classes
    "QntyError",
    "DimensionalError", 
    "UnitConversionError",
    "VariableNotFoundError",
    "EquationSolvingError",
    "ExpressionEvaluationError",
    "DivisionByZeroError",
    "ERROR_MESSAGES",
    
    # Context management
    "ErrorContext",
    "get_dimension_string",
    "create_context",
    
    # Handlers and utilities
    "ErrorHandler",
    "ErrorHandlerMixin",
    "get_error_handler",
    "set_error_handler",
    "require_variable",
    "ensure_not_zero",
    "safe_evaluate",
]