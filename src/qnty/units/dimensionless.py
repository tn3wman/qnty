"""
Dimensionless Units Module
=========================

Complete dimensionless unit definitions and constants.
"""

from typing import List

from ..dimension import DIMENSIONLESS
from ..unit import UnitDefinition, UnitConstant
from .base import UnitModule


class DimensionlessUnits:
    """Type-safe dimensionless unit constants."""
    # Explicit declarations for type checking
    dimensionless: 'UnitConstant'


class DimensionlessUnitModule(UnitModule):
    """Dimensionless unit module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all dimensionless unit definitions."""
        return [
            UnitDefinition("dimensionless", "", DIMENSIONLESS, 1.0),
        ]
    
    def get_units_class(self):
        return DimensionlessUnits


# Register this module for auto-discovery
UNIT_MODULE = DimensionlessUnitModule()