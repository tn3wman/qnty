"""
Temperature Units Module
========================

Complete temperature unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
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

    
    # Common aliases for test compatibility
    pass


class TemperatureUnitModule(UnitModule):
    """Temperature unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all temperature unit definitions."""
        return [
            UnitDefinition("celsius", "°C", DIMENSIONLESS, 1),
            UnitDefinition("fahrenheit", "°F", DIMENSIONLESS, 0.555556),
            UnitDefinition("reaumur", "°Ré", DIMENSIONLESS, 1.25),
            UnitDefinition("kelvin", "K", DIMENSIONLESS, 1),
            UnitDefinition("rankine", "°R", DIMENSIONLESS, 0.555556),

        ]
    
    def get_units_class(self):
        return TemperatureUnits
    


# Register this module for auto-discovery
UNIT_MODULE = TemperatureUnitModule()