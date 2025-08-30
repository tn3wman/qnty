"""
MagneticPermeability Units Module
=================================

Complete magnetic permeability unit definitions and constants.
"""

from ..dimension import MAGNETIC_PERMEABILITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MagneticPermeabilityUnits:
    """Type-safe magnetic permeability unit constants."""
    # Explicit declarations for type checking
    henrys_per_meter: 'UnitConstant'
    newton_per_square_ampere: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MagneticPermeabilityUnitModule(UnitModule):
    """MagneticPermeability unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all magnetic permeability unit definitions."""
        return [
            UnitDefinition("henrys_per_meter", "H/m", MAGNETIC_PERMEABILITY, 1),
            UnitDefinition("newton_per_square_ampere", "N/A  2", MAGNETIC_PERMEABILITY, 1),

        ]
    
    def get_units_class(self):
        return MagneticPermeabilityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MagneticPermeabilityUnitModule()