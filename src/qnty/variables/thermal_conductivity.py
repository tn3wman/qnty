"""
ThermalConductivity Variable Module
====================================

Type-safe thermal conductivity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import THERMAL_CONDUCTIVITY
from ..units import ThermalConductivityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ThermalConductivitySetter(TypeSafeSetter):
    """ThermalConductivity-specific setter with only thermal conductivity units."""
    
    def __init__(self, variable: 'ThermalConductivity', value: float):
        super().__init__(variable, value)
    
    # Only thermal conductivity units available - compile-time safe!
    @property
    def fahrenheits(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.fahrenheit)
        return cast('ThermalConductivity', self.variable)
    @property
    def fahrenheits(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.fahrenheit)
        return cast('ThermalConductivity', self.variable)
    @property
    def fahrenheits(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.fahrenheit)
        return cast('ThermalConductivity', self.variable)
    @property
    def celsius(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.celsius)
        return cast('ThermalConductivity', self.variable)
    @property
    def kelvins(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.kelvin)
        return cast('ThermalConductivity', self.variable)
    @property
    def kelvins(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.kelvin)
        return cast('ThermalConductivity', self.variable)
    @property
    def kelvins(self) -> 'ThermalConductivity':
        self.variable.quantity = FastQuantity(self.value, ThermalConductivityUnits.kelvin)
        return cast('ThermalConductivity', self.variable)
    
    # Short aliases for convenience
    pass


class ThermalConductivity(TypedVariable):
    """Type-safe thermal conductivity variable with expression capabilities."""
    
    _setter_class = ThermalConductivitySetter
    _expected_dimension = THERMAL_CONDUCTIVITY
    _default_unit_property = "kelvins"
    
    def set(self, value: float) -> ThermalConductivitySetter:
        """Create a thermal conductivity setter for this variable with proper type annotation."""
        return ThermalConductivitySetter(self, value)


class ThermalConductivityModule(VariableModule):
    """ThermalConductivity variable module definition."""
    
    def get_variable_class(self):
        return ThermalConductivity
    
    def get_setter_class(self):
        return ThermalConductivitySetter
    
    def get_expected_dimension(self):
        return THERMAL_CONDUCTIVITY


# Register this module for auto-discovery
VARIABLE_MODULE = ThermalConductivityModule()