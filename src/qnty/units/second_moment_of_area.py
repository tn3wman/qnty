"""
SecondMomentOfArea Units Module
===============================

Complete second moment of area unit definitions and constants.
"""

from ..dimension import SECOND_MOMENT_OF_AREA
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SecondMomentOfAreaUnits:
    """Type-safe second moment of area unit constants."""
    # Explicit declarations for type checking
    inch_quadrupled: 'UnitConstant'
    centimeter_quadrupled: 'UnitConstant'
    foot_quadrupled: 'UnitConstant'
    meter_quadrupled: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SecondMomentOfAreaUnitModule(UnitModule):
    """SecondMomentOfArea unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all second moment of area unit definitions."""
        return [
            UnitDefinition("inch_quadrupled", "in  4", SECOND_MOMENT_OF_AREA, 4.1623e-07),
            UnitDefinition("centimeter_quadrupled", "cm4", SECOND_MOMENT_OF_AREA, 1.00e-08),
            UnitDefinition("foot_quadrupled", "ft4", SECOND_MOMENT_OF_AREA, 0.0086310),
            UnitDefinition("meter_quadrupled", "m4", SECOND_MOMENT_OF_AREA, 1),

        ]
    
    def get_units_class(self):
        return SecondMomentOfAreaUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SecondMomentOfAreaUnitModule()