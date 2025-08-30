"""
LuminousFlux Units Module
=========================

Complete luminous flux unit definitions and constants.
"""

from ..dimension import LUMINOSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class LuminousFluxUnits:
    """Type-safe luminous flux unit constants."""
    # Explicit declarations for type checking
    candela_steradian: 'UnitConstant'
    lumen: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class LuminousFluxUnitModule(UnitModule):
    """LuminousFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all luminous flux unit definitions."""
        return [
            UnitDefinition("candela_steradian", "cd sr", LUMINOSITY, 1),
            UnitDefinition("lumen", "lumen", LUMINOSITY, 1),

        ]
    
    def get_units_class(self):
        return LuminousFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = LuminousFluxUnitModule()