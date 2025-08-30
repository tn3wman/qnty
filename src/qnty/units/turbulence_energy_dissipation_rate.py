"""
TurbulenceEnergyDissipationRate Units Module
============================================

Complete turbulence energy dissipation rate unit definitions and constants.
"""

from ..dimension import TURBULENCE_ENERGY_DISSIPATION_RATE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class TurbulenceEnergyDissipationRateUnits:
    """Type-safe turbulence energy dissipation rate unit constants."""
    # Explicit declarations for type checking
    square_foot_per_cubic_second: 'UnitConstant'
    square_meter_per_cubic_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class TurbulenceEnergyDissipationRateUnitModule(UnitModule):
    """TurbulenceEnergyDissipationRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all turbulence energy dissipation rate unit definitions."""
        return [
            UnitDefinition("square_foot_per_cubic_second", "ft2 / s3 or sq ft/sec  3", TURBULENCE_ENERGY_DISSIPATION_RATE, 0.0929),
            UnitDefinition("square_meter_per_cubic_second", "m2 / s3", TURBULENCE_ENERGY_DISSIPATION_RATE, 1),

        ]
    
    def get_units_class(self):
        return TurbulenceEnergyDissipationRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = TurbulenceEnergyDissipationRateUnitModule()