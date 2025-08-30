"""
HeatOfVaporization Variable Module
===================================

Type-safe heat of vaporization variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import HeatOfVaporizationUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class HeatOfVaporizationSetter(TypeSafeSetter):
    """HeatOfVaporization-specific setter with only heat of vaporization units."""
    
    def __init__(self, variable: 'HeatOfVaporization', value: float):
        super().__init__(variable, value)
    
    # Only heat of vaporization units available - compile-time safe!
    @property
    def british_thermal_unit_per_pounds(self) -> 'HeatOfVaporization':
        self.variable.quantity = FastQuantity(self.value, HeatOfVaporizationUnits.british_thermal_unit_per_pound)
        return cast('HeatOfVaporization', self.variable)
    @property
    def calorie_per_grams(self) -> 'HeatOfVaporization':
        self.variable.quantity = FastQuantity(self.value, HeatOfVaporizationUnits.calorie_per_gram)
        return cast('HeatOfVaporization', self.variable)
    @property
    def chu_per_pounds(self) -> 'HeatOfVaporization':
        self.variable.quantity = FastQuantity(self.value, HeatOfVaporizationUnits.chu_per_pound)
        return cast('HeatOfVaporization', self.variable)
    @property
    def joule_per_kilograms(self) -> 'HeatOfVaporization':
        self.variable.quantity = FastQuantity(self.value, HeatOfVaporizationUnits.joule_per_kilogram)
        return cast('HeatOfVaporization', self.variable)
    
    # Short aliases for convenience
    pass


class HeatOfVaporization(TypedVariable):
    """Type-safe heat of vaporization variable with expression capabilities."""
    
    _setter_class = HeatOfVaporizationSetter
    _expected_dimension = ENERGY
    _default_unit_property = "joule_per_kilograms"
    
    def set(self, value: float) -> HeatOfVaporizationSetter:
        """Create a heat of vaporization setter for this variable with proper type annotation."""
        return HeatOfVaporizationSetter(self, value)


class HeatOfVaporizationModule(VariableModule):
    """HeatOfVaporization variable module definition."""
    
    def get_variable_class(self):
        return HeatOfVaporization
    
    def get_setter_class(self):
        return HeatOfVaporizationSetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = HeatOfVaporizationModule()