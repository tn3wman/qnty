"""
HeatOfVaporization Units Module
===============================

Complete heat of vaporization unit definitions and constants.
"""

from ..dimension import ENERGY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class HeatOfVaporizationUnits:
    """Type-safe heat of vaporization unit constants."""
    # Explicit declarations for type checking
    british_thermal_unit_per_pound: 'UnitConstant'
    calorie_per_gram: 'UnitConstant'
    chu_per_pound: 'UnitConstant'
    joule_per_kilogram: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class HeatOfVaporizationUnitModule(UnitModule):
    """HeatOfVaporization unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all heat of vaporization unit definitions."""
        return [
            UnitDefinition("british_thermal_unit_per_pound", "Btu/lb", ENERGY, 2326),
            UnitDefinition("calorie_per_gram", "cal / g", ENERGY, 4186),
            UnitDefinition("chu_per_pound", "Chu/lb", ENERGY, 4186.8),
            UnitDefinition("joule_per_kilogram", "J/kg", ENERGY, 1),

        ]
    
    def get_units_class(self):
        return HeatOfVaporizationUnits
    


# Register this module for auto-discovery
UNIT_MODULE = HeatOfVaporizationUnitModule()