"""
MomentumFlux Units Module
=========================

Complete momentum flux unit definitions and constants.
"""

from ..dimension import PRESSURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MomentumFluxUnits:
    """Type-safe momentum flux unit constants."""
    # Explicit declarations for type checking
    dyne_per_square_centimeter: 'UnitConstant'
    gram_per_centimeter_per_square_second: 'UnitConstant'
    newton_per_square_meter: 'UnitConstant'
    pound_force_per_square_foot: 'UnitConstant'
    pound_mass_per_foot_per_square_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MomentumFluxUnitModule(UnitModule):
    """MomentumFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all momentum flux unit definitions."""
        return [
            UnitDefinition("dyne_per_square_centimeter", "dyn/ cm2", PRESSURE, 10),
            UnitDefinition("gram_per_centimeter_per_square_second", "g / cm / s2", PRESSURE, 10),
            UnitDefinition("newton_per_square_meter", "N / m2", PRESSURE, 1),
            UnitDefinition("pound_force_per_square_foot", "lbf / sq ft", PRESSURE, 478.8),
            UnitDefinition("pound_mass_per_foot_per_square_second", "lbm / ft / s2 or lb / ft / sec2", PRESSURE, 14.882),

        ]
    
    def get_units_class(self):
        return MomentumFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MomentumFluxUnitModule()