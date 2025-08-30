"""
Illuminance Variable Module
============================

Type-safe illuminance variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ILLUMINANCE
from ..units import IlluminanceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class IlluminanceSetter(TypeSafeSetter):
    """Illuminance-specific setter with only illuminance units."""
    
    def __init__(self, variable: 'Illuminance', value: float):
        super().__init__(variable, value)
    
    # Only illuminance units available - compile-time safe!
    @property
    def footcandles(self) -> 'Illuminance':
        self.variable.quantity = FastQuantity(self.value, IlluminanceUnits.footcandle)
        return cast('Illuminance', self.variable)
    @property
    def luxs(self) -> 'Illuminance':
        self.variable.quantity = FastQuantity(self.value, IlluminanceUnits.lux)
        return cast('Illuminance', self.variable)
    @property
    def noxs(self) -> 'Illuminance':
        self.variable.quantity = FastQuantity(self.value, IlluminanceUnits.nox)
        return cast('Illuminance', self.variable)
    @property
    def phots(self) -> 'Illuminance':
        self.variable.quantity = FastQuantity(self.value, IlluminanceUnits.phot)
        return cast('Illuminance', self.variable)
    @property
    def skots(self) -> 'Illuminance':
        self.variable.quantity = FastQuantity(self.value, IlluminanceUnits.skot)
        return cast('Illuminance', self.variable)
    
    # Short aliases for convenience
    pass


class Illuminance(TypedVariable):
    """Type-safe illuminance variable with expression capabilities."""
    
    _setter_class = IlluminanceSetter
    _expected_dimension = ILLUMINANCE
    _default_unit_property = "luxs"
    
    def set(self, value: float) -> IlluminanceSetter:
        """Create a illuminance setter for this variable with proper type annotation."""
        return IlluminanceSetter(self, value)


class IlluminanceModule(VariableModule):
    """Illuminance variable module definition."""
    
    def get_variable_class(self):
        return Illuminance
    
    def get_setter_class(self):
        return IlluminanceSetter
    
    def get_expected_dimension(self):
        return ILLUMINANCE


# Register this module for auto-discovery
VARIABLE_MODULE = IlluminanceModule()