"""
ElectricResistance Variable Module
===================================

Type-safe electric resistance variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_RESISTANCE
from ..units import ElectricResistanceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricResistanceSetter(TypeSafeSetter):
    """ElectricResistance-specific setter with only electric resistance units."""
    
    def __init__(self, variable: 'ElectricResistance', value: float):
        super().__init__(variable, value)
    
    # Only electric resistance units available - compile-time safe!
    @property
    def abohms(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.abohm)
        return cast('ElectricResistance', self.variable)
    @property
    def jacobis(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.jacobi)
        return cast('ElectricResistance', self.variable)
    @property
    def lenzs(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.lenz)
        return cast('ElectricResistance', self.variable)
    @property
    def ohms(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.ohm)
        return cast('ElectricResistance', self.variable)
    @property
    def ohm_intl_means(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.ohm_intl_mean)
        return cast('ElectricResistance', self.variable)
    @property
    def ohm_intl_us(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.ohm_intl_us)
        return cast('ElectricResistance', self.variable)
    @property
    def ohm_legals(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.ohm_legal)
        return cast('ElectricResistance', self.variable)
    @property
    def preeces(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.preece)
        return cast('ElectricResistance', self.variable)
    @property
    def statohms(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.statohm)
        return cast('ElectricResistance', self.variable)
    @property
    def wheatstones(self) -> 'ElectricResistance':
        self.variable.quantity = FastQuantity(self.value, ElectricResistanceUnits.wheatstone)
        return cast('ElectricResistance', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricResistance(TypedVariable):
    """Type-safe electric resistance variable with expression capabilities."""
    
    _setter_class = ElectricResistanceSetter
    _expected_dimension = ELECTRIC_RESISTANCE
    _default_unit_property = "ohms"
    
    def set(self, value: float) -> ElectricResistanceSetter:
        """Create a electric resistance setter for this variable with proper type annotation."""
        return ElectricResistanceSetter(self, value)


class ElectricResistanceModule(VariableModule):
    """ElectricResistance variable module definition."""
    
    def get_variable_class(self):
        return ElectricResistance
    
    def get_setter_class(self):
        return ElectricResistanceSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_RESISTANCE


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricResistanceModule()