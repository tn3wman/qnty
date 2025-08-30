"""
VelocityLinear Variable Module
===============================

Type-safe velocity, linear variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import VELOCITY
from ..units import VelocityLinearUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VelocityLinearSetter(TypeSafeSetter):
    """VelocityLinear-specific setter with only velocity, linear units."""
    
    def __init__(self, variable: 'VelocityLinear', value: float):
        super().__init__(variable, value)
    
    # Only velocity, linear units available - compile-time safe!
    @property
    def foot_per_hours(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.foot_per_hour)
        return cast('VelocityLinear', self.variable)
    @property
    def foot_per_minutes(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.foot_per_minute)
        return cast('VelocityLinear', self.variable)
    @property
    def foot_per_seconds(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.foot_per_second)
        return cast('VelocityLinear', self.variable)
    @property
    def inch_per_seconds(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.inch_per_second)
        return cast('VelocityLinear', self.variable)
    @property
    def international_knots(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.international_knot)
        return cast('VelocityLinear', self.variable)
    @property
    def kilometer_per_hours(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.kilometer_per_hour)
        return cast('VelocityLinear', self.variable)
    @property
    def kilometer_per_seconds(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.kilometer_per_second)
        return cast('VelocityLinear', self.variable)
    @property
    def meter_per_seconds(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.meter_per_second)
        return cast('VelocityLinear', self.variable)
    @property
    def mile_per_hours(self) -> 'VelocityLinear':
        self.variable.quantity = FastQuantity(self.value, VelocityLinearUnits.mile_per_hour)
        return cast('VelocityLinear', self.variable)
    
    # Short aliases for convenience
    pass


class VelocityLinear(TypedVariable):
    """Type-safe velocity, linear variable with expression capabilities."""
    
    _setter_class = VelocityLinearSetter
    _expected_dimension = VELOCITY
    _default_unit_property = "meter_per_seconds"
    
    def set(self, value: float) -> VelocityLinearSetter:
        """Create a velocity, linear setter for this variable with proper type annotation."""
        return VelocityLinearSetter(self, value)


class VelocityLinearModule(VariableModule):
    """VelocityLinear variable module definition."""
    
    def get_variable_class(self):
        return VelocityLinear
    
    def get_setter_class(self):
        return VelocityLinearSetter
    
    def get_expected_dimension(self):
        return VELOCITY


# Register this module for auto-discovery
VARIABLE_MODULE = VelocityLinearModule()