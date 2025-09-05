"""
Consistent Error Handling System for Qnty Library.

This module provides a unified approach to error handling across the library,
with consistent exception types, error messages, and logging patterns.
"""

import logging
from typing import Any, Optional
from dataclasses import dataclass


# Custom Exception Hierarchy
class QntyError(Exception):
    """Base exception for all qnty library errors."""
    
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}
        self.message = message


class DimensionalError(QntyError):
    """Raised when operations involve incompatible dimensions."""
    
    def __init__(self, operation: str, left_dim: str, right_dim: str, context: Optional[dict] = None):
        message = f"Incompatible dimensions for {operation}: {left_dim} and {right_dim}"
        super().__init__(message, context)
        self.operation = operation
        self.left_dimension = left_dim
        self.right_dimension = right_dim


class UnitConversionError(QntyError):
    """Raised when unit conversions fail."""
    
    def __init__(self, from_unit: str, to_unit: str, reason: str = "", context: Optional[dict] = None):
        message = f"Cannot convert from '{from_unit}' to '{to_unit}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, context)
        self.from_unit = from_unit
        self.to_unit = to_unit


class VariableNotFoundError(QntyError):
    """Raised when a required variable is not found."""
    
    def __init__(self, variable_name: str, available_vars: Optional[list[str]] = None, context: Optional[dict] = None):
        message = f"Variable '{variable_name}' not found"
        if available_vars:
            message += f". Available variables: {', '.join(available_vars)}"
        super().__init__(message, context)
        self.variable_name = variable_name
        self.available_vars = available_vars or []


class EquationSolvingError(QntyError):
    """Raised when equation solving fails."""
    
    def __init__(self, equation_name: str, target_var: str, reason: str = "", context: Optional[dict] = None):
        message = f"Cannot solve equation '{equation_name}' for variable '{target_var}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, context)
        self.equation_name = equation_name
        self.target_var = target_var


class ExpressionEvaluationError(QntyError):
    """Raised when expression evaluation fails."""
    
    def __init__(self, expression: str, reason: str = "", context: Optional[dict] = None):
        message = f"Cannot evaluate expression '{expression}'"
        if reason:
            message += f": {reason}"
        super().__init__(message, context)
        self.expression = expression


class DivisionByZeroError(QntyError):
    """Raised for division by zero operations."""
    
    def __init__(self, dividend: str, context: Optional[dict] = None):
        message = f"Division by zero: {dividend} / 0"
        super().__init__(message, context)
        self.dividend = dividend


