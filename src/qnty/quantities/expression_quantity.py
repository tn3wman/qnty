"""
Expression Variable Base Class
==============================

Base class that extends TypeSafeVariable with mathematical expression
and equation capabilities.
"""

from __future__ import annotations

from ..equations.equation import Equation
from ..expressions import BinaryOperation, Expression, wrap_operand, ScopeDiscoveryService
from .quantity import Quantity, TypeSafeVariable

# Type alias for cleaner method signatures
Operand = TypeSafeVariable | Quantity | int | float | Expression
ReverseOperand = Quantity | int | float

# Cache for commonly used wrapped constants to avoid repeated wrap_operand calls
_CONSTANT_CACHE = {}


def _initialize_constant_cache():
    """Initialize cache with common constants."""
    common_constants = [0, 1, 2, 3, 4, 5, -1, -2, 0.5, 1.0, 2.0, 10, 100, 1000]
    for value in common_constants:
        _CONSTANT_CACHE[value] = wrap_operand(value)


# Initialize on module load
_initialize_constant_cache()


class ExpressionQuantity(TypeSafeVariable):
    """
    TypeSafeVariable extended with expression and equation capabilities.

    This adds mathematical operations that create expressions and equations,
    keeping the base TypeSafeVariable free of these dependencies.
    """

    def _get_self_wrapped(self) -> Expression:
        """Get wrapped self expression, cached for performance."""
        if not hasattr(self, "_wrapped_self"):
            self._wrapped_self = wrap_operand(self)
        return self._wrapped_self

    @staticmethod
    def _get_cached_constant(value) -> Expression:
        """Get cached wrapped constant for common values."""
        if isinstance(value, int | float) and value in _CONSTANT_CACHE:
            return _CONSTANT_CACHE[value]
        return wrap_operand(value)

    def equals(self, expression: Operand) -> Equation:
        """Create an equation: self = expression."""
        rhs_expr = wrap_operand(expression)
        return Equation(f"{self.name}_eq", self, rhs_expr)

    def solve_from(self, expression: Operand) -> TypeSafeVariable:
        """
        Create an equation (self = expression) and immediately solve it.

        This is a convenience method that combines equation creation and solving.
        It automatically discovers variables from the calling scope.

        Args:
            expression: The expression this variable should equal

        Returns:
            self: The variable with updated quantity

        Example:
            T_bar = Length(0.147, "inches", "T_bar")
            U_m = Dimensionless(0.125, "U_m")
            T = Length("T", is_known=False)
            T.solve_from(T_bar * (1 - U_m))  # Solves T = T_bar * (1 - U_m)
        """
        # Create the equation
        equation = self.equals(expression)

        # Get all variables referenced in the equation
        required_vars = equation.variables
        
        # Use centralized scope discovery service
        variables_found = ScopeDiscoveryService.discover_variables(required_vars, enable_caching=True)
        
        # Add self if not found
        self_name = self.symbol if self.symbol else self.name
        if self_name not in variables_found:
            variables_found[self_name] = self
        
        # Solve the equation
        equation.solve_for(self_name, variables_found)
        return self

    def __add__(self, other: Operand) -> Expression:
        """Add this variable to another operand, returning an Expression."""
        # Fast path for simple cases
        if isinstance(other, int | float):
            return BinaryOperation("+", self._get_self_wrapped(), self._get_cached_constant(other))
        return BinaryOperation("+", self._get_self_wrapped(), wrap_operand(other))

    def __radd__(self, other: ReverseOperand) -> Expression:
        """Reverse add for this variable."""
        return BinaryOperation("+", self._get_cached_constant(other), self._get_self_wrapped())

    def __sub__(self, other: Operand) -> Expression:
        """Subtract another operand from this variable, returning an Expression."""
        if isinstance(other, int | float):
            return BinaryOperation("-", self._get_self_wrapped(), self._get_cached_constant(other))
        return BinaryOperation("-", self._get_self_wrapped(), wrap_operand(other))

    def __rsub__(self, other: ReverseOperand) -> Expression:
        """Reverse subtract for this variable."""
        return BinaryOperation("-", self._get_cached_constant(other), self._get_self_wrapped())

    def __mul__(self, other: Operand) -> Expression:
        """Multiply this variable by another operand, returning an Expression."""
        if isinstance(other, int | float):
            return BinaryOperation("*", self._get_self_wrapped(), self._get_cached_constant(other))
        return BinaryOperation("*", self._get_self_wrapped(), wrap_operand(other))

    def __rmul__(self, other: ReverseOperand) -> Expression:
        """Reverse multiply for this variable."""
        return BinaryOperation("*", self._get_cached_constant(other), self._get_self_wrapped())

    def __truediv__(self, other: Operand) -> Expression:
        """Divide this variable by another operand, returning an Expression."""
        if isinstance(other, int | float):
            return BinaryOperation("/", self._get_self_wrapped(), self._get_cached_constant(other))
        return BinaryOperation("/", self._get_self_wrapped(), wrap_operand(other))

    def __rtruediv__(self, other: ReverseOperand) -> Expression:
        """Reverse divide for this variable."""
        return BinaryOperation("/", self._get_cached_constant(other), self._get_self_wrapped())

    def __pow__(self, other: Operand) -> Expression:
        """Raise this variable to a power, returning an Expression."""
        if isinstance(other, int | float):
            return BinaryOperation("**", self._get_self_wrapped(), self._get_cached_constant(other))
        return BinaryOperation("**", self._get_self_wrapped(), wrap_operand(other))

    def __rpow__(self, other: ReverseOperand) -> Expression:
        """Reverse power for this variable."""
        return BinaryOperation("**", self._get_cached_constant(other), self._get_self_wrapped())

    # Comparison methods
    def lt(self, other: Operand) -> Expression:
        """Less than comparison (<)."""
        return BinaryOperation("<", self._get_self_wrapped(), wrap_operand(other))

    def leq(self, other: Operand) -> Expression:
        """Less than or equal comparison (<=)."""
        return BinaryOperation("<=", self._get_self_wrapped(), wrap_operand(other))

    def geq(self, other: Operand) -> Expression:
        """Greater than or equal comparison (>=)."""
        return BinaryOperation(">=", self._get_self_wrapped(), wrap_operand(other))

    def gt(self, other: Operand) -> Expression:
        """Greater than comparison (>)."""
        return BinaryOperation(">", self._get_self_wrapped(), wrap_operand(other))

    # Python comparison operators - optimized direct implementations
    def __lt__(self, other: Operand) -> Expression:
        """Less than comparison (<) operator."""
        return BinaryOperation("<", self._get_self_wrapped(), wrap_operand(other))

    def __le__(self, other: Operand) -> Expression:
        """Less than or equal comparison (<=) operator."""
        return BinaryOperation("<=", self._get_self_wrapped(), wrap_operand(other))

    def __gt__(self, other: Operand) -> Expression:
        """Greater than comparison (>) operator."""
        return BinaryOperation(">", self._get_self_wrapped(), wrap_operand(other))

    def __ge__(self, other: Operand) -> Expression:
        """Greater than or equal comparison (>=) operator."""
        return BinaryOperation(">=", self._get_self_wrapped(), wrap_operand(other))

    def solve(self) -> TypeSafeVariable:
        """
        Solve for this variable by automatically discovering equations and variables from scope.

        This method:
        1. Searches the calling scope for equations involving this variable
        2. Discovers all variables referenced in those equations
        3. Attempts to solve for this variable using available values

        Returns:
            self: The variable with updated quantity if solved successfully

        Raises:
            ValueError: If no solvable equation is found or if solving fails
        """
        self_name = self.symbol if self.symbol else self.name
        
        # Use scope discovery service to find all variables and equations
        all_objects = ScopeDiscoveryService.find_variables_in_scope()
        
        # Search for equations and variables
        equations_found = []
        
        # Use the service to find all objects in scope
        import inspect
        frame = inspect.currentframe()
        if frame is None:
            raise ValueError("Unable to access calling scope")
            
        try:
            # Find user frame
            user_frame = ScopeDiscoveryService._find_user_frame(frame.f_back)
            if user_frame is None:
                raise ValueError("Unable to access calling scope")
                
            # Search for equations in locals and globals
            for obj in list(user_frame.f_locals.values()) + list(user_frame.f_globals.values()):
                if self._is_equation(obj) and self._equation_contains_variable(obj):
                    equations_found.append(obj)
                    
        finally:
            del frame
        
        # Get all variables using scope discovery service 
        variables_found = all_objects.copy()
        
        # Add self to variables if not found
        if self_name not in variables_found:
            variables_found[self_name] = self

        # Try to solve using found equations
        if not equations_found:
            raise ValueError(f"No equations found in scope containing variable '{self_name}'")

        # Try each equation to see if it can solve for this variable
        for equation in equations_found:
            try:
                if self._can_equation_solve_for_self(equation, variables_found):
                    equation.solve_for(self_name, variables_found)
                    return self
            except Exception:
                continue  # Try next equation

        raise ValueError(f"Unable to solve for variable '{self_name}' with available equations and values")

    def _is_equation(self, obj) -> bool:
        """Check if object is an equation."""
        return hasattr(obj, "solve_for") and hasattr(obj, "variables")

    def _is_variable(self, obj) -> bool:
        """Check if object is a qnty variable using centralized service."""
        return ScopeDiscoveryService._is_typesafe_variable(obj)

    def _equation_contains_variable(self, equation) -> bool:
        """Check if equation contains this variable."""
        if not hasattr(equation, "variables"):
            return False
        try:
            var_name = self.symbol if self.symbol else self.name
            return var_name in equation.variables
        except Exception:
            return False

    def _get_variable_name(self, var) -> str | None:
        """Get the name/symbol to use for a variable using centralized service."""
        return ScopeDiscoveryService._get_variable_name(var)

    def _can_equation_solve_for_self(self, equation, variables: dict[str, TypeSafeVariable]) -> bool:
        """Check if equation can solve for this variable."""
        try:
            var_name = self.symbol if self.symbol else self.name

            # Get known variables (those with quantities)
            known_vars = {name for name, var in variables.items() if var is not self and var.quantity is not None}

            return equation.can_solve_for(var_name, known_vars)
        except Exception:
            return False
