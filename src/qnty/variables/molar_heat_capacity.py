"""
MolarHeatCapacity Variable Module
==================================

Type-safe molar heat capacity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MOLAR_HEAT_CAPACITY
from ..units import MolarHeatCapacityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MolarHeatCapacitySetter(TypeSafeSetter):
    """MolarHeatCapacity-specific setter with only molar heat capacity units."""
    
    def __init__(self, variable: 'MolarHeatCapacity', value: float):
        super().__init__(variable, value)
    
    # Only molar heat capacity units available - compile-time safe!
    @property
    def fahrenheits(self) -> 'MolarHeatCapacity':
        self.variable.quantity = FastQuantity(self.value, MolarHeatCapacityUnits.fahrenheit)
        return cast('MolarHeatCapacity', self.variable)
    @property
    def celsius(self) -> 'MolarHeatCapacity':
        self.variable.quantity = FastQuantity(self.value, MolarHeatCapacityUnits.celsius)
        return cast('MolarHeatCapacity', self.variable)
    @property
    def celsius(self) -> 'MolarHeatCapacity':
        self.variable.quantity = FastQuantity(self.value, MolarHeatCapacityUnits.celsius)
        return cast('MolarHeatCapacity', self.variable)
    
    # Short aliases for convenience
    pass


class MolarHeatCapacity(TypedVariable):
    """Type-safe molar heat capacity variable with expression capabilities."""
    
    _setter_class = MolarHeatCapacitySetter
    _expected_dimension = MOLAR_HEAT_CAPACITY
    _default_unit_property = "fahrenheits"
    
    def set(self, value: float) -> MolarHeatCapacitySetter:
        """Create a molar heat capacity setter for this variable with proper type annotation."""
        return MolarHeatCapacitySetter(self, value)


class MolarHeatCapacityModule(VariableModule):
    """MolarHeatCapacity variable module definition."""
    
    def get_variable_class(self):
        return MolarHeatCapacity
    
    def get_setter_class(self):
        return MolarHeatCapacitySetter
    
    def get_expected_dimension(self):
        return MOLAR_HEAT_CAPACITY


# Register this module for auto-discovery
VARIABLE_MODULE = MolarHeatCapacityModule()