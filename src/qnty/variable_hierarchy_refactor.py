"""
Variable Hierarchy Simplification
==================================

This module provides a simplified 2-level inheritance structure to replace
the current 4-level chain: TypeSafeVariable → ExpressionQuantity → TypedQuantity → Generated Variables

New Structure: QuantityVariable (base) → Domain Variables (Length, Pressure, etc.)

This refactoring addresses the most significant remaining code smell identified in the analysis.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .constants import FLOAT_EQUALITY_TOLERANCE
from .generated.dimensions import DimensionSignature
from .cache_manager import get_cache_manager
from .error_handling import ErrorHandlerMixin, ErrorContext

if TYPE_CHECKING:
    from .quantities.quantity import Quantity, TypeSafeSetter
    from .expressions.nodes import Expression
    from .equations.equation import Equation


# --- Mixin Components for Clean Separation of Concerns ---

class QuantityManagementMixin:
    """Handles core quantity storage and basic operations."""
    
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

    def mark_known(self) -> None:
        """Mark variable as having a known value."""
        self._is_known = True

    def mark_unknown(self) -> None:
        """Mark variable as unknown."""
        self._is_known = False

    def update(self, value: Any = None, unit: Any = None, 
               quantity: Optional[Quantity] = None, is_known: Optional[bool] = None) -> 'QuantityVariable':
        """Flexible update method for variable properties."""
        if quantity is not None:
            self.quantity = quantity
        elif value is not None:
            # Create new quantity from value and unit
            # Implementation would depend on unit system
            pass
        
        if is_known is not None:
            self._is_known = is_known
            
        return self


class ConstructorMixin:
    """Handles flexible variable initialization patterns."""
    
    def __init__(self, *args, **kwargs):
        """Unified constructor handling multiple initialization patterns."""
        self._initialize_from_args(*args, **kwargs)
    
    def _initialize_from_args(self, *args, **kwargs) -> None:
        """Process constructor arguments flexibly."""
        # Handle different constructor patterns:
        # Variable(name)
        # Variable(value, unit, name)  
        # Variable(name=..., value=..., unit=...)
        # Variable(quantity=...)
        
        if len(args) == 1 and len(kwargs) == 0:
            # Variable(name) pattern
            if isinstance(args[0], str):
                self._name = args[0]
                self._is_known = False
            else:
                # Variable(value) pattern - assume dimensionless
                self._initialize_with_value(args[0])
                
        elif len(args) == 3:
            # Variable(value, unit, name) pattern
            value, unit, name = args
            self._initialize_with_value_unit_name(value, unit, name)
            
        elif 'quantity' in kwargs:
            self.quantity = kwargs['quantity']
            self._name = kwargs.get('name', '')
            
        # Handle remaining kwargs
        for key, value in kwargs.items():
            if key == 'name':
                self._name = value
            elif key == 'is_known':
                self._is_known = value

    def _initialize_with_value(self, value: Any) -> None:
        """Initialize with just a value."""
        # Implementation specific to quantity system
        pass
        
    def _initialize_with_value_unit_name(self, value: Any, unit: Any, name: str) -> None:
        """Initialize with value, unit, and name."""
        # Implementation specific to quantity system
        pass


class ArithmeticMixin:
    """Provides unified arithmetic operations with user-controllable return types."""
    
    def __init__(self):
        self._arithmetic_mode: str = 'auto'  # 'quantity', 'expression', 'auto'

    def set_arithmetic_mode(self, mode: str) -> 'QuantityVariable':
        """Set arithmetic return type preference."""
        if mode not in ('quantity', 'expression', 'auto'):
            raise ValueError(f"Invalid arithmetic mode: {mode}")
        self._arithmetic_mode = mode
        return self

    def __add__(self, other) -> Any:
        """Unified addition with mode-based dispatch."""
        return self._dispatch_arithmetic('add', other)
    
    def __sub__(self, other) -> Any:
        """Unified subtraction with mode-based dispatch."""
        return self._dispatch_arithmetic('subtract', other)
    
    def __mul__(self, other) -> Any:
        """Unified multiplication with mode-based dispatch."""
        return self._dispatch_arithmetic('multiply', other)
    
    def __truediv__(self, other) -> Any:
        """Unified division with mode-based dispatch."""
        return self._dispatch_arithmetic('divide', other)
    
    def __pow__(self, other) -> Any:
        """Unified exponentiation with mode-based dispatch."""
        return self._dispatch_arithmetic('power', other)

    def _dispatch_arithmetic(self, operation: str, other) -> Any:
        """Dispatch arithmetic operations based on mode and context."""
        if self._arithmetic_mode == 'quantity':
            return self._quantity_arithmetic(operation, other)
        elif self._arithmetic_mode == 'expression':
            return self._expression_arithmetic(operation, other)
        else:  # auto mode
            return self._auto_arithmetic(operation, other)

    def _quantity_arithmetic(self, operation: str, other) -> 'Quantity':
        """Fast path arithmetic returning Quantity objects."""
        # Implementation would use direct quantity operations
        # for maximum performance
        pass
    
    def _expression_arithmetic(self, operation: str, other) -> 'Expression':
        """Flexible path arithmetic returning Expression objects."""
        # Implementation would create expression trees
        # for symbolic manipulation
        pass
    
    def _auto_arithmetic(self, operation: str, other) -> Any:
        """Automatic mode - choose best return type based on context."""
        # Logic to determine whether to return Quantity or Expression
        # based on whether operands have known values
        if self.is_known and hasattr(other, 'is_known') and other.is_known:
            return self._quantity_arithmetic(operation, other)
        else:
            return self._expression_arithmetic(operation, other)


class ExpressionMixin:
    """Provides expression and equation creation capabilities."""
    
    def equals(self, other) -> 'Equation':
        """Create an equation: self = other."""
        from .equations.equation import Equation
        return Equation(lhs=self, rhs=other)
    
    def lt(self, other) -> 'Expression':
        """Create less-than comparison expression."""
        from .expressions.nodes import BinaryOperation
        return BinaryOperation('<', self, other)
    
    def leq(self, other) -> 'Expression':
        """Create less-than-or-equal comparison expression."""
        from .expressions.nodes import BinaryOperation
        return BinaryOperation('<=', self, other)
    
    def geq(self, other) -> 'Expression':
        """Create greater-than-or-equal comparison expression."""
        from .expressions.nodes import BinaryOperation
        return BinaryOperation('>=', self, other)
    
    def gt(self, other) -> 'Expression':
        """Create greater-than comparison expression."""
        from .expressions.nodes import BinaryOperation
        return BinaryOperation('>', self, other)


# --- Unified Base Class ---

class QuantityVariable(
    QuantityManagementMixin, 
    ConstructorMixin, 
    ArithmeticMixin, 
    ExpressionMixin, 
    ErrorHandlerMixin
):
    """
    Unified variable class that combines all capabilities through mixins.
    
    This replaces the 4-level inheritance chain with a clean mixin-based approach:
    - QuantityManagementMixin: Core quantity storage and state
    - ConstructorMixin: Flexible initialization patterns  
    - ArithmeticMixin: Unified arithmetic with user control
    - ExpressionMixin: Expression and equation creation
    - ErrorHandlerMixin: Consistent error handling
    """
    
    # Class attributes that subclasses must define
    _dimension: Optional[DimensionSignature] = None
    _setter_class: Optional[type] = None
    _default_unit_property: Optional[str] = None
    
    def __init__(self, *args, **kwargs):
        """Initialize all mixin components."""
        QuantityManagementMixin.__init__(self)
        ConstructorMixin.__init__(self, *args, **kwargs)
        ArithmeticMixin.__init__(self)
        ErrorHandlerMixin.__init__(self)
        
        # Validate dimension compatibility if quantity is set
        if self._quantity is not None and self._dimension is not None:
            self._validate_dimension_compatibility()

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

    @property
    def name(self) -> str:
        """Get variable name."""
        return self._name
    
    @name.setter  
    def name(self, value: str) -> None:
        """Set variable name."""
        self._name = value

    @property
    def symbol(self) -> Optional[str]:
        """Get variable symbol for equations."""
        return self._symbol or self._name
    
    @symbol.setter
    def symbol(self, value: Optional[str]) -> None:
        """Set variable symbol."""
        self._symbol = value

    def __str__(self) -> str:
        """String representation of variable."""
        if self.is_known and self._quantity is not None:
            return f"{self._name} = {self._quantity}"
        else:
            return f"{self._name} (unknown)"
    
    def __repr__(self) -> str:
        """Detailed representation for debugging."""
        return f"{self.__class__.__name__}(name='{self._name}', is_known={self.is_known}, quantity={self._quantity})"


# --- Migration Helper Functions ---

def create_variable_from_legacy(legacy_variable) -> QuantityVariable:
    """Create new QuantityVariable from legacy 4-level hierarchy variable."""
    # Extract properties from legacy variable
    new_var = QuantityVariable()
    new_var._name = getattr(legacy_variable, '_name', '')
    new_var._quantity = getattr(legacy_variable, '_quantity', None)  
    new_var._is_known = getattr(legacy_variable, '_is_known', False)
    new_var._symbol = getattr(legacy_variable, '_symbol', None)
    return new_var


# --- Domain-Specific Variable Classes ---

class Length(QuantityVariable):
    """Length variable with simplified inheritance."""
    
    from .generated.dimensions import LENGTH
    _dimension = LENGTH
    _default_unit_property = "meters"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pressure(QuantityVariable):
    """Pressure variable with simplified inheritance."""
    
    from .generated.dimensions import PRESSURE  
    _dimension = PRESSURE
    _default_unit_property = "pascals"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Temperature(QuantityVariable):
    """Temperature variable with simplified inheritance."""
    
    from .generated.dimensions import TEMPERATURE
    _dimension = TEMPERATURE
    _default_unit_property = "kelvin"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Example usage demonstrating the benefits:

def demonstrate_simplified_hierarchy():
    """
    Demonstrate the benefits of the simplified hierarchy:
    
    BEFORE (4-level): TypeSafeVariable → ExpressionQuantity → TypedQuantity → Length
    AFTER (2-level): QuantityVariable → Length
    
    Benefits:
    1. Clearer method resolution order (2 levels vs 4)
    2. Focused mixin responsibilities vs scattered inheritance
    3. Single arithmetic system with user control
    4. Better performance from reduced inheritance overhead
    5. Easier debugging and maintenance
    """
    
    # Create variables with clean 2-level hierarchy
    length = Length(10.0, "mm", "beam_length")
    width = Length(5.0, "mm", "beam_width") 
    
    # Arithmetic operations with user-controllable return types
    length.set_arithmetic_mode('quantity')  # Fast path for performance
    area_qty = length * width  # Returns Quantity for speed
    
    width.set_arithmetic_mode('expression')  # Flexible path for symbolic work
    area_expr = length * width  # Returns Expression for manipulation
    
    # Auto mode (default) chooses best return type based on context
    pressure = Pressure("p", is_known=False)  # Unknown variable
    force = pressure * area_qty  # Returns Expression (symbolic)
    
    # Unified constructor patterns  
    temp1 = Temperature("ambient_temp")  # Name-only constructor
    temp2 = Temperature(298.15, "K", "room_temp")  # Value/unit/name constructor
    temp3 = Temperature(name="process_temp", value=373, unit="K")  # Keyword constructor
    
    # Expression capabilities preserved
    constraint = pressure.geq(101325)  # Pressure >= 1 atm
    equation = force.equals(pressure * area_qty)  # F = P * A
    
    return {
        'variables': [length, width, pressure, temp1, temp2, temp3],
        'expressions': [area_qty, area_expr, force, constraint, equation]
    }


# --- Implementation Plan ---

@dataclass 
class ImplementationPlan:
    """Implementation plan for hierarchy simplification."""
    
    phase_1_tasks = [
        "Create QuantityVariable with mixin architecture",
        "Implement ArithmeticDispatcher for unified operations", 
        "Test mixin composition and method resolution",
        "Create migration utilities for legacy variables"
    ]
    
    phase_2_tasks = [
        "Update code generation to use QuantityVariable base",
        "Migrate Length, Pressure, Temperature as examples",
        "Create comprehensive test suite for new hierarchy",
        "Performance benchmark against 4-level chain"
    ]
    
    phase_3_tasks = [
        "Migrate all 100+ generated variable classes",
        "Update problem system to use new hierarchy", 
        "Ensure backward compatibility during transition",
        "Validate all 187 tests pass with new system"
    ]
    
    phase_4_tasks = [
        "Remove deprecated 4-level inheritance classes",
        "Update documentation and examples",
        "Create migration guide for users",
        "Final performance validation"
    ]
    
    estimated_timeline = "8-11 days"
    risk_level = "HIGH"
    mitigation_strategies = [
        "Implement behind feature flag initially",
        "Comprehensive backward compatibility layer",
        "Step-by-step validation with test suite",
        "Rollback plan for each phase"
    ]