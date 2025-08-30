"""
Concentration Variable Module
==============================

Type-safe concentration variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import CONCENTRATION
from ..units import ConcentrationUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ConcentrationSetter(TypeSafeSetter):
    """Concentration-specific setter with only concentration units."""
    
    def __init__(self, variable: 'Concentration', value: float):
        super().__init__(variable, value)
    
    # Only concentration units available - compile-time safe!
    @property
    def grains_of_i_per_cubic_foots(self) -> 'Concentration':
        self.variable.quantity = FastQuantity(self.value, ConcentrationUnits.grains_of_i_per_cubic_foot)
        return cast('Concentration', self.variable)
    @property
    def grains_of_i_per_gallon_us(self) -> 'Concentration':
        self.variable.quantity = FastQuantity(self.value, ConcentrationUnits.grains_of_i_per_gallon_us)
        return cast('Concentration', self.variable)
    
    # Short aliases for convenience
    pass


class Concentration(TypedVariable):
    """Type-safe concentration variable with expression capabilities."""
    
    _setter_class = ConcentrationSetter
    _expected_dimension = CONCENTRATION
    _default_unit_property = "grains_of_i_per_cubic_foots"
    
    def set(self, value: float) -> ConcentrationSetter:
        """Create a concentration setter for this variable with proper type annotation."""
        return ConcentrationSetter(self, value)


class ConcentrationModule(VariableModule):
    """Concentration variable module definition."""
    
    def get_variable_class(self):
        return Concentration
    
    def get_setter_class(self):
        return ConcentrationSetter
    
    def get_expected_dimension(self):
        return CONCENTRATION


# Register this module for auto-discovery
VARIABLE_MODULE = ConcentrationModule()