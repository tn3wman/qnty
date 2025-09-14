"""
Equation System
===============

Mathematical equations for qnty variables with solving capabilities.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from ..constants import SOLVER_DEFAULT_TOLERANCE
from ..core.quantity import FieldQuantity
from ..utils.scope_discovery import ScopeDiscoveryService
from .nodes import Expression, VariableReference

if TYPE_CHECKING:
    from ..core.quantity import Quantity

_logger = logging.getLogger(__name__)

# Global optimization flags
_SCOPE_DISCOVERY_ENABLED = False  # Disabled by default due to high overhead


class Equation:
    """
    Represents a mathematical equation with left-hand side equal to right-hand side.
    Optimized with __slots__ for memory efficiency.
    """

    __slots__ = ("name", "lhs", "rhs", "_variables")

    def __init__(self, name: str, lhs: FieldQuantity | Expression, rhs: Expression):
        self.name = name

        # Convert Variable to VariableReference if needed - use isinstance for performance
        if isinstance(lhs, FieldQuantity):
            self.lhs = VariableReference(lhs)
        else:
            # It's already an Expression
            self.lhs = cast(Expression, lhs)

        self.rhs = rhs
        self._variables: set[str] | None = None  # Lazy initialization for better performance

    def get_all_variables(self) -> set[str]:
        """Get all variable names used in this equation."""
        if self._variables is None:
            # Both lhs and rhs should be Expressions after __init__ conversion
            lhs_vars = self.lhs.get_variables()
            rhs_vars = self.rhs.get_variables()
            self._variables = lhs_vars | rhs_vars
        return self._variables

    @property
    def variables(self) -> set[str]:
        """Get all variable names used in this equation (cached property)."""
        return self.get_all_variables()

    def get_unknown_variables(self, known_vars: set[str]) -> set[str]:
        """Get variables that are unknown (not in known_vars set)."""
        return self.variables - known_vars

    def get_known_variables(self, known_vars: set[str]) -> set[str]:
        """Get variables that are known (in known_vars set)."""
        return self.variables & known_vars

    def can_solve_for(self, target_var: str, known_vars: set[str]) -> bool:
        """Check if this equation can solve for target_var given known_vars."""
        if target_var not in self.variables:
            return False

        # Direct assignment case: lhs is the variable
        if isinstance(self.lhs, VariableReference) and self.lhs.name == target_var:
            rhs_vars = self.rhs.get_variables()
            return rhs_vars.issubset(known_vars)

        # General case: can solve if target_var is the only unknown
        unknown_vars = self.get_unknown_variables(known_vars)
        return unknown_vars == {target_var}

    def _solve_algebraically(self, target_var: str, variable_values: dict[str, FieldQuantity]) -> Quantity | None:
        """
        Attempt to solve equation algebraically for target_var.
        Handles common algebraic manipulations.
        """
        # Case 1: LHS is a simple variable (X = expression)
        # But we need to solve for a variable in the RHS
        if hasattr(self.lhs, "name"):
            lhs_var = self.lhs.name
            if lhs_var in variable_values and hasattr(variable_values[lhs_var], "is_known") and variable_values[lhs_var].is_known:
                # LHS is known, need to solve RHS = LHS for target_var
                return self._solve_expression_for_var(self.rhs, target_var, self.lhs.evaluate(variable_values), variable_values)

        # Case 2: RHS is a simple variable (expression = X)
        # And we need to solve for a variable in the LHS
        if hasattr(self.rhs, "name"):
            rhs_var = self.rhs.name
            if rhs_var in variable_values and hasattr(variable_values[rhs_var], "is_known") and variable_values[rhs_var].is_known:
                # RHS is known, need to solve LHS = RHS for target_var
                return self._solve_expression_for_var(self.lhs, target_var, self.rhs.evaluate(variable_values), variable_values)

        # Case 3: Both sides are expressions
        # Try to isolate target_var
        return self._isolate_variable(target_var, variable_values)

    def _solve_expression_for_var(self, expr: Expression, target_var: str, known_value: Quantity, variable_values: dict[str, FieldQuantity]) -> Quantity | None:
        """
        Solve expression = known_value for target_var.
        Handles common patterns like A + B = C, A * B = C, etc.
        """
        if not hasattr(expr, "operator") or not hasattr(expr, "left") or not hasattr(expr, "right"):
            return None

        # Handle binary operations
        left_has_target = target_var in expr.left.get_variables()
        right_has_target = target_var in expr.right.get_variables()

        # Target should be in exactly one side
        if left_has_target and right_has_target:
            return None  # Too complex

        if not left_has_target and not right_has_target:
            return None  # Target not in expression

        # Evaluate the side without the target
        if left_has_target:
            # Target is on left, evaluate right
            right_val = expr.right.evaluate(variable_values)
            # Now solve: left op right_val = known_value for target in left
            return self._invert_operation(expr.operator, expr.left, right_val, known_value, target_var, variable_values, is_left=True)
        else:
            # Target is on right, evaluate left
            left_val = expr.left.evaluate(variable_values)
            # Now solve: left_val op right = known_value for target in right
            return self._invert_operation(expr.operator, expr.right, left_val, known_value, target_var, variable_values, is_left=False)

    def _invert_operation(
        self, operator: str, target_expr: Expression, other_val: Quantity, result_val: Quantity, target_var: str, variable_values: dict[str, FieldQuantity], is_left: bool
    ) -> Quantity | None:
        """
        Invert a binary operation to solve for target_var.

        If is_left=True: solve target_expr op other_val = result_val for target_var in target_expr
        If is_left=False: solve other_val op target_expr = result_val for target_var in target_expr
        """
        # Simple case: target_expr is just the variable we're looking for
        if hasattr(target_expr, "name") and target_expr.name == target_var:
            if operator == "+":
                # A + B = C => A = C - B
                return result_val - other_val
            elif operator == "-":
                if is_left:
                    # A - B = C => A = C + B
                    return result_val + other_val
                else:
                    # B - A = C => A = B - C
                    return other_val - result_val
            elif operator == "*":
                # A * B = C => A = C / B
                return result_val / other_val
            elif operator == "/":
                if is_left:
                    # A / B = C => A = C * B
                    return result_val * other_val
                else:
                    # B / A = C => A = B / C
                    return other_val / result_val
            elif operator == "**":
                if is_left:
                    # A ** B = C => A = C ** (1/B)
                    # Only works if B is a constant
                    if hasattr(other_val, "value") and other_val.value is not None:
                        try:
                            exponent = 1.0 / other_val.value
                            if hasattr(result_val, "__pow__"):
                                return result_val.__pow__(exponent)
                            elif hasattr(result_val, "value") and hasattr(result_val, "unit"):
                                # Manual power calculation for Quantity types
                                new_value = result_val.value**exponent
                                return type(result_val)(new_value, result_val.unit)
                        except (ZeroDivisionError, ValueError, TypeError, AttributeError):
                            pass
                # B ** A = C is more complex, skip for now

        # Recursively solve if target_expr is also a binary operation
        return self._solve_expression_for_var(target_expr, target_var, result_val, variable_values)

    def _isolate_variable(self, target_var: str, variable_values: dict[str, FieldQuantity]) -> Quantity | None:
        """
        Try to isolate target_var when both LHS and RHS are complex expressions.
        This is a simplified version that handles basic cases.
        """
        # For now, we don't handle complex equation rearrangement
        # This could be expanded in the future with a proper algebraic solver
        return None

    def solve_for(self, target_var: str, variable_values: dict[str, FieldQuantity]) -> FieldQuantity:
        """
        Solve the equation for target_var.
        Returns the target variable with updated quantity.
        """
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' not found in equation")

        # Case 1: Direct assignment: target = expression
        if isinstance(self.lhs, VariableReference) and self.lhs.name == target_var:
            # Direct assignment: target_var = rhs
            result_qty = self.rhs.evaluate(variable_values)

        # Case 2: Try algebraic manipulation for simple cases
        else:
            result_qty = self._solve_algebraically(target_var, variable_values)
            if result_qty is None:
                raise NotImplementedError(f"Cannot solve for {target_var} in equation {self}. Algebraic manipulation not supported for this equation form.")

        # Get the variable object to update
        var_obj = variable_values.get(target_var)
        if var_obj is None:
            raise ValueError(f"Variable '{target_var}' not found in variable_values")

        # Convert result to preferred unit or original unit if available
        target_unit_constant = None

        # First priority: existing quantity unit
        if var_obj.quantity is not None and hasattr(var_obj.quantity, "unit"):
            target_unit_constant = getattr(var_obj.quantity, "unit", None)
        # Second priority: preferred unit from constructor
        elif hasattr(var_obj, "preferred_unit") and var_obj.preferred_unit is not None:
            # Look up unit constant from string name
            preferred_unit_name = var_obj.preferred_unit
            try:
                # Get the dimension-specific units class
                class_name = var_obj.__class__.__name__
                units_class_name = f"{class_name}Units"

                # Import unit catalog dynamically to avoid circular imports
                from ..core import unit_catalog

                units_class = getattr(unit_catalog, units_class_name, None)
                if units_class and hasattr(units_class, preferred_unit_name):
                    target_unit_constant = getattr(units_class, preferred_unit_name)
                    _logger.debug(f"Found preferred unit constant: {preferred_unit_name}")
                else:
                    _logger.debug(f"Could not find unit constant for {preferred_unit_name} in {units_class_name}")
            except (ImportError, AttributeError) as e:
                _logger.debug(f"Failed to lookup preferred unit {preferred_unit_name}: {e}")

        if target_unit_constant is not None:
            try:
                result_qty = result_qty.to(target_unit_constant)
                _logger.debug(f"Converted {target_var} result to preferred unit: {target_unit_constant.symbol}")
            except (ValueError, TypeError, AttributeError) as e:
                _logger.debug(f"Unit conversion failed for {target_var} to {target_unit_constant}: {e}. Using calculated unit.")

        # Update the variable and return it
        if result_qty.value is not None:
            var_obj.value = result_qty.value
            # Try to set quantity if possible
            try:
                if hasattr(result_qty, "unit"):
                    var_obj.quantity = result_qty
            except (AttributeError, TypeError):
                pass  # Quantity assignment not supported

        # Set known status using appropriate attribute
        try:
            if hasattr(var_obj, "_is_known"):
                var_obj._is_known = True
            elif hasattr(var_obj, "is_known"):
                var_obj.is_known = True
        except (AttributeError, TypeError):
            pass  # Known status setting not supported
        return var_obj

    def check_residual(self, variable_values: dict[str, FieldQuantity], tolerance: float = SOLVER_DEFAULT_TOLERANCE) -> bool:
        """
        Check if equation is satisfied by evaluating residual (LHS - RHS).
        Returns True if |residual| < tolerance, accounting for units.
        """
        try:
            # Both lhs and rhs should be Expressions after __init__ conversion
            lhs_value = self.lhs.evaluate(variable_values)
            rhs_value = self.rhs.evaluate(variable_values)

            # Check dimensional compatibility using public API
            if not self._are_dimensionally_compatible(lhs_value, rhs_value):
                return False

            # Convert to same units for comparison
            if hasattr(lhs_value, "unit") and hasattr(rhs_value, "to"):
                rhs_converted = rhs_value.to(lhs_value.unit)
                if hasattr(lhs_value, "value") and hasattr(rhs_converted, "value") and lhs_value.value is not None and rhs_converted.value is not None:
                    residual = abs(lhs_value.value - rhs_converted.value)
                else:
                    residual = float("inf")
            else:
                if hasattr(lhs_value, "value") and hasattr(rhs_value, "value") and lhs_value.value is not None and rhs_value.value is not None:
                    residual = abs(lhs_value.value - rhs_value.value)
                else:
                    residual = float("inf")

            return residual < tolerance
        except (ValueError, TypeError, AttributeError, KeyError) as e:
            _logger.debug(f"Expected error in residual check for equation '{self.name}': {e}")
            return False
        except Exception as e:
            error_msg = f"Unexpected error in residual check for equation '{self.name}': {e}"
            _logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def _discover_variables_from_scope(self) -> dict[str, FieldQuantity]:
        """
        Automatically discover variables from the calling scope using centralized service.
        """
        if not _SCOPE_DISCOVERY_ENABLED:
            return {}

        # Use centralized scope discovery service
        return ScopeDiscoveryService.discover_variables(self.variables, enable_caching=True)

    def _are_dimensionally_compatible(self, lhs_value, rhs_value) -> bool:
        """Check if two quantities are dimensionally compatible."""
        try:
            # Try to convert - if successful, they're compatible
            rhs_value.to(lhs_value.unit)
            return True
        except (ValueError, TypeError, AttributeError):
            return False

    def _analyze_variable_states(self, discovered: dict[str, FieldQuantity]) -> dict[str, str]:
        """Analyze which variables are known vs unknown."""
        states = {}
        for var_name in self.variables:
            if var_name not in discovered:
                states[var_name] = "missing"
            else:
                var = discovered[var_name]
                if hasattr(var, "is_known") and not var.is_known:
                    states[var_name] = "unknown"
                elif hasattr(var, "quantity") and var.quantity is not None:
                    states[var_name] = "known"
                else:
                    states[var_name] = "unknown"
        return states

    def _determine_solvability(self, states: dict[str, str], discovered: dict[str, FieldQuantity]) -> tuple[bool, str, dict[str, FieldQuantity]]:
        """Determine if equation can be solved based on variable states."""
        if "missing" in states.values():
            return False, "", {}

        unknowns = [name for name, state in states.items() if state == "unknown"]

        # Can only auto-solve if there's exactly one unknown
        if len(unknowns) == 1:
            return True, unknowns[0], discovered

        return False, "", {}

    def _can_auto_solve(self) -> tuple[bool, str, dict[str, FieldQuantity]]:
        """Check if equation can be auto-solved from scope using centralized service."""
        try:
            discovered = self._discover_variables_from_scope()
            if not discovered:
                return False, "", {}

            variable_states = self._analyze_variable_states(discovered)
            return self._determine_solvability(variable_states, discovered)

        except (AttributeError, KeyError, ValueError, TypeError) as e:
            _logger.debug(f"Cannot auto-solve equation '{self.name}': {e}")
            return False, "", {}

    def _try_auto_solve(self) -> bool:
        """Try to automatically solve the equation if possible."""
        try:
            can_solve, target_var, variables = self._can_auto_solve()
            if can_solve:
                self.solve_for(target_var, variables)
                return True
            return False
        except (AttributeError, KeyError, ValueError, TypeError) as e:
            _logger.debug(f"Auto-solve failed for equation '{self.name}': {e}")
            return False

    def __str__(self) -> str:
        # Try to auto-solve if possible before displaying
        self._try_auto_solve()
        return f"{self.lhs} = {self.rhs}"

    def __repr__(self) -> str:
        return f"Equation(name='{self.name}', lhs={self.lhs!r}, rhs={self.rhs!r})"
