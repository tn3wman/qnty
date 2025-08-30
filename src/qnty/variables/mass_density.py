"""
MassDensity Variable Module
============================

Type-safe mass density variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS_DENSITY
from ..units import MassDensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MassDensitySetter(TypeSafeSetter):
    """MassDensity-specific setter with only mass density units."""
    
    def __init__(self, variable: 'MassDensity', value: float):
        super().__init__(variable, value)
    
    # Only mass density units available - compile-time safe!
    @property
    def gram_per_cubic_centimeters(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.gram_per_cubic_centimeter)
        return cast('MassDensity', self.variable)
    @property
    def gram_per_cubic_decimeters(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.gram_per_cubic_decimeter)
        return cast('MassDensity', self.variable)
    @property
    def gram_per_cubic_meters(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.gram_per_cubic_meter)
        return cast('MassDensity', self.variable)
    @property
    def gram_per_liters(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.gram_per_liter)
        return cast('MassDensity', self.variable)
    @property
    def kilogram_per_cubic_meters(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.kilogram_per_cubic_meter)
        return cast('MassDensity', self.variable)
    @property
    def ounce_avdp_per_us_gallons(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.ounce_avdp_per_us_gallon)
        return cast('MassDensity', self.variable)
    @property
    def pound_avdp_per_cubic_foots(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.pound_avdp_per_cubic_foot)
        return cast('MassDensity', self.variable)
    @property
    def pound_avdp_per_us_gallons(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.pound_avdp_per_us_gallon)
        return cast('MassDensity', self.variable)
    @property
    def pound_mass_per_cubic_inchs(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.pound_mass_per_cubic_inch)
        return cast('MassDensity', self.variable)
    @property
    def ton_metric_per_cubic_meters(self) -> 'MassDensity':
        self.variable.quantity = FastQuantity(self.value, MassDensityUnits.ton_metric_per_cubic_meter)
        return cast('MassDensity', self.variable)
    
    # Short aliases for convenience
    pass


class MassDensity(TypedVariable):
    """Type-safe mass density variable with expression capabilities."""
    
    _setter_class = MassDensitySetter
    _expected_dimension = MASS_DENSITY
    _default_unit_property = "gram_per_cubic_decimeters"
    
    def set(self, value: float) -> MassDensitySetter:
        """Create a mass density setter for this variable with proper type annotation."""
        return MassDensitySetter(self, value)


class MassDensityModule(VariableModule):
    """MassDensity variable module definition."""
    
    def get_variable_class(self):
        return MassDensity
    
    def get_setter_class(self):
        return MassDensitySetter
    
    def get_expected_dimension(self):
        return MASS_DENSITY


# Register this module for auto-discovery
VARIABLE_MODULE = MassDensityModule()