"""
SpecificEnthalpy Units Module
=============================

Complete specific enthalpy unit definitions and constants.
"""

from ..dimension import ENERGY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SpecificEnthalpyUnits:
    """Type-safe specific enthalpy unit constants."""
    # Explicit declarations for type checking
    british_thermal_unit_mean_per_pound: 'UnitConstant'
    british_thermal_unit_per_pound: 'UnitConstant'
    calorie_per_gram: 'UnitConstant'
    chu_per_pound: 'UnitConstant'
    joule_per_kilogram: 'UnitConstant'
    kilojoule_per_kilogram: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SpecificEnthalpyUnitModule(UnitModule):
    """SpecificEnthalpy unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all specific enthalpy unit definitions."""
        return [
            UnitDefinition("british_thermal_unit_mean_per_pound", "Btu (mean)/lb", ENERGY, 2327.8),
            UnitDefinition("british_thermal_unit_per_pound", "Btu/lb", ENERGY, 2324.4),
            UnitDefinition("calorie_per_gram", "cal / g", ENERGY, 4186.8),
            UnitDefinition("chu_per_pound", "Chu/lb", ENERGY, 4186.8),
            UnitDefinition("joule_per_kilogram", "J/kg", ENERGY, 1),
            UnitDefinition("kilojoule_per_kilogram", "kJ/kg", ENERGY, 1000),

        ]
    
    def get_units_class(self):
        return SpecificEnthalpyUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SpecificEnthalpyUnitModule()