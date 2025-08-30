"""
Radioactivity Units Module
==========================

Complete radioactivity unit definitions and constants.
"""

from ..dimension import RADIOACTIVITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class RadioactivityUnits:
    """Type-safe radioactivity unit constants."""
    # Explicit declarations for type checking
    becquerel: 'UnitConstant'
    curie: 'UnitConstant'
    mache_unit: 'UnitConstant'
    rutherford: 'UnitConstant'
    stat: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class RadioactivityUnitModule(UnitModule):
    """Radioactivity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all radioactivity unit definitions."""
        return [
            UnitDefinition("becquerel", "Bq", RADIOACTIVITY, 1),
            UnitDefinition("curie", "Ci", RADIOACTIVITY, 3.70e+10),
            UnitDefinition("mache_unit", "Mache", RADIOACTIVITY, 13.32),
            UnitDefinition("rutherford", "Rd", RADIOACTIVITY, 1.00e+06),
            UnitDefinition("stat", "stat", RADIOACTIVITY, 1.34e-16),

        ]
    
    def get_units_class(self):
        return RadioactivityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = RadioactivityUnitModule()