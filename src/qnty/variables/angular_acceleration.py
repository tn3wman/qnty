"""
AngularAcceleration Variable Module
====================================

Type-safe angular acceleration variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ANGULAR_ACCELERATION
from ..units import AngularAccelerationUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AngularAccelerationSetter(TypeSafeSetter):
    """AngularAcceleration-specific setter with only angular acceleration units."""
    
    def __init__(self, variable: 'AngularAcceleration', value: float):
        super().__init__(variable, value)
    
    # Only angular acceleration units available - compile-time safe!
    @property
    def radian_per_second_squareds(self) -> 'AngularAcceleration':
        self.variable.quantity = FastQuantity(self.value, AngularAccelerationUnits.radian_per_second_squared)
        return cast('AngularAcceleration', self.variable)
    @property
    def revolution_per_second_squareds(self) -> 'AngularAcceleration':
        self.variable.quantity = FastQuantity(self.value, AngularAccelerationUnits.revolution_per_second_squared)
        return cast('AngularAcceleration', self.variable)
    @property
    def rpm_or_revolution_per_minute_per_minutes(self) -> 'AngularAcceleration':
        self.variable.quantity = FastQuantity(self.value, AngularAccelerationUnits.rpm_or_revolution_per_minute_per_minute)
        return cast('AngularAcceleration', self.variable)
    
    # Short aliases for convenience
    pass


class AngularAcceleration(TypedVariable):
    """Type-safe angular acceleration variable with expression capabilities."""
    
    _setter_class = AngularAccelerationSetter
    _expected_dimension = ANGULAR_ACCELERATION
    _default_unit_property = "radian_per_second_squareds"
    
    def set(self, value: float) -> AngularAccelerationSetter:
        """Create a angular acceleration setter for this variable with proper type annotation."""
        return AngularAccelerationSetter(self, value)


class AngularAccelerationModule(VariableModule):
    """AngularAcceleration variable module definition."""
    
    def get_variable_class(self):
        return AngularAcceleration
    
    def get_setter_class(self):
        return AngularAccelerationSetter
    
    def get_expected_dimension(self):
        return ANGULAR_ACCELERATION


# Register this module for auto-discovery
VARIABLE_MODULE = AngularAccelerationModule()