"""
SurfaceMassDensity Variable Module
===================================

Type-safe surface mass density variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS_DENSITY
from ..units import SurfaceMassDensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SurfaceMassDensitySetter(TypeSafeSetter):
    """SurfaceMassDensity-specific setter with only surface mass density units."""
    
    def __init__(self, variable: 'SurfaceMassDensity', value: float):
        super().__init__(variable, value)
    
    # Only surface mass density units available - compile-time safe!
    @property
    def gram_per_square_centimeters(self) -> 'SurfaceMassDensity':
        self.variable.quantity = FastQuantity(self.value, SurfaceMassDensityUnits.gram_per_square_centimeter)
        return cast('SurfaceMassDensity', self.variable)
    @property
    def gram_per_square_meters(self) -> 'SurfaceMassDensity':
        self.variable.quantity = FastQuantity(self.value, SurfaceMassDensityUnits.gram_per_square_meter)
        return cast('SurfaceMassDensity', self.variable)
    @property
    def kilogram_per_square_meters(self) -> 'SurfaceMassDensity':
        self.variable.quantity = FastQuantity(self.value, SurfaceMassDensityUnits.kilogram_per_square_meter)
        return cast('SurfaceMassDensity', self.variable)
    @property
    def pound_mass_per_square_foots(self) -> 'SurfaceMassDensity':
        self.variable.quantity = FastQuantity(self.value, SurfaceMassDensityUnits.pound_mass_per_square_foot)
        return cast('SurfaceMassDensity', self.variable)
    @property
    def pound_mass_per_square_inchs(self) -> 'SurfaceMassDensity':
        self.variable.quantity = FastQuantity(self.value, SurfaceMassDensityUnits.pound_mass_per_square_inch)
        return cast('SurfaceMassDensity', self.variable)
    
    # Short aliases for convenience
    pass


class SurfaceMassDensity(TypedVariable):
    """Type-safe surface mass density variable with expression capabilities."""
    
    _setter_class = SurfaceMassDensitySetter
    _expected_dimension = MASS_DENSITY
    _default_unit_property = "kilogram_per_square_meters"
    
    def set(self, value: float) -> SurfaceMassDensitySetter:
        """Create a surface mass density setter for this variable with proper type annotation."""
        return SurfaceMassDensitySetter(self, value)


class SurfaceMassDensityModule(VariableModule):
    """SurfaceMassDensity variable module definition."""
    
    def get_variable_class(self):
        return SurfaceMassDensity
    
    def get_setter_class(self):
        return SurfaceMassDensitySetter
    
    def get_expected_dimension(self):
        return MASS_DENSITY


# Register this module for auto-discovery
VARIABLE_MODULE = SurfaceMassDensityModule()