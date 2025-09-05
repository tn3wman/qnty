"""
Composite Expression Rebuilder for Equation Reconstruction System.

Handles reconstruction of composite expressions that were malformed
during proxy operations and equation composition.
"""

from typing import Any
from logging import Logger

from qnty.equations.equation import Equation
from qnty.expressions import BinaryOperation, Constant, UnaryFunction, VariableReference, cos, sin
from qnty.core.quantities.unified_variable import UnifiedVariable as Variable

# Type aliases
VariableDict = dict[str, Variable]
ReconstructionResult = Equation | None

# Constants for pattern matching
MATH_OPERATORS = {"(", ")", "+", "-", "*", "/"}


class CompositeExpressionRebuilder:
    """
    Focused class for rebuilding composite expressions from malformed patterns.
    
    Handles reconstruction of expressions that were malformed during proxy
    evaluation and provides methods to recover the original mathematical structure.
    """
    
    def __init__(self, variables: VariableDict, logger: Logger):
        """
        Initialize the composite expression rebuilder.
        
        Args:
            variables: Dictionary of available variables
            logger: Logger for debugging
        """
        self.variables = variables
        self.logger = logger
    
    def reconstruct_malformed_proxy_expression(self, equation: Equation, malformed_vars: list[str]) -> Any | None:
        """
        Generically reconstruct expressions that were malformed due to proxy evaluation.

        Args:
            equation: The equation containing malformed expressions
            malformed_vars: List of malformed variable names (kept for signature compatibility)

        Returns:
            Reconstructed expression if successful, None otherwise

        Note:
            Malformed variables look like: "(var1 - (var2 - var3) * 2.0) = 1.315 in"
            We extract the mathematical pattern and rebuild it symbolically using existing variables.
            The malformed_vars parameter is kept for potential future use and API consistency.
        """
        eq_str = str(equation)
        self.logger.debug(f"Reconstructing malformed equation: {eq_str}")

        try:
            # Extract the RHS expression from the equation
            if hasattr(equation, "rhs"):
                rhs_expr = equation.rhs
                return self._rebuild_expression_from_malformed(rhs_expr)
        except Exception as e:
            self.logger.debug(f"Failed to reconstruct malformed expression: {e}")

        return None
    
    def identify_malformed_variables(self, missing_vars: list[str]) -> list[str]:
        """
        Identify variables that are malformed due to proxy evaluation.

        Args:
            missing_vars: List of missing variable names

        Returns:
            List of malformed variable names
        """
        # Look for missing variables that have composite patterns (parentheses and operators)
        return [var for var in missing_vars 
                if ("(" in var and ")" in var and 
                    any(op in var for op in MATH_OPERATORS))]
    
    def _rebuild_expression_from_malformed(self, expr: Any) -> Any | None:
        """
        Recursively rebuild an expression that contains malformed variable references.
        
        Args:
            expr: The expression to rebuild
            
        Returns:
            Rebuilt expression if successful, None otherwise
        """
        if isinstance(expr, VariableReference):
            # Check if this is a malformed variable reference
            var_symbol = expr.name
            if " = " in var_symbol:
                # This is malformed - try to extract the original pattern
                return self._parse_malformed_variable_pattern(var_symbol)
            elif var_symbol in self.variables:
                return expr
            elif (any(op in var_symbol for op in ["+", "-", "*", "/"]) and 
                  any(char.isalpha() for char in var_symbol) and 
                  var_symbol.count("_") >= 1):
                # This is a composite expression pattern - try to parse and rebuild it
                return self._parse_composite_expression_pattern(var_symbol)
            else:
                return None

        elif hasattr(expr, "symbol") and isinstance(getattr(expr, "symbol", None), str):
            # This might be a malformed Variable object (not VariableReference)
            var_symbol = expr.symbol
            if " = " in var_symbol:
                # This is malformed - try to extract the original pattern
                return self._parse_malformed_variable_pattern(var_symbol)
            elif var_symbol in self.variables:
                return self.variables[var_symbol]
            else:
                return None

        elif isinstance(expr, BinaryOperation):
            # Recursively rebuild operands
            left_rebuilt = self._rebuild_expression_from_malformed(expr.left)
            right_rebuilt = self._rebuild_expression_from_malformed(expr.right)

            if left_rebuilt and right_rebuilt:
                return BinaryOperation(expr.operator, left_rebuilt, right_rebuilt)

        elif isinstance(expr, UnaryFunction):
            operand_rebuilt = self._rebuild_expression_from_malformed(expr.operand)
            if operand_rebuilt:
                if expr.function_name == "sin":
                    return sin(operand_rebuilt)
                elif expr.function_name == "cos":
                    return cos(operand_rebuilt)
                else:
                    return UnaryFunction(expr.function_name, operand_rebuilt)

        elif isinstance(expr, Constant):
            return expr

        return None
    
    def _parse_malformed_variable_pattern(self, malformed_symbol: str) -> Any | None:
        """
        Parse a malformed variable symbol and extract the mathematical pattern.
        
        Args:
            malformed_symbol: The malformed symbol to parse
            
        Returns:
            Parsed expression if successful, None otherwise
        """
        # Import the parser for handling the actual pattern parsing
        from .expression_parser import ExpressionParser
        
        parser = ExpressionParser(self.variables, self.logger)
        return parser.parse_malformed_variable_pattern(malformed_symbol)
    
    def _parse_composite_expression_pattern(self, composite_symbol: str) -> Any | None:
        """
        Parse a composite expression pattern using the expression parser.
        
        Args:
            composite_symbol: The composite symbol to parse
            
        Returns:
            Parsed expression if successful, None otherwise
        """
        # Import the parser for handling the actual pattern parsing
        from .expression_parser import ExpressionParser
        
        parser = ExpressionParser(self.variables, self.logger)
        return parser.parse_composite_expression_pattern(composite_symbol)