"""
MagneticField Units Module
==========================

Complete magnetic field unit definitions and constants.
"""

from ..dimension import MAGNETIC_FIELD
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MagneticFieldUnits:
    """Type-safe magnetic field unit constants."""
    # Explicit declarations for type checking
    ampere_per_meter: 'UnitConstant'
    lenz: 'UnitConstant'
    oersted: 'UnitConstant'
    praoersted: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MagneticFieldUnitModule(UnitModule):
    """MagneticField unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all magnetic field unit definitions."""
        return [
            UnitDefinition("ampere_per_meter", "A/m", MAGNETIC_FIELD, 1),
            UnitDefinition("lenz", "lenz", MAGNETIC_FIELD, 1),
            UnitDefinition("oersted", "Oe", MAGNETIC_FIELD, 79.57747),
            UnitDefinition("praoersted", "-", MAGNETIC_FIELD, 11459.08),

        ]
    
    def get_units_class(self):
        return MagneticFieldUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MagneticFieldUnitModule()