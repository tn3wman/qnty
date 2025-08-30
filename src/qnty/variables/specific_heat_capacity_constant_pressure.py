"""
SpecificHeatCapacityconstantPressure Variable Module
=====================================================

Type-safe specific heat capacity (constant pressure) variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE
from ..units import SpecificHeatCapacityconstantPressureUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SpecificHeatCapacityconstantPressureSetter(TypeSafeSetter):
    """SpecificHeatCapacityconstantPressure-specific setter with only specific heat capacity (constant pressure) units."""
    
    def __init__(self, variable: 'SpecificHeatCapacityconstantPressure', value: float):
        super().__init__(variable, value)
    
    # Only specific heat capacity (constant pressure) units available - compile-time safe!
    @property
    def fahrenheits(self) -> 'SpecificHeatCapacityconstantPressure':
        self.variable.quantity = FastQuantity(self.value, SpecificHeatCapacityconstantPressureUnits.fahrenheit)
        return cast('SpecificHeatCapacityconstantPressure', self.variable)
    @property
    def celsius(self) -> 'SpecificHeatCapacityconstantPressure':
        self.variable.quantity = FastQuantity(self.value, SpecificHeatCapacityconstantPressureUnits.celsius)
        return cast('SpecificHeatCapacityconstantPressure', self.variable)
    @property
    def celsius(self) -> 'SpecificHeatCapacityconstantPressure':
        self.variable.quantity = FastQuantity(self.value, SpecificHeatCapacityconstantPressureUnits.celsius)
        return cast('SpecificHeatCapacityconstantPressure', self.variable)
    
    # Short aliases for convenience
    @property
    def kPa(self) -> 'SpecificHeatCapacityconstantPressure':
        """Kilopascal alias."""
        self.variable.quantity = FastQuantity(self.value, SpecificHeatCapacityconstantPressureUnits.kPa)
        return cast('SpecificHeatCapacityconstantPressure', self.variable)


class SpecificHeatCapacityconstantPressure(TypedVariable):
    """Type-safe specific heat capacity (constant pressure) variable with expression capabilities."""
    
    _setter_class = SpecificHeatCapacityconstantPressureSetter
    _expected_dimension = SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE
    _default_unit_property = "fahrenheits"
    
    def set(self, value: float) -> SpecificHeatCapacityconstantPressureSetter:
        """Create a specific heat capacity (constant pressure) setter for this variable with proper type annotation."""
        return SpecificHeatCapacityconstantPressureSetter(self, value)


class SpecificHeatCapacityconstantPressureModule(VariableModule):
    """SpecificHeatCapacityconstantPressure variable module definition."""
    
    def get_variable_class(self):
        return SpecificHeatCapacityconstantPressure
    
    def get_setter_class(self):
        return SpecificHeatCapacityconstantPressureSetter
    
    def get_expected_dimension(self):
        return SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE


# Register this module for auto-discovery
VARIABLE_MODULE = SpecificHeatCapacityconstantPressureModule()