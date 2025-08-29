"""
Time Variable Module
====================

Type-safe time variables with specialized setter and fluent API.
"""

from typing import TYPE_CHECKING, cast

from ..dimension import TIME
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable

from ..units import TimeUnits


class TimeSetter(TypeSafeSetter):
    """Time-specific setter with only time units."""
    
    def __init__(self, variable: 'Time', value: float):
        super().__init__(variable, value)
    
    # Only time units available - compile-time safe!
    @property
    def seconds(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.second)
        return cast('Time', self.variable)
    
    @property
    def minutes(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.minute)
        return cast('Time', self.variable)
    
    @property
    def hours(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.hour)
        return cast('Time', self.variable)
    
    @property
    def days(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.day)
        return cast('Time', self.variable)
    
    @property
    def years(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.year)
        return cast('Time', self.variable)
    
    @property
    def julian_years(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.julian_year)
        return cast('Time', self.variable)
    
    @property
    def centuries(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.century)
        return cast('Time', self.variable)
    
    @property
    def millennia(self) -> 'Time':
        self.variable.quantity = FastQuantity(self.value, TimeUnits.millennium)
        return cast('Time', self.variable)
    
    # Short aliases for convenience
    @property
    def s(self) -> 'Time':
        return self.seconds
    
    @property
    def min(self) -> 'Time':
        return self.minutes
    
    @property
    def h(self) -> 'Time':
        return self.hours
    
    @property
    def hr(self) -> 'Time':
        return self.hours
    
    @property
    def d(self) -> 'Time':
        return self.days
    
    @property
    def yr(self) -> 'Time':
        return self.years
    
    @property
    def a(self) -> 'Time':
        return self.julian_years


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