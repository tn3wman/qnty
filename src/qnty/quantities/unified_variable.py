"""
Unified Variable System - Simplified 2-Level Hierarchy
======================================================

This module implements the simplified variable hierarchy that replaces the current 4-level chain:

BEFORE: TypeSafeVariable → ExpressionQuantity → TypedQuantity → Generated Variables
AFTER:  UnifiedVariable → Domain Variables (Length, Pressure, etc.)

Key improvements:
- Simplified method resolution (2 levels vs 4)
- Unified arithmetic system with user control
- Cleaner separation of concerns through focused mixins
- Maintained backward compatibility
"""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Optional, Any, Union, Self
from dataclasses import dataclass

from ..constants import FLOAT_EQUALITY_TOLERANCE, DIVISION_BY_ZERO_THRESHOLD
from ..cache_manager import get_cache_manager
from ..error_handling import ErrorHandlerMixin, ErrorContext

if TYPE_CHECKING:
    from .quantity import Quantity, TypeSafeSetter
    from ..expressions.nodes import Expression
    from ..equations.equation import Equation
    from ..generated.dimensions import DimensionSignature

# TypeSafeVariable import removed - no longer inheriting


class ArithmeticDispatcher:
    """
    Unified arithmetic dispatcher that eliminates the confusion between
    Quantity-based and Expression-based arithmetic operations.
    
    Provides user-controllable return types while maintaining performance.
    """
    
    @staticmethod
    def add(left: Any, right: Any, return_type: str = 'auto') -> Any:
        """Unified addition with controllable return type."""
        if return_type == 'quantity' or (return_type == 'auto' and ArithmeticDispatcher._should_return_quantity(left, right)):
            return ArithmeticDispatcher._quantity_add(left, right)
        else:
            return ArithmeticDispatcher._expression_add(left, right)
    
    @staticmethod
    def subtract(left: Any, right: Any, return_type: str = 'auto') -> Any:
        """Unified subtraction with controllable return type."""
        if return_type == 'quantity' or (return_type == 'auto' and ArithmeticDispatcher._should_return_quantity(left, right)):
            return ArithmeticDispatcher._quantity_subtract(left, right)
        else:
            return ArithmeticDispatcher._expression_subtract(left, right)
    
    @staticmethod
    def multiply(left: Any, right: Any, return_type: str = 'auto') -> Any:
        """Unified multiplication with controllable return type."""
        if return_type == 'quantity' or (return_type == 'auto' and ArithmeticDispatcher._should_return_quantity(left, right)):
            return ArithmeticDispatcher._quantity_multiply(left, right)
        else:
            return ArithmeticDispatcher._expression_multiply(left, right)
    
    @staticmethod
    def divide(left: Any, right: Any, return_type: str = 'auto') -> Any:
        """Unified division with controllable return type."""
        if return_type == 'quantity' or (return_type == 'auto' and ArithmeticDispatcher._should_return_quantity(left, right)):
            return ArithmeticDispatcher._quantity_divide(left, right)
        else:
            return ArithmeticDispatcher._expression_divide(left, right)
    
    @staticmethod
    def power(left: Any, right: Any, return_type: str = 'auto') -> Any:
        """Unified exponentiation with controllable return type."""
        if return_type == 'quantity' or (return_type == 'auto' and ArithmeticDispatcher._should_return_quantity(left, right)):
            return ArithmeticDispatcher._quantity_power(left, right)
        else:
            return ArithmeticDispatcher._expression_power(left, right)
    
    @staticmethod
    def _should_return_quantity(left: Any, right: Any) -> bool:
        """Determine if operations should return Quantity (fast path) or Expression (flexible path)."""
        # Return Quantity if both operands have known values
        left_is_known = hasattr(left, 'is_known') and left.is_known and hasattr(left, 'quantity') and left.quantity is not None
        right_is_known = hasattr(right, 'is_known') and right.is_known and hasattr(right, 'quantity') and right.quantity is not None
        
        # Also handle primitive types (int, float) as known
        if isinstance(right, (int, float)):
            right_is_known = True
        if isinstance(left, (int, float)):
            left_is_known = True
            
        return left_is_known and right_is_known
    
    @staticmethod
    def _quantity_add(left: Any, right: Any):
        """Fast path addition returning Quantity."""
        from .quantity import Quantity
        from ..expressions.nodes import BinaryOperation
        
        # Get quantities from variables or use direct quantities
        left_qty = left.quantity if hasattr(left, 'quantity') else left
        right_qty = right.quantity if hasattr(right, 'quantity') else right
        
        # If either operand has no quantity, fall back to expression mode
        if left_qty is None or right_qty is None:
            return BinaryOperation('+', left, right)
        
        # Handle numeric constants - create dimensionless quantities properly
        if isinstance(right, (int, float)):
            from ..generated.units import DimensionlessUnits
            right_qty = Quantity(right, DimensionlessUnits.dimensionless)
        if isinstance(left, (int, float)):
            from ..generated.units import DimensionlessUnits
            left_qty = Quantity(left, DimensionlessUnits.dimensionless)
        
        return left_qty + right_qty
    
    @staticmethod
    def _expression_add(left: Any, right: Any) -> 'Expression':
        """Flexible path addition returning Expression."""
        from ..expressions.nodes import BinaryOperation, wrap_operand
        return BinaryOperation('+', wrap_operand(left), wrap_operand(right))
    
    @staticmethod
    def _quantity_subtract(left: Any, right: Any) -> 'Quantity':
        """Fast path subtraction returning Quantity."""
        from .quantity import Quantity
        
        left_qty = left.quantity if hasattr(left, 'quantity') else left
        right_qty = right.quantity if hasattr(right, 'quantity') else right
        
        if isinstance(right, (int, float)):
            from ..generated.units import DimensionlessUnits
            right_qty = Quantity(right, DimensionlessUnits.dimensionless)
        if isinstance(left, (int, float)):
            from ..generated.units import DimensionlessUnits
            left_qty = Quantity(left, DimensionlessUnits.dimensionless)
        
        return left_qty - right_qty
    
    @staticmethod
    def _expression_subtract(left: Any, right: Any) -> 'Expression':
        """Flexible path subtraction returning Expression."""
        from ..expressions.nodes import BinaryOperation, wrap_operand
        return BinaryOperation('-', wrap_operand(left), wrap_operand(right))
    
    @staticmethod
    def _quantity_multiply(left: Any, right: Any) -> 'Quantity':
        """Fast path multiplication returning Quantity."""
        from .quantity import Quantity
        
        left_qty = left.quantity if hasattr(left, 'quantity') else left
        right_qty = right.quantity if hasattr(right, 'quantity') else right
        
        if isinstance(right, (int, float)):
            from ..generated.units import DimensionlessUnits
            right_qty = Quantity(right, DimensionlessUnits.dimensionless)
        if isinstance(left, (int, float)):
            from ..generated.units import DimensionlessUnits
            left_qty = Quantity(left, DimensionlessUnits.dimensionless)
        
        return left_qty * right_qty
    
    @staticmethod
    def _expression_multiply(left: Any, right: Any) -> 'Expression':
        """Flexible path multiplication returning Expression."""
        from ..expressions.nodes import BinaryOperation, wrap_operand
        return BinaryOperation('*', wrap_operand(left), wrap_operand(right))
    
    @staticmethod
    def _quantity_divide(left: Any, right: Any) -> 'Quantity':
        """Fast path division returning Quantity."""
        from .quantity import Quantity
        
        left_qty = left.quantity if hasattr(left, 'quantity') else left
        right_qty = right.quantity if hasattr(right, 'quantity') else right
        
        if isinstance(right, (int, float)):
            from ..generated.units import DimensionlessUnits
            right_qty = Quantity(right, DimensionlessUnits.dimensionless)
        if isinstance(left, (int, float)):
            from ..generated.units import DimensionlessUnits
            left_qty = Quantity(left, DimensionlessUnits.dimensionless)
        
        return left_qty / right_qty
    
    @staticmethod
    def _expression_divide(left: Any, right: Any) -> 'Expression':
        """Flexible path division returning Expression."""
        from ..expressions.nodes import BinaryOperation, wrap_operand
        return BinaryOperation('/', wrap_operand(left), wrap_operand(right))
    
    @staticmethod
    def _quantity_power(left: Any, right: Any) -> 'Quantity':
        """Fast path exponentiation returning Quantity."""
        from .quantity import Quantity
        
        left_qty = left.quantity if hasattr(left, 'quantity') else left
        if isinstance(right, (int, float)):
            return left_qty ** right
        else:
            right_qty = right.quantity if hasattr(right, 'quantity') else right
            return left_qty ** right_qty
    
    @staticmethod
    def _expression_power(left: Any, right: Any) -> 'Expression':
        """Flexible path exponentiation returning Expression."""
        from ..expressions.nodes import BinaryOperation, wrap_operand
        return BinaryOperation('**', wrap_operand(left), wrap_operand(right))


