"""
HeatTransferCoefficient Variable Module
========================================

Type-safe heat transfer coefficient variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import HEAT_TRANSFER_COEFFICIENT
from ..units import HeatTransferCoefficientUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class HeatTransferCoefficientSetter(TypeSafeSetter):
    """HeatTransferCoefficient-specific setter with only heat transfer coefficient units."""
    
    def __init__(self, variable: 'HeatTransferCoefficient', value: float):
        super().__init__(variable, value)
    
    # Only heat transfer coefficient units available - compile-time safe!
    @property
    def fahrenheits(self) -> 'HeatTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, HeatTransferCoefficientUnits.fahrenheit)
        return cast('HeatTransferCoefficient', self.variable)
    @property
    def celsius(self) -> 'HeatTransferCoefficient':
        self.variable.quantity = FastQuantity(self.value, HeatTransferCoefficientUnits.celsius)
        return cast('HeatTransferCoefficient', self.variable)
    
    # Short aliases for convenience
    pass


class HeatTransferCoefficient(TypedVariable):
    """Type-safe heat transfer coefficient variable with expression capabilities."""
    
    _setter_class = HeatTransferCoefficientSetter
    _expected_dimension = HEAT_TRANSFER_COEFFICIENT
    _default_unit_property = "fahrenheits"
    
    def set(self, value: float) -> HeatTransferCoefficientSetter:
        """Create a heat transfer coefficient setter for this variable with proper type annotation."""
        return HeatTransferCoefficientSetter(self, value)


class HeatTransferCoefficientModule(VariableModule):
    """HeatTransferCoefficient variable module definition."""
    
    def get_variable_class(self):
        return HeatTransferCoefficient
    
    def get_setter_class(self):
        return HeatTransferCoefficientSetter
    
    def get_expected_dimension(self):
        return HEAT_TRANSFER_COEFFICIENT


# Register this module for auto-discovery
VARIABLE_MODULE = HeatTransferCoefficientModule()