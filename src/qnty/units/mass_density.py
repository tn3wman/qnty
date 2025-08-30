"""
MassDensity Units Module
========================

Complete mass density unit definitions and constants.
"""

from ..dimension import MASS_DENSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MassDensityUnits:
    """Type-safe mass density unit constants."""
    # Explicit declarations for type checking
    gram_per_cubic_centimeter: 'UnitConstant'
    gram_per_cubic_decimeter: 'UnitConstant'
    gram_per_cubic_meter: 'UnitConstant'
    gram_per_liter: 'UnitConstant'
    kilogram_per_cubic_meter: 'UnitConstant'
    ounce_avdp_per_us_gallon: 'UnitConstant'
    pound_avdp_per_cubic_foot: 'UnitConstant'
    pound_avdp_per_us_gallon: 'UnitConstant'
    pound_mass_per_cubic_inch: 'UnitConstant'
    ton_metric_per_cubic_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MassDensityUnitModule(UnitModule):
    """MassDensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mass density unit definitions."""
        return [
            UnitDefinition("gram_per_cubic_centimeter", "g/cc or g/ml", MASS_DENSITY, 1000),
            UnitDefinition("gram_per_cubic_decimeter", "g / dm3", MASS_DENSITY, 1),
            UnitDefinition("gram_per_cubic_meter", "g / m3", MASS_DENSITY, 0.001),
            UnitDefinition("gram_per_liter", "g / l or g/L", MASS_DENSITY, 1),
            UnitDefinition("kilogram_per_cubic_meter", "kg / m3", MASS_DENSITY, 1),
            UnitDefinition("ounce_avdp_per_us_gallon", "oz/gal", MASS_DENSITY, 7.489152),
            UnitDefinition("pound_avdp_per_cubic_foot", "lb / cu ft or lb/ft  3", MASS_DENSITY, 16.01846),
            UnitDefinition("pound_avdp_per_us_gallon", "lb/gal", MASS_DENSITY, 119.826),
            UnitDefinition("pound_mass_per_cubic_inch", "lb / cu in or lb / in3", MASS_DENSITY, 0.000276799),
            UnitDefinition("ton_metric_per_cubic_meter", "t / m3 or MT / m3", MASS_DENSITY, 1000),

        ]
    
    def get_units_class(self):
        return MassDensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MassDensityUnitModule()