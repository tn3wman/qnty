"""
ElectricCurrentIntensity Variable Module
=========================================

Type-safe electric current intensity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import CURRENT
from ..units import ElectricCurrentIntensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricCurrentIntensitySetter(TypeSafeSetter):
    """ElectricCurrentIntensity-specific setter with only electric current intensity units."""
    
    def __init__(self, variable: 'ElectricCurrentIntensity', value: float):
        super().__init__(variable, value)
    
    # Only electric current intensity units available - compile-time safe!
    @property
    def abamperes(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.abampere)
        return cast('ElectricCurrentIntensity', self.variable)
    @property
    def ampere_intl_means(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.ampere_intl_mean)
        return cast('ElectricCurrentIntensity', self.variable)
    @property
    def ampere_intl_us(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.ampere_intl_us)
        return cast('ElectricCurrentIntensity', self.variable)
    @property
    def amperes(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.ampere)
        return cast('ElectricCurrentIntensity', self.variable)
    @property
    def biots(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.biot)
        return cast('ElectricCurrentIntensity', self.variable)
    @property
    def statamperes(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.statampere)
        return cast('ElectricCurrentIntensity', self.variable)
    @property
    def uas(self) -> 'ElectricCurrentIntensity':
        self.variable.quantity = FastQuantity(self.value, ElectricCurrentIntensityUnits.ua)
        return cast('ElectricCurrentIntensity', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricCurrentIntensity(TypedVariable):
    """Type-safe electric current intensity variable with expression capabilities."""
    
    _setter_class = ElectricCurrentIntensitySetter
    _expected_dimension = CURRENT
    _default_unit_property = "amperes"
    
    def set(self, value: float) -> ElectricCurrentIntensitySetter:
        """Create a electric current intensity setter for this variable with proper type annotation."""
        return ElectricCurrentIntensitySetter(self, value)


class ElectricCurrentIntensityModule(VariableModule):
    """ElectricCurrentIntensity variable module definition."""
    
    def get_variable_class(self):
        return ElectricCurrentIntensity
    
    def get_setter_class(self):
        return ElectricCurrentIntensitySetter
    
    def get_expected_dimension(self):
        return CURRENT


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricCurrentIntensityModule()