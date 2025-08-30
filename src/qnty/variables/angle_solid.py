"""
AngleSolid Variable Module
===========================

Type-safe angle, solid variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import AngleSolidUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AngleSolidSetter(TypeSafeSetter):
    """AngleSolid-specific setter with only angle, solid units."""
    
    def __init__(self, variable: 'AngleSolid', value: float):
        super().__init__(variable, value)
    
    # Only angle, solid units available - compile-time safe!
    @property
    def spats(self) -> 'AngleSolid':
        self.variable.quantity = FastQuantity(self.value, AngleSolidUnits.spat)
        return cast('AngleSolid', self.variable)
    @property
    def square_degrees(self) -> 'AngleSolid':
        self.variable.quantity = FastQuantity(self.value, AngleSolidUnits.square_degree)
        return cast('AngleSolid', self.variable)
    @property
    def square_gons(self) -> 'AngleSolid':
        self.variable.quantity = FastQuantity(self.value, AngleSolidUnits.square_gon)
        return cast('AngleSolid', self.variable)
    @property
    def steradians(self) -> 'AngleSolid':
        self.variable.quantity = FastQuantity(self.value, AngleSolidUnits.steradian)
        return cast('AngleSolid', self.variable)
    
    # Short aliases for convenience
    pass


class AngleSolid(TypedVariable):
    """Type-safe angle, solid variable with expression capabilities."""
    
    _setter_class = AngleSolidSetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "steradians"
    
    def set(self, value: float) -> AngleSolidSetter:
        """Create a angle, solid setter for this variable with proper type annotation."""
        return AngleSolidSetter(self, value)


class AngleSolidModule(VariableModule):
    """AngleSolid variable module definition."""
    
    def get_variable_class(self):
        return AngleSolid
    
    def get_setter_class(self):
        return AngleSolidSetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = AngleSolidModule()