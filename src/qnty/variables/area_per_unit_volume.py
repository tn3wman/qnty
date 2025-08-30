"""
AreaPerUnitVolume Variable Module
==================================

Type-safe area per unit volume variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import AREA_PER_UNIT_VOLUME
from ..units import AreaPerUnitVolumeUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AreaPerUnitVolumeSetter(TypeSafeSetter):
    """AreaPerUnitVolume-specific setter with only area per unit volume units."""
    
    def __init__(self, variable: 'AreaPerUnitVolume', value: float):
        super().__init__(variable, value)
    
    # Only area per unit volume units available - compile-time safe!
    @property
    def square_centimeter_per_cubic_centimeters(self) -> 'AreaPerUnitVolume':
        self.variable.quantity = FastQuantity(self.value, AreaPerUnitVolumeUnits.square_centimeter_per_cubic_centimeter)
        return cast('AreaPerUnitVolume', self.variable)
    @property
    def square_foot_per_cubic_foots(self) -> 'AreaPerUnitVolume':
        self.variable.quantity = FastQuantity(self.value, AreaPerUnitVolumeUnits.square_foot_per_cubic_foot)
        return cast('AreaPerUnitVolume', self.variable)
    @property
    def square_meter_per_cubic_meters(self) -> 'AreaPerUnitVolume':
        self.variable.quantity = FastQuantity(self.value, AreaPerUnitVolumeUnits.square_meter_per_cubic_meter)
        return cast('AreaPerUnitVolume', self.variable)
    
    # Short aliases for convenience
    pass


class AreaPerUnitVolume(TypedVariable):
    """Type-safe area per unit volume variable with expression capabilities."""
    
    _setter_class = AreaPerUnitVolumeSetter
    _expected_dimension = AREA_PER_UNIT_VOLUME
    _default_unit_property = "square_meter_per_cubic_meters"
    
    def set(self, value: float) -> AreaPerUnitVolumeSetter:
        """Create a area per unit volume setter for this variable with proper type annotation."""
        return AreaPerUnitVolumeSetter(self, value)


class AreaPerUnitVolumeModule(VariableModule):
    """AreaPerUnitVolume variable module definition."""
    
    def get_variable_class(self):
        return AreaPerUnitVolume
    
    def get_setter_class(self):
        return AreaPerUnitVolumeSetter
    
    def get_expected_dimension(self):
        return AREA_PER_UNIT_VOLUME


# Register this module for auto-discovery
VARIABLE_MODULE = AreaPerUnitVolumeModule()