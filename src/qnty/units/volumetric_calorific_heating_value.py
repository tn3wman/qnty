"""
VolumetricCalorificheatingValue Units Module
============================================

Complete volumetric calorific (heating) value unit definitions and constants.
"""

from ..dimension import PRESSURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumetricCalorificheatingValueUnits:
    """Type-safe volumetric calorific (heating) value unit constants."""
    # Explicit declarations for type checking
    british_thermal_unit_per_cubic_foot: 'UnitConstant'
    british_thermal_unit_per_gallon_uk: 'UnitConstant'
    british_thermal_unit_per_gallon_us: 'UnitConstant'
    calorie_per_cubic_centimeter: 'UnitConstant'
    chu_per_cubic_foot: 'UnitConstant'
    joule_per_cubic_meter: 'UnitConstant'
    kilocalorie_per_cubic_foot: 'UnitConstant'
    kilocalorie_per_cubic_meter: 'UnitConstant'
    therm_100_k_btu_per_cubic_foot: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumetricCalorificheatingValueUnitModule(UnitModule):
    """VolumetricCalorificheatingValue unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volumetric calorific (heating) value unit definitions."""
        return [
            UnitDefinition("british_thermal_unit_per_cubic_foot", "Btu / ft3 or Btu/cft", PRESSURE, 37260),
            UnitDefinition("british_thermal_unit_per_gallon_uk", "Btu/gal (UK)", PRESSURE, 2.3209e+05),
            UnitDefinition("british_thermal_unit_per_gallon_us", "Btu/gal (US)", PRESSURE, 1.9326e+05),
            UnitDefinition("calorie_per_cubic_centimeter", "cal / cm3 or cal / cc", PRESSURE, 4.1868e+06),
            UnitDefinition("chu_per_cubic_foot", "Chu / ft3 or Chu / cft", PRESSURE, 67067),
            UnitDefinition("joule_per_cubic_meter", "J / m3", PRESSURE, 1),
            UnitDefinition("kilocalorie_per_cubic_foot", "kcal / ft3 or kcal / cft", PRESSURE, 1.4786e+05),
            UnitDefinition("kilocalorie_per_cubic_meter", "kcal / m3", PRESSURE, 4186.8),
            UnitDefinition("therm_100_k_btu_per_cubic_foot", "thm/cft", PRESSURE, 3.7260e+09),

        ]
    
    def get_units_class(self):
        return VolumetricCalorificheatingValueUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumetricCalorificheatingValueUnitModule()