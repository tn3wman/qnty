"""
PowerThermalDuty Variable Module
=================================

Type-safe power, thermal duty variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import POWER
from ..units import PowerThermalDutyUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class PowerThermalDutySetter(TypeSafeSetter):
    """PowerThermalDuty-specific setter with only power, thermal duty units."""
    
    def __init__(self, variable: 'PowerThermalDuty', value: float):
        super().__init__(variable, value)
    
    # Only power, thermal duty units available - compile-time safe!
    @property
    def abwatt_emu_of_powers(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.abwatt_emu_of_power)
        return cast('PowerThermalDuty', self.variable)
    @property
    def boiler_horsepowers(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.boiler_horsepower)
        return cast('PowerThermalDuty', self.variable)
    @property
    def british_thermal_unit_mean_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.british_thermal_unit_mean_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def british_thermal_unit_mean_per_minutes(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.british_thermal_unit_mean_per_minute)
        return cast('PowerThermalDuty', self.variable)
    @property
    def british_thermal_unit_thermochemical_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.british_thermal_unit_thermochemical_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def british_thermal_unit_thermochemical_per_minutes(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.british_thermal_unit_thermochemical_per_minute)
        return cast('PowerThermalDuty', self.variable)
    @property
    def calorie_mean_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.calorie_mean_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def calorie_thermochemical_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.calorie_thermochemical_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def donkey(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.donkey)
        return cast('PowerThermalDuty', self.variable)
    @property
    def erg_per_seconds(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.erg_per_second)
        return cast('PowerThermalDuty', self.variable)
    @property
    def foot_pondal_per_seconds(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.foot_pondal_per_second)
        return cast('PowerThermalDuty', self.variable)
    @property
    def foot_pound_force_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.foot_pound_force_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def foot_pound_force_per_minutes(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.foot_pound_force_per_minute)
        return cast('PowerThermalDuty', self.variable)
    @property
    def foot_pound_force_per_seconds(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.foot_pound_force_per_second)
        return cast('PowerThermalDuty', self.variable)
    @property
    def horsepowers(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.horsepower)
        return cast('PowerThermalDuty', self.variable)
    @property
    def horsepower_electrics(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.horsepower_electric)
        return cast('PowerThermalDuty', self.variable)
    @property
    def horsepower_uks(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.horsepower_uk)
        return cast('PowerThermalDuty', self.variable)
    @property
    def kcal_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.kcal_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def kilogram_force_meter_per_seconds(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.kilogram_force_meter_per_second)
        return cast('PowerThermalDuty', self.variable)
    @property
    def kilowatts(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.kilowatt)
        return cast('PowerThermalDuty', self.variable)
    @property
    def megawatts(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.megawatt)
        return cast('PowerThermalDuty', self.variable)
    @property
    def metric_horsepowers(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.metric_horsepower)
        return cast('PowerThermalDuty', self.variable)
    @property
    def million_british_thermal_units_per_hour_petroleums(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.million_british_thermal_units_per_hour_petroleum)
        return cast('PowerThermalDuty', self.variable)
    @property
    def million_kilocalorie_per_hours(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.million_kilocalorie_per_hour)
        return cast('PowerThermalDuty', self.variable)
    @property
    def prony(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.prony)
        return cast('PowerThermalDuty', self.variable)
    @property
    def ton_of_refrigeration_us(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.ton_of_refrigeration_us)
        return cast('PowerThermalDuty', self.variable)
    @property
    def tons(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.ton)
        return cast('PowerThermalDuty', self.variable)
    @property
    def voltamperes(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.voltampere)
        return cast('PowerThermalDuty', self.variable)
    @property
    def water_horsepowers(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.water_horsepower)
        return cast('PowerThermalDuty', self.variable)
    @property
    def watts(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.watt)
        return cast('PowerThermalDuty', self.variable)
    @property
    def watt_international_means(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.watt_international_mean)
        return cast('PowerThermalDuty', self.variable)
    @property
    def watt_international_us(self) -> 'PowerThermalDuty':
        self.variable.quantity = FastQuantity(self.value, PowerThermalDutyUnits.watt_international_us)
        return cast('PowerThermalDuty', self.variable)
    
    # Short aliases for convenience
    pass


class PowerThermalDuty(TypedVariable):
    """Type-safe power, thermal duty variable with expression capabilities."""
    
    _setter_class = PowerThermalDutySetter
    _expected_dimension = POWER
    _default_unit_property = "watts"
    
    def set(self, value: float) -> PowerThermalDutySetter:
        """Create a power, thermal duty setter for this variable with proper type annotation."""
        return PowerThermalDutySetter(self, value)


class PowerThermalDutyModule(VariableModule):
    """PowerThermalDuty variable module definition."""
    
    def get_variable_class(self):
        return PowerThermalDuty
    
    def get_setter_class(self):
        return PowerThermalDutySetter
    
    def get_expected_dimension(self):
        return POWER


# Register this module for auto-discovery
VARIABLE_MODULE = PowerThermalDutyModule()