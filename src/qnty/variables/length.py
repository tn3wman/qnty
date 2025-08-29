"""
Length Variable Module
=====================

Type-safe length variables with specialized setter and fluent API.
"""

from typing import TYPE_CHECKING, cast

from ..dimension import LENGTH
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable

from ..units import LengthUnits


class LengthSetter(TypeSafeSetter):
    """Length-specific setter with only length units."""
    
    def __init__(self, variable: 'Length', value: float):
        super().__init__(variable, value)
    
    # Only length units available - compile-time safe!
    @property
    def meters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.meter)
        return cast('Length', self.variable)
    
    @property
    def millimeters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.millimeter)
        return cast('Length', self.variable)
    
    @property
    def centimeters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.centimeter)
        return cast('Length', self.variable)
    
    @property
    def inches(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.inch)
        return cast('Length', self.variable)
    
    @property
    def feet(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.foot)
        return cast('Length', self.variable)
    
    # Short aliases for convenience
    @property
    def m(self) -> 'Length':
        return self.meters
    
    @property
    def mm(self) -> 'Length':
        return self.millimeters
    
    @property
    def cm(self) -> 'Length':
        return self.centimeters
    
    @property
    def in_(self) -> 'Length':
        return self.inches
    
    @property
    def ft(self) -> 'Length':
        return self.feet


class Length(TypedVariable):
    """Type-safe length variable with expression capabilities."""
    
    _setter_class = LengthSetter
    _expected_dimension = LENGTH
    _default_unit_property = "meters"
    
    def set(self, value: float) -> LengthSetter:
        """Create a length setter for this variable with proper type annotation."""
        return LengthSetter(self, value)


class LengthModule(VariableModule):
    """Length variable module definition."""
    
    def get_variable_class(self):
        return Length
    
    def get_setter_class(self):
        return LengthSetter
    
    def get_expected_dimension(self):
        return LENGTH


# Register this module for auto-discovery
VARIABLE_MODULE = LengthModule()