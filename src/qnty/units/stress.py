"""
Stress Units Module
===================

Complete stress unit definitions and constants.
"""

from ..dimension import PRESSURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class StressUnits:
    """Type-safe stress unit constants."""
    # Explicit declarations for type checking
    dyne_per_square_centimeter: 'UnitConstant'
    gigapascal: 'UnitConstant'
    hectopascal: 'UnitConstant'
    kilogram_force_per_square_centimeter: 'UnitConstant'
    kilogram_force_per_square_meter: 'UnitConstant'
    kip_force_per_square_inch: 'UnitConstant'
    megapascal: 'UnitConstant'
    newton_per_square_meter: 'UnitConstant'
    ounce_force_per_square_inch: 'UnitConstant'
    pascal: 'UnitConstant'
    pound_force_per_square_foot: 'UnitConstant'
    pound_force_per_square_inch: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class StressUnitModule(UnitModule):
    """Stress unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all stress unit definitions."""
        return [
            UnitDefinition("dyne_per_square_centimeter", "dyn/ cm2", PRESSURE, 0.1),
            UnitDefinition("gigapascal", "GPa", PRESSURE, 1.00e+09),
            UnitDefinition("hectopascal", "hPa", PRESSURE, 100),
            UnitDefinition("kilogram_force_per_square_centimeter", "at or kgf / cm2", PRESSURE, 9.8067e+04),
            UnitDefinition("kilogram_force_per_square_meter", "kgf / m2", PRESSURE, 9.80665),
            UnitDefinition("kip_force_per_square_inch", "KSI or ksi or kip  f / in2", PRESSURE, 6.8948e+06),
            UnitDefinition("megapascal", "MPa", PRESSURE, 1.00e+06),
            UnitDefinition("newton_per_square_meter", "N / m2", PRESSURE, 1),
            UnitDefinition("ounce_force_per_square_inch", "OSI or osi or ozf / in2", PRESSURE, 430.922),
            UnitDefinition("pascal", "Pa", PRESSURE, 1),
            UnitDefinition("pound_force_per_square_foot", "PSF or psf or lbf / ft2", PRESSURE, 47.880259),
            UnitDefinition("pound_force_per_square_inch", "PSI or psi or lbf / in2", PRESSURE, 6.8948e+03),

        ]
    
    def get_units_class(self):
        return StressUnits
    


# Register this module for auto-discovery
UNIT_MODULE = StressUnitModule()