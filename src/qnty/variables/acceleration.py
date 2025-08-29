"""
Acceleration Variable Module
============================

Type-safe acceleration variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ACCELERATION
from ..units import AccelerationUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AccelerationSetter(TypeSafeSetter):
    """Acceleration-specific setter with only acceleration units."""
    
    def __init__(self, variable: 'Acceleration', value: float):
        super().__init__(variable, value)
    
    # Only acceleration units available - compile-time safe!
    @property
    def meters_per_second_squared(self) -> 'Acceleration':
        self.variable.quantity = FastQuantity(self.value, AccelerationUnits.meter_per_second_squared)
        return cast('Acceleration', self.variable)
    
    @property
    def feet_per_second_squared(self) -> 'Acceleration':
        self.variable.quantity = FastQuantity(self.value, AccelerationUnits.foot_per_second_squared)
        return cast('Acceleration', self.variable)
    
    # Short aliases for convenience
    @property
    def mps2(self) -> 'Acceleration':
        return self.meters_per_second_squared
    
    @property
    def fps2(self) -> 'Acceleration':
        return self.feet_per_second_squared


class Acceleration(TypedVariable):
    """Type-safe acceleration variable with expression capabilities."""
    
    _setter_class = AccelerationSetter
    _expected_dimension = ACCELERATION
    _default_unit_property = "meters_per_second_squared"
    
    def set(self, value: float) -> AccelerationSetter:
        """Create an acceleration setter for this variable with proper type annotation."""
        return AccelerationSetter(self, value)


class AccelerationModule(VariableModule):
    """Acceleration variable module definition."""
    
    def get_variable_class(self):
        return Acceleration
    
    def get_setter_class(self):
        return AccelerationSetter
    
    def get_expected_dimension(self):
        return ACCELERATION


# Register this module for auto-discovery
VARIABLE_MODULE = AccelerationModule()
