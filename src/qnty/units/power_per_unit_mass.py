"""
PowerPerUnitMassOrSpecificPower Units Module
============================================

Complete power per unit mass or specific power unit definitions and constants.
"""

from ..dimension import POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class PowerPerUnitMassOrSpecificPowerUnits:
    """Type-safe power per unit mass or specific power unit constants."""
    # Explicit declarations for type checking
    british_thermal_unit_per_hour_per_pound_mass: 'UnitConstant'
    calorie_per_second_per_gram: 'UnitConstant'
    kilocalorie_per_hour_per_kilogram: 'UnitConstant'
    watt_per_kilogram: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class PowerPerUnitMassOrSpecificPowerUnitModule(UnitModule):
    """PowerPerUnitMassOrSpecificPower unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all power per unit mass or specific power unit definitions."""
        return [
            UnitDefinition("british_thermal_unit_per_hour_per_pound_mass", "Btu/h/lb or Btu/ (lb hr)", POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER, 0.64612),
            UnitDefinition("calorie_per_second_per_gram", "cal/s/g or cal/(g sec)", POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER, 4186.8),
            UnitDefinition("kilocalorie_per_hour_per_kilogram", "kcal/h/kg or kcal/ (kg hr)", POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER, 1.163),
            UnitDefinition("watt_per_kilogram", "W/kg", POWER_PER_UNIT_MASS_OR_SPECIFIC_POWER, 1),

        ]
    
    def get_units_class(self):
        return PowerPerUnitMassOrSpecificPowerUnits
    


# Register this module for auto-discovery
UNIT_MODULE = PowerPerUnitMassOrSpecificPowerUnitModule()