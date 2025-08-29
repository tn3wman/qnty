"""
Temperature Units Module
========================

Complete temperature unit definitions and constants.
"""

from ..dimension import TEMPERATURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class TemperatureUnits:
    """Type-safe temperature unit constants."""
    # Explicit declarations for type checking
    celsius: 'UnitConstant'
    fahrenheit: 'UnitConstant'
    reaumur: 'UnitConstant'
    kelvin: 'UnitConstant'
    rankine: 'UnitConstant'
    
    # Common aliases
    K: 'UnitConstant'


class TemperatureUnitModule(UnitModule):
    """Temperature unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all temperature unit definitions."""
        return [
            UnitDefinition("celsius", "mathrmCcirc", TEMPERATURE, 1),
            UnitDefinition("fahrenheit", "mathrmFcirc", TEMPERATURE, 0.555556),
            UnitDefinition("reaumur", "Récirc", TEMPERATURE, 1.25),
            UnitDefinition("kelvin", "K", TEMPERATURE, 1),
            UnitDefinition("rankine", "circmathrmR", TEMPERATURE, 0.555556),
        ]
    
    def get_units_class(self):
        return TemperatureUnits


# Register this module for auto-discovery
UNIT_MODULE = TemperatureUnitModule()