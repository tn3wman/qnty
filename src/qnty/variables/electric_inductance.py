"""
ElectricInductance Variable Module
===================================

Type-safe electric inductance variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_INDUCTANCE
from ..units import ElectricInductanceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricInductanceSetter(TypeSafeSetter):
    """ElectricInductance-specific setter with only electric inductance units."""
    
    def __init__(self, variable: 'ElectricInductance', value: float):
        super().__init__(variable, value)
    
    # Only electric inductance units available - compile-time safe!
    @property
    def abhenry(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.abhenry)
        return cast('ElectricInductance', self.variable)
    @property
    def cms(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.cm)
        return cast('ElectricInductance', self.variable)
    @property
    def henry(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.henry)
        return cast('ElectricInductance', self.variable)
    @property
    def henry_intl_means(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.henry_intl_mean)
        return cast('ElectricInductance', self.variable)
    @property
    def henry_intl_us(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.henry_intl_us)
        return cast('ElectricInductance', self.variable)
    @property
    def mics(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.mic)
        return cast('ElectricInductance', self.variable)
    @property
    def stathenry(self) -> 'ElectricInductance':
        self.variable.quantity = FastQuantity(self.value, ElectricInductanceUnits.stathenry)
        return cast('ElectricInductance', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricInductance(TypedVariable):
    """Type-safe electric inductance variable with expression capabilities."""
    
    _setter_class = ElectricInductanceSetter
    _expected_dimension = ELECTRIC_INDUCTANCE
    _default_unit_property = "henry"
    
    def set(self, value: float) -> ElectricInductanceSetter:
        """Create a electric inductance setter for this variable with proper type annotation."""
        return ElectricInductanceSetter(self, value)


class ElectricInductanceModule(VariableModule):
    """ElectricInductance variable module definition."""
    
    def get_variable_class(self):
        return ElectricInductance
    
    def get_setter_class(self):
        return ElectricInductanceSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_INDUCTANCE


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricInductanceModule()