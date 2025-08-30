"""
NormalityOfSolution Variable Module
====================================

Type-safe normality of solution variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import NORMALITY
from ..units import NormalityOfSolutionUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class NormalityOfSolutionSetter(TypeSafeSetter):
    """NormalityOfSolution-specific setter with only normality of solution units."""
    
    def __init__(self, variable: 'NormalityOfSolution', value: float):
        super().__init__(variable, value)
    
    # Only normality of solution units available - compile-time safe!
    @property
    def gram_equivalents_per_cubic_meters(self) -> 'NormalityOfSolution':
        self.variable.quantity = FastQuantity(self.value, NormalityOfSolutionUnits.gram_equivalents_per_cubic_meter)
        return cast('NormalityOfSolution', self.variable)
    @property
    def gram_equivalents_per_liters(self) -> 'NormalityOfSolution':
        self.variable.quantity = FastQuantity(self.value, NormalityOfSolutionUnits.gram_equivalents_per_liter)
        return cast('NormalityOfSolution', self.variable)
    @property
    def pound_equivalents_per_cubic_foots(self) -> 'NormalityOfSolution':
        self.variable.quantity = FastQuantity(self.value, NormalityOfSolutionUnits.pound_equivalents_per_cubic_foot)
        return cast('NormalityOfSolution', self.variable)
    @property
    def pound_equivalents_per_gallons(self) -> 'NormalityOfSolution':
        self.variable.quantity = FastQuantity(self.value, NormalityOfSolutionUnits.pound_equivalents_per_gallon)
        return cast('NormalityOfSolution', self.variable)
    
    # Short aliases for convenience
    pass


class NormalityOfSolution(TypedVariable):
    """Type-safe normality of solution variable with expression capabilities."""
    
    _setter_class = NormalityOfSolutionSetter
    _expected_dimension = NORMALITY
    _default_unit_property = "gram_equivalents_per_cubic_meters"
    
    def set(self, value: float) -> NormalityOfSolutionSetter:
        """Create a normality of solution setter for this variable with proper type annotation."""
        return NormalityOfSolutionSetter(self, value)


class NormalityOfSolutionModule(VariableModule):
    """NormalityOfSolution variable module definition."""
    
    def get_variable_class(self):
        return NormalityOfSolution
    
    def get_setter_class(self):
        return NormalityOfSolutionSetter
    
    def get_expected_dimension(self):
        return NORMALITY


# Register this module for auto-discovery
VARIABLE_MODULE = NormalityOfSolutionModule()