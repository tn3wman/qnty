"""
MassTransferCoefficient Variable Module
========================================

Type-safe mass transfer coefficient variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS_TRANSFER_COEFFICIENT
from ..units import MassTransferCoefficientUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MassTransferCoefficientSetter(TypeSafeSetter):
    """MassTransferCoefficient-specific setter with only mass transfer coefficient units."""
    
    def __init__(self, variable: 'MassTransferCoefficient', value: float):
        super().__init__(variable, value)
    
    # Only mass transfer coefficient units available - compile-time safe!
    @property
    def gram_per_square_centimeter_per_seconds(self) -> 'MassTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, MassTransferCoefficientUnits.gram_per_square_centimeter_per_second)
        return cast('MassTransferCoefficient', self.variable)
    @property
    def kilogram_per_square_meter_per_seconds(self) -> 'MassTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, MassTransferCoefficientUnits.kilogram_per_square_meter_per_second)
        return cast('MassTransferCoefficient', self.variable)
    @property
    def pounds_force_per_cubic_foot_per_hours(self) -> 'MassTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, MassTransferCoefficientUnits.pounds_force_per_cubic_foot_per_hour)
        return cast('MassTransferCoefficient', self.variable)
    @property
    def pounds_mass_per_square_foot_per_hours(self) -> 'MassTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, MassTransferCoefficientUnits.pounds_mass_per_square_foot_per_hour)
        return cast('MassTransferCoefficient', self.variable)
    @property
    def pounds_mass_per_square_foot_per_seconds(self) -> 'MassTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, MassTransferCoefficientUnits.pounds_mass_per_square_foot_per_second)
        return cast('MassTransferCoefficient', self.variable)
    
    # Short aliases for convenience
    pass


class MassTransferCoefficient(TypedVariable):
    """Type-safe mass transfer coefficient variable with expression capabilities."""
    
    _setter_class = MassTransferCoefficientSetter
    _expected_dimension = MASS_TRANSFER_COEFFICIENT
    _default_unit_property = "kilogram_per_square_meter_per_seconds"
    
    def set(self, value: float) -> MassTransferCoefficientSetter:
        """Create a mass transfer coefficient setter for this variable with proper type annotation."""
        return MassTransferCoefficientSetter(self, value)


class MassTransferCoefficientModule(VariableModule):
    """MassTransferCoefficient variable module definition."""
    
    def get_variable_class(self):
        return MassTransferCoefficient
    
    def get_setter_class(self):
        return MassTransferCoefficientSetter
    
    def get_expected_dimension(self):
        return MASS_TRANSFER_COEFFICIENT


# Register this module for auto-discovery
VARIABLE_MODULE = MassTransferCoefficientModule()