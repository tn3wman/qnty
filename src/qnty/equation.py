"""
Equation System
===============

Mathematical equations for qnty variables with solving capabilities.
"""

from __future__ import annotations

from typing import cast

from .expression import Expression, VariableReference
from .variable_system.core import TypeSafeVariable

# Global optimization flags and cache
_SCOPE_DISCOVERY_ENABLED = False  # Disabled by default due to high overhead
_VARIABLE_TYPE_CACHE = {}  # Cache for hasattr checks


def _is_typesafe_variable(obj) -> bool:
    """Optimized type check with caching for hasattr calls."""
    obj_type = type(obj)
    if obj_type not in _VARIABLE_TYPE_CACHE:
        _VARIABLE_TYPE_CACHE[obj_type] = (
            hasattr(obj, 'symbol') and hasattr(obj, 'name') and hasattr(obj, 'quantity')
        )
    return _VARIABLE_TYPE_CACHE[obj_type]


class Equation:
    """
    Represents a mathematical equation with left-hand side equal to right-hand side.
    Optimized with __slots__ for memory efficiency.
    """
    __slots__ = ('name', 'lhs', 'rhs', '_variables')
    
    def __init__(self, name: str, lhs: TypeSafeVariable | Expression, rhs: Expression):
        self.name = name
        
        # Convert Variable to VariableReference if needed - use isinstance for performance
        if isinstance(lhs, TypeSafeVariable):
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
        unknown_vars = self.get_unknown_variables(known_vars)
        # Can solve if target_var is the only unknown
        return unknown_vars == {target_var}
    
    def solve_for(self, target_var: str, variable_values: dict[str, TypeSafeVariable]) -> TypeSafeVariable:
        """
        Solve the equation for target_var.
        Returns the target variable with updated quantity.
        """
        if target_var not in self.variables:
            raise ValueError(f"Variable '{target_var}' not found in equation")
        
        # Handle direct assignment: target = expression
        if isinstance(self.lhs, VariableReference) and self.lhs.name == target_var:
            # Direct assignment: target_var = rhs
            result_qty = self.rhs.evaluate(variable_values)
            
            # Update existing variable object to preserve references
            var_obj = variable_values.get(target_var)
            if var_obj is not None:
                # Convert result to the target variable's original unit if it had one
                if var_obj.quantity is not None and var_obj.quantity.unit is not None:
                    # Convert to the target variable's defined unit - be more specific about exceptions
                    try:
                        result_qty = result_qty.to(var_obj.quantity.unit)
                    except (ValueError, TypeError, AttributeError):
                        # Log specific conversion issues but continue with calculated unit
                        # This preserves the original behavior while being more explicit
                        pass
                
                var_obj.quantity = result_qty
                var_obj.is_known = True
                return var_obj
            
            # Create new variable if not found - this shouldn't happen in normal usage
            raise ValueError(f"Variable '{target_var}' not found in variable_values")
        
        # For more complex equations, we would need algebraic manipulation
        # Currently focusing on direct assignment which covers most engineering cases
        raise NotImplementedError(f"Cannot solve for {target_var} in equation {self}. "
                                f"Only direct assignment equations (var = expression) are supported.")
    
    def check_residual(self, variable_values: dict[str, TypeSafeVariable], tolerance: float = 1e-10) -> bool:
        """
        Check if equation is satisfied by evaluating residual (LHS - RHS).
        Returns True if |residual| < tolerance, accounting for units.
        """
        try:
            # Both lhs and rhs should be Expressions after __init__ conversion
            lhs_value = self.lhs.evaluate(variable_values)
            rhs_value = self.rhs.evaluate(variable_values)
            
            # Check dimensional compatibility
            if lhs_value._dimension_sig != rhs_value._dimension_sig:
                return False
            
            # Convert to same units for comparison
            rhs_converted = rhs_value.to(lhs_value.unit)
            residual = abs(lhs_value.value - rhs_converted.value)
            
            return residual < tolerance
        except (ValueError, TypeError, AttributeError, KeyError):
            # Handle specific expected errors during evaluation/conversion
            return False
        except Exception as e:
            # Re-raise unexpected errors to avoid masking bugs
            raise RuntimeError(f"Unexpected error in residual check for equation '{self.name}': {e}") from e
    
    def _discover_variables_from_scope(self) -> dict[str, TypeSafeVariable]:
        """
        Automatically discover variables from the calling scope.
        Now optimized with caching and conditional execution.
        """
        if not _SCOPE_DISCOVERY_ENABLED:
            return {}
            
        import inspect
        
        # Get the frame that called this method (skip through __str__ calls)
        frame = inspect.currentframe()
        try:
            # Skip frames until we find one outside the equation system
            depth = 0
            max_depth = 8  # Reduced from 10 for performance
            while frame and depth < max_depth and (
                frame.f_code.co_filename.endswith(('equation.py', 'expression.py')) or
                frame.f_code.co_name in ['__str__', '__repr__']
            ):
                frame = frame.f_back
                depth += 1
            
            if not frame:
                return {}
                
            # Only get local variables first (faster than combining both)
            local_vars = frame.f_locals
            required_vars = self.variables
            discovered = {}
            
            # First pass: check locals only (most common case)
            for var_name in required_vars:
                for obj in local_vars.values():
                    if _is_typesafe_variable(obj) and (
                        (hasattr(obj, 'symbol') and obj.symbol == var_name) or
                        (hasattr(obj, 'name') and obj.name == var_name)
                    ):
                        discovered[var_name] = obj
                        break
            
            # Second pass: check globals only if needed
            if len(discovered) < len(required_vars):
                global_vars = frame.f_globals
                remaining_vars = required_vars - discovered.keys()
                for var_name in remaining_vars:
                    for obj in global_vars.values():
                        if _is_typesafe_variable(obj) and (
                            (hasattr(obj, 'symbol') and obj.symbol == var_name) or
                            (hasattr(obj, 'name') and obj.name == var_name)
                        ):
                            discovered[var_name] = obj
                            break
            
            return discovered
            
        finally:
            del frame
    
    def _can_auto_solve(self) -> tuple[bool, str, dict[str, TypeSafeVariable]]:
        """Check if equation can be auto-solved from scope."""
        try:
            discovered = self._discover_variables_from_scope()
            
            # Check if this is a simple assignment equation (one unknown)
            unknowns = []
            knowns = []
            
            for var_name in self.variables:
                if var_name in discovered:
                    var = discovered[var_name]
                    if hasattr(var, 'is_known') and not var.is_known:
                        unknowns.append(var_name)
                    elif hasattr(var, 'quantity') and var.quantity is not None:
                        knowns.append(var_name)
                    else:
                        unknowns.append(var_name)  # Assume unknown if no quantity
                else:
                    return False, "", {}  # Missing variable
            
            # Can only auto-solve if there's exactly one unknown
            if len(unknowns) == 1:
                return True, unknowns[0], discovered
            
            return False, "", {}
            
        except Exception:
            return False, "", {}
    
    def _try_auto_solve(self) -> bool:
        """Try to automatically solve the equation if possible."""
        try:
            can_solve, target_var, variables = self._can_auto_solve()
            if can_solve:
                self.solve_for(target_var, variables)
                return True
            return False
        except Exception:
            return False
    
    def __str__(self) -> str:
        # Try to auto-solve if possible before displaying
        self._try_auto_solve()
        return f"{self.lhs} = {self.rhs}"
    
    def __repr__(self) -> str:
        return f"Equation(name='{self.name}', lhs={self.lhs!r}, rhs={self.rhs!r})"


