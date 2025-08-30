"""
Forcebody Variable Module
==========================

Type-safe force (body) variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import FORCE_BODY
from ..units import ForcebodyUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ForcebodySetter(TypeSafeSetter):
    """Forcebody-specific setter with only force (body) units."""
    
    def __init__(self, variable: 'Forcebody', value: float):
        super().__init__(variable, value)
    
    # Only force (body) units available - compile-time safe!
    @property
    def dyne_per_cubic_centimeters(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.dyne_per_cubic_centimeter)
        return cast('Forcebody', self.variable)
    @property
    def kilogram_force_per_cubic_centimeters(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.kilogram_force_per_cubic_centimeter)
        return cast('Forcebody', self.variable)
    @property
    def kilogram_force_per_cubic_meters(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.kilogram_force_per_cubic_meter)
        return cast('Forcebody', self.variable)
    @property
    def newton_per_cubic_meters(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.newton_per_cubic_meter)
        return cast('Forcebody', self.variable)
    @property
    def pound_force_per_cubic_foots(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.pound_force_per_cubic_foot)
        return cast('Forcebody', self.variable)
    @property
    def pound_force_per_cubic_inchs(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.pound_force_per_cubic_inch)
        return cast('Forcebody', self.variable)
    @property
    def ton_force_per_cubic_foots(self) -> 'Forcebody':
        self.variable.quantity = FastQuantity(self.value, ForcebodyUnits.ton_force_per_cubic_foot)
        return cast('Forcebody', self.variable)
    
    # Short aliases for convenience
    pass


class Forcebody(TypedVariable):
    """Type-safe force (body) variable with expression capabilities."""
    
    _setter_class = ForcebodySetter
    _expected_dimension = FORCE_BODY
    _default_unit_property = "dyne_per_cubic_centimeters"
    
    def set(self, value: float) -> ForcebodySetter:
        """Create a force (body) setter for this variable with proper type annotation."""
        return ForcebodySetter(self, value)


class ForcebodyModule(VariableModule):
    """Forcebody variable module definition."""
    
    def get_variable_class(self):
        return Forcebody
    
    def get_setter_class(self):
        return ForcebodySetter
    
    def get_expected_dimension(self):
        return FORCE_BODY


# Register this module for auto-discovery
VARIABLE_MODULE = ForcebodyModule()