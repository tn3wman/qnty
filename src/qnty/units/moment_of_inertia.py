"""
MomentOfInertia Units Module
============================

Complete moment of inertia unit definitions and constants.
"""

from ..dimension import MOMENT_OF_INERTIA
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MomentOfInertiaUnits:
    """Type-safe moment of inertia unit constants."""
    # Explicit declarations for type checking
    gram_force_centimeter_square_second: 'UnitConstant'
    gram_square_centimeter: 'UnitConstant'
    kilogram_force_centimeter_square_second: 'UnitConstant'
    kilogram_force_meter_square_second: 'UnitConstant'
    kilogram_square_centimeter: 'UnitConstant'
    kilogram_square_meter: 'UnitConstant'
    ounce_force_inch_square_second: 'UnitConstant'
    ounce_mass_square_inch: 'UnitConstant'
    pound_mass_square_foot: 'UnitConstant'
    pound_mass_square_inch: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MomentOfInertiaUnitModule(UnitModule):
    """MomentOfInertia unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all moment of inertia unit definitions."""
        return [
            UnitDefinition("gram_force_centimeter_square_second", "gf cm s2", MOMENT_OF_INERTIA, 9.8067e-05),
            UnitDefinition("gram_square_centimeter", "g cm2", MOMENT_OF_INERTIA, 1.00e-07),
            UnitDefinition("kilogram_force_centimeter_square_second", "kgf cm s 2", MOMENT_OF_INERTIA, 0.098067),
            UnitDefinition("kilogram_force_meter_square_second", "kgf m s2", MOMENT_OF_INERTIA, 9.8067),
            UnitDefinition("kilogram_square_centimeter", "kg cm2", MOMENT_OF_INERTIA, 1.00e-04),
            UnitDefinition("kilogram_square_meter", "kg m2", MOMENT_OF_INERTIA, 1),
            UnitDefinition("ounce_force_inch_square_second", "ozf in s2", MOMENT_OF_INERTIA, 0.0070616),
            UnitDefinition("ounce_mass_square_inch", "oz in  2", MOMENT_OF_INERTIA, 1.8290e-05),
            UnitDefinition("pound_mass_square_foot", "lb ft  2 or lb sq ft", MOMENT_OF_INERTIA, 0.04214),
            UnitDefinition("pound_mass_square_inch", "lb in2", MOMENT_OF_INERTIA, 2.9264e-04),

        ]
    
    def get_units_class(self):
        return MomentOfInertiaUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MomentOfInertiaUnitModule()