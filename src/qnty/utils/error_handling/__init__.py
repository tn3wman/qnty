"""
Error handling infrastructure for the Qnty library.

This package provides comprehensive error handling capabilities including
custom exceptions, error handlers, and context management.

Public API:
- Exception classes: QntyError, DimensionalError, UnitConversionError, etc.
- Error handling: ErrorHandler, ErrorHandlerMixin
- Context management: ErrorContext
- Convenience functions: require_variable, ensure_not_zero, safe_evaluate
"""

# Import all exception classes
from .exceptions import (
    QntyError,
    DimensionalError,
    UnitConversionError,
    VariableNotFoundError,
    EquationSolvingError,
    ExpressionEvaluationError,
    DivisionByZeroError,
    ERROR_MESSAGES,
)

# Import context management
from .context import (
    ErrorContext,
    get_dimension_string,
    create_context,
)

# Import handlers and utilities
from .handlers import (
    ErrorHandler,
    ErrorHandlerMixin,
    get_error_handler,
    set_error_handler,
    require_variable,
    ensure_not_zero,
    safe_evaluate,
)

# Define public API
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
