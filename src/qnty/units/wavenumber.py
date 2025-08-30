"""
Wavenumber Units Module
=======================

Complete wavenumber unit definitions and constants.
"""

from ..dimension import WAVENUMBER
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class WavenumberUnits:
    """Type-safe wavenumber unit constants."""
    # Explicit declarations for type checking
    diopter: 'UnitConstant'
    kayser: 'UnitConstant'
    reciprocal_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class WavenumberUnitModule(UnitModule):
    """Wavenumber unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all wavenumber unit definitions."""
        return [
            UnitDefinition("diopter", "D", WAVENUMBER, 1),
            UnitDefinition("kayser", "K", WAVENUMBER, 100),
            UnitDefinition("reciprocal_meter", "1/m", WAVENUMBER, 1),

        ]
    
    def get_units_class(self):
        return WavenumberUnits
    


# Register this module for auto-discovery
UNIT_MODULE = WavenumberUnitModule()