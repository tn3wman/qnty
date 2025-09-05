"""
Equation reconstruction system for handling composite expressions.

This module provides the advanced equation reconstruction capabilities
that allow EngineeringProblem to automatically fix malformed equations
created during composition and proxy operations.
"""

from logging import Logger
from typing import Any

from qnty.equations.equation import Equation
from qnty.quantities.unified_variable import UnifiedVariable as Variable
from .expression_parser import ExpressionParser
from .namespace_mapper import NamespaceMapper
from .delayed_expression_resolver import DelayedExpressionResolver
from .composite_expression_rebuilder import CompositeExpressionRebuilder

# Type aliases for better readability
VariableDict = dict[str, Variable]
ReconstructionResult = Equation | None

# Constants for pattern matching  
CONDITIONAL_PATTERNS: set[str] = {"cond("}
FUNCTION_PATTERNS: set[str] = {"sin(", "cos(", "tan(", "log(", "exp("}
MATH_OPERATORS: set[str] = {"(", ")", "+", "-", "*", "/"}


# Custom exceptions for better error handling
class EquationReconstructionError(Exception):
    """Base exception for equation reconstruction errors."""
    pass


class MalformedExpressionError(EquationReconstructionError):
    """Raised when expressions are malformed and cannot be reconstructed."""
    pass


class NamespaceMappingError(EquationReconstructionError):
    """Raised when namespace mapping fails."""
    pass


class PatternReconstructionError(EquationReconstructionError):
    """Raised when mathematical pattern reconstruction fails."""
    pass


class EquationReconstructor:
    """
    Handles reconstruction of equations with composite expressions.

    This refactored class provides equation reconstruction capabilities by
    coordinating focused component classes for parsing, namespace mapping,
    delayed resolution, and composite expression rebuilding.

    Key Features:
    - Delegates to focused component classes for specific responsibilities
    - Generic composite expression reconstruction
    - Malformed equation recovery from proxy operations
    - Namespace variable mapping and resolution
    - Mathematical pattern parsing and rebuilding
    - Performance optimization through focused caching

    Example Usage:
        reconstructor = EquationReconstructor(problem)
        fixed_equation = reconstructor.fix_malformed_equation(broken_equation)
    """

    def __init__(self, problem: Any) -> None:
        """
        Initialize the equation reconstructor.

        Args:
            problem: The EngineeringProblem instance containing variables and logger

        Raises:
            ValueError: If problem doesn't have required attributes
        """
        if not hasattr(problem, "variables") or not hasattr(problem, "logger"):
            raise ValueError("Problem must have 'variables' and 'logger' attributes")

        self.problem: Any = problem
        self.variables: VariableDict = problem.variables
        self.logger: Logger = problem.logger

        # Initialize focused component classes
        self.expression_parser = ExpressionParser(self.variables, self.logger)
        self.namespace_mapper = NamespaceMapper(self.variables, self.logger)
        self.delayed_resolver = DelayedExpressionResolver(self.variables, self.logger)
        self.composite_rebuilder = CompositeExpressionRebuilder(self.variables, self.logger)

    def fix_malformed_equation(self, equation: Equation) -> ReconstructionResult:
        """
        Generic method to fix equations that were malformed during class definition.

        Specifically handles composite expressions like '(D - (T - c) * 2.0)' that should
        reference namespaced variables like 'branch_D', 'branch_T', 'branch_c'.

        Args:
            equation: The malformed equation to fix

        Returns:
            Fixed equation if reconstruction succeeds, None otherwise

        Raises:
            EquationReconstructionError: If equation reconstruction fails with detailed error
        """
        if equation is None:
            return None

        try:
            # Get all variables referenced in the equation
            all_vars = equation.get_all_variables()
            missing_vars = [var for var in all_vars if var not in self.variables]

            if not missing_vars:
                return equation  # Nothing to fix

            self.logger.debug(f"Found missing variables in equation: {missing_vars}")

            # Attempt to reconstruct equations with composite variables using generic approach
            fixed_equation = self._reconstruct_composite_expressions(equation, missing_vars)

            if fixed_equation:
                self.logger.debug(f"Successfully reconstructed equation: {fixed_equation}")
                return fixed_equation
            else:
                self.logger.debug("Failed to reconstruct equation")
                return None

        except Exception as e:
            self.logger.debug(f"Error in fix_malformed_equation: {e}")
            return None

    def _reconstruct_composite_expressions(self, equation: Equation, missing_vars: list[str]) -> ReconstructionResult:
        """
        Generic reconstruction of equations with composite expressions.

        Delegates to NamespaceMapper for variable mapping and ExpressionParser 
        for substitution operations.

        Args:
            equation: The equation to reconstruct
            missing_vars: List of missing variable names

        Returns:
            Reconstructed equation if successful, None otherwise

        Raises:
            NamespaceMappingError: If namespace mapping fails
        """
        if not missing_vars:
            return None

        try:
            # Extract variable symbols from composite expressions
            composite_vars = self.namespace_mapper.extract_base_variables_from_composites(missing_vars)

            if not composite_vars:
                self.logger.debug("No composite variables found to extract")
                return None

            # Find which namespaces contain these variables
            namespace_mappings = self.namespace_mapper.find_namespace_mappings(composite_vars)

            if not namespace_mappings:
                self.logger.debug("No namespace mappings found")
                return None

            # Reconstruct the equation by substituting composite expressions
            return self._substitute_composite_expressions(equation, missing_vars, namespace_mappings)

        except Exception as e:
            self.logger.debug(f"Error in _reconstruct_composite_expressions: {e}")
            return None

    def _substitute_composite_expressions(self, equation: Equation, missing_vars: list[str], namespace_mappings: dict[str, str]) -> ReconstructionResult:
        """
        Substitute composite expressions with properly namespaced variables.

        Args:
            equation: The equation to substitute expressions in
            missing_vars: List of missing variable names
            namespace_mappings: Mapping from base variables to namespaced variables

        Returns:
            Reconstructed equation if successful, None otherwise
        """
        if not missing_vars or not namespace_mappings:
            return None

        try:
            # Get the equation string representation for debugging
            eq_str = str(equation)
            self.logger.debug(f"Substituting expressions in equation: {eq_str}")

            # For each missing composite expression, try to rebuild it
            for missing_var in missing_vars:
                if missing_var in eq_str:
                    reconstructed_expr = self._reconstruct_expression_from_mapping(missing_var, namespace_mappings)
                    if reconstructed_expr:
                        # Replace the original equation's RHS or LHS
                        lhs_var = self._get_lhs_variable(equation)
                        if lhs_var:
                            return lhs_var.equals(reconstructed_expr)

            return None

        except Exception as e:
            self.logger.debug(f"Error in _substitute_composite_expressions: {e}")
            return None

    def _reconstruct_expression_from_mapping(self, composite_expr: str, namespace_mappings: dict[str, str]) -> Any | None:
        """
        Reconstruct a composite expression using the namespace mappings.

        Args:
            composite_expr: The composite expression string to reconstruct
            namespace_mappings: Mapping from base variables to namespaced variables

        Returns:
            Reconstructed expression if successful, None otherwise
        """
        if not composite_expr or not namespace_mappings:
            return None

        try:
            # Create a substitution pattern for the expression
            substituted_expr = composite_expr

            # Replace base variable names with their namespaced counterparts
            import re
            for base_var, namespaced_var in namespace_mappings.items():
                if namespaced_var in self.variables:
                    # Use word boundary regex to avoid partial matches
                    pattern = r"\b" + re.escape(base_var) + r"\b"
                    substituted_expr = re.sub(pattern, namespaced_var, substituted_expr)

            # Try to evaluate the substituted expression using the expression parser
            return self.expression_parser.parse_composite_expression_pattern(substituted_expr)

        except Exception as e:
            self.logger.debug(f"Error in expression reconstruction: {e}")
            return None

    def _get_lhs_variable(self, equation: Equation) -> Variable | None:
        """
        Safely extract the left-hand side variable from an equation.

        Args:
            equation: The equation to extract LHS from

        Returns:
            The LHS variable if valid, None otherwise
        """
        # Import here to avoid circular imports
        from qnty.expressions import VariableReference
        
        # Check if lhs is a VariableReference
        if isinstance(equation.lhs, VariableReference):
            var_name = equation.lhs.name
            if var_name in self.variables:
                return self.variables[var_name]
        # Check if lhs is a Variable with symbol attribute
        elif hasattr(equation.lhs, "symbol"):
            symbol = getattr(equation.lhs, "symbol", None)
            if isinstance(symbol, str) and symbol in self.variables:
                return self.variables[symbol]

        return None

    def contains_delayed_expressions(self, equation: Equation) -> bool:
        """
        Check if an equation contains delayed expressions that need resolution.

        Args:
            equation: The equation to check for delayed expressions

        Returns:
            True if equation contains delayed expressions
        """
        return self.delayed_resolver.contains_delayed_expressions(equation)

    def resolve_delayed_equation(self, equation: Equation) -> ReconstructionResult:
        """
        Resolve a delayed equation by evaluating its delayed expressions.

        Args:
            equation: The equation with delayed expressions to resolve

        Returns:
            Resolved equation if successful, None otherwise
        """
        return self.delayed_resolver.resolve_delayed_equation(equation)

    def should_attempt_reconstruction(self, equation: Equation) -> bool:
        """
        Determine if we should attempt to reconstruct this equation.

        Only attempt reconstruction for simple mathematical expressions,
        not complex structures like conditionals.

        Args:
            equation: The equation to evaluate for reconstruction

        Returns:
            True if reconstruction should be attempted
        """
        if equation is None:
            return False

        try:
            equation_str = str(equation)

            # Skip conditional equations using constant set
            if any(pattern in equation_str for pattern in CONDITIONAL_PATTERNS):
                return False

            # Skip equations with complex function calls
            if any(func in equation_str for func in FUNCTION_PATTERNS):
                # These might be complex - only attempt if they're in the problematic patterns
                self.logger.debug(f"Equation contains complex functions: {equation_str}")

            # Only attempt if the missing variables look like mathematical expressions
            all_vars = equation.get_all_variables()
            missing_vars = [var for var in all_vars if var not in self.variables]

            for missing_var in missing_vars:
                # Check if this looks like a mathematical expression we can handle
                if any(char in missing_var for char in MATH_OPERATORS):
                    return True

            return False

        except Exception as e:
            self.logger.debug(f"Error in should_attempt_reconstruction: {e}")
            return False

    def reconstruct_composite_expressions_generically(self, equation: Equation) -> ReconstructionResult:
        """
        Generically reconstruct equations with composite expressions by parsing the
        composite symbols and rebuilding them from existing variables.

        Enhanced to handle malformed expressions from proxy evaluation.

        Args:
            equation: The equation to reconstruct

        Returns:
            Reconstructed equation if successful, None otherwise

        Raises:
            MalformedExpressionError: If expressions are too malformed to reconstruct
        """
        if equation is None:
            return None

        try:
            all_vars = equation.get_all_variables()
            missing_vars = [var for var in all_vars if var not in self.variables]

            if not missing_vars:
                return equation

            # Get the LHS variable with proper validation
            lhs_var = self._get_lhs_variable(equation)
            if lhs_var is None:
                return None

            # Check for malformed expressions that contain evaluated numeric values
            malformed_vars = self.composite_rebuilder.identify_malformed_variables(missing_vars)

            if malformed_vars:
                # This is a malformed expression from proxy evaluation
                reconstructed_rhs = self.composite_rebuilder.reconstruct_malformed_proxy_expression(equation, malformed_vars)
                if reconstructed_rhs:
                    return lhs_var.equals(reconstructed_rhs)
                return None

            # Reconstruct the RHS by parsing and rebuilding composite expressions
            reconstructed_rhs = self.expression_parser.parse_and_rebuild_expression(equation.rhs, missing_vars)

            if reconstructed_rhs:
                return lhs_var.equals(reconstructed_rhs)

            return None

        except Exception as e:
            self.logger.debug(f"Reconstruction failed: {e}")
            return None

    def _clear_caches(self) -> None:
        """
        Clear all internal caches. Should be called when variables change.

        This method provides a way to reset cached data when the problem
        state changes, ensuring cache consistency.
        """
        self.namespace_mapper.clear_caches()

    # Delegation methods for public API compatibility
    def parse_composite_expression_pattern(self, composite_symbol: str) -> Any | None:
        """
        Parse a composite expression pattern using the expression parser.
        
        Args:
            composite_symbol: The composite expression string to parse
            
        Returns:
            Reconstructed expression if successful, None otherwise
        """
        return self.expression_parser.parse_composite_expression_pattern(composite_symbol)
    
    def parse_malformed_variable_pattern(self, malformed_symbol: str) -> Any | None:
        """
        Parse a malformed variable pattern using the expression parser.
        
        Args:
            malformed_symbol: The malformed variable symbol to parse
            
        Returns:
            Reconstructed expression if successful, None otherwise
        """
        return self.expression_parser.parse_malformed_variable_pattern(malformed_symbol)

    def parse_and_rebuild_expression(self, expr: Any, missing_vars: list[str]) -> Any | None:
        """
        Parse composite expressions and rebuild them using existing variables.

        Args:
            expr: The expression to parse and rebuild
            missing_vars: List of missing variable names

        Returns:
            Rebuilt expression if successful, None otherwise
        """
        return self.expression_parser.parse_and_rebuild_expression(expr, missing_vars)