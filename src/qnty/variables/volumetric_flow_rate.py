"""
VolumetricFlowRate Variable Module
===================================

Type-safe volumetric flow rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import VOLUMETRIC_FLOW_RATE
from ..units import VolumetricFlowRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumetricFlowRateSetter(TypeSafeSetter):
    """VolumetricFlowRate-specific setter with only volumetric flow rate units."""
    
    def __init__(self, variable: 'VolumetricFlowRate', value: float):
        super().__init__(variable, value)
    
    # Only volumetric flow rate units available - compile-time safe!
    @property
    def cubic_feet_per_day(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_feet_per_day)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_feet_per_hours(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_feet_per_hour)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_feet_per_minutes(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_feet_per_minute)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_feet_per_seconds(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_feet_per_second)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_meters_per_day(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_meters_per_day)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_meters_per_hours(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_meters_per_hour)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_meters_per_minutes(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_meters_per_minute)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def cubic_meters_per_seconds(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.cubic_meters_per_second)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def gallons_per_day(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.gallons_per_day)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def gallons_per_hours(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.gallons_per_hour)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def gallons_per_minutes(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.gallons_per_minute)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def gallons_per_seconds(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.gallons_per_second)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def liters_per_day(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.liters_per_day)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def liters_per_hours(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.liters_per_hour)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def liters_per_minutes(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.liters_per_minute)
        return cast('VolumetricFlowRate', self.variable)
    @property
    def liters_per_seconds(self) -> 'VolumetricFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricFlowRateUnits.liters_per_second)
        return cast('VolumetricFlowRate', self.variable)
    
    # Short aliases for convenience
    pass


class VolumetricFlowRate(TypedVariable):
    """Type-safe volumetric flow rate variable with expression capabilities."""
    
    _setter_class = VolumetricFlowRateSetter
    _expected_dimension = VOLUMETRIC_FLOW_RATE
    _default_unit_property = "cubic_meters_per_seconds"
    
    def set(self, value: float) -> VolumetricFlowRateSetter:
        """Create a volumetric flow rate setter for this variable with proper type annotation."""
        return VolumetricFlowRateSetter(self, value)


class VolumetricFlowRateModule(VariableModule):
    """VolumetricFlowRate variable module definition."""
    
    def get_variable_class(self):
        return VolumetricFlowRate
    
    def get_setter_class(self):
        return VolumetricFlowRateSetter
    
    def get_expected_dimension(self):
        return VOLUMETRIC_FLOW_RATE


# Register this module for auto-discovery
VARIABLE_MODULE = VolumetricFlowRateModule()