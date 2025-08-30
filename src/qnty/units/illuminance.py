"""
Illuminance Units Module
========================

Complete illuminance unit definitions and constants.
"""

from ..dimension import ILLUMINANCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class IlluminanceUnits:
    """Type-safe illuminance unit constants."""
    # Explicit declarations for type checking
    footcandle: 'UnitConstant'
    lux: 'UnitConstant'
    nox: 'UnitConstant'
    phot: 'UnitConstant'
    skot: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class IlluminanceUnitModule(UnitModule):
    """Illuminance unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all illuminance unit definitions."""
        return [
            UnitDefinition("footcandle", "ft-C or ft-Cd", ILLUMINANCE, 10.76391),
            UnitDefinition("lux", "lx", ILLUMINANCE, 1),
            UnitDefinition("nox", "nox", ILLUMINANCE, 1.00e-03),
            UnitDefinition("phot", "ph", ILLUMINANCE, 1.00e+04),
            UnitDefinition("skot", "skot", ILLUMINANCE, 1.00e-03),

        ]
    
    def get_units_class(self):
        return IlluminanceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = IlluminanceUnitModule()