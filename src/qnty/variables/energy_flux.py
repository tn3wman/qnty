"""
EnergyFlux Variable Module
===========================

Type-safe energy flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY_FLUX
from ..units import EnergyFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class EnergyFluxSetter(TypeSafeSetter):
    """EnergyFlux-specific setter with only energy flux units."""
    
    def __init__(self, variable: 'EnergyFlux', value: float):
        super().__init__(variable, value)
    
    # Only energy flux units available - compile-time safe!
    @property
    def btu_per_square_foot_per_hours(self) -> 'EnergyFlux':
        self.variable.quantity = FastQuantity(self.value, EnergyFluxUnits.btu_per_square_foot_per_hour)
        return cast('EnergyFlux', self.variable)
    @property
    def calorie_per_square_centimeter_per_seconds(self) -> 'EnergyFlux':
        self.variable.quantity = FastQuantity(self.value, EnergyFluxUnits.calorie_per_square_centimeter_per_second)
        return cast('EnergyFlux', self.variable)
    @property
    def celsius(self) -> 'EnergyFlux':
        self.variable.quantity = FastQuantity(self.value, EnergyFluxUnits.celsius)
        return cast('EnergyFlux', self.variable)
    @property
    def kilocalorie_per_square_foot_per_hours(self) -> 'EnergyFlux':
        self.variable.quantity = FastQuantity(self.value, EnergyFluxUnits.kilocalorie_per_square_foot_per_hour)
        return cast('EnergyFlux', self.variable)
    @property
    def kilocalorie_per_square_meter_per_hours(self) -> 'EnergyFlux':
        self.variable.quantity = FastQuantity(self.value, EnergyFluxUnits.kilocalorie_per_square_meter_per_hour)
        return cast('EnergyFlux', self.variable)
    @property
    def watt_per_square_meters(self) -> 'EnergyFlux':
        self.variable.quantity = FastQuantity(self.value, EnergyFluxUnits.watt_per_square_meter)
        return cast('EnergyFlux', self.variable)
    
    # Short aliases for convenience
    pass


class EnergyFlux(TypedVariable):
    """Type-safe energy flux variable with expression capabilities."""
    
    _setter_class = EnergyFluxSetter
    _expected_dimension = ENERGY_FLUX
    _default_unit_property = "watt_per_square_meters"
    
    def set(self, value: float) -> EnergyFluxSetter:
        """Create a energy flux setter for this variable with proper type annotation."""
        return EnergyFluxSetter(self, value)


class EnergyFluxModule(VariableModule):
    """EnergyFlux variable module definition."""
    
    def get_variable_class(self):
        return EnergyFlux
    
    def get_setter_class(self):
        return EnergyFluxSetter
    
    def get_expected_dimension(self):
        return ENERGY_FLUX


# Register this module for auto-discovery
VARIABLE_MODULE = EnergyFluxModule()