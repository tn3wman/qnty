"""
MassFractionOfI Variable Module
================================

Type-safe mass fraction of "i" variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import MassFractionOfIUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MassFractionOfISetter(TypeSafeSetter):
    """MassFractionOfI-specific setter with only mass fraction of "i" units."""
    
    def __init__(self, variable: 'MassFractionOfI', value: float):
        super().__init__(variable, value)
    
    # Only mass fraction of "i" units available - compile-time safe!
    @property
    def grains_of_i_per_pound_totals(self) -> 'MassFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MassFractionOfIUnits.grains_of_i_per_pound_total)
        return cast('MassFractionOfI', self.variable)
    @property
    def gram_of_i_per_kilogram_totals(self) -> 'MassFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MassFractionOfIUnits.gram_of_i_per_kilogram_total)
        return cast('MassFractionOfI', self.variable)
    @property
    def kilogram_of_i_per_kilogram_totals(self) -> 'MassFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MassFractionOfIUnits.kilogram_of_i_per_kilogram_total)
        return cast('MassFractionOfI', self.variable)
    @property
    def pound_of_i_per_pound_totals(self) -> 'MassFractionOfI':
        self.variable.quantity = FastQuantity(self.value, MassFractionOfIUnits.pound_of_i_per_pound_total)
        return cast('MassFractionOfI', self.variable)
    
    # Short aliases for convenience
    pass


class MassFractionOfI(TypedVariable):
    """Type-safe mass fraction of "i" variable with expression capabilities."""
    
    _setter_class = MassFractionOfISetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "kilogram_of_i_per_kilogram_totals"
    
    def set(self, value: float) -> MassFractionOfISetter:
        """Create a mass fraction of "i" setter for this variable with proper type annotation."""
        return MassFractionOfISetter(self, value)


class MassFractionOfIModule(VariableModule):
    """MassFractionOfI variable module definition."""
    
    def get_variable_class(self):
        return MassFractionOfI
    
    def get_setter_class(self):
        return MassFractionOfISetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = MassFractionOfIModule()