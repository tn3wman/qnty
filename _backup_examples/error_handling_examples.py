"""
Examples showing how to refactor inconsistent error handling using the unified system.

This demonstrates before/after patterns for error handling across the library.
"""

from .error_handling import ErrorHandler, ErrorContext, ErrorHandlerMixin, require_variable, ensure_not_zero


class BinaryOperationRefactoredExample(ErrorHandlerMixin):
    """
    AFTER: BinaryOperation using consistent error handling.
    
    BEFORE: Mixed error handling patterns
    AFTER: Unified error handling with proper context and logging
    """
    
    def __init__(self, operator: str, left, right):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right
    
    def evaluate_before_refactoring(self, variable_values):
        """
        BEFORE: Inconsistent error handling patterns.
        
        Problems:
        - Mixed exception types (ValueError, RuntimeError, etc.)
        - Inconsistent error messages
        - No context for debugging
        - Different patterns across methods
        """
        try:
            left_val = self.left.evaluate(variable_values)
            right_val = self.right.evaluate(variable_values)
        except Exception as e:
            # Inconsistent: sometimes ValueError, sometimes RuntimeError
            raise ValueError(f"Error evaluating binary operation '{self}': {e}") from e
        
        if self.operator == "/":
            # Inconsistent zero checking logic
            if abs(right_val.value) < 1e-15:  # Magic number, inconsistent threshold
                raise ValueError(f"Division by zero in expression: {self}")  # Generic message
        
        # No context information for debugging
        # Inconsistent error message formats
    
    def evaluate_after_refactoring(self, variable_values):
        """
        AFTER: Consistent error handling using unified system.
        
        Benefits:
        - Consistent exception types and hierarchy
        - Rich context information for debugging
        - Standardized error messages
        - Proper error chaining
        - Centralized logging
        """
        context = ErrorContext(
            module="expressions.nodes",
            function="evaluate",
            operation=f"binary_operation_{self.operator}",
            variables={"expression": str(self)},
            additional_info={"operator": self.operator}
        )
        
        try:
            left_val = self.left.evaluate(variable_values)
            right_val = self.right.evaluate(variable_values)
        except Exception as e:
            self._error_handler.handle_expression_evaluation_error(str(self), str(e), context)
        
        if self.operator == "/":
            # Consistent zero checking with proper context
            ensure_not_zero(right_val, context)
        
        # Ensure dimensional compatibility for arithmetic operations
        if self.operator in {"+", "-"}:
            self.ensure_dimensional_compatibility(left_val, right_val, self.operator)
        
        # Continue with normal operation...
        return self._perform_operation(left_val, right_val)
    
    def _perform_operation(self, left_val, right_val):
        """Dummy method for example."""
        return left_val  # Simplified for example


class EquationRefactoredExample(ErrorHandlerMixin):
    """
    AFTER: Equation using consistent error handling.
    
    BEFORE: Multiple inconsistent error patterns
    AFTER: Unified error handling with proper context
    """
    
    def __init__(self, name: str, lhs, rhs):
        super().__init__()
        self.name = name
        self.lhs = lhs
        self.rhs = rhs
        self.variables = {name}  # Simplified for example
    
    def solve_for_before_refactoring(self, target_var: str, variable_values: dict):
        """
        BEFORE: Multiple inconsistent error handling patterns.
        
        Problems:
        - Different exception types for similar errors
        - Inconsistent variable validation
        - No context for debugging failures
        - Generic error messages
        """
        # Inconsistent validation
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' not found in equation")  # Generic message
        
        # Inconsistent variable access
        var_obj = variable_values.get(target_var)
        if var_obj is None:
            raise ValueError(f"Variable '{target_var}' not found in variable_values")  # Different message format
        
        try:
            result_qty = self.rhs.evaluate(variable_values)
        except Exception:
            # Swallowing all exceptions inconsistently
            raise NotImplementedError("Cannot solve equation")  # Wrong exception type
        
        # No context for debugging unit conversion failures
        try:
            result_qty = result_qty.to(var_obj.quantity.unit)
        except (ValueError, TypeError, AttributeError):
            # Silent failure - hard to debug
            pass
    
    def solve_for_after_refactoring(self, target_var: str, variable_values: dict):
        """
        AFTER: Consistent error handling with proper context.
        
        Benefits:
        - Standardized variable validation
        - Rich context for debugging
        - Consistent exception hierarchy
        - Proper error chaining
        - Detailed logging
        """
        context = ErrorContext(
            module="equations.equation",
            function="solve_for", 
            operation="equation_solving",
            variables={"equation": self.name, "target": target_var},
            additional_info={"available_vars": list(variable_values.keys())}
        )
        
        # Consistent variable validation
        if target_var not in self.variables:
            self._error_handler.handle_equation_solving_error(
                self.name, target_var, "Variable not in equation", context
            )
        
        # Use standardized variable access
        var_obj = require_variable(target_var, variable_values, context)
        
        # Evaluate RHS with proper error handling
        try:
            result_qty = self.rhs.evaluate(variable_values)
        except Exception as e:
            self._error_handler.handle_expression_evaluation_error(str(self.rhs), str(e), context)
        
        # Handle unit conversion with context
        if var_obj.quantity and var_obj.quantity.unit:
            try:
                result_qty = result_qty.to(var_obj.quantity.unit)
            except Exception as e:
                self._error_handler.handle_unit_conversion_error(
                    str(result_qty.unit), str(var_obj.quantity.unit), str(e), context
                )
        
        var_obj.quantity = result_qty
        var_obj.is_known = True
        return var_obj


