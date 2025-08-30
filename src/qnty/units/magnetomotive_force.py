"""
MagnetomotiveForce Units Module
===============================

Complete magnetomotive force unit definitions and constants.
"""

from ..dimension import CURRENT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MagnetomotiveForceUnits:
    """Type-safe magnetomotive force unit constants."""
    # Explicit declarations for type checking
    abampereturn: 'UnitConstant'
    ampere: 'UnitConstant'
    ampereturn: 'UnitConstant'
    gilbert: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MagnetomotiveForceUnitModule(UnitModule):
    """MagnetomotiveForce unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all magnetomotive force unit definitions."""
        return [
            UnitDefinition("abampereturn", "emu cgs", CURRENT, 10),
            UnitDefinition("ampere", "A", CURRENT, 1),
            UnitDefinition("ampereturn", "A-turn", CURRENT, 2864.77),
            UnitDefinition("gilbert", "Gb", CURRENT, 0.79577),

        ]
    
    def get_units_class(self):
        return MagnetomotiveForceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MagnetomotiveForceUnitModule()