"""
LuminousFlux Variable Module
=============================

Type-safe luminous flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import LUMINOSITY
from ..units import LuminousFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class LuminousFluxSetter(TypeSafeSetter):
    """LuminousFlux-specific setter with only luminous flux units."""
    
    def __init__(self, variable: 'LuminousFlux', value: float):
        super().__init__(variable, value)
    
    # Only luminous flux units available - compile-time safe!
    @property
    def candela_steradians(self) -> 'LuminousFlux':
        self.variable.quantity = FastQuantity(self.value, LuminousFluxUnits.candela_steradian)
        return cast('LuminousFlux', self.variable)
    @property
    def lumens(self) -> 'LuminousFlux':
        self.variable.quantity = FastQuantity(self.value, LuminousFluxUnits.lumen)
        return cast('LuminousFlux', self.variable)
    
    # Short aliases for convenience
    pass


class LuminousFlux(TypedVariable):
    """Type-safe luminous flux variable with expression capabilities."""
    
    _setter_class = LuminousFluxSetter
    _expected_dimension = LUMINOSITY
    _default_unit_property = "candela_steradians"
    
    def set(self, value: float) -> LuminousFluxSetter:
        """Create a luminous flux setter for this variable with proper type annotation."""
        return LuminousFluxSetter(self, value)


class LuminousFluxModule(VariableModule):
    """LuminousFlux variable module definition."""
    
    def get_variable_class(self):
        return LuminousFlux
    
    def get_setter_class(self):
        return LuminousFluxSetter
    
    def get_expected_dimension(self):
        return LUMINOSITY


# Register this module for auto-discovery
VARIABLE_MODULE = LuminousFluxModule()