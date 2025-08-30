"""
Luminanceself Units Module
==========================

Complete luminance (self) unit definitions and constants.
"""

from ..dimension import LUMINANCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class LuminanceselfUnits:
    """Type-safe luminance (self) unit constants."""
    # Explicit declarations for type checking
    apostilb: 'UnitConstant'
    blondel: 'UnitConstant'
    candela_per_square_meter: 'UnitConstant'
    footlambert: 'UnitConstant'
    lambert: 'UnitConstant'
    luxon: 'UnitConstant'
    nit: 'UnitConstant'
    stilb: 'UnitConstant'
    troland: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class LuminanceselfUnitModule(UnitModule):
    """Luminanceself unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all luminance (self) unit definitions."""
        return [
            UnitDefinition("apostilb", "asb", LUMINANCE, 0.31831),
            UnitDefinition("blondel", "B1", LUMINANCE, 0.31831),
            UnitDefinition("candela_per_square_meter", "cd / m2", LUMINANCE, 1),
            UnitDefinition("footlambert", "ft-L", LUMINANCE, 3.426259),
            UnitDefinition("lambert", "L", LUMINANCE, 3183.1),
            UnitDefinition("luxon", "luxon", LUMINANCE, 1.00e+04),
            UnitDefinition("nit", "nit", LUMINANCE, 1),
            UnitDefinition("stilb", "sb", LUMINANCE, 1.00e+04),
            UnitDefinition("troland", "luxon", LUMINANCE, 1.00e+04),

        ]
    
    def get_units_class(self):
        return LuminanceselfUnits
    


# Register this module for auto-discovery
UNIT_MODULE = LuminanceselfUnitModule()