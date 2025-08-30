"""
LuminousIntensity Units Module
==============================

Complete luminous intensity unit definitions and constants.
"""

from ..dimension import LUMINOSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class LuminousIntensityUnits:
    """Type-safe luminous intensity unit constants."""
    # Explicit declarations for type checking
    candela: 'UnitConstant'
    candle_international: 'UnitConstant'
    carcel: 'UnitConstant'
    hefner_unit: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class LuminousIntensityUnitModule(UnitModule):
    """LuminousIntensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all luminous intensity unit definitions."""
        return [
            UnitDefinition("candela", "cd", LUMINOSITY, 1),
            UnitDefinition("candle_international", "Cd (int)", LUMINOSITY, 1.01937),
            UnitDefinition("carcel", "carcel", LUMINOSITY, 10),
            UnitDefinition("hefner_unit", "HK", LUMINOSITY, 0.903),

        ]
    
    def get_units_class(self):
        return LuminousIntensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = LuminousIntensityUnitModule()