class QuantityManagementMixin:
    """Handles core quantity storage and state management."""
    
    def __init__(self):
        self._quantity: Optional[Quantity] = None
        self._is_known: bool = False
        self._name: str = ""
        self._symbol: Optional[str] = None
        
    @property
    def quantity(self) -> Optional[Quantity]:
        """Get the underlying quantity."""
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: Optional[Quantity]) -> None:
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
    
    def update(self, value: Any = None, unit: Any = None, 
               quantity: Optional[Quantity] = None, is_known: Optional[bool] = None) -> Self:
        """Flexible update method for variable properties."""
        if quantity is not None:
            self.quantity = quantity
        elif value is not None and unit is not None:
            # Create new quantity from value and unit using existing setter system
            if hasattr(self, '_create_quantity_from_value_unit'):
                self.quantity = self._create_quantity_from_value_unit(value, unit)
        
        if is_known is not None:
            self._is_known = is_known
            
        return self


class FlexibleConstructorMixin:
    """Handles flexible variable initialization patterns maintaining backward compatibility."""
    
    def _initialize_from_args(self, *args, **kwargs) -> None:
        """Process constructor arguments with full backward compatibility."""
        is_dimensionless = self.__class__.__name__ == "Dimensionless"
        
        if len(args) == 1 and isinstance(args[0], str):
            # Pattern: Variable("name") - may have is_known in kwargs
            self._name = args[0]
            self._is_known = kwargs.get('is_known', False)
            
        elif len(args) == 2:
            if is_dimensionless:
                # Dimensionless pattern: Variable(value, "name")
                value, name = args
                self._name = name
                self._is_known = True
                # For dimensionless, create quantity directly
                from .quantity import Quantity
                from ..generated.units import DimensionlessUnits
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
        if 'name' in kwargs:
            self._name = kwargs['name']
        if 'is_known' in kwargs:
            self._is_known = kwargs['is_known']
        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity']
            
        # Set default name if not provided
        if not hasattr(self, '_name') or not self._name:
            self._name = f"var_{id(self)}"
    
    def _initialize_with_value_unit(self, value: Any, unit: Any) -> None:
        """Initialize with value and unit."""
        if hasattr(self, '_create_quantity_from_value_unit'):
            self.quantity = self._create_quantity_from_value_unit(value, unit)
        self._is_known = True
    
    def _initialize_with_value_unit_name(self, value: Any, unit: Any, name: str) -> None:
        """Initialize with value, unit, and name."""
        self._name = name
        self._initialize_with_value_unit(value, unit)
    
    def _create_quantity_from_value_unit(self, value: Any, unit: Any) -> Optional[Quantity]:
        """Create quantity from value and unit using setter system."""
        if hasattr(self, '_setter_class') and self._setter_class is not None:
            # Use the setter system like TypedQuantity does
            setter = self._setter_class(self, value)
            unit_prop = self._find_unit_property(setter, str(unit))
            if unit_prop:
                getattr(setter, unit_prop)
                return self.quantity  # Setter should have set the quantity
        
        # Fallback to direct quantity creation
        from .quantity import Quantity
        return Quantity(value, str(unit))
    
    @classmethod
    def _find_unit_property(cls, setter: 'TypeSafeSetter', unit: str) -> Optional[str]:
        """Find unit property with optimized lookup."""
        from ..cache_manager import get_cache_manager
        
        if not hasattr(cls, '_setter_class') or cls._setter_class is None:
            return None

        cache_manager = get_cache_manager()
        
        # Ultra-fast path: Check pre-computed mappings first
        if hasattr(cls, '_unit_mappings') and unit in cls._unit_mappings:
            return cls._unit_mappings[unit]

        # Fast path: Check unified cache
        cached_property = cache_manager.get_unit_property(cls._setter_class, unit)
        if cached_property is not None:
            return cached_property
            
        # Check validation cache to avoid redundant work
        validation_result = cache_manager.get_validation_result(cls._setter_class, unit)
        if validation_result is not None:
            if validation_result and hasattr(setter, unit):
                cache_manager.cache_unit_property(cls._setter_class, unit, unit)
                return unit
            elif not validation_result:
                return None

        # Slow path: Try all variants and cache results
        for unit_variant in [unit, unit + "s", unit[:-1] if unit.endswith("s") else None]:
            if unit_variant and hasattr(setter, unit_variant):
                cache_manager.cache_unit_property(cls._setter_class, unit, unit_variant)
                cache_manager.cache_validation_result(cls._setter_class, unit, True)
                return unit_variant

        # Cache miss - remember that this unit doesn't exist
        cache_manager.cache_unit_property(cls._setter_class, unit, None)
        cache_manager.cache_validation_result(cls._setter_class, unit, False)
        return None


class UnifiedArithmeticMixin:
    """Provides unified arithmetic operations with user-controllable return types."""
    
    def __init__(self):
        self._arithmetic_mode: str = 'expression'  # 'quantity', 'expression', 'auto'
    
    def set_arithmetic_mode(self, mode: str) -> Self:
        """Set arithmetic return type preference."""
        if mode not in ('quantity', 'expression', 'auto'):
            raise ValueError(f"Invalid arithmetic mode: {mode}")
        self._arithmetic_mode = mode
        return self
    
    def __add__(self, other) -> Any:
        """Unified addition with mode-based dispatch."""
        return ArithmeticDispatcher.add(self, other, self._arithmetic_mode)
    
    def __radd__(self, other) -> Any:
        """Reverse addition."""
        return ArithmeticDispatcher.add(other, self, self._arithmetic_mode)
    
    def __sub__(self, other) -> Any:
        """Unified subtraction with mode-based dispatch."""
        return ArithmeticDispatcher.subtract(self, other, self._arithmetic_mode)
    
    def __rsub__(self, other) -> Any:
        """Reverse subtraction."""
        return ArithmeticDispatcher.subtract(other, self, self._arithmetic_mode)
    
    def __mul__(self, other) -> Any:
        """Unified multiplication with mode-based dispatch."""
        return ArithmeticDispatcher.multiply(self, other, self._arithmetic_mode)
    
    def __rmul__(self, other) -> Any:
        """Reverse multiplication."""
        return ArithmeticDispatcher.multiply(other, self, self._arithmetic_mode)
    
    def __truediv__(self, other) -> Any:
        """Unified division with mode-based dispatch."""
        return ArithmeticDispatcher.divide(self, other, self._arithmetic_mode)
    
    def __rtruediv__(self, other) -> Any:
        """Reverse division."""
        return ArithmeticDispatcher.divide(other, self, self._arithmetic_mode)
    
    def __pow__(self, other) -> Any:
        """Unified exponentiation with mode-based dispatch."""
        return ArithmeticDispatcher.power(self, other, self._arithmetic_mode)
    
    def __rpow__(self, other) -> Any:
        """Reverse exponentiation."""
        return ArithmeticDispatcher.power(other, self, self._arithmetic_mode)


