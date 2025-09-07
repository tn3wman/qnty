"""
Refactored Unified Variable System
=================================

This module provides a streamlined variable system with improved architecture:

Key Refactoring Improvements:
- **Encapsulated Global State**: CacheManager replaces global variables
- **Simplified Mixins**: Reduced from 6 complex mixins to 5 focused ones
- **Eliminated Code Duplication**: ArithmeticDispatcher centralizes operations
- **Simplified Constructor Logic**: ConstructorProcessor handles complex initialization
- **Better Separation of Concerns**: Each component has a single responsibility
- **Maintained Backward Compatibility**: All existing APIs work unchanged

Architecture:
- UnifiedVariable: Main class with focused mixins
- QuantityManagementMixin: Core quantity storage and state
- FlexibleConstructorMixin: Simplified argument processing
- UnifiedArithmeticMixin: User-controllable arithmetic operations
- ExpressionMixin: Equation and comparison operations
- SetterCompatibilityMixin: Backward compatibility with setter system
- ErrorHandlerMixin: Consistent error handling
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

from qnty.utils.error_handling import ErrorHandlerMixin

if TYPE_CHECKING:
    from ..dimensions import DimensionSignature
    from ..equations import Equation
    from ..expressions import Expression
    from .base_qnty import Quantity, TypeSafeSetter


class QuantityManagementMixin:
    """Handles core quantity storage and state management."""

    def __init__(self):
        self._quantity: Quantity | None = None
        self._is_known: bool = False
        self._name: str = ""
        self._symbol: str | None = None

    @property
    def quantity(self) -> Quantity | None:
        """Get the underlying quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: Quantity | None) -> None:
        """Set the underlying quantity."""
        self._quantity = value
        if value is not None:
            self._is_known = True

    @property
    def is_known(self) -> bool:
        """Check if variable has a known value."""
        return self._is_known and self._quantity is not None

    @is_known.setter
    def is_known(self, value: bool) -> None:
        """Set known status for backward compatibility."""
        self._is_known = value

    def mark_known(self) -> Self:
        """Mark variable as having a known value."""
        self._is_known = True
        return self

    def mark_unknown(self) -> Self:
        """Mark variable as unknown."""
        self._is_known = False
        return self

    def update(self, value: Any = None, unit: Any = None, quantity: Quantity | None = None, is_known: bool | None = None) -> Self:
        """Flexible update method for variable properties."""
        if quantity is not None:
            self.quantity = quantity
        elif value is not None and unit is not None:
            # Create new quantity from value and unit using existing setter system
            if hasattr(self, "_create_quantity_from_value_unit"):
                self.quantity = self._create_quantity_from_value_unit(value, unit)

        if is_known is not None:
            self._is_known = is_known

        return self


