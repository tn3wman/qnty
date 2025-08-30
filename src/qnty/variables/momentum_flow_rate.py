"""
MomentumFlowRate Variable Module
=================================

Type-safe momentum flow rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import FORCE
from ..units import MomentumFlowRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MomentumFlowRateSetter(TypeSafeSetter):
    """MomentumFlowRate-specific setter with only momentum flow rate units."""
    
    def __init__(self, variable: 'MomentumFlowRate', value: float):
        super().__init__(variable, value)
    
    # Only momentum flow rate units available - compile-time safe!
    @property
    def foot_pounds_per_square_hours(self) -> 'MomentumFlowRate':
        self.variable.quantity = FastQuantity(self.value, MomentumFlowRateUnits.foot_pounds_per_square_hour)
        return cast('MomentumFlowRate', self.variable)
    @property
    def foot_pounds_per_square_minutes(self) -> 'MomentumFlowRate':
        self.variable.quantity = FastQuantity(self.value, MomentumFlowRateUnits.foot_pounds_per_square_minute)
        return cast('MomentumFlowRate', self.variable)
    @property
    def foot_pounds_per_square_seconds(self) -> 'MomentumFlowRate':
        self.variable.quantity = FastQuantity(self.value, MomentumFlowRateUnits.foot_pounds_per_square_second)
        return cast('MomentumFlowRate', self.variable)
    @property
    def gram_centimeters_per_square_seconds(self) -> 'MomentumFlowRate':
        self.variable.quantity = FastQuantity(self.value, MomentumFlowRateUnits.gram_centimeters_per_square_second)
        return cast('MomentumFlowRate', self.variable)
    @property
    def kilogram_meters_per_square_seconds(self) -> 'MomentumFlowRate':
        self.variable.quantity = FastQuantity(self.value, MomentumFlowRateUnits.kilogram_meters_per_square_second)
        return cast('MomentumFlowRate', self.variable)
    
    # Short aliases for convenience
    pass


class MomentumFlowRate(TypedVariable):
    """Type-safe momentum flow rate variable with expression capabilities."""
    
    _setter_class = MomentumFlowRateSetter
    _expected_dimension = FORCE
    _default_unit_property = "kilogram_meters_per_square_seconds"
    
    def set(self, value: float) -> MomentumFlowRateSetter:
        """Create a momentum flow rate setter for this variable with proper type annotation."""
        return MomentumFlowRateSetter(self, value)


class MomentumFlowRateModule(VariableModule):
    """MomentumFlowRate variable module definition."""
    
    def get_variable_class(self):
        return MomentumFlowRate
    
    def get_setter_class(self):
        return MomentumFlowRateSetter
    
    def get_expected_dimension(self):
        return FORCE


# Register this module for auto-discovery
VARIABLE_MODULE = MomentumFlowRateModule()