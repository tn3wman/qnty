"""
VolumetricCalorificheatingValue Variable Module
================================================

Type-safe volumetric calorific (heating) value variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import PRESSURE
from ..units import VolumetricCalorificheatingValueUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumetricCalorificheatingValueSetter(TypeSafeSetter):
    """VolumetricCalorificheatingValue-specific setter with only volumetric calorific (heating) value units."""
    
    def __init__(self, variable: 'VolumetricCalorificheatingValue', value: float):
        super().__init__(variable, value)
    
    # Only volumetric calorific (heating) value units available - compile-time safe!
    @property
    def british_thermal_unit_per_cubic_foots(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.british_thermal_unit_per_cubic_foot)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def british_thermal_unit_per_gallon_uks(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.british_thermal_unit_per_gallon_uk)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def british_thermal_unit_per_gallon_us(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.british_thermal_unit_per_gallon_us)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def calorie_per_cubic_centimeters(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.calorie_per_cubic_centimeter)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def chu_per_cubic_foots(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.chu_per_cubic_foot)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def joule_per_cubic_meters(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.joule_per_cubic_meter)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def kilocalorie_per_cubic_foots(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.kilocalorie_per_cubic_foot)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def kilocalorie_per_cubic_meters(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.kilocalorie_per_cubic_meter)
        return cast('VolumetricCalorificheatingValue', self.variable)
    @property
    def therm_100_k_btu_per_cubic_foots(self) -> 'VolumetricCalorificheatingValue':
        self.variable.quantity = FastQuantity(self.value, VolumetricCalorificheatingValueUnits.therm_100_k_btu_per_cubic_foot)
        return cast('VolumetricCalorificheatingValue', self.variable)
    
    # Short aliases for convenience
    pass


class VolumetricCalorificheatingValue(TypedVariable):
    """Type-safe volumetric calorific (heating) value variable with expression capabilities."""
    
    _setter_class = VolumetricCalorificheatingValueSetter
    _expected_dimension = PRESSURE
    _default_unit_property = "british_thermal_unit_per_cubic_foots"
    
    def set(self, value: float) -> VolumetricCalorificheatingValueSetter:
        """Create a volumetric calorific (heating) value setter for this variable with proper type annotation."""
        return VolumetricCalorificheatingValueSetter(self, value)


class VolumetricCalorificheatingValueModule(VariableModule):
    """VolumetricCalorificheatingValue variable module definition."""
    
    def get_variable_class(self):
        return VolumetricCalorificheatingValue
    
    def get_setter_class(self):
        return VolumetricCalorificheatingValueSetter
    
    def get_expected_dimension(self):
        return PRESSURE


# Register this module for auto-discovery
VARIABLE_MODULE = VolumetricCalorificheatingValueModule()