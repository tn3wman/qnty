"""
SurfaceMassDensity Units Module
===============================

Complete surface mass density unit definitions and constants.
"""

from ..dimension import MASS_DENSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SurfaceMassDensityUnits:
    """Type-safe surface mass density unit constants."""
    # Explicit declarations for type checking
    gram_per_square_centimeter: 'UnitConstant'
    gram_per_square_meter: 'UnitConstant'
    kilogram_per_square_meter: 'UnitConstant'
    pound_mass_per_square_foot: 'UnitConstant'
    pound_mass_per_square_inch: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SurfaceMassDensityUnitModule(UnitModule):
    """SurfaceMassDensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all surface mass density unit definitions."""
        return [
            UnitDefinition("gram_per_square_centimeter", "kg / cm2", MASS_DENSITY, 10),
            UnitDefinition("gram_per_square_meter", "g / m2", MASS_DENSITY, 0.001),
            UnitDefinition("kilogram_per_square_meter", "kg / m2", MASS_DENSITY, 1),
            UnitDefinition("pound_mass_per_square_foot", "lb / ft2", MASS_DENSITY, 4.882427),
            UnitDefinition("pound_mass_per_square_inch", "lb / in2", MASS_DENSITY, 703.07),

        ]
    
    def get_units_class(self):
        return SurfaceMassDensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SurfaceMassDensityUnitModule()