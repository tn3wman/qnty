"""
LinearMassDensity Variable Module
==================================

Type-safe linear mass density variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS_DENSITY
from ..units import LinearMassDensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class LinearMassDensitySetter(TypeSafeSetter):
    """LinearMassDensity-specific setter with only linear mass density units."""
    
    def __init__(self, variable: 'LinearMassDensity', value: float):
        super().__init__(variable, value)
    
    # Only linear mass density units available - compile-time safe!
    @property
    def deniers(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.denier)
        return cast('LinearMassDensity', self.variable)
    @property
    def kilogram_per_centimeters(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.kilogram_per_centimeter)
        return cast('LinearMassDensity', self.variable)
    @property
    def kilogram_per_meters(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.kilogram_per_meter)
        return cast('LinearMassDensity', self.variable)
    @property
    def pound_per_foots(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.pound_per_foot)
        return cast('LinearMassDensity', self.variable)
    @property
    def pound_per_inchs(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.pound_per_inch)
        return cast('LinearMassDensity', self.variable)
    @property
    def pound_per_yards(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.pound_per_yard)
        return cast('LinearMassDensity', self.variable)
    @property
    def ton_metric_per_kilometers(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.ton_metric_per_kilometer)
        return cast('LinearMassDensity', self.variable)
    @property
    def ton_metric_per_meters(self) -> 'LinearMassDensity':
        self.variable.quantity = FastQuantity(self.value, LinearMassDensityUnits.ton_metric_per_meter)
        return cast('LinearMassDensity', self.variable)
    
    # Short aliases for convenience
    pass


class LinearMassDensity(TypedVariable):
    """Type-safe linear mass density variable with expression capabilities."""
    
    _setter_class = LinearMassDensitySetter
    _expected_dimension = MASS_DENSITY
    _default_unit_property = "kilogram_per_meters"
    
    def set(self, value: float) -> LinearMassDensitySetter:
        """Create a linear mass density setter for this variable with proper type annotation."""
        return LinearMassDensitySetter(self, value)


class LinearMassDensityModule(VariableModule):
    """LinearMassDensity variable module definition."""
    
    def get_variable_class(self):
        return LinearMassDensity
    
    def get_setter_class(self):
        return LinearMassDensitySetter
    
    def get_expected_dimension(self):
        return MASS_DENSITY


# Register this module for auto-discovery
VARIABLE_MODULE = LinearMassDensityModule()