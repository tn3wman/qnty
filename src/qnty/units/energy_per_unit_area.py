"""
EnergyPerUnitArea Units Module
==============================

Complete energy per unit area unit definitions and constants.
"""

from ..dimension import ENERGY_PER_UNIT_AREA
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class EnergyPerUnitAreaUnits:
    """Type-safe energy per unit area unit constants."""
    # Explicit declarations for type checking
    british_thermal_unit_per_square_foot: 'UnitConstant'
    joule_per_square_meter: 'UnitConstant'
    langley: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class EnergyPerUnitAreaUnitModule(UnitModule):
    """EnergyPerUnitArea unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all energy per unit area unit definitions."""
        return [
            UnitDefinition("british_thermal_unit_per_square_foot", "Btu / ft2 or Btu/sq ft", ENERGY_PER_UNIT_AREA, 11354),
            UnitDefinition("joule_per_square_meter", "J / m2", ENERGY_PER_UNIT_AREA, 1),
            UnitDefinition("langley", "Ly", ENERGY_PER_UNIT_AREA, 41840),

        ]
    
    def get_units_class(self):
        return EnergyPerUnitAreaUnits
    


# Register this module for auto-discovery
UNIT_MODULE = EnergyPerUnitAreaUnitModule()