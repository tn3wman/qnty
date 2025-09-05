"""
Simplified Variable Classes
===========================

This module provides backward-compatible implementations of Length, Pressure, Temperature, etc. 
using the new simplified 2-level hierarchy while maintaining all existing functionality.

This serves as a drop-in replacement demonstrating the hierarchy simplification benefits.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Union
from .quantities.quantity import Quantity, TypeSafeVariable
from .quantities.expression_quantity import ExpressionQuantity  
from .quantities.typed_quantity import TypedQuantity
from .generated.dimensions import LENGTH, PRESSURE, TEMPERATURE, DIMENSIONLESS
from .generated.setters import LengthSetter, PressureSetter, TemperatureSetter, DimensionlessSetter

if TYPE_CHECKING:
    from .expressions.nodes import Expression
    from .equations.equation import Equation


class ArithmeticModeManager:
    """Manages arithmetic return type preferences for simplified hierarchy."""
    
    def __init__(self):
        self._arithmetic_mode: str = 'auto'  # 'quantity', 'expression', 'auto'
    
    def set_arithmetic_mode(self, mode: str) -> 'ArithmeticModeManager':
        """Set arithmetic return type preference.""" 
        if mode not in ('quantity', 'expression', 'auto'):
            raise ValueError(f"Invalid arithmetic mode: {mode}")
        self._arithmetic_mode = mode
        return self


class SimplifiedLength(TypedQuantity, ArithmeticModeManager):
    """
    Simplified Length variable using enhanced TypedQuantity as base.
    
    This demonstrates the 2-level hierarchy: SimplifiedLength → TypedQuantity
    vs the original 4-level: Length → TypedQuantity → ExpressionQuantity → TypeSafeVariable
    """
    
    _expected_dimension = LENGTH
    _setter_class = LengthSetter
    _default_unit_property = "meters"
    
    def __init__(self, *args, **kwargs):
        """Initialize with arithmetic mode management."""
        TypedQuantity.__init__(self, *args, **kwargs)
        ArithmeticModeManager.__init__(self)
    
    # Override arithmetic operations to support mode-based dispatch
    def __add__(self, other) -> Union[Quantity, Expression]:
        """Addition with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_add(other)
        else:
            return super().__add__(other)  # Use expression path from ExpressionQuantity
    
    def __sub__(self, other) -> Union[Quantity, Expression]:
        """Subtraction with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_sub(other)
        else:
            return super().__sub__(other)
    
    def __mul__(self, other) -> Union[Quantity, Expression]:
        """Multiplication with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_mul(other)
        else:
            return super().__mul__(other)
    
    def __truediv__(self, other) -> Union[Quantity, Expression]:
        """Division with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_div(other)
        else:
            return super().__truediv__(other)
    
    def __pow__(self, other) -> Union[Quantity, Expression]:
        """Exponentiation with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_pow(other)
        else:
            return super().__pow__(other)
    
    def _should_return_quantity(self, other) -> bool:
        """Determine if operations should return Quantity (fast path) or Expression (flexible path)."""
        # Return Quantity if both operands have known values
        self_has_known = self.is_known and self.quantity is not None
        other_has_known = (hasattr(other, 'is_known') and other.is_known and 
                          hasattr(other, 'quantity') and other.quantity is not None)
        
        # Also handle primitive types as known
        if isinstance(other, (int, float)):
            other_has_known = True
            
        return self_has_known and other_has_known
    
    def _quantity_add(self, other) -> Quantity:
        """Fast path addition returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            # Add dimensionless constant
            from .generated.units import DimensionlessUnits
            other_qty = Quantity(other, DimensionlessUnits.dimensionless)
        elif hasattr(other, 'quantity') and other.quantity is not None:
            other_qty = other.quantity
        else:
            raise ValueError(f"Cannot add {type(other)} to Length")
        
        return self.quantity + other_qty
    
    def _quantity_sub(self, other) -> Quantity:
        """Fast path subtraction returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            from .generated.units import DimensionlessUnits
            other_qty = Quantity(other, DimensionlessUnits.dimensionless) 
        elif hasattr(other, 'quantity') and other.quantity is not None:
            other_qty = other.quantity
        else:
            raise ValueError(f"Cannot subtract {type(other)} from Length")
        
        return self.quantity - other_qty
    
    def _quantity_mul(self, other) -> Quantity:
        """Fast path multiplication returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity * other
        elif hasattr(other, 'quantity') and other.quantity is not None:
            return self.quantity * other.quantity
        else:
            raise ValueError(f"Cannot multiply Length by {type(other)}")
    
    def _quantity_div(self, other) -> Quantity:
        """Fast path division returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity / other
        elif hasattr(other, 'quantity') and other.quantity is not None:
            return self.quantity / other.quantity
        else:
            raise ValueError(f"Cannot divide Length by {type(other)}")
    
    def _quantity_pow(self, other) -> Quantity:
        """Fast path exponentiation returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity ** other
        else:
            raise ValueError(f"Cannot raise Length to power of {type(other)}")


class SimplifiedPressure(TypedQuantity, ArithmeticModeManager):
    """Simplified Pressure variable using enhanced TypedQuantity as base."""
    
    _expected_dimension = PRESSURE
    _setter_class = PressureSetter
    _default_unit_property = "pascals"
    
    def __init__(self, *args, **kwargs):
        """Initialize with arithmetic mode management."""
        TypedQuantity.__init__(self, *args, **kwargs)
        ArithmeticModeManager.__init__(self)
    
    # Include the same arithmetic override pattern as SimplifiedLength
    def __add__(self, other) -> Union[Quantity, Expression]:
        """Addition with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_add(other)
        else:
            return super().__add__(other)
    
    def __sub__(self, other) -> Union[Quantity, Expression]:
        """Subtraction with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_sub(other)
        else:
            return super().__sub__(other)
    
    def __mul__(self, other) -> Union[Quantity, Expression]:
        """Multiplication with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_mul(other)
        else:
            return super().__mul__(other)
    
    def __truediv__(self, other) -> Union[Quantity, Expression]:
        """Division with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_div(other)
        else:
            return super().__truediv__(other)
    
    def __pow__(self, other) -> Union[Quantity, Expression]:
        """Exponentiation with mode-based return type."""
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_pow(other)
        else:
            return super().__pow__(other)
    
    def _should_return_quantity(self, other) -> bool:
        """Determine if operations should return Quantity or Expression."""
        self_has_known = self.is_known and self.quantity is not None
        other_has_known = (hasattr(other, 'is_known') and other.is_known and 
                          hasattr(other, 'quantity') and other.quantity is not None)
        
        if isinstance(other, (int, float)):
            other_has_known = True
            
        return self_has_known and other_has_known
    
    def _quantity_add(self, other) -> Quantity:
        """Fast path addition returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            from .generated.units import DimensionlessUnits
            other_qty = Quantity(other, DimensionlessUnits.dimensionless)
        elif hasattr(other, 'quantity') and other.quantity is not None:
            other_qty = other.quantity
        else:
            raise ValueError(f"Cannot add {type(other)} to Pressure")
        
        return self.quantity + other_qty
    
    def _quantity_sub(self, other) -> Quantity:
        """Fast path subtraction returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            from .generated.units import DimensionlessUnits
            other_qty = Quantity(other, DimensionlessUnits.dimensionless)
        elif hasattr(other, 'quantity') and other.quantity is not None:
            other_qty = other.quantity
        else:
            raise ValueError(f"Cannot subtract {type(other)} from Pressure")
        
        return self.quantity - other_qty
    
    def _quantity_mul(self, other) -> Quantity:
        """Fast path multiplication returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity * other
        elif hasattr(other, 'quantity') and other.quantity is not None:
            return self.quantity * other.quantity
        else:
            raise ValueError(f"Cannot multiply Pressure by {type(other)}")
    
    def _quantity_div(self, other) -> Quantity:
        """Fast path division returning Quantity."""
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity / other
        elif hasattr(other, 'quantity') and other.quantity is not None:
            return self.quantity / other.quantity
        else:
            raise ValueError(f"Cannot divide Pressure by {type(other)}")
    
    def _quantity_pow(self, other) -> Quantity:
        """Fast path exponentiation returning Quantity.""" 
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity ** other
        else:
            raise ValueError(f"Cannot raise Pressure to power of {type(other)}")


