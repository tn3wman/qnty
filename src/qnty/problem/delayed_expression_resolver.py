"""
Delayed Expression Resolver for Equation Reconstruction System.

Handles resolution of delayed expressions and equations that contain
components that need deferred evaluation.
"""

from typing import Any
from logging import Logger

from qnty.equations.equation import Equation
from qnty.expressions import VariableReference
from qnty.quantities.unified_variable import UnifiedVariable as Variable

# Type aliases
VariableDict = dict[str, Variable]
ReconstructionResult = Equation | None

# Tuple of types for isinstance() checks
VALID_EXPRESSION_TYPES = (VariableReference, Variable, int, float)


class DelayedExpressionResolver:
    """
    Focused class for resolving delayed expressions and equations.
    
    Handles components that have deferred evaluation needs and provides
    safe resolution with proper type checking and context management.
    """
    
    def __init__(self, variables: VariableDict, logger: Logger):
        """
        Initialize the delayed expression resolver.
        
        Args:
            variables: Dictionary of available variables
            logger: Logger for debugging
        """
        self.variables = variables
        self.logger = logger
    
    def contains_delayed_expressions(self, equation: Equation) -> bool:
        """
        Check if an equation contains delayed expressions that need resolution.

        Args:
            equation: The equation to check for delayed expressions

        Returns:
            True if equation contains delayed expressions
        """
        if equation is None:
            return False

        try:
            # Check if the RHS contains delayed expressions
            return self._expression_has_delayed_components(equation.rhs)
        except Exception as e:
            self.logger.debug(f"Error checking delayed expressions: {e}")
            return False
    
    def resolve_delayed_equation(self, equation: Equation) -> ReconstructionResult:
        """
        Resolve a delayed equation by evaluating its delayed expressions.

        Args:
            equation: The equation with delayed expressions to resolve

        Returns:
            Resolved equation if successful, None otherwise
        """
        if equation is None:
            return None

        try:
            # Create context with all current variables
            context = self.variables.copy()

            # If the RHS is delayed, resolve it
            if hasattr(equation.rhs, "resolve"):
                resolve_method = getattr(equation.rhs, "resolve", None)
                if callable(resolve_method):
                    resolved_rhs = resolve_method(context)
                    if resolved_rhs:
                        # Get the left-hand side variable
                        lhs_var = self._extract_lhs_variable(equation, context)

                        if lhs_var and self._is_valid_expression_type(resolved_rhs):
                            # Type narrowing - we know resolved_rhs is valid
                            return lhs_var.equals(resolved_rhs)  # type: ignore[arg-type]
                        else:
                            self.logger.debug(f"Invalid LHS variable or resolved RHS type: {type(resolved_rhs)}")
                            return None

            return None

        except Exception as e:
            self.logger.debug(f"Error resolving delayed equation: {e}")
            return None
    
    def _expression_has_delayed_components(self, expr: Any) -> bool:
        """
        Recursively check if an expression contains delayed components.

        Args:
            expr: The expression to check

        Returns:
            True if expression contains delayed components
        """
        if expr is None:
            return False

        if hasattr(expr, "resolve"):
            # This is a delayed component
            return True

        # Check if it's an equation with delayed RHS
        if hasattr(expr, "rhs") and hasattr(expr.rhs, "resolve"):
            return True

        # For expressions with operands, check recursively
        if hasattr(expr, "left") and hasattr(expr, "right"):
            return (self._expression_has_delayed_components(expr.left) or 
                   self._expression_has_delayed_components(expr.right))

        if hasattr(expr, "operand"):
            return self._expression_has_delayed_components(expr.operand)

        if hasattr(expr, "args"):
            return any(self._expression_has_delayed_components(arg) for arg in expr.args)

        return False
    
    def _extract_lhs_variable(self, equation: Equation, context: VariableDict) -> Variable | None:
        """
        Extract the left-hand side variable from an equation.
        
        Args:
            equation: The equation to extract from
            context: Variable context for lookups
            
        Returns:
            The LHS variable if found, None otherwise
        """
        if isinstance(equation.lhs, VariableReference):
            var_name = equation.lhs.name
            if var_name in context:
                return context[var_name]
        elif hasattr(equation.lhs, "symbol"):
            symbol = getattr(equation.lhs, "symbol", None)
            if isinstance(symbol, str) and symbol in context:
                return context[symbol]
        
        return None
    
    def _is_valid_expression_type(self, obj: Any) -> bool:
        """
        Check if an object is a valid expression type for use with Variable.equals().

        Args:
            obj: The object to check

        Returns:
            True if the object is a valid expression type
        """
        # Import here to avoid circular imports and include more types
        from qnty.expressions import BinaryOperation, Constant, UnaryFunction
        from qnty.quantities.quantity import Quantity
        
        extended_types = VALID_EXPRESSION_TYPES + (BinaryOperation, Constant, UnaryFunction, Quantity)
        return isinstance(obj, extended_types)