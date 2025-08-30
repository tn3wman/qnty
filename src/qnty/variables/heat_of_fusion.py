"""
HeatOfFusion Variable Module
=============================

Type-safe heat of fusion variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import HeatOfFusionUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class HeatOfFusionSetter(TypeSafeSetter):
    """HeatOfFusion-specific setter with only heat of fusion units."""
    
    def __init__(self, variable: 'HeatOfFusion', value: float):
        super().__init__(variable, value)
    
    # Only heat of fusion units available - compile-time safe!
    @property
    def british_thermal_unit_mean_per_pounds(self) -> 'HeatOfFusion':
        self.variable.quantity = FastQuantity(self.value, HeatOfFusionUnits.british_thermal_unit_mean_per_pound)
        return cast('HeatOfFusion', self.variable)
    @property
    def british_thermal_unit_per_pounds(self) -> 'HeatOfFusion':
        self.variable.quantity = FastQuantity(self.value, HeatOfFusionUnits.british_thermal_unit_per_pound)
        return cast('HeatOfFusion', self.variable)
    @property
    def calorie_per_grams(self) -> 'HeatOfFusion':
        self.variable.quantity = FastQuantity(self.value, HeatOfFusionUnits.calorie_per_gram)
        return cast('HeatOfFusion', self.variable)
    @property
    def chu_per_pounds(self) -> 'HeatOfFusion':
        self.variable.quantity = FastQuantity(self.value, HeatOfFusionUnits.chu_per_pound)
        return cast('HeatOfFusion', self.variable)
    @property
    def joule_per_kilograms(self) -> 'HeatOfFusion':
        self.variable.quantity = FastQuantity(self.value, HeatOfFusionUnits.joule_per_kilogram)
        return cast('HeatOfFusion', self.variable)
    
    # Short aliases for convenience
    pass


class HeatOfFusion(TypedVariable):
    """Type-safe heat of fusion variable with expression capabilities."""
    
    _setter_class = HeatOfFusionSetter
    _expected_dimension = ENERGY
    _default_unit_property = "joule_per_kilograms"
    
    def set(self, value: float) -> HeatOfFusionSetter:
        """Create a heat of fusion setter for this variable with proper type annotation."""
        return HeatOfFusionSetter(self, value)


class HeatOfFusionModule(VariableModule):
    """HeatOfFusion variable module definition."""
    
    def get_variable_class(self):
        return HeatOfFusion
    
    def get_setter_class(self):
        return HeatOfFusionSetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = HeatOfFusionModule()