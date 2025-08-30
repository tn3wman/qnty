"""
Stress Variable Module
=======================

Type-safe stress variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import PRESSURE
from ..units import StressUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class StressSetter(TypeSafeSetter):
    """Stress-specific setter with only stress units."""
    
    def __init__(self, variable: 'Stress', value: float):
        super().__init__(variable, value)
    
    # Only stress units available - compile-time safe!
    @property
    def dyne_per_square_centimeters(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.dyne_per_square_centimeter)
        return cast('Stress', self.variable)
    @property
    def gigapascals(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.gigapascal)
        return cast('Stress', self.variable)
    @property
    def hectopascals(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.hectopascal)
        return cast('Stress', self.variable)
    @property
    def kilogram_force_per_square_centimeters(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.kilogram_force_per_square_centimeter)
        return cast('Stress', self.variable)
    @property
    def kilogram_force_per_square_meters(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.kilogram_force_per_square_meter)
        return cast('Stress', self.variable)
    @property
    def kip_force_per_square_inchs(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.kip_force_per_square_inch)
        return cast('Stress', self.variable)
    @property
    def megapascals(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.megapascal)
        return cast('Stress', self.variable)
    @property
    def newton_per_square_meters(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.newton_per_square_meter)
        return cast('Stress', self.variable)
    @property
    def ounce_force_per_square_inchs(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.ounce_force_per_square_inch)
        return cast('Stress', self.variable)
    @property
    def pascals(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.pascal)
        return cast('Stress', self.variable)
    @property
    def pound_force_per_square_foots(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.pound_force_per_square_foot)
        return cast('Stress', self.variable)
    @property
    def pound_force_per_square_inchs(self) -> 'Stress':
        self.variable.quantity = FastQuantity(self.value, StressUnits.pound_force_per_square_inch)
        return cast('Stress', self.variable)
    
    # Short aliases for convenience
    pass


class Stress(TypedVariable):
    """Type-safe stress variable with expression capabilities."""
    
    _setter_class = StressSetter
    _expected_dimension = PRESSURE
    _default_unit_property = "pascals"
    
    def set(self, value: float) -> StressSetter:
        """Create a stress setter for this variable with proper type annotation."""
        return StressSetter(self, value)


class StressModule(VariableModule):
    """Stress variable module definition."""
    
    def get_variable_class(self):
        return Stress
    
    def get_setter_class(self):
        return StressSetter
    
    def get_expected_dimension(self):
        return PRESSURE


# Register this module for auto-discovery
VARIABLE_MODULE = StressModule()