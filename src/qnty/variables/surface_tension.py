"""
SurfaceTension Variable Module
===============================

Type-safe surface tension variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SURFACE_TENSION
from ..units import SurfaceTensionUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SurfaceTensionSetter(TypeSafeSetter):
    """SurfaceTension-specific setter with only surface tension units."""
    
    def __init__(self, variable: 'SurfaceTension', value: float):
        super().__init__(variable, value)
    
    # Only surface tension units available - compile-time safe!
    @property
    def dyne_per_centimeters(self) -> 'SurfaceTension':
        self.variable.quantity = FastQuantity(self.value, SurfaceTensionUnits.dyne_per_centimeter)
        return cast('SurfaceTension', self.variable)
    @property
    def gram_force_per_centimeters(self) -> 'SurfaceTension':
        self.variable.quantity = FastQuantity(self.value, SurfaceTensionUnits.gram_force_per_centimeter)
        return cast('SurfaceTension', self.variable)
    @property
    def newton_per_meters(self) -> 'SurfaceTension':
        self.variable.quantity = FastQuantity(self.value, SurfaceTensionUnits.newton_per_meter)
        return cast('SurfaceTension', self.variable)
    @property
    def pound_force_per_foots(self) -> 'SurfaceTension':
        self.variable.quantity = FastQuantity(self.value, SurfaceTensionUnits.pound_force_per_foot)
        return cast('SurfaceTension', self.variable)
    @property
    def pound_force_per_inchs(self) -> 'SurfaceTension':
        self.variable.quantity = FastQuantity(self.value, SurfaceTensionUnits.pound_force_per_inch)
        return cast('SurfaceTension', self.variable)
    
    # Short aliases for convenience
    pass


class SurfaceTension(TypedVariable):
    """Type-safe surface tension variable with expression capabilities."""
    
    _setter_class = SurfaceTensionSetter
    _expected_dimension = SURFACE_TENSION
    _default_unit_property = "newton_per_meters"
    
    def set(self, value: float) -> SurfaceTensionSetter:
        """Create a surface tension setter for this variable with proper type annotation."""
        return SurfaceTensionSetter(self, value)


class SurfaceTensionModule(VariableModule):
    """SurfaceTension variable module definition."""
    
    def get_variable_class(self):
        return SurfaceTension
    
    def get_setter_class(self):
        return SurfaceTensionSetter
    
    def get_expected_dimension(self):
        return SURFACE_TENSION


# Register this module for auto-discovery
VARIABLE_MODULE = SurfaceTensionModule()