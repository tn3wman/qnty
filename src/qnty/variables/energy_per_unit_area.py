"""
EnergyPerUnitArea Variable Module
==================================

Type-safe energy per unit area variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY_PER_UNIT_AREA
from ..units import EnergyPerUnitAreaUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class EnergyPerUnitAreaSetter(TypeSafeSetter):
    """EnergyPerUnitArea-specific setter with only energy per unit area units."""
    
    def __init__(self, variable: 'EnergyPerUnitArea', value: float):
        super().__init__(variable, value)
    
    # Only energy per unit area units available - compile-time safe!
    @property
    def british_thermal_unit_per_square_foots(self) -> 'EnergyPerUnitArea':
        self.variable.quantity = FastQuantity(self.value, EnergyPerUnitAreaUnits.british_thermal_unit_per_square_foot)
        return cast('EnergyPerUnitArea', self.variable)
    @property
    def joule_per_square_meters(self) -> 'EnergyPerUnitArea':
        self.variable.quantity = FastQuantity(self.value, EnergyPerUnitAreaUnits.joule_per_square_meter)
        return cast('EnergyPerUnitArea', self.variable)
    @property
    def langley(self) -> 'EnergyPerUnitArea':
        self.variable.quantity = FastQuantity(self.value, EnergyPerUnitAreaUnits.langley)
        return cast('EnergyPerUnitArea', self.variable)
    
    # Short aliases for convenience
    pass


class EnergyPerUnitArea(TypedVariable):
    """Type-safe energy per unit area variable with expression capabilities."""
    
    _setter_class = EnergyPerUnitAreaSetter
    _expected_dimension = ENERGY_PER_UNIT_AREA
    _default_unit_property = "joule_per_square_meters"
    
    def set(self, value: float) -> EnergyPerUnitAreaSetter:
        """Create a energy per unit area setter for this variable with proper type annotation."""
        return EnergyPerUnitAreaSetter(self, value)


class EnergyPerUnitAreaModule(VariableModule):
    """EnergyPerUnitArea variable module definition."""
    
    def get_variable_class(self):
        return EnergyPerUnitArea
    
    def get_setter_class(self):
        return EnergyPerUnitAreaSetter
    
    def get_expected_dimension(self):
        return ENERGY_PER_UNIT_AREA


# Register this module for auto-discovery
VARIABLE_MODULE = EnergyPerUnitAreaModule()