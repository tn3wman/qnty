"""
NormalityOfSolution Units Module
================================

Complete normality of solution unit definitions and constants.
"""

from ..dimension import NORMALITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class NormalityOfSolutionUnits:
    """Type-safe normality of solution unit constants."""
    # Explicit declarations for type checking
    gram_equivalents_per_cubic_meter: 'UnitConstant'
    gram_equivalents_per_liter: 'UnitConstant'
    pound_equivalents_per_cubic_foot: 'UnitConstant'
    pound_equivalents_per_gallon: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class NormalityOfSolutionUnitModule(UnitModule):
    """NormalityOfSolution unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all normality of solution unit definitions."""
        return [
            UnitDefinition("gram_equivalents_per_cubic_meter", "eq / m3", NORMALITY, 1),
            UnitDefinition("gram_equivalents_per_liter", "eq/l", NORMALITY, 1000),
            UnitDefinition("pound_equivalents_per_cubic_foot", "lb eq / ft3 or lb eq/cft", NORMALITY, 77844),
            UnitDefinition("pound_equivalents_per_gallon", "lb eq/gal (US)", NORMALITY, 10406),

        ]
    
    def get_units_class(self):
        return NormalityOfSolutionUnits
    


# Register this module for auto-discovery
UNIT_MODULE = NormalityOfSolutionUnitModule()