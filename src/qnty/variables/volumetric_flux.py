"""
VolumetricFlux Variable Module
===============================

Type-safe volumetric flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import VOLUMETRIC_FLUX
from ..units import VolumetricFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumetricFluxSetter(TypeSafeSetter):
    """VolumetricFlux-specific setter with only volumetric flux units."""
    
    def __init__(self, variable: 'VolumetricFlux', value: float):
        super().__init__(variable, value)
    
    # Only volumetric flux units available - compile-time safe!
    @property
    def cubic_feet_per_square_foot_per_day(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_feet_per_square_foot_per_day)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_feet_per_square_foot_per_hours(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_feet_per_square_foot_per_hour)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_feet_per_square_foot_per_minutes(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_feet_per_square_foot_per_minute)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_feet_per_square_foot_per_seconds(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_feet_per_square_foot_per_second)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_meters_per_square_meter_per_day(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_meters_per_square_meter_per_day)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_meters_per_square_meter_per_hours(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_meters_per_square_meter_per_hour)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_meters_per_square_meter_per_minutes(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_meters_per_square_meter_per_minute)
        return cast('VolumetricFlux', self.variable)
    @property
    def cubic_meters_per_square_meter_per_seconds(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.cubic_meters_per_square_meter_per_second)
        return cast('VolumetricFlux', self.variable)
    @property
    def gallons_per_square_foot_per_day(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.gallons_per_square_foot_per_day)
        return cast('VolumetricFlux', self.variable)
    @property
    def gallons_per_square_foot_per_hours(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.gallons_per_square_foot_per_hour)
        return cast('VolumetricFlux', self.variable)
    @property
    def gallons_per_square_foot_per_minutes(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.gallons_per_square_foot_per_minute)
        return cast('VolumetricFlux', self.variable)
    @property
    def gallons_per_square_foot_per_seconds(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.gallons_per_square_foot_per_second)
        return cast('VolumetricFlux', self.variable)
    @property
    def liters_per_square_meter_per_day(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.liters_per_square_meter_per_day)
        return cast('VolumetricFlux', self.variable)
    @property
    def liters_per_square_meter_per_hours(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.liters_per_square_meter_per_hour)
        return cast('VolumetricFlux', self.variable)
    @property
    def liters_per_square_meter_per_minutes(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.liters_per_square_meter_per_minute)
        return cast('VolumetricFlux', self.variable)
    @property
    def liters_per_square_meter_per_seconds(self) -> 'VolumetricFlux':
        self.variable.quantity = FastQuantity(self.value, VolumetricFluxUnits.liters_per_square_meter_per_second)
        return cast('VolumetricFlux', self.variable)
    
    # Short aliases for convenience
    pass


class VolumetricFlux(TypedVariable):
    """Type-safe volumetric flux variable with expression capabilities."""
    
    _setter_class = VolumetricFluxSetter
    _expected_dimension = VOLUMETRIC_FLUX
    _default_unit_property = "cubic_meters_per_square_meter_per_seconds"
    
    def set(self, value: float) -> VolumetricFluxSetter:
        """Create a volumetric flux setter for this variable with proper type annotation."""
        return VolumetricFluxSetter(self, value)


class VolumetricFluxModule(VariableModule):
    """VolumetricFlux variable module definition."""
    
    def get_variable_class(self):
        return VolumetricFlux
    
    def get_setter_class(self):
        return VolumetricFluxSetter
    
    def get_expected_dimension(self):
        return VOLUMETRIC_FLUX


# Register this module for auto-discovery
VARIABLE_MODULE = VolumetricFluxModule()