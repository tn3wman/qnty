"""
RadiationExposure Units Module
==============================

Complete radiation exposure unit definitions and constants.
"""

from ..dimension import RADIATION_EXPOSURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class RadiationExposureUnits:
    """Type-safe radiation exposure unit constants."""
    # Explicit declarations for type checking
    coulomb_per_kilogram: 'UnitConstant'
    d_unit: 'UnitConstant'
    pastille_dose_b_unit: 'UnitConstant'
    röentgen: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class RadiationExposureUnitModule(UnitModule):
    """RadiationExposure unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all radiation exposure unit definitions."""
        return [
            UnitDefinition("coulomb_per_kilogram", "C/kg", RADIATION_EXPOSURE, 1),
            UnitDefinition("d_unit", "D unit", RADIATION_EXPOSURE, 0.0258),
            UnitDefinition("pastille_dose_b_unit", "B unit", RADIATION_EXPOSURE, 0.129),
            UnitDefinition("röentgen", "R", RADIATION_EXPOSURE, 0.000258),

        ]
    
    def get_units_class(self):
        return RadiationExposureUnits
    


# Register this module for auto-discovery
UNIT_MODULE = RadiationExposureUnitModule()