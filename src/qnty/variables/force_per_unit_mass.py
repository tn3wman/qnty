"""
ForcePerUnitMass Variable Module
=================================

Type-safe force per unit mass variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ACCELERATION
from ..units import ForcePerUnitMassUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ForcePerUnitMassSetter(TypeSafeSetter):
    """ForcePerUnitMass-specific setter with only force per unit mass units."""
    
    def __init__(self, variable: 'ForcePerUnitMass', value: float):
        super().__init__(variable, value)
    
    # Only force per unit mass units available - compile-time safe!
    @property
    def dyne_per_grams(self) -> 'ForcePerUnitMass':
        self.variable.quantity = FastQuantity(self.value, ForcePerUnitMassUnits.dyne_per_gram)
        return cast('ForcePerUnitMass', self.variable)
    @property
    def kilogram_force_per_kilograms(self) -> 'ForcePerUnitMass':
        self.variable.quantity = FastQuantity(self.value, ForcePerUnitMassUnits.kilogram_force_per_kilogram)
        return cast('ForcePerUnitMass', self.variable)
    @property
    def newton_per_kilograms(self) -> 'ForcePerUnitMass':
        self.variable.quantity = FastQuantity(self.value, ForcePerUnitMassUnits.newton_per_kilogram)
        return cast('ForcePerUnitMass', self.variable)
    @property
    def pound_force_per_pound_mass(self) -> 'ForcePerUnitMass':
        self.variable.quantity = FastQuantity(self.value, ForcePerUnitMassUnits.pound_force_per_pound_mass)
        return cast('ForcePerUnitMass', self.variable)
    @property
    def pound_force_per_slugs(self) -> 'ForcePerUnitMass':
        self.variable.quantity = FastQuantity(self.value, ForcePerUnitMassUnits.pound_force_per_slug)
        return cast('ForcePerUnitMass', self.variable)
    
    # Short aliases for convenience
    pass


class ForcePerUnitMass(TypedVariable):
    """Type-safe force per unit mass variable with expression capabilities."""
    
    _setter_class = ForcePerUnitMassSetter
    _expected_dimension = ACCELERATION
    _default_unit_property = "newton_per_kilograms"
    
    def set(self, value: float) -> ForcePerUnitMassSetter:
        """Create a force per unit mass setter for this variable with proper type annotation."""
        return ForcePerUnitMassSetter(self, value)


class ForcePerUnitMassModule(VariableModule):
    """ForcePerUnitMass variable module definition."""
    
    def get_variable_class(self):
        return ForcePerUnitMass
    
    def get_setter_class(self):
        return ForcePerUnitMassSetter
    
    def get_expected_dimension(self):
        return ACCELERATION


# Register this module for auto-discovery
VARIABLE_MODULE = ForcePerUnitMassModule()