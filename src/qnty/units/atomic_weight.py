"""
AtomicWeight Units Module
=========================

Complete atomic weight unit definitions and constants.
"""

from ..dimension import ATOMIC_WEIGHT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AtomicWeightUnits:
    """Type-safe atomic weight unit constants."""
    # Explicit declarations for type checking
    atomic_mass_unit_12c: 'UnitConstant'
    grams_per_mole: 'UnitConstant'
    kilograms_per_kilomole: 'UnitConstant'
    pounds_per_pound_mole: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AtomicWeightUnitModule(UnitModule):
    """AtomicWeight unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all atomic weight unit definitions."""
        return [
            UnitDefinition("atomic_mass_unit_12c", "amu", ATOMIC_WEIGHT, 1),
            UnitDefinition("grams_per_mole", "g/mol", ATOMIC_WEIGHT, 1),
            UnitDefinition("kilograms_per_kilomole", "kg/kmol", ATOMIC_WEIGHT, 1),
            UnitDefinition("pounds_per_pound_mole", "lb / lb- mol or lb / mole", ATOMIC_WEIGHT, 1),

        ]
    
    def get_units_class(self):
        return AtomicWeightUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AtomicWeightUnitModule()