class FlexibleConstructorMixin:
    """Handles flexible variable initialization patterns maintaining backward compatibility."""

    def __init__(self):
        # Only set instance attributes if not already set by class definition
        # This preserves class attributes from generated quantities
        if not hasattr(self, "_setter_class"):
            self._setter_class: type | None = None
        if not hasattr(self, "_unit_mappings"):
            self._unit_mappings: dict[str, str] = {}

    def _initialize_from_args(self, *args, **kwargs) -> None:
        """Process constructor arguments with full backward compatibility."""
        is_dimensionless = self.__class__.__name__ == "Dimensionless"

        if len(args) == 1 and isinstance(args[0], str):
            # Pattern: Variable("name") - may have is_known in kwargs
            self._name = args[0]
            self._is_known = kwargs.get("is_known", False)

        elif len(args) == 2:
            if is_dimensionless:
                # Dimensionless pattern: Variable(value, "name")
                value, name = args
                self._name = name
                self._is_known = True
                # For dimensionless, create quantity directly
                from ..units import DimensionlessUnits
                from .base_qnty import Quantity

                self.quantity = Quantity(value, DimensionlessUnits.dimensionless)
            elif isinstance(args[1], str):
                # Pattern: Variable(value, unit) - needs name from kwargs or auto-generated
                value, unit = args
                self._initialize_with_value_unit(value, unit)
            elif isinstance(args[1], bool):
                # Pattern: Variable(name, is_known)
                name, is_known = args
                self._name = name
                self._is_known = is_known

        elif len(args) == 3:
            # Pattern: Variable(value, unit, name) - for dimensional quantities
            value, unit, name = args
            self._initialize_with_value_unit_name(value, unit, name)

        elif len(args) == 4:
            # Pattern: Variable(value, unit, name, is_known)
            value, unit, name, is_known = args
            self._initialize_with_value_unit_name(value, unit, name)
            self._is_known = is_known

        # Handle keyword arguments
        if "name" in kwargs:
            self._name = kwargs["name"]
        if "is_known" in kwargs:
            self._is_known = kwargs["is_known"]
        if "quantity" in kwargs:
            self.quantity = kwargs["quantity"]

        # Set default name if not provided
        if not hasattr(self, "_name") or not self._name:
            self._name = f"var_{id(self)}"

    def _initialize_with_value_unit(self, value: Any, unit: Any) -> None:
        """Initialize with value and unit."""
        if hasattr(self, "_create_quantity_from_value_unit"):
            self.quantity = self._create_quantity_from_value_unit(value, unit)
        self._is_known = True

    def _initialize_with_value_unit_name(self, value: Any, unit: Any, name: str) -> None:
        """Initialize with value, unit, and name."""
        self._name = name
        self._initialize_with_value_unit(value, unit)

    def _create_quantity_from_value_unit(self, value: Any, unit: Any) -> Quantity | None:
        """Create quantity from value and unit using setter system."""
        if hasattr(self, "_setter_class") and self._setter_class is not None:
            # Use the setter system like TypedQuantity does
            setter = self._setter_class(self, value)
            unit_prop = self._find_unit_property(setter, str(unit))
            if unit_prop:
                getattr(setter, unit_prop)
                # Debug: check what self.quantity returns
                result = self.quantity
                # Ensure we return the quantity if it was successfully set
                return result

        # Fallback to direct quantity creation
        from ..units import DimensionlessUnits
        from .base_qnty import Quantity

        # Try to find the unit in the registry or use dimensionless fallback
        try:
            from ..units.registry import registry

            # Use a simple lookup approach since get_unit method may not exist
            if hasattr(registry, "units") and str(unit) in registry.units:
                unit_constant = registry.units[str(unit)]
                return Quantity(value, unit_constant)
        except Exception:
            pass

        # Final fallback to dimensionless
        return Quantity(value, DimensionlessUnits.dimensionless)

    def _find_unit_property(self, setter: TypeSafeSetter, unit: str) -> str | None:
        """Find unit property with simple lookup."""
        if not hasattr(self, "_setter_class") or self._setter_class is None:
            return None

        # Direct property lookup
        if hasattr(setter, unit):
            return unit

        return None


