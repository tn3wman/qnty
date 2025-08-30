"""
Force Variable Module
======================

Type-safe force variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import FORCE
from ..units import ForceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ForceSetter(TypeSafeSetter):
    """Force-specific setter with only force units."""
    
    def __init__(self, variable: 'Force', value: float):
        super().__init__(variable, value)
    
    # Only force units available - compile-time safe!
    @property
    def crinals(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.crinal)
        return cast('Force', self.variable)
    @property
    def dynes(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.dyne)
        return cast('Force', self.variable)
    @property
    def funals(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.funal)
        return cast('Force', self.variable)
    @property
    def kilogram_forces(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.kilogram_force)
        return cast('Force', self.variable)
    @property
    def kip_forces(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.kip_force)
        return cast('Force', self.variable)
    @property
    def newtons(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.newton)
        return cast('Force', self.variable)
    @property
    def ounce_forces(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.ounce_force)
        return cast('Force', self.variable)
    @property
    def ponds(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.pond)
        return cast('Force', self.variable)
    @property
    def pound_forces(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.pound_force)
        return cast('Force', self.variable)
    @property
    def poundals(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.poundal)
        return cast('Force', self.variable)
    @property
    def slug_forces(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.slug_force)
        return cast('Force', self.variable)
    @property
    def sthènes(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.sthène)
        return cast('Force', self.variable)
    @property
    def ton_force_longs(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.ton_force_long)
        return cast('Force', self.variable)
    @property
    def ton_force_metrics(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.ton_force_metric)
        return cast('Force', self.variable)
    @property
    def ton_force_shorts(self) -> 'Force':
        self.variable.quantity = FastQuantity(self.value, ForceUnits.ton_force_short)
        return cast('Force', self.variable)
    
    # Short aliases for convenience
    pass


class Force(TypedVariable):
    """Type-safe force variable with expression capabilities."""
    
    _setter_class = ForceSetter
    _expected_dimension = FORCE
    _default_unit_property = "newtons"
    
    def set(self, value: float) -> ForceSetter:
        """Create a force setter for this variable with proper type annotation."""
        return ForceSetter(self, value)


class ForceModule(VariableModule):
    """Force variable module definition."""
    
    def get_variable_class(self):
        return Force
    
    def get_setter_class(self):
        return ForceSetter
    
    def get_expected_dimension(self):
        return FORCE


# Register this module for auto-discovery
VARIABLE_MODULE = ForceModule()