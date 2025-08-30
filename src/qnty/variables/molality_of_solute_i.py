"""
MolalityOfSoluteI Variable Module
==================================

Type-safe molality of solute "i" variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MOLALITY
from ..units import MolalityOfSoluteIUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MolalityOfSoluteISetter(TypeSafeSetter):
    """MolalityOfSoluteI-specific setter with only molality of solute "i" units."""
    
    def __init__(self, variable: 'MolalityOfSoluteI', value: float):
        super().__init__(variable, value)
    
    # Only molality of solute "i" units available - compile-time safe!
    @property
    def gram_moles_of_i_per_kilograms(self) -> 'MolalityOfSoluteI':
        self.variable.quantity = FastQuantity(self.value, MolalityOfSoluteIUnits.gram_moles_of_i_per_kilogram)
        return cast('MolalityOfSoluteI', self.variable)
    @property
    def kilogram_mols_of_i_per_kilograms(self) -> 'MolalityOfSoluteI':
        self.variable.quantity = FastQuantity(self.value, MolalityOfSoluteIUnits.kilogram_mols_of_i_per_kilogram)
        return cast('MolalityOfSoluteI', self.variable)
    @property
    def kmols_of_i_per_kilograms(self) -> 'MolalityOfSoluteI':
        self.variable.quantity = FastQuantity(self.value, MolalityOfSoluteIUnits.kmols_of_i_per_kilogram)
        return cast('MolalityOfSoluteI', self.variable)
    @property
    def mols_of_i_per_grams(self) -> 'MolalityOfSoluteI':
        self.variable.quantity = FastQuantity(self.value, MolalityOfSoluteIUnits.mols_of_i_per_gram)
        return cast('MolalityOfSoluteI', self.variable)
    @property
    def pound_moles_of_i_per_pound_mass(self) -> 'MolalityOfSoluteI':
        self.variable.quantity = FastQuantity(self.value, MolalityOfSoluteIUnits.pound_moles_of_i_per_pound_mass)
        return cast('MolalityOfSoluteI', self.variable)
    
    # Short aliases for convenience
    pass


class MolalityOfSoluteI(TypedVariable):
    """Type-safe molality of solute "i" variable with expression capabilities."""
    
    _setter_class = MolalityOfSoluteISetter
    _expected_dimension = MOLALITY
    _default_unit_property = "gram_moles_of_i_per_kilograms"
    
    def set(self, value: float) -> MolalityOfSoluteISetter:
        """Create a molality of solute "i" setter for this variable with proper type annotation."""
        return MolalityOfSoluteISetter(self, value)


class MolalityOfSoluteIModule(VariableModule):
    """MolalityOfSoluteI variable module definition."""
    
    def get_variable_class(self):
        return MolalityOfSoluteI
    
    def get_setter_class(self):
        return MolalityOfSoluteISetter
    
    def get_expected_dimension(self):
        return MOLALITY


# Register this module for auto-discovery
VARIABLE_MODULE = MolalityOfSoluteIModule()