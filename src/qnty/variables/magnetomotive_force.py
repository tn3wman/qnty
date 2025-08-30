"""
MagnetomotiveForce Variable Module
===================================

Type-safe magnetomotive force variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import CURRENT
from ..units import MagnetomotiveForceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MagnetomotiveForceSetter(TypeSafeSetter):
    """MagnetomotiveForce-specific setter with only magnetomotive force units."""
    
    def __init__(self, variable: 'MagnetomotiveForce', value: float):
        super().__init__(variable, value)
    
    # Only magnetomotive force units available - compile-time safe!
    @property
    def abampereturns(self) -> 'MagnetomotiveForce':
        self.variable.quantity = FastQuantity(self.value, MagnetomotiveForceUnits.abampereturn)
        return cast('MagnetomotiveForce', self.variable)
    @property
    def amperes(self) -> 'MagnetomotiveForce':
        self.variable.quantity = FastQuantity(self.value, MagnetomotiveForceUnits.ampere)
        return cast('MagnetomotiveForce', self.variable)
    @property
    def ampereturns(self) -> 'MagnetomotiveForce':
        self.variable.quantity = FastQuantity(self.value, MagnetomotiveForceUnits.ampereturn)
        return cast('MagnetomotiveForce', self.variable)
    @property
    def gilberts(self) -> 'MagnetomotiveForce':
        self.variable.quantity = FastQuantity(self.value, MagnetomotiveForceUnits.gilbert)
        return cast('MagnetomotiveForce', self.variable)
    
    # Short aliases for convenience
    pass


class MagnetomotiveForce(TypedVariable):
    """Type-safe magnetomotive force variable with expression capabilities."""
    
    _setter_class = MagnetomotiveForceSetter
    _expected_dimension = CURRENT
    _default_unit_property = "amperes"
    
    def set(self, value: float) -> MagnetomotiveForceSetter:
        """Create a magnetomotive force setter for this variable with proper type annotation."""
        return MagnetomotiveForceSetter(self, value)


class MagnetomotiveForceModule(VariableModule):
    """MagnetomotiveForce variable module definition."""
    
    def get_variable_class(self):
        return MagnetomotiveForce
    
    def get_setter_class(self):
        return MagnetomotiveForceSetter
    
    def get_expected_dimension(self):
        return CURRENT


# Register this module for auto-discovery
VARIABLE_MODULE = MagnetomotiveForceModule()