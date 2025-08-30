"""
SpecificVolume Units Module
===========================

Complete specific volume unit definitions and constants.
"""

from ..dimension import SPECIFIC_VOLUME
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SpecificVolumeUnits:
    """Type-safe specific volume unit constants."""
    # Explicit declarations for type checking
    cubic_centimeter_per_gram: 'UnitConstant'
    cubic_foot_per_kilogram: 'UnitConstant'
    cubic_foot_per_pound: 'UnitConstant'
    cubic_meter_per_kilogram: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SpecificVolumeUnitModule(UnitModule):
    """SpecificVolume unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all specific volume unit definitions."""
        return [
            UnitDefinition("cubic_centimeter_per_gram", "cm3 / g or cc / g", SPECIFIC_VOLUME, 0.001),
            UnitDefinition("cubic_foot_per_kilogram", "ft3 / kg or cft / kg", SPECIFIC_VOLUME, 0.028317),
            UnitDefinition("cubic_foot_per_pound", "ft3 / lb or cft / lb", SPECIFIC_VOLUME, 0.062428),
            UnitDefinition("cubic_meter_per_kilogram", "m3 / kg", SPECIFIC_VOLUME, 1),

        ]
    
    def get_units_class(self):
        return SpecificVolumeUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SpecificVolumeUnitModule()