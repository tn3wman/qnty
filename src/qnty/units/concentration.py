"""
Concentration Units Module
==========================

Complete concentration unit definitions and constants.
"""

from ..dimension import CONCENTRATION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ConcentrationUnits:
    """Type-safe concentration unit constants."""
    # Explicit declarations for type checking
    grains_of_i_per_cubic_foot: 'UnitConstant'
    grains_of_i_per_gallon_us: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ConcentrationUnitModule(UnitModule):
    """Concentration unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all concentration unit definitions."""
        return [
            UnitDefinition("grains_of_i_per_cubic_foot", "gr / ft3 or gr/cft", CONCENTRATION, 0.002288),
            UnitDefinition("grains_of_i_per_gallon_us", "gr/gal", CONCENTRATION, 0.017115),

        ]
    
    def get_units_class(self):
        return ConcentrationUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ConcentrationUnitModule()