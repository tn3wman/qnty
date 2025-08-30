"""
Temperature Variable Module
============================

Type-safe temperature variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import TemperatureUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class TemperatureSetter(TypeSafeSetter):
    """Temperature-specific setter with only temperature units."""
    
    def __init__(self, variable: 'Temperature', value: float):
        super().__init__(variable, value)
    
    # Only temperature units available - compile-time safe!
    @property
    def celsius(self) -> 'Temperature':
        self.variable.quantity = FastQuantity(self.value, TemperatureUnits.celsius)
        return cast('Temperature', self.variable)
    @property
    def fahrenheits(self) -> 'Temperature':
        self.variable.quantity = FastQuantity(self.value, TemperatureUnits.fahrenheit)
        return cast('Temperature', self.variable)
    @property
    def reaumurs(self) -> 'Temperature':
        self.variable.quantity = FastQuantity(self.value, TemperatureUnits.reaumur)
        return cast('Temperature', self.variable)
    @property
    def kelvins(self) -> 'Temperature':
        self.variable.quantity = FastQuantity(self.value, TemperatureUnits.kelvin)
        return cast('Temperature', self.variable)
    @property
    def rankines(self) -> 'Temperature':
        self.variable.quantity = FastQuantity(self.value, TemperatureUnits.rankine)
        return cast('Temperature', self.variable)
    
    # Short aliases for convenience
    pass


class Temperature(TypedVariable):
    """Type-safe temperature variable with expression capabilities."""
    
    _setter_class = TemperatureSetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "kelvins"
    
    def set(self, value: float) -> TemperatureSetter:
        """Create a temperature setter for this variable with proper type annotation."""
        return TemperatureSetter(self, value)


class TemperatureModule(VariableModule):
    """Temperature variable module definition."""
    
    def get_variable_class(self):
        return Temperature
    
    def get_setter_class(self):
        return TemperatureSetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = TemperatureModule()