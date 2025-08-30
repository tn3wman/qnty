"""
Dimensionless Variable Module
============================

Type-safe dimensionless variables with specialized setter and fluent API.
"""

from typing import TYPE_CHECKING, cast

from ..dimension import DIMENSIONLESS
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable

from ..units import DimensionlessUnits


class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with only dimensionless units."""
    
    def __init__(self, variable: 'Dimensionless', value: float):
        super().__init__(variable, value)
    
    # Dimensionless units
    @property
    def dimensionless(self) -> 'Dimensionless':
        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)
        return cast('Dimensionless', self.variable)
    
    # Common alias for no units
    @property
    def unitless(self) -> 'Dimensionless':
        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)
        return cast('Dimensionless', self.variable)


class Dimensionless(TypedVariable):
    """Type-safe dimensionless variable with expression capabilities."""

    _setter_class = DimensionlessSetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "dimensionless"
    
    def set(self, value: float) -> DimensionlessSetter:
        """Create a dimensionless setter for this variable with proper type annotation."""
        return DimensionlessSetter(self, value)


class DimensionlessModule(VariableModule):
    """Dimensionless variable module definition."""
    
    def get_variable_class(self):
        return Dimensionless
    
    def get_setter_class(self):
        return DimensionlessSetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = DimensionlessModule()