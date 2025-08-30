"""
VelocityAngular Variable Module
================================

Type-safe velocity, angular variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ANGULAR_VELOCITY
from ..units import VelocityAngularUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VelocityAngularSetter(TypeSafeSetter):
    """VelocityAngular-specific setter with only velocity, angular units."""
    
    def __init__(self, variable: 'VelocityAngular', value: float):
        super().__init__(variable, value)
    
    # Only velocity, angular units available - compile-time safe!
    @property
    def per_minutes(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.per_minute)
        return cast('VelocityAngular', self.variable)
    @property
    def per_seconds(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.per_second)
        return cast('VelocityAngular', self.variable)
    @property
    def grade_per_minutes(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.grade_per_minute)
        return cast('VelocityAngular', self.variable)
    @property
    def radian_per_minutes(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.radian_per_minute)
        return cast('VelocityAngular', self.variable)
    @property
    def radian_per_seconds(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.radian_per_second)
        return cast('VelocityAngular', self.variable)
    @property
    def revolution_per_minutes(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.revolution_per_minute)
        return cast('VelocityAngular', self.variable)
    @property
    def revolution_per_seconds(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.revolution_per_second)
        return cast('VelocityAngular', self.variable)
    @property
    def turn_per_minutes(self) -> 'VelocityAngular':
        self.variable.quantity = FastQuantity(self.value, VelocityAngularUnits.turn_per_minute)
        return cast('VelocityAngular', self.variable)
    
    # Short aliases for convenience
    pass


class VelocityAngular(TypedVariable):
    """Type-safe velocity, angular variable with expression capabilities."""
    
    _setter_class = VelocityAngularSetter
    _expected_dimension = ANGULAR_VELOCITY
    _default_unit_property = "radian_per_seconds"
    
    def set(self, value: float) -> VelocityAngularSetter:
        """Create a velocity, angular setter for this variable with proper type annotation."""
        return VelocityAngularSetter(self, value)


class VelocityAngularModule(VariableModule):
    """VelocityAngular variable module definition."""
    
    def get_variable_class(self):
        return VelocityAngular
    
    def get_setter_class(self):
        return VelocityAngularSetter
    
    def get_expected_dimension(self):
        return ANGULAR_VELOCITY


# Register this module for auto-discovery
VARIABLE_MODULE = VelocityAngularModule()