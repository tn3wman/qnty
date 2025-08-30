"""
SpecificVolume Variable Module
===============================

Type-safe specific volume variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SPECIFIC_VOLUME
from ..units import SpecificVolumeUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SpecificVolumeSetter(TypeSafeSetter):
    """SpecificVolume-specific setter with only specific volume units."""
    
    def __init__(self, variable: 'SpecificVolume', value: float):
        super().__init__(variable, value)
    
    # Only specific volume units available - compile-time safe!
    @property
    def cubic_centimeter_per_grams(self) -> 'SpecificVolume':
        self.variable.quantity = FastQuantity(self.value, SpecificVolumeUnits.cubic_centimeter_per_gram)
        return cast('SpecificVolume', self.variable)
    @property
    def cubic_foot_per_kilograms(self) -> 'SpecificVolume':
        self.variable.quantity = FastQuantity(self.value, SpecificVolumeUnits.cubic_foot_per_kilogram)
        return cast('SpecificVolume', self.variable)
    @property
    def cubic_foot_per_pounds(self) -> 'SpecificVolume':
        self.variable.quantity = FastQuantity(self.value, SpecificVolumeUnits.cubic_foot_per_pound)
        return cast('SpecificVolume', self.variable)
    @property
    def cubic_meter_per_kilograms(self) -> 'SpecificVolume':
        self.variable.quantity = FastQuantity(self.value, SpecificVolumeUnits.cubic_meter_per_kilogram)
        return cast('SpecificVolume', self.variable)
    
    # Short aliases for convenience
    pass


class SpecificVolume(TypedVariable):
    """Type-safe specific volume variable with expression capabilities."""
    
    _setter_class = SpecificVolumeSetter
    _expected_dimension = SPECIFIC_VOLUME
    _default_unit_property = "cubic_meter_per_kilograms"
    
    def set(self, value: float) -> SpecificVolumeSetter:
        """Create a specific volume setter for this variable with proper type annotation."""
        return SpecificVolumeSetter(self, value)


class SpecificVolumeModule(VariableModule):
    """SpecificVolume variable module definition."""
    
    def get_variable_class(self):
        return SpecificVolume
    
    def get_setter_class(self):
        return SpecificVolumeSetter
    
    def get_expected_dimension(self):
        return SPECIFIC_VOLUME


# Register this module for auto-discovery
VARIABLE_MODULE = SpecificVolumeModule()