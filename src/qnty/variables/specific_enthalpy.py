"""
SpecificEnthalpy Variable Module
=================================

Type-safe specific enthalpy variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import SpecificEnthalpyUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SpecificEnthalpySetter(TypeSafeSetter):
    """SpecificEnthalpy-specific setter with only specific enthalpy units."""
    
    def __init__(self, variable: 'SpecificEnthalpy', value: float):
        super().__init__(variable, value)
    
    # Only specific enthalpy units available - compile-time safe!
    @property
    def british_thermal_unit_mean_per_pounds(self) -> 'SpecificEnthalpy':
        self.variable.quantity = FastQuantity(self.value, SpecificEnthalpyUnits.british_thermal_unit_mean_per_pound)
        return cast('SpecificEnthalpy', self.variable)
    @property
    def british_thermal_unit_per_pounds(self) -> 'SpecificEnthalpy':
        self.variable.quantity = FastQuantity(self.value, SpecificEnthalpyUnits.british_thermal_unit_per_pound)
        return cast('SpecificEnthalpy', self.variable)
    @property
    def calorie_per_grams(self) -> 'SpecificEnthalpy':
        self.variable.quantity = FastQuantity(self.value, SpecificEnthalpyUnits.calorie_per_gram)
        return cast('SpecificEnthalpy', self.variable)
    @property
    def chu_per_pounds(self) -> 'SpecificEnthalpy':
        self.variable.quantity = FastQuantity(self.value, SpecificEnthalpyUnits.chu_per_pound)
        return cast('SpecificEnthalpy', self.variable)
    @property
    def joule_per_kilograms(self) -> 'SpecificEnthalpy':
        self.variable.quantity = FastQuantity(self.value, SpecificEnthalpyUnits.joule_per_kilogram)
        return cast('SpecificEnthalpy', self.variable)
    @property
    def kilojoule_per_kilograms(self) -> 'SpecificEnthalpy':
        self.variable.quantity = FastQuantity(self.value, SpecificEnthalpyUnits.kilojoule_per_kilogram)
        return cast('SpecificEnthalpy', self.variable)
    
    # Short aliases for convenience
    pass


class SpecificEnthalpy(TypedVariable):
    """Type-safe specific enthalpy variable with expression capabilities."""
    
    _setter_class = SpecificEnthalpySetter
    _expected_dimension = ENERGY
    _default_unit_property = "joule_per_kilograms"
    
    def set(self, value: float) -> SpecificEnthalpySetter:
        """Create a specific enthalpy setter for this variable with proper type annotation."""
        return SpecificEnthalpySetter(self, value)


class SpecificEnthalpyModule(VariableModule):
    """SpecificEnthalpy variable module definition."""
    
    def get_variable_class(self):
        return SpecificEnthalpy
    
    def get_setter_class(self):
        return SpecificEnthalpySetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = SpecificEnthalpyModule()