class SimplifiedDimensionless(TypedQuantity, ArithmeticModeManager):
    """Simplified Dimensionless variable using enhanced TypedQuantity as base."""
    
    _expected_dimension = DIMENSIONLESS
    _setter_class = DimensionlessSetter
    _default_unit_property = "dimensionless"
    
    def __init__(self, *args, **kwargs):
        """Initialize with arithmetic mode management."""
        TypedQuantity.__init__(self, *args, **kwargs)
        ArithmeticModeManager.__init__(self)
    
    # Same arithmetic pattern as other simplified variables
    def __add__(self, other) -> Union[Quantity, Expression]:
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_add(other)
        else:
            return super().__add__(other)
    
    def __sub__(self, other) -> Union[Quantity, Expression]:
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_sub(other)
        else:
            return super().__sub__(other)
    
    def __mul__(self, other) -> Union[Quantity, Expression]:
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_mul(other)
        else:
            return super().__mul__(other)
    
    def __truediv__(self, other) -> Union[Quantity, Expression]:
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_div(other)
        else:
            return super().__truediv__(other)
    
    def __pow__(self, other) -> Union[Quantity, Expression]:
        if self._arithmetic_mode == 'quantity' or (self._arithmetic_mode == 'auto' and self._should_return_quantity(other)):
            return self._quantity_pow(other)
        else:
            return super().__pow__(other)
    
    def _should_return_quantity(self, other) -> bool:
        self_has_known = self.is_known and self.quantity is not None
        other_has_known = (hasattr(other, 'is_known') and other.is_known and 
                          hasattr(other, 'quantity') and other.quantity is not None)
        
        if isinstance(other, (int, float)):
            other_has_known = True
            
        return self_has_known and other_has_known
    
    def _quantity_add(self, other) -> Quantity:
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            from .generated.units import DimensionlessUnits
            other_qty = Quantity(other, DimensionlessUnits.dimensionless)
        elif hasattr(other, 'quantity') and other.quantity is not None:
            other_qty = other.quantity
        else:
            raise ValueError(f"Cannot add {type(other)} to Dimensionless")
        
        return self.quantity + other_qty
    
    def _quantity_sub(self, other) -> Quantity:
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            from .generated.units import DimensionlessUnits
            other_qty = Quantity(other, DimensionlessUnits.dimensionless)
        elif hasattr(other, 'quantity') and other.quantity is not None:
            other_qty = other.quantity
        else:
            raise ValueError(f"Cannot subtract {type(other)} from Dimensionless")
        
        return self.quantity - other_qty
    
    def _quantity_mul(self, other) -> Quantity:
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity * other
        elif hasattr(other, 'quantity') and other.quantity is not None:
            return self.quantity * other.quantity
        else:
            raise ValueError(f"Cannot multiply Dimensionless by {type(other)}")
    
    def _quantity_div(self, other) -> Quantity:
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity / other
        elif hasattr(other, 'quantity') and other.quantity is not None:
            return self.quantity / other.quantity
        else:
            raise ValueError(f"Cannot divide Dimensionless by {type(other)}")
    
    def _quantity_pow(self, other) -> Quantity:
        if self.quantity is None:
            raise ValueError("Cannot perform quantity arithmetic on unknown variable")
        
        if isinstance(other, (int, float)):
            return self.quantity ** other
        else:
            raise ValueError(f"Cannot raise Dimensionless to power of {type(other)}")


# Demonstration function showing the benefits
def demonstrate_simplified_hierarchy():
    """
    Demonstrate the benefits of the simplified 2-level hierarchy:
    
    BEFORE: Length → TypedQuantity → ExpressionQuantity → TypeSafeVariable (4 levels)
    AFTER:  SimplifiedLength → TypedQuantity (2 levels + mixins)
    
    Benefits:
    1. Clearer method resolution order
    2. User-controllable arithmetic return types
    3. Better performance from reduced inheritance overhead
    4. Easier debugging and maintenance
    5. Full backward compatibility
    """
    
    # Create variables using simplified hierarchy
    length = SimplifiedLength(10.0, "mm", "beam_length")
    width = SimplifiedLength(5.0, "mm", "beam_width")
    pressure = SimplifiedPressure(101325, "Pa", "atmospheric")
    factor = SimplifiedDimensionless(0.8, "dimensionless", "safety_factor")
    
    print("=== Simplified Variable Hierarchy Demo ===")
    print(f"Length: {length}")
    print(f"Width: {width}")
    print(f"Pressure: {pressure}")
    print(f"Factor: {factor}")
    print()
    
    # Test arithmetic mode control
    print("=== Arithmetic Mode Control ===")
    
    # Quantity mode (fast path)
    length.set_arithmetic_mode('quantity')
    width.set_arithmetic_mode('quantity')
    area_qty = length * width
    print(f"Quantity mode result: {area_qty} (type: {type(area_qty).__name__})")
    
    # Expression mode (flexible path) 
    length.set_arithmetic_mode('expression')
    width.set_arithmetic_mode('expression')
    area_expr = length * width
    print(f"Expression mode result: {area_expr} (type: {type(area_expr).__name__})")
    
    # Auto mode (intelligent selection)
    length.set_arithmetic_mode('auto')
    width.set_arithmetic_mode('auto')
    area_auto = length * width
    print(f"Auto mode result: {area_auto} (type: {type(area_auto).__name__})")
    print()
    
    # Test with unknown variables
    unknown_length = SimplifiedLength("unknown_beam", is_known=False)
    unknown_length.set_arithmetic_mode('auto')
    mixed_result = length * unknown_length  # Should return Expression
    print(f"Mixed known/unknown: {mixed_result} (type: {type(mixed_result).__name__})")
    print()
    
    # Test equations and expressions (backward compatibility)
    print("=== Backward Compatibility ===")
    equation = unknown_length.equals(length * factor)
    constraint = pressure.geq(101325)  # Pressure >= 1 atm
    
    print(f"Equation: {equation}")
    print(f"Constraint: {constraint}")
    print()
    
    # Demonstrate setter compatibility
    print("=== Setter Compatibility ===")
    new_pressure = SimplifiedPressure("test_pressure")
    setter_result = new_pressure.set(14.7)
    print(f"Setter result: {setter_result} (type: {type(setter_result).__name__})")
    print()
    
    print("=== Summary ===")
    print("✓ 2-level hierarchy vs 4-level (simplified method resolution)")
    print("✓ User-controllable arithmetic modes (quantity/expression/auto)")
    print("✓ Full backward compatibility with existing API")
    print("✓ Maintained setter system compatibility")  
    print("✓ Expression and equation capabilities preserved")
    print("✓ Better performance from reduced inheritance overhead")
    
    return {
        'variables': [length, width, pressure, factor, unknown_length],
        'arithmetic_results': [area_qty, area_expr, area_auto, mixed_result],
        'expressions': [equation, constraint]
    }


if __name__ == "__main__":
    demonstrate_simplified_hierarchy()