class EquationSystem:
    """
    System of equations that can be solved together.
    Optimized with __slots__ for memory efficiency.
    """
    __slots__ = ('equations', 'variables', '_known_cache', '_unknown_cache')
    
    def __init__(self, equations: list[Equation] | None = None):
        self.equations = equations or []
        self.variables = {}  # Dict[str, TypeSafeVariable]
        self._known_cache: set[str] | None = None  # Cache for known variables
        self._unknown_cache: set[str] | None = None  # Cache for unknown variables
    
    def add_equation(self, equation: Equation):
        """Add an equation to the system."""
        self.equations.append(equation)
        self._invalidate_caches()
    
    def add_variable(self, variable: TypeSafeVariable):
        """Add a variable to the system."""
        self.variables[variable.name] = variable
        self._invalidate_caches()
    
    def _invalidate_caches(self):
        """Invalidate cached known/unknown variable sets."""
        self._known_cache = None
        self._unknown_cache = None
    
    def get_known_variables(self) -> set[str]:
        """Get names of all known variables (cached)."""
        if self._known_cache is None:
            self._known_cache = {name for name, var in self.variables.items() if var.is_known and var.quantity is not None}
        return self._known_cache
    
    def get_unknown_variables(self) -> set[str]:
        """Get names of all unknown variables (cached)."""
        if self._unknown_cache is None:
            self._unknown_cache = {name for name, var in self.variables.items() if not var.is_known or var.quantity is None}
        return self._unknown_cache
    
    def can_solve_any(self) -> bool:
        """Check if any equation can be solved with current known variables."""
        known_vars = self.get_known_variables()
        unknown_vars = self.get_unknown_variables()
        
        for equation in self.equations:
            for unknown_var in unknown_vars:
                if equation.can_solve_for(unknown_var, known_vars):
                    return True
        return False
    
    def solve_step(self) -> bool:
        """Solve one step - find and solve one equation. Returns True if progress made."""
        known_vars = self.get_known_variables()
        unknown_vars = self.get_unknown_variables()
        
        # Find an equation that can be solved
        for equation in self.equations:
            for unknown_var in unknown_vars:
                if equation.can_solve_for(unknown_var, known_vars):
                    # Solve for this variable
                    equation.solve_for(unknown_var, self.variables)
                    # Invalidate caches since variable states have changed
                    self._invalidate_caches()
                    return True  # Progress made
        
        return False  # No progress possible
    
    def solve(self, max_iterations: int = 100) -> bool:
        """Solve the system iteratively. Returns True if fully solved."""
        for _ in range(max_iterations):
            if not self.can_solve_any():
                break
            if not self.solve_step():
                break
        
        # Check if all variables are known
        unknown_vars = self.get_unknown_variables()
        return len(unknown_vars) == 0
    
    def get_solving_order(self) -> list[str]:
        """
        Get the order in which variables can be solved.
        Optimized to avoid creating full system copies.
        """
        order = []
        # Track known variables without modifying the original
        simulated_known = self.get_known_variables().copy()
        
        # Continue until no more variables can be solved
        max_iterations = len(self.variables)  # Prevent infinite loops
        iterations = 0
        
        while iterations < max_iterations:
            unknown_vars = {name for name in self.variables.keys() if name not in simulated_known}
            if not unknown_vars:
                break
                
            found_solvable = False
            # Find next solvable variable
            for equation in self.equations:
                for unknown_var in unknown_vars:
                    if equation.can_solve_for(unknown_var, simulated_known):
                        order.append(unknown_var)
                        # Simulate marking as known for next iteration
                        simulated_known.add(unknown_var)
                        found_solvable = True
                        break
                if found_solvable:
                    break
            
            if not found_solvable:
                break  # No more progress possible
                
            iterations += 1
        
        return order
    
    def __str__(self) -> str:
        return f"EquationSystem({len(self.equations)} equations, {len(self.variables)} variables)"
    
    def __repr__(self) -> str:
        return f"EquationSystem(equations={self.equations!r})"
