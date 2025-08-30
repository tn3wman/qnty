"""
SpecificGravity Units Module
============================

Complete specific gravity unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SpecificGravityUnits:
    """Type-safe specific gravity unit constants."""
    # Explicit declarations for type checking
    dimensionless: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SpecificGravityUnitModule(UnitModule):
    """SpecificGravity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all specific gravity unit definitions."""
        return [
            UnitDefinition("dimensionless", "Dmls", DIMENSIONLESS, 1),

        ]
    
    def get_units_class(self):
        return SpecificGravityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SpecificGravityUnitModule()