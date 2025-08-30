"""
Permeability Units Module
=========================

Complete permeability unit definitions and constants.
"""

from ..dimension import AREA
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class PermeabilityUnits:
    """Type-safe permeability unit constants."""
    # Explicit declarations for type checking
    darcy: 'UnitConstant'
    square_feet: 'UnitConstant'
    square_meters: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class PermeabilityUnitModule(UnitModule):
    """Permeability unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all permeability unit definitions."""
        return [
            UnitDefinition("darcy", "darcy", AREA, 9.8692e-13),
            UnitDefinition("square_feet", "ft2 or sq ft", AREA, 0.0929),
            UnitDefinition("square_meters", "m2", AREA, 1),

        ]
    
    def get_units_class(self):
        return PermeabilityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = PermeabilityUnitModule()