"""
KineticEnergyOfTurbulence Units Module
======================================

Complete kinetic energy of turbulence unit definitions and constants.
"""

from ..dimension import ENERGY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class KineticEnergyOfTurbulenceUnits:
    """Type-safe kinetic energy of turbulence unit constants."""
    # Explicit declarations for type checking
    square_foot_per_second_squared: 'UnitConstant'
    square_meters_per_second_squared: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class KineticEnergyOfTurbulenceUnitModule(UnitModule):
    """KineticEnergyOfTurbulence unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all kinetic energy of turbulence unit definitions."""
        return [
            UnitDefinition("square_foot_per_second_squared", "ft2 / s2 or sqft/sec  2", ENERGY, 0.0929),
            UnitDefinition("square_meters_per_second_squared", "m2 / s2", ENERGY, 1),

        ]
    
    def get_units_class(self):
        return KineticEnergyOfTurbulenceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = KineticEnergyOfTurbulenceUnitModule()