class ExpressionMixin:
    """Provides expression and equation creation capabilities."""
    
    def equals(self, other) -> 'Equation':
        """Create an equation: self = other."""
        from ..equations.equation import Equation
        equation_name = f"{self.name}_eq"
        return Equation(name=equation_name, lhs=self, rhs=other)
    
    def lt(self, other) -> 'Expression':
        """Create less-than comparison expression."""
        from ..expressions.nodes import BinaryOperation
        return BinaryOperation('<', self, other)
    
    def leq(self, other) -> 'Expression':
        """Create less-than-or-equal comparison expression."""
        from ..expressions.nodes import BinaryOperation
        return BinaryOperation('<=', self, other)
    
    def geq(self, other) -> 'Expression':
        """Create greater-than-or-equal comparison expression."""
        from ..expressions.nodes import BinaryOperation
        return BinaryOperation('>=', self, other)
    
    def gt(self, other) -> 'Expression':
        """Create greater-than comparison expression."""
        from ..expressions.nodes import BinaryOperation
        return BinaryOperation('>', self, other)
    
    # Python comparison operators for convenience
    def __lt__(self, other) -> 'Expression':
        return self.lt(other)
    
    def __le__(self, other) -> 'Expression':
        return self.leq(other)
    
    def __ge__(self, other) -> 'Expression':
        return self.geq(other)
    
    def __gt__(self, other) -> 'Expression':
        return self.gt(other)
    
    def __eq__(self, other) -> 'Expression':
        """Create equality comparison expression."""
        from ..expressions.nodes import BinaryOperation
        return BinaryOperation('==', self, other)
    
    def __ne__(self, other) -> 'Expression':
        """Create inequality comparison expression."""
        from ..expressions.nodes import BinaryOperation
        return BinaryOperation('!=', self, other)
    
    def get_variables(self) -> set[str]:
        """Get variable names used in this variable (for equation system compatibility)."""
        return {self.symbol or self.name}
    
    def evaluate(self, variable_values: dict[str, 'UnifiedVariable']) -> 'Quantity':
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
        """Solve this variable from an expression."""
        # Create equation: self = expression
        equation = self.equals(expression)
        
        # Try to solve the equation
        try:
            solved_value = equation.solve_for(self.symbol or self.name, {})
            if solved_value is not None and hasattr(solved_value, 'quantity'):
                self.quantity = solved_value.quantity
                self._is_known = True
        except Exception:
            # If solving fails, at least create the equation relationship
            pass
        
        return self


