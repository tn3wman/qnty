"""
MolarityOfI Variable Module
============================

Type-safe molarity of "i" variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MOLARITY
from ..units import MolarityOfIUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MolarityOfISetter(TypeSafeSetter):
    """MolarityOfI-specific setter with only molarity of "i" units."""
    
    def __init__(self, variable: 'MolarityOfI', value: float):
        super().__init__(variable, value)
    
    # Only molarity of "i" units available - compile-time safe!
    @property
    def gram_moles_of_i_per_cubic_meters(self) -> 'MolarityOfI':
        self.variable.quantity = FastQuantity(self.value, MolarityOfIUnits.gram_moles_of_i_per_cubic_meter)
        return cast('MolarityOfI', self.variable)
    @property
    def gram_moles_of_i_per_liters(self) -> 'MolarityOfI':
        self.variable.quantity = FastQuantity(self.value, MolarityOfIUnits.gram_moles_of_i_per_liter)
        return cast('MolarityOfI', self.variable)
    @property
    def kilogram_moles_of_i_per_cubic_meters(self) -> 'MolarityOfI':
        self.variable.quantity = FastQuantity(self.value, MolarityOfIUnits.kilogram_moles_of_i_per_cubic_meter)
        return cast('MolarityOfI', self.variable)
    @property
    def kilogram_moles_of_i_per_liters(self) -> 'MolarityOfI':
        self.variable.quantity = FastQuantity(self.value, MolarityOfIUnits.kilogram_moles_of_i_per_liter)
        return cast('MolarityOfI', self.variable)
    @property
    def pound_moles_of_i_per_cubic_foots(self) -> 'MolarityOfI':
        self.variable.quantity = FastQuantity(self.value, MolarityOfIUnits.pound_moles_of_i_per_cubic_foot)
        return cast('MolarityOfI', self.variable)
    @property
    def pound_moles_of_per_gallon_us(self) -> 'MolarityOfI':
        self.variable.quantity = FastQuantity(self.value, MolarityOfIUnits.pound_moles_of_per_gallon_us)
        return cast('MolarityOfI', self.variable)
    
    # Short aliases for convenience
    pass


class MolarityOfI(TypedVariable):
    """Type-safe molarity of "i" variable with expression capabilities."""
    
    _setter_class = MolarityOfISetter
    _expected_dimension = MOLARITY
    _default_unit_property = "gram_moles_of_i_per_cubic_meters"
    
    def set(self, value: float) -> MolarityOfISetter:
        """Create a molarity of "i" setter for this variable with proper type annotation."""
        return MolarityOfISetter(self, value)


class MolarityOfIModule(VariableModule):
    """MolarityOfI variable module definition."""
    
    def get_variable_class(self):
        return MolarityOfI
    
    def get_setter_class(self):
        return MolarityOfISetter
    
    def get_expected_dimension(self):
        return MOLARITY


# Register this module for auto-discovery
VARIABLE_MODULE = MolarityOfIModule()