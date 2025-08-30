"""
SpecificLength Variable Module
===============================

Type-safe specific length variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SPECIFIC_LENGTH
from ..units import SpecificLengthUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SpecificLengthSetter(TypeSafeSetter):
    """SpecificLength-specific setter with only specific length units."""
    
    def __init__(self, variable: 'SpecificLength', value: float):
        super().__init__(variable, value)
    
    # Only specific length units available - compile-time safe!
    @property
    def centimeter_per_grams(self) -> 'SpecificLength':
        self.variable.quantity = FastQuantity(self.value, SpecificLengthUnits.centimeter_per_gram)
        return cast('SpecificLength', self.variable)
    @property
    def cotton_counts(self) -> 'SpecificLength':
        self.variable.quantity = FastQuantity(self.value, SpecificLengthUnits.cotton_count)
        return cast('SpecificLength', self.variable)
    @property
    def ft_per_pounds(self) -> 'SpecificLength':
        self.variable.quantity = FastQuantity(self.value, SpecificLengthUnits.ft_per_pound)
        return cast('SpecificLength', self.variable)
    @property
    def meters_per_kilograms(self) -> 'SpecificLength':
        self.variable.quantity = FastQuantity(self.value, SpecificLengthUnits.meters_per_kilogram)
        return cast('SpecificLength', self.variable)
    @property
    def newton_meters(self) -> 'SpecificLength':
        self.variable.quantity = FastQuantity(self.value, SpecificLengthUnits.newton_meter)
        return cast('SpecificLength', self.variable)
    @property
    def worsteds(self) -> 'SpecificLength':
        self.variable.quantity = FastQuantity(self.value, SpecificLengthUnits.worsted)
        return cast('SpecificLength', self.variable)
    
    # Short aliases for convenience
    pass


class SpecificLength(TypedVariable):
    """Type-safe specific length variable with expression capabilities."""
    
    _setter_class = SpecificLengthSetter
    _expected_dimension = SPECIFIC_LENGTH
    _default_unit_property = "meters_per_kilograms"
    
    def set(self, value: float) -> SpecificLengthSetter:
        """Create a specific length setter for this variable with proper type annotation."""
        return SpecificLengthSetter(self, value)


class SpecificLengthModule(VariableModule):
    """SpecificLength variable module definition."""
    
    def get_variable_class(self):
        return SpecificLength
    
    def get_setter_class(self):
        return SpecificLengthSetter
    
    def get_expected_dimension(self):
        return SPECIFIC_LENGTH


# Register this module for auto-discovery
VARIABLE_MODULE = SpecificLengthModule()