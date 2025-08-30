"""
PowerPerUnitVolumeOrPowerDensity Variable Module
=================================================

Type-safe power per unit volume or power density variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY
from ..units import PowerPerUnitVolumeOrPowerDensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class PowerPerUnitVolumeOrPowerDensitySetter(TypeSafeSetter):
    """PowerPerUnitVolumeOrPowerDensity-specific setter with only power per unit volume or power density units."""
    
    def __init__(self, variable: 'PowerPerUnitVolumeOrPowerDensity', value: float):
        super().__init__(variable, value)
    
    # Only power per unit volume or power density units available - compile-time safe!
    @property
    def british_thermal_unit_per_hour_per_cubic_foots(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.british_thermal_unit_per_hour_per_cubic_foot)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    @property
    def calorie_per_second_per_cubic_centimeters(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.calorie_per_second_per_cubic_centimeter)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    @property
    def chu_per_hour_per_cubic_foots(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.chu_per_hour_per_cubic_foot)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    @property
    def kilocalorie_per_hour_per_cubic_centimeters(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.kilocalorie_per_hour_per_cubic_centimeter)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    @property
    def kilocalorie_per_hour_per_cubic_foots(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.kilocalorie_per_hour_per_cubic_foot)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    @property
    def kilocalorie_per_second_per_cubic_centimeters(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.kilocalorie_per_second_per_cubic_centimeter)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    @property
    def watt_per_cubic_meters(self) -> 'PowerPerUnitVolumeOrPowerDensity':
        self.variable.quantity = FastQuantity(self.value, PowerPerUnitVolumeOrPowerDensityUnits.watt_per_cubic_meter)
        return cast('PowerPerUnitVolumeOrPowerDensity', self.variable)
    
    # Short aliases for convenience
    pass


class PowerPerUnitVolumeOrPowerDensity(TypedVariable):
    """Type-safe power per unit volume or power density variable with expression capabilities."""
    
    _setter_class = PowerPerUnitVolumeOrPowerDensitySetter
    _expected_dimension = POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY
    _default_unit_property = "british_thermal_unit_per_hour_per_cubic_foots"
    
    def set(self, value: float) -> PowerPerUnitVolumeOrPowerDensitySetter:
        """Create a power per unit volume or power density setter for this variable with proper type annotation."""
        return PowerPerUnitVolumeOrPowerDensitySetter(self, value)


class PowerPerUnitVolumeOrPowerDensityModule(VariableModule):
    """PowerPerUnitVolumeOrPowerDensity variable module definition."""
    
    def get_variable_class(self):
        return PowerPerUnitVolumeOrPowerDensity
    
    def get_setter_class(self):
        return PowerPerUnitVolumeOrPowerDensitySetter
    
    def get_expected_dimension(self):
        return POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY


# Register this module for auto-discovery
VARIABLE_MODULE = PowerPerUnitVolumeOrPowerDensityModule()