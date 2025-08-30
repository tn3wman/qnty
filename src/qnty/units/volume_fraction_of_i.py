"""
VolumeFractionOfI Units Module
==============================

Complete volume fraction of "i" unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumeFractionOfIUnits:
    """Type-safe volume fraction of "i" unit constants."""
    # Explicit declarations for type checking
    cubic_centimeters_of_i_per_cubic_meter_total: 'UnitConstant'
    cubic_foot_of_i_per_cubic_foot_total: 'UnitConstant'
    cubic_meters_of_i_per_cubic_meter_total: 'UnitConstant'
    gallons_of_i_per_gallon_total: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumeFractionOfIUnitModule(UnitModule):
    """VolumeFractionOfI unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volume fraction of "i" unit definitions."""
        return [
            UnitDefinition("cubic_centimeters_of_i_per_cubic_meter_total", "cmi3 / m3 or cci / m3", DIMENSIONLESS, 0.0001),
            UnitDefinition("cubic_foot_of_i_per_cubic_foot_total", "fti3 / ft3 or cfti / cft", DIMENSIONLESS, 1),
            UnitDefinition("cubic_meters_of_i_per_cubic_meter_total", "mi 3 / m3", DIMENSIONLESS, 1),
            UnitDefinition("gallons_of_i_per_gallon_total", "gali / gal", DIMENSIONLESS, 1),

        ]
    
    def get_units_class(self):
        return VolumeFractionOfIUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumeFractionOfIUnitModule()