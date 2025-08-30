"""
MassFlux Units Module
=====================

Complete mass flux unit definitions and constants.
"""

from ..dimension import MASS_FLUX
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MassFluxUnits:
    """Type-safe mass flux unit constants."""
    # Explicit declarations for type checking
    kilogram_per_square_meter_per_day: 'UnitConstant'
    kilogram_per_square_meter_per_hour: 'UnitConstant'
    kilogram_per_square_meter_per_minute: 'UnitConstant'
    kilogram_per_square_meter_per_second: 'UnitConstant'
    pound_per_square_foot_per_day: 'UnitConstant'
    pound_per_square_foot_per_hour: 'UnitConstant'
    pound_per_square_foot_per_minute: 'UnitConstant'
    pound_per_square_foot_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MassFluxUnitModule(UnitModule):
    """MassFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mass flux unit definitions."""
        return [
            UnitDefinition("kilogram_per_square_meter_per_day", "kg /left(m2 ~dright)", MASS_FLUX, 1.1574e-05),
            UnitDefinition("kilogram_per_square_meter_per_hour", "kg /left(m2 ~hright)", MASS_FLUX, 2.7778e-04),
            UnitDefinition("kilogram_per_square_meter_per_minute", "kg /left(m2 ~minright)", MASS_FLUX, 0.016667),
            UnitDefinition("kilogram_per_square_meter_per_second", "kg /left(m2 ~sright)", MASS_FLUX, 1),
            UnitDefinition("pound_per_square_foot_per_day", "lb /left(ft2 ~dright) or lb/sqft/ da", MASS_FLUX, 5.6478e-05),
            UnitDefinition("pound_per_square_foot_per_hour", "lb /left(ft2 ~hright) or lb/sqft/ hr", MASS_FLUX, 0.0013555),
            UnitDefinition("pound_per_square_foot_per_minute", "lb /left(ft2 min right) or lb/ sqft/min", MASS_FLUX, 0.081329),
            UnitDefinition("pound_per_square_foot_per_second", "lb /left(ft2 ~sright) or lb/sqft/ sec", MASS_FLUX, 4.8797),

        ]
    
    def get_units_class(self):
        return MassFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MassFluxUnitModule()