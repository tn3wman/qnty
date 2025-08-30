"""
SpecificGravity Variable Module
================================

Type-safe specific gravity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import SpecificGravityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SpecificGravitySetter(TypeSafeSetter):
    """SpecificGravity-specific setter with only specific gravity units."""
    
    def __init__(self, variable: 'SpecificGravity', value: float):
        super().__init__(variable, value)
    
    # Only specific gravity units available - compile-time safe!
    @property
    def dimensionless(self) -> 'SpecificGravity':
        self.variable.quantity = FastQuantity(self.value, SpecificGravityUnits.dimensionless)
        return cast('SpecificGravity', self.variable)
    
    # Short aliases for convenience
    pass


class SpecificGravity(TypedVariable):
    """Type-safe specific gravity variable with expression capabilities."""
    
    _setter_class = SpecificGravitySetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "dimensionless"
    
    def set(self, value: float) -> SpecificGravitySetter:
        """Create a specific gravity setter for this variable with proper type annotation."""
        return SpecificGravitySetter(self, value)


class SpecificGravityModule(VariableModule):
    """SpecificGravity variable module definition."""
    
    def get_variable_class(self):
        return SpecificGravity
    
    def get_setter_class(self):
        return SpecificGravitySetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = SpecificGravityModule()