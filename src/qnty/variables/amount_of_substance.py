"""
AmountOfSubstance Variable Module
==================================

Type-safe amount of substance variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import AMOUNT
from ..units import AmountOfSubstanceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AmountOfSubstanceSetter(TypeSafeSetter):
    """AmountOfSubstance-specific setter with only amount of substance units."""
    
    def __init__(self, variable: 'AmountOfSubstance', value: float):
        super().__init__(variable, value)
    
    # Only amount of substance units available - compile-time safe!
    @property
    def kilogram_mols(self) -> 'AmountOfSubstance':
        self.variable.quantity = FastQuantity(self.value, AmountOfSubstanceUnits.kilogram_mol)
        return cast('AmountOfSubstance', self.variable)
    @property
    def mole_grams(self) -> 'AmountOfSubstance':
        self.variable.quantity = FastQuantity(self.value, AmountOfSubstanceUnits.mole_gram)
        return cast('AmountOfSubstance', self.variable)
    @property
    def poundmoles(self) -> 'AmountOfSubstance':
        self.variable.quantity = FastQuantity(self.value, AmountOfSubstanceUnits.poundmole)
        return cast('AmountOfSubstance', self.variable)
    
    # Short aliases for convenience
    pass


class AmountOfSubstance(TypedVariable):
    """Type-safe amount of substance variable with expression capabilities."""
    
    _setter_class = AmountOfSubstanceSetter
    _expected_dimension = AMOUNT
    _default_unit_property = "mole_grams"
    
    def set(self, value: float) -> AmountOfSubstanceSetter:
        """Create a amount of substance setter for this variable with proper type annotation."""
        return AmountOfSubstanceSetter(self, value)


class AmountOfSubstanceModule(VariableModule):
    """AmountOfSubstance variable module definition."""
    
    def get_variable_class(self):
        return AmountOfSubstance
    
    def get_setter_class(self):
        return AmountOfSubstanceSetter
    
    def get_expected_dimension(self):
        return AMOUNT


# Register this module for auto-discovery
VARIABLE_MODULE = AmountOfSubstanceModule()