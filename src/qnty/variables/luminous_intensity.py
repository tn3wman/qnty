"""
LuminousIntensity Variable Module
==================================

Type-safe luminous intensity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import LUMINOSITY
from ..units import LuminousIntensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class LuminousIntensitySetter(TypeSafeSetter):
    """LuminousIntensity-specific setter with only luminous intensity units."""
    
    def __init__(self, variable: 'LuminousIntensity', value: float):
        super().__init__(variable, value)
    
    # Only luminous intensity units available - compile-time safe!
    @property
    def candelas(self) -> 'LuminousIntensity':
        self.variable.quantity = FastQuantity(self.value, LuminousIntensityUnits.candela)
        return cast('LuminousIntensity', self.variable)
    @property
    def candle_internationals(self) -> 'LuminousIntensity':
        self.variable.quantity = FastQuantity(self.value, LuminousIntensityUnits.candle_international)
        return cast('LuminousIntensity', self.variable)
    @property
    def carcels(self) -> 'LuminousIntensity':
        self.variable.quantity = FastQuantity(self.value, LuminousIntensityUnits.carcel)
        return cast('LuminousIntensity', self.variable)
    @property
    def hefner_units(self) -> 'LuminousIntensity':
        self.variable.quantity = FastQuantity(self.value, LuminousIntensityUnits.hefner_unit)
        return cast('LuminousIntensity', self.variable)
    
    # Short aliases for convenience
    pass


class LuminousIntensity(TypedVariable):
    """Type-safe luminous intensity variable with expression capabilities."""
    
    _setter_class = LuminousIntensitySetter
    _expected_dimension = LUMINOSITY
    _default_unit_property = "candelas"
    
    def set(self, value: float) -> LuminousIntensitySetter:
        """Create a luminous intensity setter for this variable with proper type annotation."""
        return LuminousIntensitySetter(self, value)


class LuminousIntensityModule(VariableModule):
    """LuminousIntensity variable module definition."""
    
    def get_variable_class(self):
        return LuminousIntensity
    
    def get_setter_class(self):
        return LuminousIntensitySetter
    
    def get_expected_dimension(self):
        return LUMINOSITY


# Register this module for auto-discovery
VARIABLE_MODULE = LuminousIntensityModule()