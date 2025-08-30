"""
Time Variable Module
=====================

Type-safe time variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import TIME
from ..units import TimeUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class TimeSetter(TypeSafeSetter):
    """Time-specific setter with only time units."""
    
    def __init__(self, variable: 'Time', value: float):
        super().__init__(variable, value)
    
    # Only time units available - compile-time safe!
    @property
    def blinks(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.blink)
        return cast('Time', self.variable)
    @property
    def century(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.century)
        return cast('Time', self.variable)
    @property
    def chronons(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.chronon)
        return cast('Time', self.variable)
    @property
    def gigans(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.gigan)
        return cast('Time', self.variable)
    @property
    def hours(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.hour)
        return cast('Time', self.variable)
    @property
    def julian_years(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.julian_year)
        return cast('Time', self.variable)
    @property
    def mean_solar_day(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.mean_solar_day)
        return cast('Time', self.variable)
    @property
    def milleniums(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.millenium)
        return cast('Time', self.variable)
    @property
    def minutes(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.minute)
        return cast('Time', self.variable)
    @property
    def seconds(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.second)
        return cast('Time', self.variable)
    @property
    def shakes(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.shake)
        return cast('Time', self.variable)
    @property
    def sidereal_year_1900_ads(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.sidereal_year_1900_ad)
        return cast('Time', self.variable)
    @property
    def tropical_years(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.tropical_year)
        return cast('Time', self.variable)
    @property
    def winks(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.wink)
        return cast('Time', self.variable)
    @property
    def years(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.year)
        return cast('Time', self.variable)
    
    # Short aliases for convenience
    pass


class Time(TypedVariable):
    """Type-safe time variable with expression capabilities."""
    
    _setter_class = TimeSetter
    _expected_dimension = TIME
    _default_unit_property = "seconds"
    
    def set(self, value: float) -> TimeSetter:
        """Create a time setter for this variable with proper type annotation."""
        return TimeSetter(self, value)


class TimeModule(VariableModule):
    """Time variable module definition."""
    
    def get_variable_class(self):
        return Time
    
    def get_setter_class(self):
        return TimeSetter
    
    def get_expected_dimension(self):
        return TIME


# Register this module for auto-discovery
VARIABLE_MODULE = TimeModule()