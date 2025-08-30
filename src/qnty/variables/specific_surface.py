"""
SpecificSurface Variable Module
================================

Type-safe specific surface variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SPECIFIC_SURFACE
from ..units import SpecificSurfaceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SpecificSurfaceSetter(TypeSafeSetter):
    """SpecificSurface-specific setter with only specific surface units."""
    
    def __init__(self, variable: 'SpecificSurface', value: float):
        super().__init__(variable, value)
    
    # Only specific surface units available - compile-time safe!
    @property
    def square_centimeter_per_grams(self) -> 'SpecificSurface':
        self.variable.quantity = FastQuantity(self.value, SpecificSurfaceUnits.square_centimeter_per_gram)
        return cast('SpecificSurface', self.variable)
    @property
    def square_foot_per_kilograms(self) -> 'SpecificSurface':
        self.variable.quantity = FastQuantity(self.value, SpecificSurfaceUnits.square_foot_per_kilogram)
        return cast('SpecificSurface', self.variable)
    @property
    def square_foot_per_pounds(self) -> 'SpecificSurface':
        self.variable.quantity = FastQuantity(self.value, SpecificSurfaceUnits.square_foot_per_pound)
        return cast('SpecificSurface', self.variable)
    @property
    def square_meter_per_grams(self) -> 'SpecificSurface':
        self.variable.quantity = FastQuantity(self.value, SpecificSurfaceUnits.square_meter_per_gram)
        return cast('SpecificSurface', self.variable)
    @property
    def square_meter_per_kilograms(self) -> 'SpecificSurface':
        self.variable.quantity = FastQuantity(self.value, SpecificSurfaceUnits.square_meter_per_kilogram)
        return cast('SpecificSurface', self.variable)
    
    # Short aliases for convenience
    pass


class SpecificSurface(TypedVariable):
    """Type-safe specific surface variable with expression capabilities."""
    
    _setter_class = SpecificSurfaceSetter
    _expected_dimension = SPECIFIC_SURFACE
    _default_unit_property = "square_meter_per_kilograms"
    
    def set(self, value: float) -> SpecificSurfaceSetter:
        """Create a specific surface setter for this variable with proper type annotation."""
        return SpecificSurfaceSetter(self, value)


class SpecificSurfaceModule(VariableModule):
    """SpecificSurface variable module definition."""
    
    def get_variable_class(self):
        return SpecificSurface
    
    def get_setter_class(self):
        return SpecificSurfaceSetter
    
    def get_expected_dimension(self):
        return SPECIFIC_SURFACE


# Register this module for auto-discovery
VARIABLE_MODULE = SpecificSurfaceModule()