class SetterCompatibilityMixin:
    """Provides backward compatibility with existing setter system."""
    
    def set(self, value: float) -> 'TypeSafeSetter':
        """Create setter object for fluent API compatibility."""
        if hasattr(self, '_setter_class') and self._setter_class:
            return self._setter_class(value, self)
        else:
            # Fallback to generic setter
            from .quantity import TypeSafeSetter
            return TypeSafeSetter(value, self)


class UnifiedVariable(
    QuantityManagementMixin,
    FlexibleConstructorMixin,
    UnifiedArithmeticMixin,
    ExpressionMixin,
    SetterCompatibilityMixin,
    ErrorHandlerMixin
):
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
    _dimension: Optional[DimensionSignature] = None
    _setter_class: Optional[type] = None
    _default_unit_property: Optional[str] = None
    _unit_mappings: dict[str, str] = {}
    
    def __init__(self, *args, **kwargs):
        """Initialize all mixin components with backward compatibility."""
        # Initialize mixins
        QuantityManagementMixin.__init__(self)
        UnifiedArithmeticMixin.__init__(self)
        ErrorHandlerMixin.__init__(self)
        
        # Process constructor arguments
        self._initialize_from_args(*args, **kwargs)
        
        # Initialize attributes required for compatibility
        self.validation_checks = []
        self._parent_problem = None
        if not hasattr(self, '_symbol'):
            self._symbol = None
    
    def _validate_dimension_compatibility(self) -> None:
        """Ensure quantity dimension matches expected dimension."""
        if (self._quantity is not None and 
            hasattr(self._quantity, '_dimension_sig') and 
            self._quantity._dimension_sig != self._dimension):
            
            context = ErrorContext(
                module=self.__class__.__module__,
                function="__init__",
                operation="dimension_validation",
                variables={"expected": str(self._dimension), "actual": str(self._quantity._dimension_sig)}
            )
            self._error_handler.handle_dimensional_error(
                "initialization", self._dimension, self._quantity._dimension_sig, context
            )
    
    def _create_quantity_from_value_unit_with_validation(self, value: Any, unit: Any) -> Optional[Quantity]:
        """Create quantity with dimension validation - simplified version."""
        # For now, skip complex dimension validation since registry doesn't have get_unit_definition
        # The setter system will handle unit validation
        from .quantity import Quantity
        return Quantity(value, str(unit))
    
    @property
    def name(self) -> str:
        """Get variable name."""
        return getattr(self, '_name', '')
    
    @property 
    def expected_dimension(self) -> Optional[DimensionSignature]:
        """Get expected dimension for backward compatibility."""
        return self._dimension
    
    @expected_dimension.setter
    def expected_dimension(self, value: Optional[DimensionSignature]) -> None:
        """Set expected dimension for backward compatibility."""
        self._dimension = value
    
    @name.setter
    def name(self, value: str) -> None:
        """Set variable name."""
        self._name = value
    
    @property
    def symbol(self) -> Optional[str]:
        """Get variable symbol for equations."""
        return getattr(self, '_symbol', None) or self.name
    
    @symbol.setter
    def symbol(self, value: Optional[str]) -> None:
        """Set variable symbol."""
        self._symbol = value
    
    def __str__(self) -> str:
        """String representation of variable."""
        if self.is_known and self._quantity is not None:
            return f"{self.name} = {self._quantity}"
        else:
            return f"{self.name} (unset)"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return f"{self.__class__.__name__}(name='{self.name}', is_known={self.is_known}, quantity={self._quantity})"




