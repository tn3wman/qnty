"""
Length Units Module
==================

Complete length unit definitions and constants.
"""

from typing import List

from ..dimension import LENGTH
from ..unit import UnitDefinition, UnitConstant
from .base import UnitModule


class LengthUnits:
    """Type-safe length unit constants."""
    # Explicit declarations for type checking
    meter: 'UnitConstant'
    millimeter: 'UnitConstant'
    centimeter: 'UnitConstant'
    inch: 'UnitConstant'
    foot: 'UnitConstant'
    
    # Common aliases
    m: 'UnitConstant'
    mm: 'UnitConstant'
    cm: 'UnitConstant'
    in_: 'UnitConstant'
    ft: 'UnitConstant'


class LengthUnitModule(UnitModule):
    """Length unit module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all length unit definitions."""
        return [
            UnitDefinition("meter", "m", LENGTH, 1.0),
            UnitDefinition("millimeter", "mm", LENGTH, 0.001),
            UnitDefinition("centimeter", "cm", LENGTH, 0.01),
            UnitDefinition("inch", "in", LENGTH, 0.0254),
            UnitDefinition("foot", "ft", LENGTH, 0.3048),
        ]
    
    def get_units_class(self):
        return LengthUnits


# Register this module for auto-discovery
UNIT_MODULE = LengthUnitModule()