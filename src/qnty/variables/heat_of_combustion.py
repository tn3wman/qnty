"""
HeatOfCombustion Variable Module
=================================

Type-safe heat of combustion variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import HeatOfCombustionUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class HeatOfCombustionSetter(TypeSafeSetter):
    """HeatOfCombustion-specific setter with only heat of combustion units."""
    
    def __init__(self, variable: 'HeatOfCombustion', value: float):
        super().__init__(variable, value)
    
    # Only heat of combustion units available - compile-time safe!
    @property
    def british_thermal_unit_per_pounds(self) -> 'HeatOfCombustion':
        self.variable.quantity = FastQuantity(self.value, HeatOfCombustionUnits.british_thermal_unit_per_pound)
        return cast('HeatOfCombustion', self.variable)
    @property
    def calorie_per_grams(self) -> 'HeatOfCombustion':
        self.variable.quantity = FastQuantity(self.value, HeatOfCombustionUnits.calorie_per_gram)
        return cast('HeatOfCombustion', self.variable)
    @property
    def chu_per_pounds(self) -> 'HeatOfCombustion':
        self.variable.quantity = FastQuantity(self.value, HeatOfCombustionUnits.chu_per_pound)
        return cast('HeatOfCombustion', self.variable)
    @property
    def joule_per_kilograms(self) -> 'HeatOfCombustion':
        self.variable.quantity = FastQuantity(self.value, HeatOfCombustionUnits.joule_per_kilogram)
        return cast('HeatOfCombustion', self.variable)
    
    # Short aliases for convenience
    pass


class HeatOfCombustion(TypedVariable):
    """Type-safe heat of combustion variable with expression capabilities."""
    
    _setter_class = HeatOfCombustionSetter
    _expected_dimension = ENERGY
    _default_unit_property = "joule_per_kilograms"
    
    def set(self, value: float) -> HeatOfCombustionSetter:
        """Create a heat of combustion setter for this variable with proper type annotation."""
        return HeatOfCombustionSetter(self, value)


class HeatOfCombustionModule(VariableModule):
    """HeatOfCombustion variable module definition."""
    
    def get_variable_class(self):
        return HeatOfCombustion
    
    def get_setter_class(self):
        return HeatOfCombustionSetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = HeatOfCombustionModule()