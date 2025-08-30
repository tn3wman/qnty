"""
AngularMomentum Variable Module
================================

Type-safe angular momentum variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ANGULAR_MOMENTUM
from ..units import AngularMomentumUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AngularMomentumSetter(TypeSafeSetter):
    """AngularMomentum-specific setter with only angular momentum units."""
    
    def __init__(self, variable: 'AngularMomentum', value: float):
        super().__init__(variable, value)
    
    # Only angular momentum units available - compile-time safe!
    @property
    def gram_centimeter_squared_per_seconds(self) -> 'AngularMomentum':
        self.variable.quantity = FastQuantity(self.value, AngularMomentumUnits.gram_centimeter_squared_per_second)
        return cast('AngularMomentum', self.variable)
    @property
    def kilogram_meter_squared_per_seconds(self) -> 'AngularMomentum':
        self.variable.quantity = FastQuantity(self.value, AngularMomentumUnits.kilogram_meter_squared_per_second)
        return cast('AngularMomentum', self.variable)
    @property
    def pound_force_square_foot_per_seconds(self) -> 'AngularMomentum':
        self.variable.quantity = FastQuantity(self.value, AngularMomentumUnits.pound_force_square_foot_per_second)
        return cast('AngularMomentum', self.variable)
    
    # Short aliases for convenience
    pass


class AngularMomentum(TypedVariable):
    """Type-safe angular momentum variable with expression capabilities."""
    
    _setter_class = AngularMomentumSetter
    _expected_dimension = ANGULAR_MOMENTUM
    _default_unit_property = "kilogram_meter_squared_per_seconds"
    
    def set(self, value: float) -> AngularMomentumSetter:
        """Create a angular momentum setter for this variable with proper type annotation."""
        return AngularMomentumSetter(self, value)


class AngularMomentumModule(VariableModule):
    """AngularMomentum variable module definition."""
    
    def get_variable_class(self):
        return AngularMomentum
    
    def get_setter_class(self):
        return AngularMomentumSetter
    
    def get_expected_dimension(self):
        return ANGULAR_MOMENTUM


# Register this module for auto-discovery
VARIABLE_MODULE = AngularMomentumModule()