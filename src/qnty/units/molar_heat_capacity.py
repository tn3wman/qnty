"""
MolarHeatCapacity Units Module
==============================

Complete molar heat capacity unit definitions and constants.
"""

from ..dimension import MOLAR_HEAT_CAPACITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MolarHeatCapacityUnits:
    """Type-safe molar heat capacity unit constants."""
    # Explicit declarations for type checking
    fahrenheit: 'UnitConstant'
    celsius: 'UnitConstant'
    celsius: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MolarHeatCapacityUnitModule(UnitModule):
    """MolarHeatCapacity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all molar heat capacity unit definitions."""
        return [
            UnitDefinition("fahrenheit", "°F", MOLAR_HEAT_CAPACITY, 4.1868),
            UnitDefinition("celsius", "°C", MOLAR_HEAT_CAPACITY, 4.1868),
            UnitDefinition("celsius", "°C", MOLAR_HEAT_CAPACITY, 1),

        ]
    
    def get_units_class(self):
        return MolarHeatCapacityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MolarHeatCapacityUnitModule()