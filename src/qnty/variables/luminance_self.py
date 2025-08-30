"""
Luminanceself Variable Module
==============================

Type-safe luminance (self) variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import LUMINANCE
from ..units import LuminanceselfUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class LuminanceselfSetter(TypeSafeSetter):
    """Luminanceself-specific setter with only luminance (self) units."""
    
    def __init__(self, variable: 'Luminanceself', value: float):
        super().__init__(variable, value)
    
    # Only luminance (self) units available - compile-time safe!
    @property
    def apostilbs(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.apostilb)
        return cast('Luminanceself', self.variable)
    @property
    def blondels(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.blondel)
        return cast('Luminanceself', self.variable)
    @property
    def candela_per_square_meters(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.candela_per_square_meter)
        return cast('Luminanceself', self.variable)
    @property
    def footlamberts(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.footlambert)
        return cast('Luminanceself', self.variable)
    @property
    def lamberts(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.lambert)
        return cast('Luminanceself', self.variable)
    @property
    def luxons(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.luxon)
        return cast('Luminanceself', self.variable)
    @property
    def nits(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.nit)
        return cast('Luminanceself', self.variable)
    @property
    def stilbs(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.stilb)
        return cast('Luminanceself', self.variable)
    @property
    def trolands(self) -> 'Luminanceself':
        self.variable.quantity = FastQuantity(self.value, LuminanceselfUnits.troland)
        return cast('Luminanceself', self.variable)
    
    # Short aliases for convenience
    pass


class Luminanceself(TypedVariable):
    """Type-safe luminance (self) variable with expression capabilities."""
    
    _setter_class = LuminanceselfSetter
    _expected_dimension = LUMINANCE
    _default_unit_property = "apostilbs"
    
    def set(self, value: float) -> LuminanceselfSetter:
        """Create a luminance (self) setter for this variable with proper type annotation."""
        return LuminanceselfSetter(self, value)


class LuminanceselfModule(VariableModule):
    """Luminanceself variable module definition."""
    
    def get_variable_class(self):
        return Luminanceself
    
    def get_setter_class(self):
        return LuminanceselfSetter
    
    def get_expected_dimension(self):
        return LUMINANCE


# Register this module for auto-discovery
VARIABLE_MODULE = LuminanceselfModule()