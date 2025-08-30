"""
MoleFractionOfI Units Module
============================

Complete mole fraction of "i" unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MoleFractionOfIUnits:
    """Type-safe mole fraction of "i" unit constants."""
    # Explicit declarations for type checking
    gram_mole_of_i_per_gram_mole_total: 'UnitConstant'
    kilogram_mole_of_i_per_kilogram_mole_total: 'UnitConstant'
    kilomole_of_i_per_kilomole_total: 'UnitConstant'
    pound_mole_of_i_per_pound_mole_total: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MoleFractionOfIUnitModule(UnitModule):
    """MoleFractionOfI unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mole fraction of "i" unit definitions."""
        return [
            UnitDefinition("gram_mole_of_i_per_gram_mole_total", "moli / mol", DIMENSIONLESS, 1),
            UnitDefinition("kilogram_mole_of_i_per_kilogram_mole_total", "kmoli / kmol", DIMENSIONLESS, 1),
            UnitDefinition("kilomole_of_i_per_kilomole_total", "kmoli / kmol", DIMENSIONLESS, 1),
            UnitDefinition("pound_mole_of_i_per_pound_mole_total", "lb moli / lb mol", DIMENSIONLESS, 1),

        ]
    
    def get_units_class(self):
        return MoleFractionOfIUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MoleFractionOfIUnitModule()