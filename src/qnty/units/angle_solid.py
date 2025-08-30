"""
AngleSolid Units Module
=======================

Complete angle, solid unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AngleSolidUnits:
    """Type-safe angle, solid unit constants."""
    # Explicit declarations for type checking
    spat: 'UnitConstant'
    square_degree: 'UnitConstant'
    square_gon: 'UnitConstant'
    steradian: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AngleSolidUnitModule(UnitModule):
    """AngleSolid unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all angle, solid unit definitions."""
        return [
            UnitDefinition("spat", "spat", DIMENSIONLESS, 12.5663),
            UnitDefinition("square_degree", "left( °right)2", DIMENSIONLESS, 0.000304617),
            UnitDefinition("square_gon", "(g)  2", DIMENSIONLESS, 0.00024674),
            UnitDefinition("steradian", "sr", DIMENSIONLESS, 1),

        ]
    
    def get_units_class(self):
        return AngleSolidUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AngleSolidUnitModule()