"""
LinearMomentum Variable Module
===============================

Type-safe linear momentum variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import LINEAR_MOMENTUM
from ..units import LinearMomentumUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class LinearMomentumSetter(TypeSafeSetter):
    """LinearMomentum-specific setter with only linear momentum units."""
    
    def __init__(self, variable: 'LinearMomentum', value: float):
        super().__init__(variable, value)
    
    # Only linear momentum units available - compile-time safe!
    @property
    def foot_pounds_force_per_hours(self) -> 'LinearMomentum':
        self.variable.quantity = FastQuantity(self.value, LinearMomentumUnits.foot_pounds_force_per_hour)
        return cast('LinearMomentum', self.variable)
    @property
    def foot_pounds_force_per_minutes(self) -> 'LinearMomentum':
        self.variable.quantity = FastQuantity(self.value, LinearMomentumUnits.foot_pounds_force_per_minute)
        return cast('LinearMomentum', self.variable)
    @property
    def foot_pounds_force_per_seconds(self) -> 'LinearMomentum':
        self.variable.quantity = FastQuantity(self.value, LinearMomentumUnits.foot_pounds_force_per_second)
        return cast('LinearMomentum', self.variable)
    @property
    def gram_centimeters_per_seconds(self) -> 'LinearMomentum':
        self.variable.quantity = FastQuantity(self.value, LinearMomentumUnits.gram_centimeters_per_second)
        return cast('LinearMomentum', self.variable)
    @property
    def kilogram_meters_per_seconds(self) -> 'LinearMomentum':
        self.variable.quantity = FastQuantity(self.value, LinearMomentumUnits.kilogram_meters_per_second)
        return cast('LinearMomentum', self.variable)
    
    # Short aliases for convenience
    pass


class LinearMomentum(TypedVariable):
    """Type-safe linear momentum variable with expression capabilities."""
    
    _setter_class = LinearMomentumSetter
    _expected_dimension = LINEAR_MOMENTUM
    _default_unit_property = "kilogram_meters_per_seconds"
    
    def set(self, value: float) -> LinearMomentumSetter:
        """Create a linear momentum setter for this variable with proper type annotation."""
        return LinearMomentumSetter(self, value)


class LinearMomentumModule(VariableModule):
    """LinearMomentum variable module definition."""
    
    def get_variable_class(self):
        return LinearMomentum
    
    def get_setter_class(self):
        return LinearMomentumSetter
    
    def get_expected_dimension(self):
        return LINEAR_MOMENTUM


# Register this module for auto-discovery
VARIABLE_MODULE = LinearMomentumModule()