"""
PowerPerUnitMassOrSpecificPower Variable Module
================================================

Type-safe power per unit mass or specific power variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER
from ..units import PowerPerUnitMassOrSpecificPowerUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class PowerPerUnitMassOrSpecificPowerSetter(TypeSafeSetter):
    """PowerPerUnitMassOrSpecificPower-specific setter with only power per unit mass or specific power units."""
    
    def __init__(self, variable: 'PowerPerUnitMassOrSpecificPower', value: float):
        super().__init__(variable, value)
    
    # Only power per unit mass or specific power units available - compile-time safe!
    @property
    def british_thermal_unit_per_hour_per_pound_mass(self) -> 'PowerPerUnitMassOrSpecificPower':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitMassOrSpecificPowerUnits.british_thermal_unit_per_hour_per_pound_mass)
        return cast('PowerPerUnitMassOrSpecificPower', self.variable)
    @property
    def calorie_per_second_per_grams(self) -> 'PowerPerUnitMassOrSpecificPower':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitMassOrSpecificPowerUnits.calorie_per_second_per_gram)
        return cast('PowerPerUnitMassOrSpecificPower', self.variable)
    @property
    def kilocalorie_per_hour_per_kilograms(self) -> 'PowerPerUnitMassOrSpecificPower':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitMassOrSpecificPowerUnits.kilocalorie_per_hour_per_kilogram)
        return cast('PowerPerUnitMassOrSpecificPower', self.variable)
    @property
    def watt_per_kilograms(self) -> 'PowerPerUnitMassOrSpecificPower':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitMassOrSpecificPowerUnits.watt_per_kilogram)
        return cast('PowerPerUnitMassOrSpecificPower', self.variable)
    
    # Short aliases for convenience
    pass


class PowerPerUnitMassOrSpecificPower(TypedVariable):
    """Type-safe power per unit mass or specific power variable with expression capabilities."""
    
    _setter_class = PowerPerUnitMassOrSpecificPowerSetter
    _expected_dimension = POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER
    _default_unit_property = "british_thermal_unit_per_hour_per_pound_masss"
    
    def set(self, value: float) -> PowerPerUnitMassOrSpecificPowerSetter:
        """Create a power per unit mass or specific power setter for this variable with proper type annotation."""
        return PowerPerUnitMassOrSpecificPowerSetter(self, value)


class PowerPerUnitMassOrSpecificPowerModule(VariableModule):
    """PowerPerUnitMassOrSpecificPower variable module definition."""
    
    def get_variable_class(self):
        return PowerPerUnitMassOrSpecificPower
    
    def get_setter_class(self):
        return PowerPerUnitMassOrSpecificPowerSetter
    
    def get_expected_dimension(self):
        return POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER


# Register this module for auto-discovery
VARIABLE_MODULE = PowerPerUnitMassOrSpecificPowerModule()