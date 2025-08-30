"""
LinearMassDensity Units Module
==============================

Complete linear mass density unit definitions and constants.
"""

from ..dimension import MASS_DENSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class LinearMassDensityUnits:
    """Type-safe linear mass density unit constants."""
    # Explicit declarations for type checking
    denier: 'UnitConstant'
    kilogram_per_centimeter: 'UnitConstant'
    kilogram_per_meter: 'UnitConstant'
    pound_per_foot: 'UnitConstant'
    pound_per_inch: 'UnitConstant'
    pound_per_yard: 'UnitConstant'
    ton_metric_per_kilometer: 'UnitConstant'
    ton_metric_per_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class LinearMassDensityUnitModule(UnitModule):
    """LinearMassDensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all linear mass density unit definitions."""
        return [
            UnitDefinition("denier", "denier", MASS_DENSITY, 1.111e-07),
            UnitDefinition("kilogram_per_centimeter", "kg/cm", MASS_DENSITY, 100),
            UnitDefinition("kilogram_per_meter", "kg/m", MASS_DENSITY, 1),
            UnitDefinition("pound_per_foot", "lb/ft", MASS_DENSITY, 1.488),
            UnitDefinition("pound_per_inch", "lb/in", MASS_DENSITY, 17.858),
            UnitDefinition("pound_per_yard", "lb/yd", MASS_DENSITY, 0.49606),
            UnitDefinition("ton_metric_per_kilometer", "t/km or MT/km", MASS_DENSITY, 1),
            UnitDefinition("ton_metric_per_meter", "t/m or MT/m", MASS_DENSITY, 1000),

        ]
    
    def get_units_class(self):
        return LinearMassDensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = LinearMassDensityUnitModule()