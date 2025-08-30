"""
DynamicFluidity Variable Module
================================

Type-safe dynamic fluidity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DYNAMIC_FLUIDITY
from ..units import DynamicFluidityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class DynamicFluiditySetter(TypeSafeSetter):
    """DynamicFluidity-specific setter with only dynamic fluidity units."""
    
    def __init__(self, variable: 'DynamicFluidity', value: float):
        super().__init__(variable, value)
    
    # Only dynamic fluidity units available - compile-time safe!
    @property
    def rhes(self) -> 'DynamicFluidity':
        self.variable.quantity = FastQuantity(self.value, DynamicFluidityUnits.rhe)
        return cast('DynamicFluidity', self.variable)
    @property
    def square_foot_per_pound_seconds(self) -> 'DynamicFluidity':
        self.variable.quantity = FastQuantity(self.value, DynamicFluidityUnits.square_foot_per_pound_second)
        return cast('DynamicFluidity', self.variable)
    @property
    def square_meters_per_newton_per_seconds(self) -> 'DynamicFluidity':
        self.variable.quantity = FastQuantity(self.value, DynamicFluidityUnits.square_meters_per_newton_per_second)
        return cast('DynamicFluidity', self.variable)
    
    # Short aliases for convenience
    pass


class DynamicFluidity(TypedVariable):
    """Type-safe dynamic fluidity variable with expression capabilities."""
    
    _setter_class = DynamicFluiditySetter
    _expected_dimension = DYNAMIC_FLUIDITY
    _default_unit_property = "rhes"
    
    def set(self, value: float) -> DynamicFluiditySetter:
        """Create a dynamic fluidity setter for this variable with proper type annotation."""
        return DynamicFluiditySetter(self, value)


class DynamicFluidityModule(VariableModule):
    """DynamicFluidity variable module definition."""
    
    def get_variable_class(self):
        return DynamicFluidity
    
    def get_setter_class(self):
        return DynamicFluiditySetter
    
    def get_expected_dimension(self):
        return DYNAMIC_FLUIDITY


# Register this module for auto-discovery
VARIABLE_MODULE = DynamicFluidityModule()