"""
AmountOfSubstance Units Module
==============================

Complete amount of substance unit definitions and constants.
"""

from ..dimension import AMOUNT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AmountOfSubstanceUnits:
    """Type-safe amount of substance unit constants."""
    # Explicit declarations for type checking
    kilogram_mol: 'UnitConstant'
    mole_gram: 'UnitConstant'
    poundmole: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AmountOfSubstanceUnitModule(UnitModule):
    """AmountOfSubstance unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all amount of substance unit definitions."""
        return [
            UnitDefinition("kilogram_mol", "kmol", AMOUNT, 1000),
            UnitDefinition("mole_gram", "mol", AMOUNT, 1),
            UnitDefinition("poundmole", "lb-mol or mole", AMOUNT, 453.6),

        ]
    
    def get_units_class(self):
        return AmountOfSubstanceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AmountOfSubstanceUnitModule()