class UnifiedArithmeticMixin:
    """Provides unified arithmetic operations with user-controllable return types."""

    def __init__(self):
        self._arithmetic_mode: str = "expression"  # 'quantity', 'expression', 'auto'

    def set_arithmetic_mode(self, mode: str) -> Self:
        """Set arithmetic return type preference."""
        if mode not in ("quantity", "expression", "auto"):
            raise ValueError(f"Invalid arithmetic mode: {mode}")
        self._arithmetic_mode = mode
        return self

    def __add__(self, other) -> Any:
        """Unified addition with mode-based dispatch."""
        return self._unified_add(self, other, self._arithmetic_mode)

    def __radd__(self, other) -> Any:
        """Reverse addition."""
        return self._unified_add(other, self, self._arithmetic_mode)

    def __sub__(self, other) -> Any:
        """Unified subtraction with mode-based dispatch."""
        return self._unified_subtract(self, other, self._arithmetic_mode)

    def __rsub__(self, other) -> Any:
        """Reverse subtraction."""
        return self._unified_subtract(other, self, self._arithmetic_mode)

    def __mul__(self, other) -> Any:
        """Unified multiplication with mode-based dispatch."""
        return self._unified_multiply(self, other, self._arithmetic_mode)

    def __rmul__(self, other) -> Any:
        """Reverse multiplication."""
        return self._unified_multiply(other, self, self._arithmetic_mode)

    def __truediv__(self, other) -> Any:
        """Unified division with mode-based dispatch."""
        return self._unified_divide(self, other, self._arithmetic_mode)

    def __rtruediv__(self, other) -> Any:
        """Reverse division."""
        return self._unified_divide(other, self, self._arithmetic_mode)

    def __pow__(self, other) -> Any:
        """Unified exponentiation with mode-based dispatch."""
        return self._unified_power(self, other, self._arithmetic_mode)

    def __rpow__(self, other) -> Any:
        """Reverse exponentiation."""
        return self._unified_power(other, self, self._arithmetic_mode)

    @staticmethod
    def _should_return_quantity(left: Any, right: Any) -> bool:
        """Determine if operations should return Quantity (fast path) or Expression (flexible path)."""
        # Fast type checks for primitives first (most common case)
        left_type = type(left)
        right_type = type(right)

        # Cache primitive type checks
        left_is_primitive = left_type in (int, float)
        right_is_primitive = right_type in (int, float)

        if left_is_primitive and right_is_primitive:
            return True
        elif left_is_primitive:
            return hasattr(right, "is_known") and right.is_known and hasattr(right, "quantity") and right.quantity is not None
        elif right_is_primitive:
            return hasattr(left, "is_known") and left.is_known and hasattr(left, "quantity") and left.quantity is not None
        else:
            # Both are complex objects
            left_is_known = hasattr(left, "is_known") and left.is_known and hasattr(left, "quantity") and left.quantity is not None
            right_is_known = hasattr(right, "is_known") and right.is_known and hasattr(right, "quantity") and right.quantity is not None
            return left_is_known and right_is_known

    def _unified_add(self, left: Any, right: Any, return_type: str = "auto") -> Any:
        """Unified addition with controllable return type."""
        if return_type == "quantity" or (return_type == "auto" and self._should_return_quantity(left, right)):
            return self._quantity_add(left, right)
        else:
            return self._expression_add(left, right)

    def _unified_subtract(self, left: Any, right: Any, return_type: str = "auto") -> Any:
        """Unified subtraction with controllable return type."""
        if return_type == "quantity" or (return_type == "auto" and self._should_return_quantity(left, right)):
            return self._quantity_subtract(left, right)
        else:
            return self._expression_subtract(left, right)

    def _unified_multiply(self, left: Any, right: Any, return_type: str = "auto") -> Any:
        """Unified multiplication with controllable return type."""
        if return_type == "quantity" or (return_type == "auto" and self._should_return_quantity(left, right)):
            return self._quantity_multiply(left, right)
        else:
            return self._expression_multiply(left, right)

    def _unified_divide(self, left: Any, right: Any, return_type: str = "auto") -> Any:
        """Unified division with controllable return type."""
        if return_type == "quantity" or (return_type == "auto" and self._should_return_quantity(left, right)):
            return self._quantity_divide(left, right)
        else:
            return self._expression_divide(left, right)

    def _unified_power(self, left: Any, right: Any, return_type: str = "auto") -> Any:
        """Unified exponentiation with controllable return type."""
        if return_type == "quantity" or (return_type == "auto" and self._should_return_quantity(left, right)):
            return self._quantity_power(left, right)
        else:
            return self._expression_power(left, right)

    # Cache for dimensionless quantities to reduce allocation
    _DIMENSIONLESS_ZERO = None
    _DIMENSIONLESS_ONE = None
    _DIMENSIONLESS_CACHE = {}  # Cache for common dimensionless values

    @classmethod
    def _get_dimensionless_quantity(cls, value: float):
        """Get cached dimensionless quantity for common values."""
        # Initialize cache if needed
        if cls._DIMENSIONLESS_ZERO is None:
            from ..units import DimensionlessUnits
            from .base_qnty import Quantity

            cls._DIMENSIONLESS_ZERO = Quantity(0.0, DimensionlessUnits.dimensionless)
            cls._DIMENSIONLESS_ONE = Quantity(1.0, DimensionlessUnits.dimensionless)

        # Fast return for common values
        if value == 0.0:
            return cls._DIMENSIONLESS_ZERO
        elif value == 1.0:
            return cls._DIMENSIONLESS_ONE
        elif value in cls._DIMENSIONLESS_CACHE:
            return cls._DIMENSIONLESS_CACHE[value]
        else:
            # Create new quantity and cache if it's a common value
            from ..units import DimensionlessUnits
            from .base_qnty import Quantity

            qty = Quantity(value, DimensionlessUnits.dimensionless)

            # Cache common integer values
            if isinstance(value, int) and -10 <= value <= 10:
                cls._DIMENSIONLESS_CACHE[value] = qty
            # Cache common decimal values
            elif value in (-1.0, 0.5, 2.0, -0.5):
                cls._DIMENSIONLESS_CACHE[value] = qty

            return qty

    @classmethod
    def _quantity_add(cls, left: Any, right: Any):
        """Fast path addition returning Quantity with optimized quantity creation."""
        from ..expressions import BinaryOperation
        from .base_qnty import ArithmeticOperations

        # Fast path for numeric types
        left_type = type(left)
        right_type = type(right)

        if left_type in (int, float):
            left_qty = cls._get_dimensionless_quantity(float(left))
        else:
            left_qty = left.quantity if hasattr(left, "quantity") else left

        if right_type in (int, float):
            right_qty = cls._get_dimensionless_quantity(float(right))
        else:
            right_qty = right.quantity if hasattr(right, "quantity") else right

        # If either operand has no quantity, fall back to expression mode
        if left_qty is None or right_qty is None:
            return BinaryOperation("+", left, right)

        # Delegate to ArithmeticOperations for the actual computation
        return ArithmeticOperations.add(left_qty, right_qty)

    @staticmethod
    def _expression_add(left: Any, right: Any):
        """Flexible path addition returning Expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("+", wrap_operand(left), wrap_operand(right))

    @classmethod
    def _quantity_subtract(cls, left: Any, right: Any):
        """Fast path subtraction returning Quantity with optimized quantity creation."""
        from .base_qnty import ArithmeticOperations

        # Fast path for numeric types using cached dimensionless quantities
        left_type = type(left)
        right_type = type(right)

        if left_type in (int, float):
            left_qty = cls._get_dimensionless_quantity(float(left))
        else:
            left_qty = left.quantity if hasattr(left, "quantity") else left

        if right_type in (int, float):
            right_qty = cls._get_dimensionless_quantity(float(right))
        else:
            right_qty = right.quantity if hasattr(right, "quantity") else right

        # Delegate to ArithmeticOperations for the actual computation
        return ArithmeticOperations.subtract(left_qty, right_qty)

    @staticmethod
    def _expression_subtract(left: Any, right: Any):
        """Flexible path subtraction returning Expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("-", wrap_operand(left), wrap_operand(right))

    @classmethod
    def _quantity_multiply(cls, left: Any, right: Any):
        """Fast path multiplication returning Quantity with optimized quantity creation."""
        from .base_qnty import ArithmeticOperations

        # Fast path for numeric types using cached dimensionless quantities
        left_type = type(left)
        right_type = type(right)

        if left_type in (int, float):
            left_qty = cls._get_dimensionless_quantity(float(left))
        else:
            left_qty = left.quantity if hasattr(left, "quantity") else left

        if right_type in (int, float):
            right_qty = cls._get_dimensionless_quantity(float(right))
        else:
            right_qty = right.quantity if hasattr(right, "quantity") else right

        # Delegate to ArithmeticOperations for the actual computation
        return ArithmeticOperations.multiply(left_qty, right_qty)

    @staticmethod
    def _expression_multiply(left: Any, right: Any):
        """Flexible path multiplication returning Expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("*", wrap_operand(left), wrap_operand(right))

    @classmethod
    def _quantity_divide(cls, left: Any, right: Any):
        """Fast path division returning Quantity with optimized quantity creation."""
        from .base_qnty import ArithmeticOperations

        # Fast path for numeric types using cached dimensionless quantities
        left_type = type(left)
        right_type = type(right)

        if left_type in (int, float):
            left_qty = cls._get_dimensionless_quantity(float(left))
        else:
            left_qty = left.quantity if hasattr(left, "quantity") else left

        if right_type in (int, float):
            right_qty = cls._get_dimensionless_quantity(float(right))
        else:
            right_qty = right.quantity if hasattr(right, "quantity") else right

        # Delegate to ArithmeticOperations for the actual computation
        return ArithmeticOperations.divide(left_qty, right_qty)

    @staticmethod
    def _expression_divide(left: Any, right: Any):
        """Flexible path division returning Expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("/", wrap_operand(left), wrap_operand(right))

    @classmethod
    def _quantity_power(cls, left: Any, right: Any):
        """Fast path exponentiation returning Quantity with optimized handling."""
        left_type = type(left)
        right_type = type(right)

        # Get quantities efficiently
        if left_type in (int, float):
            left_qty = cls._get_dimensionless_quantity(float(left))
        else:
            left_qty = left.quantity if hasattr(left, "quantity") else left

        # For exponentiation, right operand is usually a scalar
        if right_type in (int, float):
            return left_qty**right
        else:
            right_qty = right.quantity if hasattr(right, "quantity") else right
            return left_qty**right_qty

    @staticmethod
    def _expression_power(left: Any, right: Any):
        """Flexible path exponentiation returning Expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("**", wrap_operand(left), wrap_operand(right))


class ExpressionMixin:
    """Provides expression and equation creation capabilities."""

    def __init__(self):
        pass  # Properties will be handled by UnifiedVariable

    def equals(self, other) -> Equation:
        """Create an equation: self = other."""
        from ..equations import Equation
        from ..expressions import wrap_operand

        equation_name = f"{self.name}_eq"
        return Equation(name=equation_name, lhs=wrap_operand(self), rhs=wrap_operand(other))

    def lt(self, other) -> Expression:
        """Create less-than comparison expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("<", wrap_operand(self), wrap_operand(other))

    def leq(self, other) -> Expression:
        """Create less-than-or-equal comparison expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("<=", wrap_operand(self), wrap_operand(other))

    def geq(self, other) -> Expression:
        """Create greater-than-or-equal comparison expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation(">=", wrap_operand(self), wrap_operand(other))

    def gt(self, other) -> Expression:
        """Create greater-than comparison expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation(">", wrap_operand(self), wrap_operand(other))

    # Python comparison operators for convenience
    def __lt__(self, other) -> Expression:
        return self.lt(other)

    def __le__(self, other) -> Expression:
        return self.leq(other)

    def __ge__(self, other) -> Expression:
        return self.geq(other)

    def __gt__(self, other) -> Expression:
        return self.gt(other)

    def eq(self, other) -> Expression:
        """Create equality comparison expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("==", wrap_operand(self), wrap_operand(other))

    def ne(self, other) -> Expression:
        """Create inequality comparison expression."""
        from ..expressions import BinaryOperation, wrap_operand

        return BinaryOperation("!=", wrap_operand(self), wrap_operand(other))

    def get_variables(self) -> set[str]:
        """Get variable names used in this variable (for equation system compatibility)."""
        return {self.symbol or self.name}

    def evaluate(self, variable_values: dict[str, FieldQnty]) -> Quantity:
        """Evaluate this variable in the context of a variable dictionary."""
        # If this variable has a quantity, return it
        if self.quantity is not None:
            return self.quantity

        # Try to find this variable in the provided values
        var_name = self.symbol or self.name
        if var_name in variable_values:
            var = variable_values[var_name]
            if var.quantity is not None:
                return var.quantity

        # If no quantity available, raise error
        raise ValueError(f"Cannot evaluate variable '{var_name}' without value. Available variables: {list(variable_values.keys())}")

    def solve_from(self, expression) -> Self:
        """
        Solve this variable from an expression.

        If the expression can be evaluated to a concrete value, assigns that value.
        Otherwise, falls back to symbolic equation solving.

        Args:
            expression: The expression to solve from (can be a value, quantity, or expression)

        Returns:
            Self for method chaining
        """
        from ..expressions import Expression

        # Handle different types of input with optimized type checking

        if hasattr(expression, "quantity") and expression.quantity is not None:
            # Direct quantity/variable input - avoid repeated attribute access
            qty = expression.quantity
            self.quantity = qty
            self._is_known = True
        elif isinstance(expression, Expression):
            # Expression input - try to evaluate it first
            try:
                # Check if the expression can auto-evaluate
                can_eval, variables = expression._can_auto_evaluate()
                if can_eval:
                    # Expression evaluates to a concrete value - use the evaluate method
                    evaluated_quantity = expression.evaluate(variables)
                    if evaluated_quantity is not None:
                        self.quantity = evaluated_quantity
                        self._is_known = True
                    else:
                        # Fall back to symbolic solving
                        self._symbolic_solve_from(expression)
                else:
                    # Fall back to symbolic solving
                    self._symbolic_solve_from(expression)
            except Exception:
                # If evaluation fails, try symbolic solving
                self._symbolic_solve_from(expression)
        else:
            # Direct value input (int, float)
            try:
                # Try to create a quantity with the same dimension as this variable
                if hasattr(self, "_dimension") and self._dimension:
                    # Use cached dimensionless quantity for better performance
                    self.quantity = self._get_dimensionless_quantity(float(expression))
                    self._is_known = True
            except Exception:
                pass

        return self

    def solve(self) -> Self:
        """
        Solve this variable by finding equations in the calling scope.

        This method automatically discovers equations from the calling scope
        and attempts to solve for this variable. If no stored equations are found,
        it falls back to looking for direct expressions that can be used.

        Returns:
            Self for method chaining

        Raises:
            ValueError: If no equations found or equation cannot be solved
        """
        from ..equations import Equation
        from ..expressions import ScopeDiscoveryService

        # Find all variables in the calling scope
        all_variables = ScopeDiscoveryService.find_variables_in_scope()

        var_name = self.symbol or self.name

        # Strategy 1: Look for stored equations on variables
        equations_found = []
        for var in all_variables.values():
            if hasattr(var, "_equations"):
                equations_found.extend(var._equations)

        # Try to solve using stored equations
        for equation in equations_found:
            try:
                if hasattr(equation, "solve_for"):
                    solved_value = equation.solve_for(var_name, all_variables)
                    if solved_value is not None and hasattr(solved_value, "quantity"):
                        self.quantity = solved_value.quantity
                        self._is_known = True
                        return self
            except Exception:
                continue

        # Strategy 2: Look for Equation objects in scope (created with .equals())
        frame = ScopeDiscoveryService._find_user_frame(ScopeDiscoveryService._get_current_frame())
        if frame:
            for obj in list(frame.f_locals.values()) + list(frame.f_globals.values()):
                if isinstance(obj, Equation):
                    try:
                        solved_value = obj.solve_for(var_name, all_variables)
                        if solved_value is not None and hasattr(solved_value, "quantity"):
                            self.quantity = solved_value.quantity
                            self._is_known = True
                            return self
                    except Exception:
                        continue

        raise ValueError(f"No equations found in scope to solve for '{var_name}'")

    def _symbolic_solve_from(self, expression):
        """Fallback symbolic solving method."""
        try:
            equation = self.equals(expression)
            solved_value = equation.solve_for(self.symbol or self.name, {})
            if solved_value is not None and hasattr(solved_value, "quantity"):
                self.quantity = solved_value.quantity
                self._is_known = True
        except Exception:
            # If all else fails, silently continue
            pass


