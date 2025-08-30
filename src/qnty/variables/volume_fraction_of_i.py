"""
VolumeFractionOfI Variable Module
==================================

Type-safe volume fraction of "i" variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import VolumeFractionOfIUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumeFractionOfISetter(TypeSafeSetter):
    """VolumeFractionOfI-specific setter with only volume fraction of "i" units."""
    
    def __init__(self, variable: 'VolumeFractionOfI', value: float):
        super().__init__(variable, value)
    
    # Only volume fraction of "i" units available - compile-time safe!
    @property
    def cubic_centimeters_of_i_per_cubic_meter_totals(self) -> 'VolumeFractionOfI':
        self.variable.quantity = FastQuantity(self.value, VolumeFractionOfIUnits.cubic_centimeters_of_i_per_cubic_meter_total)
        return cast('VolumeFractionOfI', self.variable)
    @property
    def cubic_foot_of_i_per_cubic_foot_totals(self) -> 'VolumeFractionOfI':
        self.variable.quantity = FastQuantity(self.value, VolumeFractionOfIUnits.cubic_foot_of_i_per_cubic_foot_total)
        return cast('VolumeFractionOfI', self.variable)
    @property
    def cubic_meters_of_i_per_cubic_meter_totals(self) -> 'VolumeFractionOfI':
        self.variable.quantity = FastQuantity(self.value, VolumeFractionOfIUnits.cubic_meters_of_i_per_cubic_meter_total)
        return cast('VolumeFractionOfI', self.variable)
    @property
    def gallons_of_i_per_gallon_totals(self) -> 'VolumeFractionOfI':
        self.variable.quantity = FastQuantity(self.value, VolumeFractionOfIUnits.gallons_of_i_per_gallon_total)
        return cast('VolumeFractionOfI', self.variable)
    
    # Short aliases for convenience
    pass


class VolumeFractionOfI(TypedVariable):
    """Type-safe volume fraction of "i" variable with expression capabilities."""
    
    _setter_class = VolumeFractionOfISetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "cubic_foot_of_i_per_cubic_foot_totals"
    
    def set(self, value: float) -> VolumeFractionOfISetter:
        """Create a volume fraction of "i" setter for this variable with proper type annotation."""
        return VolumeFractionOfISetter(self, value)


class VolumeFractionOfIModule(VariableModule):
    """VolumeFractionOfI variable module definition."""
    
    def get_variable_class(self):
        return VolumeFractionOfI
    
    def get_setter_class(self):
        return VolumeFractionOfISetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = VolumeFractionOfIModule()