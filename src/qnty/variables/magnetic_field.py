"""
MagneticField Variable Module
==============================

Type-safe magnetic field variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MAGNETIC_FIELD
from ..units import MagneticFieldUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MagneticFieldSetter(TypeSafeSetter):
    """MagneticField-specific setter with only magnetic field units."""
    
    def __init__(self, variable: 'MagneticField', value: float):
        super().__init__(variable, value)
    
    # Only magnetic field units available - compile-time safe!
    @property
    def ampere_per_meters(self) -> 'MagneticField':
        self.variable.quantity = FastQuantity(self.value, MagneticFieldUnits.ampere_per_meter)
        return cast('MagneticField', self.variable)
    @property
    def lenzs(self) -> 'MagneticField':
        self.variable.quantity = FastQuantity(self.value, MagneticFieldUnits.lenz)
        return cast('MagneticField', self.variable)
    @property
    def oersteds(self) -> 'MagneticField':
        self.variable.quantity = FastQuantity(self.value, MagneticFieldUnits.oersted)
        return cast('MagneticField', self.variable)
    @property
    def praoersteds(self) -> 'MagneticField':
        self.variable.quantity = FastQuantity(self.value, MagneticFieldUnits.praoersted)
        return cast('MagneticField', self.variable)
    
    # Short aliases for convenience
    pass


class MagneticField(TypedVariable):
    """Type-safe magnetic field variable with expression capabilities."""
    
    _setter_class = MagneticFieldSetter
    _expected_dimension = MAGNETIC_FIELD
    _default_unit_property = "ampere_per_meters"
    
    def set(self, value: float) -> MagneticFieldSetter:
        """Create a magnetic field setter for this variable with proper type annotation."""
        return MagneticFieldSetter(self, value)


class MagneticFieldModule(VariableModule):
    """MagneticField variable module definition."""
    
    def get_variable_class(self):
        return MagneticField
    
    def get_setter_class(self):
        return MagneticFieldSetter
    
    def get_expected_dimension(self):
        return MAGNETIC_FIELD


# Register this module for auto-discovery
VARIABLE_MODULE = MagneticFieldModule()