class QuantityRefactoredExample(ErrorHandlerMixin):
    """
    AFTER: Quantity using consistent error handling for arithmetic operations.
    """
    
    def __init__(self, value, unit):
        super().__init__()
        self.value = value
        self.unit = unit
    
    def __add___before_refactoring(self, other):
        """
        BEFORE: Inconsistent dimensional checking.
        
        Problems:
        - Hardcoded error messages
        - Inconsistent exception types
        - No context for debugging
        """
        if self.unit.dimension != other.unit.dimension:
            # Hardcoded error message, no context
            raise ValueError(f"Cannot add {self.unit.name} and {other.unit.name}")
        
        # No validation of input types
        return self.__class__(self.value + other.value, self.unit)
    
    def __add___after_refactoring(self, other):
        """
        AFTER: Consistent dimensional validation and error handling.
        
        Benefits:
        - Standardized dimensional compatibility checking
        - Rich error context
        - Consistent exception types
        - Type validation
        """
        context = ErrorContext(
            module="quantities.quantity",
            function="__add__",
            operation="addition",
            variables={"left": str(self), "right": str(other)}
        )
        
        # Validate input type
        if not hasattr(other, 'unit'):
            self._error_handler.handle_unexpected_error(
                TypeError(f"Cannot add Quantity to {type(other)}"), 
                "addition", context
            )
        
        # Use standardized dimensional compatibility checking
        self.ensure_dimensional_compatibility(self, other, "addition")
        
        return self.__class__(self.value + other.value, self.unit)


def demonstrate_error_handling_improvements():
    """
    Demonstrate the improvements achieved by consistent error handling:
    
    1. **Consistent Exception Hierarchy**:
       - Before: ValueError, TypeError, RuntimeError, NotImplementedError mixed
       - After: Structured QntyError hierarchy with specific subtypes
    
    2. **Rich Context Information**:
       - Before: Generic error messages with no context
       - After: Detailed context including module, function, operation, variables
    
    3. **Standardized Error Messages**:
       - Before: Inconsistent message formats across modules
       - After: Template-based consistent messages
    
    4. **Proper Error Chaining**:
       - Before: Original exceptions often lost
       - After: Proper exception chaining with "from" keyword
    
    5. **Centralized Logging**:
       - Before: No logging or inconsistent logging
       - After: Structured logging with context
    
    6. **Debugging Support**:
       - Before: Hard to debug failed operations
       - After: Rich context makes debugging much easier
    
    Example error before refactoring:
        ValueError: Variable 'pressure' not found in equation
    
    Example error after refactoring:
        VariableNotFoundError: Variable 'pressure' not found. 
        Available variables: temperature, volume, density
        Context: {
            "module": "equations.equation",
            "function": "solve_for", 
            "operation": "equation_solving",
            "equation": "ideal_gas_law",
            "target": "pressure"
        }
    """
    pass


def migration_checklist():
    """
    Checklist for migrating existing error handling:
    
    □ Replace generic ValueError/TypeError with specific QntyError subtypes
    □ Add ErrorContext to all error scenarios
    □ Use ErrorHandlerMixin for classes with error handling
    □ Replace hardcoded error messages with templates
    □ Add proper exception chaining with "from" keyword
    □ Use convenience functions (require_variable, ensure_not_zero)
    □ Add structured logging with context
    □ Test error scenarios to ensure proper error types and messages
    □ Update documentation to reflect new exception hierarchy
    □ Consider backward compatibility for public APIs
    
    Benefits checklist:
    ✓ Easier debugging with rich context
    ✓ Consistent error handling across modules
    ✓ Better user experience with clear error messages
    ✓ Improved logging for production monitoring
    ✓ Extensible error handling system
    ✓ Type-safe exception handling
    """
    pass