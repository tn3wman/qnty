"""
AreaPerUnitVolume Units Module
==============================

Complete area per unit volume unit definitions and constants.
"""

from ..dimension import AREA_PER_UNIT_VOLUME
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AreaPerUnitVolumeUnits:
    """Type-safe area per unit volume unit constants."""
    # Explicit declarations for type checking
    square_centimeter_per_cubic_centimeter: 'UnitConstant'
    square_foot_per_cubic_foot: 'UnitConstant'
    square_meter_per_cubic_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AreaPerUnitVolumeUnitModule(UnitModule):
    """AreaPerUnitVolume unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all area per unit volume unit definitions."""
        return [
            UnitDefinition("square_centimeter_per_cubic_centimeter", "cm2 / cc", AREA_PER_UNIT_VOLUME, 100),
            UnitDefinition("square_foot_per_cubic_foot", "ft2 / ft3 or sqft/cft", AREA_PER_UNIT_VOLUME, 3.2808),
            UnitDefinition("square_meter_per_cubic_meter", "m2 / m3 or 1 / m3", AREA_PER_UNIT_VOLUME, 1),

        ]
    
    def get_units_class(self):
        return AreaPerUnitVolumeUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AreaPerUnitVolumeUnitModule()