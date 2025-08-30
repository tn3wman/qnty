"""
MoleFractionOfI Variable Module
================================

Type-safe mole fraction of "i" variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import MoleFractionOfIUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MoleFractionOfISetter(TypeSafeSetter):
    """MoleFractionOfI-specific setter with only mole fraction of "i" units."""
    
    def __init__(self, variable: 'MoleFractionOfI', value: float):
        super().__init__(variable, value)
    
    # Only mole fraction of "i" units available - compile-time safe!
    @property
    def gram_mole_of_i_per_gram_mole_totals(self) -> 'MoleFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MoleFractionOfIUnits.gram_mole_of_i_per_gram_mole_total)
        return cast('MoleFractionOfI', self.variable)
    @property
    def kilogram_mole_of_i_per_kilogram_mole_totals(self) -> 'MoleFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MoleFractionOfIUnits.kilogram_mole_of_i_per_kilogram_mole_total)
        return cast('MoleFractionOfI', self.variable)
    @property
    def kilomole_of_i_per_kilomole_totals(self) -> 'MoleFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MoleFractionOfIUnits.kilomole_of_i_per_kilomole_total)
        return cast('MoleFractionOfI', self.variable)
    @property
    def pound_mole_of_i_per_pound_mole_totals(self) -> 'MoleFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MoleFractionOfIUnits.pound_mole_of_i_per_pound_mole_total)
        return cast('MoleFractionOfI', self.variable)
    
    # Short aliases for convenience
    pass


class MoleFractionOfI(TypedVariable):
    """Type-safe mole fraction of "i" variable with expression capabilities."""
    
    _setter_class = MoleFractionOfISetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "gram_mole_of_i_per_gram_mole_totals"
    
    def set(self, value: float) -> MoleFractionOfISetter:
        """Create a mole fraction of "i" setter for this variable with proper type annotation."""
        return MoleFractionOfISetter(self, value)


class MoleFractionOfIModule(VariableModule):
    """MoleFractionOfI variable module definition."""
    
    def get_variable_class(self):
        return MoleFractionOfI
    
    def get_setter_class(self):
        return MoleFractionOfISetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = MoleFractionOfIModule()