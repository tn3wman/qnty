"""
SpecificSurface Units Module
============================

Complete specific surface unit definitions and constants.
"""

from ..dimension import SPECIFIC_SURFACE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SpecificSurfaceUnits:
    """Type-safe specific surface unit constants."""
    # Explicit declarations for type checking
    square_centimeter_per_gram: 'UnitConstant'
    square_foot_per_kilogram: 'UnitConstant'
    square_foot_per_pound: 'UnitConstant'
    square_meter_per_gram: 'UnitConstant'
    square_meter_per_kilogram: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SpecificSurfaceUnitModule(UnitModule):
    """SpecificSurface unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all specific surface unit definitions."""
        return [
            UnitDefinition("square_centimeter_per_gram", "cm2 / g", SPECIFIC_SURFACE, 0.1),
            UnitDefinition("square_foot_per_kilogram", "ft2 / kg or sq ft/kg", SPECIFIC_SURFACE, 0.092903),
            UnitDefinition("square_foot_per_pound", "ft2 / lb or sq ft/lb", SPECIFIC_SURFACE, 0.20482),
            UnitDefinition("square_meter_per_gram", "m2 / g", SPECIFIC_SURFACE, 1000),
            UnitDefinition("square_meter_per_kilogram", "m2 / kg", SPECIFIC_SURFACE, 1),

        ]
    
    def get_units_class(self):
        return SpecificSurfaceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SpecificSurfaceUnitModule()