"""
SecondRadiationConstantplanck Variable Module
==============================================

Type-safe second radiation constant (planck) variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SECOND_RADIATION_CONSTANT_PLANCK
from ..units import SecondRadiationConstantplanckUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SecondRadiationConstantplanckSetter(TypeSafeSetter):
    """SecondRadiationConstantplanck-specific setter with only second radiation constant (planck) units."""
    
    def __init__(self, variable: 'SecondRadiationConstantplanck', value: float):
        super().__init__(variable, value)
    
    # Only second radiation constant (planck) units available - compile-time safe!
    @property
    def kelvins(self) -> 'SecondRadiationConstantplanck':
        self.variable.quantity = FastQuantity(self.value, SecondRadiationConstantplanckUnits.kelvin)
        return cast('SecondRadiationConstantplanck', self.variable)
    
    # Short aliases for convenience
    pass


class SecondRadiationConstantplanck(TypedVariable):
    """Type-safe second radiation constant (planck) variable with expression capabilities."""
    
    _setter_class = SecondRadiationConstantplanckSetter
    _expected_dimension = SECOND_RADIATION_CONSTANT_PLANCK
    _default_unit_property = "kelvins"
    
    def set(self, value: float) -> SecondRadiationConstantplanckSetter:
        """Create a second radiation constant (planck) setter for this variable with proper type annotation."""
        return SecondRadiationConstantplanckSetter(self, value)


class SecondRadiationConstantplanckModule(VariableModule):
    """SecondRadiationConstantplanck variable module definition."""
    
    def get_variable_class(self):
        return SecondRadiationConstantplanck
    
    def get_setter_class(self):
        return SecondRadiationConstantplanckSetter
    
    def get_expected_dimension(self):
        return SECOND_RADIATION_CONSTANT_PLANCK


# Register this module for auto-discovery
VARIABLE_MODULE = SecondRadiationConstantplanckModule()