"""
Expression Parser for Equation Reconstruction System.

Handles parsing and rebuilding of mathematical expressions from string patterns.
"""

import re
from typing import Any
from logging import Logger

from qnty.expressions import BinaryOperation, Constant, UnaryFunction, VariableReference, cos, sin
from qnty.quantities.expression_quantity import ExpressionQuantity as Variable

# Type aliases
VariableDict = dict[str, Variable]

# Compiled regex patterns for performance
VARIABLE_PATTERN_DETAILED = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")


class ExpressionParser:
    """
    Focused class for parsing and rebuilding mathematical expressions.
    
    Handles conversion from string patterns to Expression objects using
    safe evaluation techniques and proper namespace management.
    """
    
    def __init__(self, variables: VariableDict, logger: Logger):
        """
        Initialize the expression parser.
        
        Args:
            variables: Dictionary of available variables
            logger: Logger for debugging
        """
        self.variables = variables
        self.logger = logger
    
    def parse_composite_expression_pattern(self, composite_symbol: str) -> Any | None:
        """
        Parse a composite expression pattern and reconstruct it using available variables.

        Args:
            composite_symbol: The composite expression string to parse

        Returns:
            Reconstructed expression if successful, None otherwise

        Examples:
            - "(branch_D - (branch_T_n - branch_c) * 2.0)" -> branch_D - 2.0 * (branch_T_n - branch_c)
            - "(header_T - header_c) * 2.5" -> (header_T - header_c) * 2.5
            - "d_2 * 2.0" -> d_2 * 2.0
            - "S_r / header_S" -> S_r / header_S
        """
        if not composite_symbol:
            return None

        pattern = composite_symbol

        # Handle simple patterns first (variable op constant/variable)
        simple_result = self._handle_simple_composite_patterns(pattern)
        if simple_result:
            return simple_result

        # Remove outer parentheses if the entire pattern is wrapped
        pattern = self._remove_outer_parentheses(pattern)

        # Extract variable names that exist in our system using compiled regex
        potential_vars = VARIABLE_PATTERN_DETAILED.findall(pattern)
        existing_vars = [var for var in potential_vars if var in self.variables]

        if len(existing_vars) < 1:
            self.logger.debug(f"No existing variables found in pattern: {pattern}")
            return None

        # Try to rebuild the mathematical pattern
        return self._rebuild_mathematical_pattern(pattern, existing_vars)
    
    def parse_malformed_variable_pattern(self, malformed_symbol: str) -> Any | None:
        """
        Parse a malformed variable symbol and reconstruct it using available variables.

        Args:
            malformed_symbol: The malformed variable symbol to parse

        Returns:
            Reconstructed expression if successful, None otherwise

        Examples:
            - "(var1 - (var2 - var3) * 2.0) = 1.315 in" -> var1 - 2.0 * (var2 - var3)
            - "(var1 + var2) = 0.397 in" -> var1 + var2
        """
        if not malformed_symbol or " = " not in malformed_symbol:
            return None

        pattern = malformed_symbol.split(" = ")[0].strip()

        # Remove outer parentheses if present
        pattern = self._remove_outer_parentheses(pattern)

        # Extract variable names that exist in our system using compiled regex
        potential_vars = VARIABLE_PATTERN_DETAILED.findall(pattern)
        existing_vars = [var for var in potential_vars if var in self.variables]

        if len(existing_vars) < 2:
            self.logger.debug(f"Insufficient variables in malformed pattern: {pattern}")
            return None

        # Try to rebuild common mathematical patterns
        return self._rebuild_mathematical_pattern(pattern, existing_vars)
    
    def parse_and_rebuild_expression(self, expr: Any, missing_vars: list[str]) -> Any | None:
        """
        Parse composite expressions and rebuild them using existing variables.

        Args:
            expr: The expression to parse and rebuild
            missing_vars: List of missing variable names

        Returns:
            Rebuilt expression if successful, None otherwise
        """
        if expr is None:
            return None

        if isinstance(expr, VariableReference):
            if expr.name in missing_vars:
                # This is a composite expression - try to parse and rebuild it
                return self.parse_composite_expression_pattern(expr.name)
            return expr

        elif isinstance(expr, BinaryOperation):
            # Recursively rebuild operands
            left_rebuilt = self.parse_and_rebuild_expression(expr.left, missing_vars)
            right_rebuilt = self.parse_and_rebuild_expression(expr.right, missing_vars)

            if left_rebuilt and right_rebuilt:
                return BinaryOperation(expr.operator, left_rebuilt, right_rebuilt)

        elif isinstance(expr, UnaryFunction):
            # Recursively rebuild operand
            operand_rebuilt = self.parse_and_rebuild_expression(expr.operand, missing_vars)

            if operand_rebuilt:
                return UnaryFunction(expr.function_name, operand_rebuilt)

        elif isinstance(expr, Constant):
            return expr

        return None
    
    def _handle_simple_composite_patterns(self, pattern: str) -> Any | None:
        """
        Handle simple composite patterns like 'var * const' or 'var1 / var2'.

        Args:
            pattern: The pattern string to handle

        Returns:
            Reconstructed expression if successful, None otherwise
        """
        pattern = pattern.strip()

        # Handle patterns like "d_2 * 2.0"
        if " * " in pattern:
            parts = pattern.split(" * ", 1)
            if len(parts) == 2:
                left_part, right_part = parts
                left_part = left_part.strip()
                right_part = right_part.strip()

                # Check if left is variable and right is number
                if left_part in self.variables:
                    try:
                        right_value = float(right_part)
                        left_var_ref = VariableReference(self.variables[left_part])
                        return left_var_ref * right_value
                    except ValueError:
                        # Right part is not a number, check if it's a variable
                        if right_part in self.variables:
                            left_var_ref = VariableReference(self.variables[left_part])
                            right_var_ref = VariableReference(self.variables[right_part])
                            return left_var_ref * right_var_ref

        # Handle patterns like "S_r / header_S"
        elif " / " in pattern:
            parts = pattern.split(" / ", 1)
            if len(parts) == 2:
                left_part, right_part = parts
                left_part = left_part.strip()
                right_part = right_part.strip()

                # Check if both are variables
                if left_part in self.variables and right_part in self.variables:
                    left_var_ref = VariableReference(self.variables[left_part])
                    right_var_ref = VariableReference(self.variables[right_part])
                    return left_var_ref / right_var_ref

                # Check if left is variable and right is number
                elif left_part in self.variables:
                    try:
                        right_value = float(right_part)
                        left_var_ref = VariableReference(self.variables[left_part])
                        return left_var_ref / right_value
                    except ValueError:
                        pass

        # Handle patterns like "var + const", "var - const"
        elif " + " in pattern or " - " in pattern:
            # Find the operator
            if " + " in pattern:
                operator = "+"
                parts = pattern.split(" + ", 1)
            else:
                operator = "-"
                parts = pattern.split(" - ", 1)

            if len(parts) == 2:
                left_part, right_part = parts
                left_part = left_part.strip()
                right_part = right_part.strip()

                if left_part in self.variables:
                    left_var_ref = VariableReference(self.variables[left_part])

                    # Try as number first
                    try:
                        right_value = float(right_part)
                        if operator == "+":
                            return left_var_ref + right_value
                        else:
                            return left_var_ref - right_value
                    except ValueError:
                        # Try as variable
                        if right_part in self.variables:
                            right_var_ref = VariableReference(self.variables[right_part])
                            if operator == "+":
                                return left_var_ref + right_var_ref
                            else:
                                return left_var_ref - right_var_ref

        return None
    
    def _remove_outer_parentheses(self, pattern: str) -> str:
        """
        Remove outer parentheses if they wrap the entire expression.

        Args:
            pattern: The pattern string to process

        Returns:
            Pattern with outer parentheses removed if appropriate
        """
        if not pattern.startswith("(") or not pattern.endswith(")"):
            return pattern

        # Count parentheses to make sure we're removing the outermost pair
        paren_count = 0
        for char in pattern[1:-1]:
            if char == "(":
                paren_count += 1
            elif char == ")":
                paren_count -= 1
                if paren_count < 0:
                    return pattern  # Don't remove - they don't wrap everything

        # We made it through without breaking, so the outer parens wrap everything
        return pattern[1:-1]
    
    def _rebuild_mathematical_pattern(self, pattern: str, existing_vars: list[str]) -> Any | None:
        """
        Rebuild mathematical expressions from string patterns using existing variables.

        Args:
            pattern: The mathematical pattern string to rebuild
            existing_vars: List of existing variable names to use

        Returns:
            Reconstructed expression if successful, None otherwise

        Note:
            Uses eval() in a controlled namespace with only VariableReference objects
            to ensure we get Expression objects instead of evaluated Variables.
        """
        if not pattern or not existing_vars:
            return None

        try:
            # Build secure namespace with VariableReference objects
            namespace: dict[str, Any] = {"__builtins__": {}}

            # Add VariableReference objects to namespace for secure evaluation
            for var_name in existing_vars:
                if var_name in self.variables:
                    # Create VariableReference to get Expression objects instead of raw values
                    var_ref = VariableReference(self.variables[var_name])
                    namespace[var_name] = var_ref
                else:
                    self.logger.debug(f"Variable '{var_name}' not found in available variables")

            # Evaluate the pattern to create the expression
            self.logger.debug(f"Rebuilding pattern: '{pattern}' with vars: {existing_vars}")
            result = eval(pattern, namespace)
            self.logger.debug(f"Rebuild result: {result} (type: {type(result)})")

            return result

        except Exception as e:
            self.logger.debug(f"Failed to rebuild pattern '{pattern}': {e}")
            return None