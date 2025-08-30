"""
Wavenumber Variable Module
===========================

Type-safe wavenumber variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import WAVENUMBER
from ..units import WavenumberUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class WavenumberSetter(TypeSafeSetter):
    """Wavenumber-specific setter with only wavenumber units."""
    
    def __init__(self, variable: 'Wavenumber', value: float):
        super().__init__(variable, value)
    
    # Only wavenumber units available - compile-time safe!
    @property
    def diopters(self) -> 'Wavenumber':
        self.variable.quantity = FastQuantity(self.value, WavenumberUnits.diopter)
        return cast('Wavenumber', self.variable)
    @property
    def kaysers(self) -> 'Wavenumber':
        self.variable.quantity = FastQuantity(self.value, WavenumberUnits.kayser)
        return cast('Wavenumber', self.variable)
    @property
    def reciprocal_meters(self) -> 'Wavenumber':
        self.variable.quantity = FastQuantity(self.value, WavenumberUnits.reciprocal_meter)
        return cast('Wavenumber', self.variable)
    
    # Short aliases for convenience
    pass


class Wavenumber(TypedVariable):
    """Type-safe wavenumber variable with expression capabilities."""
    
    _setter_class = WavenumberSetter
    _expected_dimension = WAVENUMBER
    _default_unit_property = "diopters"
    
    def set(self, value: float) -> WavenumberSetter:
        """Create a wavenumber setter for this variable with proper type annotation."""
        return WavenumberSetter(self, value)


class WavenumberModule(VariableModule):
    """Wavenumber variable module definition."""
    
    def get_variable_class(self):
        return Wavenumber
    
    def get_setter_class(self):
        return WavenumberSetter
    
    def get_expected_dimension(self):
        return WAVENUMBER


# Register this module for auto-discovery
VARIABLE_MODULE = WavenumberModule()