@dataclass
class ErrorContext:
    """Context information for errors to aid in debugging."""
    module: str
    function: str
    operation: str
    variables: Optional[dict[str, Any]] = None
    additional_info: Optional[dict[str, Any]] = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for error logging."""
        return {
            "module": self.module,
            "function": self.function, 
            "operation": self.operation,
            "variables": self.variables,
            "additional_info": self.additional_info
        }


class ErrorHandler:
    """
    Centralized error handling with consistent logging and context management.
    
    Provides methods for handling common error patterns across the library.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize error handler with optional custom logger."""
        self.logger = logger or logging.getLogger(__name__)
    
    def handle_dimensional_error(self, operation: str, left: Any, right: Any, context: Optional[ErrorContext] = None) -> None:
        """Handle dimensional compatibility errors."""
        left_dim = self._get_dimension_string(left)
        right_dim = self._get_dimension_string(right)
        
        error_context = context.to_dict() if context else {}
        
        self.logger.error(f"Dimensional error in {operation}: {left_dim} vs {right_dim}", extra=error_context)
        raise DimensionalError(operation, left_dim, right_dim, error_context)
    
    def handle_unit_conversion_error(self, from_unit: str, to_unit: str, reason: str = "", 
                                   context: Optional[ErrorContext] = None) -> None:
        """Handle unit conversion errors."""
        error_context = context.to_dict() if context else {}
        
        self.logger.error(f"Unit conversion failed: {from_unit} -> {to_unit} ({reason})", extra=error_context)
        raise UnitConversionError(from_unit, to_unit, reason, error_context)
    
    def handle_variable_not_found(self, variable_name: str, available_vars: Optional[list[str]] = None,
                                context: Optional[ErrorContext] = None) -> None:
        """Handle variable not found errors."""
        error_context = context.to_dict() if context else {}
        available_list = available_vars or []
        
        self.logger.error(f"Variable not found: {variable_name} (available: {available_list})", extra=error_context)
        raise VariableNotFoundError(variable_name, available_list, error_context)
    
    def handle_equation_solving_error(self, equation_name: str, target_var: str, reason: str = "",
                                    context: Optional[ErrorContext] = None) -> None:
        """Handle equation solving errors."""
        error_context = context.to_dict() if context else {}
        
        self.logger.error(f"Equation solving failed: {equation_name} for {target_var} ({reason})", extra=error_context)
        raise EquationSolvingError(equation_name, target_var, reason, error_context)
    
    def handle_expression_evaluation_error(self, expression: str, reason: str = "", 
                                         context: Optional[ErrorContext] = None) -> None:
        """Handle expression evaluation errors.""" 
        error_context = context.to_dict() if context else {}
        
        self.logger.error(f"Expression evaluation failed: {expression} ({reason})", extra=error_context)
        raise ExpressionEvaluationError(expression, reason, error_context)
    
    def handle_division_by_zero(self, dividend: Any, context: Optional[ErrorContext] = None) -> None:
        """Handle division by zero errors."""
        error_context = context.to_dict() if context else {}
        dividend_str = str(dividend)
        
        self.logger.error(f"Division by zero: {dividend_str}", extra=error_context)
        raise DivisionByZeroError(dividend_str, error_context)
    
    def handle_unexpected_error(self, original_error: Exception, operation: str, 
                              context: Optional[ErrorContext] = None) -> None:
        """Handle unexpected errors with proper context and chaining."""
        error_context = context.to_dict() if context else {}
        
        self.logger.error(f"Unexpected error in {operation}: {original_error}", 
                         extra=error_context, exc_info=True)
        
        # Re-raise as QntyError with context
        raise QntyError(f"Unexpected error in {operation}: {original_error}", error_context) from original_error
    
    def _get_dimension_string(self, obj: Any) -> str:
        """Get dimension string representation for error messages."""
        if hasattr(obj, '_dimension_sig'):
            return str(obj._dimension_sig)
        elif hasattr(obj, 'unit') and hasattr(obj.unit, 'dimension'):
            return str(obj.unit.dimension)
        else:
            return f"{type(obj).__name__}"
    
    @staticmethod
    def create_context(module: str, function: str, operation: str, **kwargs) -> ErrorContext:
        """Create error context for consistent error reporting."""
        return ErrorContext(
            module=module,
            function=function,
            operation=operation,
            additional_info=kwargs
        )


class ErrorHandlerMixin:
    """
    Mixin class that provides error handling methods to any class.
    
    Usage:
        class MyClass(ErrorHandlerMixin):
            def some_method(self):
                try:
                    # risky operation
                    pass
                except Exception as e:
                    self.handle_error(e, "some_operation")
    """
    
    def __init__(self):
        self._error_handler = ErrorHandler(logging.getLogger(self.__class__.__module__))
    
    def handle_error(self, error: Exception, operation: str, **context_kwargs) -> None:
        """Handle errors with automatic context creation."""
        context = ErrorContext(
            module=self.__class__.__module__,
            function=operation,
            operation=operation,
            additional_info=context_kwargs
        )
        self._error_handler.handle_unexpected_error(error, operation, context)
    
    def require_variable(self, var_name: str, variables: dict[str, Any]) -> Any:
        """Require a variable to exist, raising consistent error if not found."""
        if var_name not in variables:
            context = self._error_handler.create_context(
                self.__class__.__module__, 
                "require_variable",
                "variable_lookup",
                requested_variable=var_name
            )
            self._error_handler.handle_variable_not_found(var_name, list(variables.keys()), context)
        return variables[var_name]
    
    def ensure_dimensional_compatibility(self, left: Any, right: Any, operation: str) -> None:
        """Ensure two quantities have compatible dimensions for the given operation."""
        if hasattr(left, '_dimension_sig') and hasattr(right, '_dimension_sig'):
            if left._dimension_sig != right._dimension_sig:
                context = self._error_handler.create_context(
                    self.__class__.__module__,
                    "ensure_dimensional_compatibility", 
                    operation
                )
                self._error_handler.handle_dimensional_error(operation, left, right, context)


# Global error handler instance
_default_error_handler = ErrorHandler()


def get_error_handler() -> ErrorHandler:
    """Get the global error handler instance."""
    return _default_error_handler


def set_error_handler(handler: ErrorHandler) -> None:
    """Set a custom global error handler."""
    global _default_error_handler
    _default_error_handler = handler


# Convenience functions for common error patterns
def require_variable(var_name: str, variables: dict[str, Any], context: Optional[ErrorContext] = None) -> Any:
    """Require a variable to exist, raising consistent error if not found."""
    if var_name not in variables:
        _default_error_handler.handle_variable_not_found(var_name, list(variables.keys()), context)
    return variables[var_name]


def ensure_not_zero(value: Any, context: Optional[ErrorContext] = None) -> None:
    """Ensure a value is not zero for division operations."""
    if hasattr(value, 'value') and abs(value.value) < 1e-15:
        _default_error_handler.handle_division_by_zero(value, context)
    elif isinstance(value, (int, float)) and abs(value) < 1e-15:
        _default_error_handler.handle_division_by_zero(value, context)


def safe_evaluate(expression: Any, variables: dict[str, Any], context: Optional[ErrorContext] = None) -> Any:
    """Safely evaluate an expression with consistent error handling."""
    try:
        return expression.evaluate(variables)
    except Exception as e:
        error_context = context or ErrorContext("unknown", "safe_evaluate", "expression_evaluation")
        _default_error_handler.handle_expression_evaluation_error(str(expression), str(e), error_context)


# Error message templates for consistency
ERROR_MESSAGES = {
    "incompatible_dimensions": "Incompatible dimensions: {left} and {right} for operation {operation}",
    "variable_not_found": "Variable '{variable}' not found. Available: {available}",
    "unit_conversion_failed": "Cannot convert from '{from_unit}' to '{to_unit}': {reason}",
    "equation_unsolvable": "Cannot solve equation '{equation}' for variable '{variable}': {reason}",
    "division_by_zero": "Division by zero in expression: {expression}",
    "invalid_operation": "Invalid operation '{operation}' on {type}: {reason}",
}