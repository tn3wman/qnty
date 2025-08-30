"""
MolarFlux Units Module
======================

Complete molar flux unit definitions and constants.
"""

from ..dimension import MOLAR_FLUX
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MolarFluxUnits:
    """Type-safe molar flux unit constants."""
    # Explicit declarations for type checking
    kmol_per_square_meter_per_day: 'UnitConstant'
    kmol_per_square_meter_per_hour: 'UnitConstant'
    kmol_per_square_meter_per_minute: 'UnitConstant'
    kmol_per_square_meter_per_second: 'UnitConstant'
    pound_mole_per_square_foot_per_day: 'UnitConstant'
    pound_mole_per_square_foot_per_hour: 'UnitConstant'
    pound_mole_per_square_foot_per_minute: 'UnitConstant'
    pound_mole_per_square_foot_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MolarFluxUnitModule(UnitModule):
    """MolarFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all molar flux unit definitions."""
        return [
            UnitDefinition("kmol_per_square_meter_per_day", "kmol /left(m2 ~dright)", MOLAR_FLUX, 1.1574e-05),
            UnitDefinition("kmol_per_square_meter_per_hour", "kmol /left(m2 ~hright)", MOLAR_FLUX, 2.7778e-04),
            UnitDefinition("kmol_per_square_meter_per_minute", "kmol /left(m2right. amin )", MOLAR_FLUX, 0.016667),
            UnitDefinition("kmol_per_square_meter_per_second", "kmol /left(m2 ~sright)", MOLAR_FLUX, 1),
            UnitDefinition("pound_mole_per_square_foot_per_day", "lb-mol /left(ft2 ~dright) or mole/sqft/da", MOLAR_FLUX, 5.6478e-05),
            UnitDefinition("pound_mole_per_square_foot_per_hour", "lb-mol /left(ft2 ~hright) or mole/sqft/hr", MOLAR_FLUX, 0.0013555),
            UnitDefinition("pound_mole_per_square_foot_per_minute", "lb-mol /left(ft2 ~minright) or mole/sqft/min", MOLAR_FLUX, 0.081329),
            UnitDefinition("pound_mole_per_square_foot_per_second", "lb-mol /left(ft2 ~sright) or mole/sqft/sec", MOLAR_FLUX, 4.8797),

        ]
    
    def get_units_class(self):
        return MolarFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MolarFluxUnitModule()