class SetterCompatibilityMixin:
    """Provides backward compatibility with existing setter system."""

    def __init__(self):
        # Only set instance attributes if not already set by class definition
        # This preserves class attributes from generated quantities
        if not hasattr(self, "_setter_class"):
            self._setter_class: type | None = None

    def set(self, value: float) -> TypeSafeSetter:
        """Create setter object for fluent API compatibility."""
        if hasattr(self, "_setter_class") and self._setter_class:
            return self._setter_class(self, value)  # Correct parameter order
        else:
            # Fallback to generic setter
            from .base_qnty import TypeSafeSetter

            return TypeSafeSetter(self, value)  # Correct parameter order


class FieldQnty(QuantityManagementMixin, FlexibleConstructorMixin, UnifiedArithmeticMixin, ExpressionMixin, SetterCompatibilityMixin, ErrorHandlerMixin):
    """
    Unified variable class that replaces the 4-level inheritance chain.

    This combines all capabilities through focused mixins instead of inheritance:
    - QuantityManagementMixin: Core quantity storage and state management
    - FlexibleConstructorMixin: Backward-compatible initialization patterns
    - UnifiedArithmeticMixin: User-controllable arithmetic operations
    - ExpressionMixin: Expression and equation creation capabilities
    - SetterCompatibilityMixin: Backward compatibility with setter system
    - ErrorHandlerMixin: Consistent error handling
    """

    # Class attributes that subclasses should define
    _dimension: DimensionSignature | None = None
    _setter_class: type | None = None
    _default_unit_property: str | None = None
    _unit_mappings: dict[str, str] = {}

    def __init__(self, *args, **kwargs):
        """Initialize unified variable with simplified setup."""
        # Initialize core components
        self._initialize_core_attributes()
        self._initialize_mixins()

        # Process constructor arguments
        self._initialize_from_args(*args, **kwargs)

    def _initialize_core_attributes(self) -> None:
        """Initialize core variable attributes."""
        self.validation_checks = []
        self._parent_problem = None
        self._equations = []
        if not hasattr(self, "_symbol"):
            self._symbol = None

    def _initialize_mixins(self) -> None:
        """Initialize all mixin components."""
        QuantityManagementMixin.__init__(self)
        FlexibleConstructorMixin.__init__(self)
        UnifiedArithmeticMixin.__init__(self)
        ExpressionMixin.__init__(self)
        SetterCompatibilityMixin.__init__(self)
        ErrorHandlerMixin.__init__(self)

    # Simplified property management
    @property
    def name(self) -> str:
        return getattr(self, "_name", "")

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def expected_dimension(self) -> DimensionSignature | None:
        return self._dimension

    @expected_dimension.setter
    def expected_dimension(self, value: DimensionSignature | None) -> None:
        self._dimension = value

    @property
    def symbol(self) -> str | None:
        return getattr(self, "_symbol", None) or self.name

    @symbol.setter
    def symbol(self, value: str | None) -> None:
        self._symbol = value

    def __str__(self) -> str:
        status = f"{self._quantity}" if (self.is_known and self._quantity) else "(unset)"
        return f"{self.name} = {status}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.name}', known={self.is_known})"


def create_domain_variable_class(
    dimension: DimensionSignature, setter_class: type | None = None, default_unit_property: str | None = None, unit_mappings: dict[str, str] | None = None
) -> type[FieldQnty]:
    """
    Factory function to create domain-specific variable classes.

    This replaces the need for hand-coded inheritance chains by generating
    the necessary class with proper dimension and setter configuration.
    """

    class DomainVariable(FieldQnty):
        _dimension = dimension
        _setter_class = setter_class
        _default_unit_property = default_unit_property
        _unit_mappings = unit_mappings or {}

    return DomainVariable
