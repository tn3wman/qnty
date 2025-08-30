"""
MagneticFlux Variable Module
=============================

Type-safe magnetic flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MAGNETIC_FLUX
from ..units import MagneticFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MagneticFluxSetter(TypeSafeSetter):
    """MagneticFlux-specific setter with only magnetic flux units."""
    
    def __init__(self, variable: 'MagneticFlux', value: float):
        super().__init__(variable, value)
    
    # Only magnetic flux units available - compile-time safe!
    @property
    def kapp_lines(self) -> 'MagneticFlux':
        self.variable.quantity = FastQuantity(self.value, MagneticFluxUnits.kapp_line)
        return cast('MagneticFlux', self.variable)
    @property
    def lines(self) -> 'MagneticFlux':
        self.variable.quantity = FastQuantity(self.value, MagneticFluxUnits.line)
        return cast('MagneticFlux', self.variable)
    @property
    def maxwells(self) -> 'MagneticFlux':
        self.variable.quantity = FastQuantity(self.value, MagneticFluxUnits.maxwell)
        return cast('MagneticFlux', self.variable)
    @property
    def unit_poles(self) -> 'MagneticFlux':
        self.variable.quantity = FastQuantity(self.value, MagneticFluxUnits.unit_pole)
        return cast('MagneticFlux', self.variable)
    @property
    def webers(self) -> 'MagneticFlux':
        self.variable.quantity = FastQuantity(self.value, MagneticFluxUnits.weber)
        return cast('MagneticFlux', self.variable)
    
    # Short aliases for convenience
    pass


class MagneticFlux(TypedVariable):
    """Type-safe magnetic flux variable with expression capabilities."""
    
    _setter_class = MagneticFluxSetter
    _expected_dimension = MAGNETIC_FLUX
    _default_unit_property = "webers"
    
    def set(self, value: float) -> MagneticFluxSetter:
        """Create a magnetic flux setter for this variable with proper type annotation."""
        return MagneticFluxSetter(self, value)


class MagneticFluxModule(VariableModule):
    """MagneticFlux variable module definition."""
    
    def get_variable_class(self):
        return MagneticFlux
    
    def get_setter_class(self):
        return MagneticFluxSetter
    
    def get_expected_dimension(self):
        return MAGNETIC_FLUX


# Register this module for auto-discovery
VARIABLE_MODULE = MagneticFluxModule()