"""
MolalityOfSoluteI Units Module
==============================

Complete molality of solute "i" unit definitions and constants.
"""

from ..dimension import MOLALITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MolalityOfSoluteIUnits:
    """Type-safe molality of solute "i" unit constants."""
    # Explicit declarations for type checking
    gram_moles_of_i_per_kilogram: 'UnitConstant'
    kilogram_mols_of_i_per_kilogram: 'UnitConstant'
    kmols_of_i_per_kilogram: 'UnitConstant'
    mols_of_i_per_gram: 'UnitConstant'
    pound_moles_of_i_per_pound_mass: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MolalityOfSoluteIUnitModule(UnitModule):
    """MolalityOfSoluteI unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all molality of solute "i" unit definitions."""
        return [
            UnitDefinition("gram_moles_of_i_per_kilogram", "moli / kg", MOLALITY, 1),
            UnitDefinition("kilogram_mols_of_i_per_kilogram", "kmoli / kg", MOLALITY, 1000),
            UnitDefinition("kmols_of_i_per_kilogram", "kmoli / kg", MOLALITY, 1000),
            UnitDefinition("mols_of_i_per_gram", "moli / g", MOLALITY, 1000),
            UnitDefinition("pound_moles_of_i_per_pound_mass", "mole i / lb (mass)", MOLALITY, 1000),

        ]
    
    def get_units_class(self):
        return MolalityOfSoluteIUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MolalityOfSoluteIUnitModule()