def create_domain_variable_class(dimension: 'DimensionSignature', 
                                setter_class: Optional[type] = None,
                                default_unit_property: Optional[str] = None,
                                unit_mappings: Optional[dict[str, str]] = None) -> type[UnifiedVariable]:
    """
    Factory function to create domain-specific variable classes.
    
    This replaces the need for hand-coded inheritance chains by generating
    the necessary class with proper dimension and setter configuration.
    """
    class DomainVariable(UnifiedVariable):
        _dimension = dimension
        _setter_class = setter_class
        _default_unit_property = default_unit_property
        _unit_mappings = unit_mappings or {}
    
    return DomainVariable


# Example usage demonstrating backward compatibility:
if __name__ == "__main__":
    # Test that new system works with existing patterns
    from ..generated.dimensions import LENGTH, PRESSURE
    
    # Create Length class using new system
    Length = create_domain_variable_class(LENGTH, default_unit_property="meters")
    Pressure = create_domain_variable_class(PRESSURE, default_unit_property="pascals")
    
    # Test all constructor patterns
    length1 = Length("beam_length")  # Name only
    length2 = Length(10.0, "mm", "width")  # Value, unit, name
    pressure1 = Pressure(101325, "Pa", "atmospheric", is_known=True)  # Full constructor
    
    # Test arithmetic modes
    length1.set_arithmetic_mode('quantity')
    area_qty = length1 * length2  # Returns Quantity (fast path)
    
    length1.set_arithmetic_mode('expression')
    area_expr = length1 * length2  # Returns Expression (flexible path)
    
    # Test auto mode (default)
    length1.set_arithmetic_mode('auto')
    mixed_result = length1 * pressure1  # Auto-chooses based on known values
    
    print(f"New hierarchy working: {length1}, {pressure1}")
    print(f"Arithmetic results: {type(area_qty)}, {type(area_expr)}")