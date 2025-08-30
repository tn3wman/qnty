"""
MassFractionOfI Units Module
============================

Complete mass fraction of "i" unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MassFractionOfIUnits:
    """Type-safe mass fraction of "i" unit constants."""
    # Explicit declarations for type checking
    grains_of_i_per_pound_total: 'UnitConstant'
    gram_of_i_per_kilogram_total: 'UnitConstant'
    kilogram_of_i_per_kilogram_total: 'UnitConstant'
    pound_of_i_per_pound_total: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MassFractionOfIUnitModule(UnitModule):
    """MassFractionOfI unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mass fraction of "i" unit definitions."""
        return [
            UnitDefinition("grains_of_i_per_pound_total", "gri / lb", DIMENSIONLESS, 0.00014286),
            UnitDefinition("gram_of_i_per_kilogram_total", "gi / kg", DIMENSIONLESS, 0.001),
            UnitDefinition("kilogram_of_i_per_kilogram_total", "kgi / kg", DIMENSIONLESS, 1),
            UnitDefinition("pound_of_i_per_pound_total", "lbi / lb", DIMENSIONLESS, 1),

        ]
    
    def get_units_class(self):
        return MassFractionOfIUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MassFractionOfIUnitModule()