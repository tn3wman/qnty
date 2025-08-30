"""
MomentumFlux Variable Module
=============================

Type-safe momentum flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import PRESSURE
from ..units import MomentumFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MomentumFluxSetter(TypeSafeSetter):
    """MomentumFlux-specific setter with only momentum flux units."""
    
    def __init__(self, variable: 'MomentumFlux', value: float):
        super().__init__(variable, value)
    
    # Only momentum flux units available - compile-time safe!
    @property
    def dyne_per_square_centimeters(self) -> 'MomentumFlux':
        self.variable.quantity = FastQuantity(self.value, MomentumFluxUnits.dyne_per_square_centimeter)
        return cast('MomentumFlux', self.variable)
    @property
    def gram_per_centimeter_per_square_seconds(self) -> 'MomentumFlux':
        self.variable.quantity = FastQuantity(self.value, MomentumFluxUnits.gram_per_centimeter_per_square_second)
        return cast('MomentumFlux', self.variable)
    @property
    def newton_per_square_meters(self) -> 'MomentumFlux':
        self.variable.quantity = FastQuantity(self.value, MomentumFluxUnits.newton_per_square_meter)
        return cast('MomentumFlux', self.variable)
    @property
    def pound_force_per_square_foots(self) -> 'MomentumFlux':
        self.variable.quantity = FastQuantity(self.value, MomentumFluxUnits.pound_force_per_square_foot)
        return cast('MomentumFlux', self.variable)
    @property
    def pound_mass_per_foot_per_square_seconds(self) -> 'MomentumFlux':
        self.variable.quantity = FastQuantity(self.value, MomentumFluxUnits.pound_mass_per_foot_per_square_second)
        return cast('MomentumFlux', self.variable)
    
    # Short aliases for convenience
    pass


class MomentumFlux(TypedVariable):
    """Type-safe momentum flux variable with expression capabilities."""
    
    _setter_class = MomentumFluxSetter
    _expected_dimension = PRESSURE
    _default_unit_property = "newton_per_square_meters"
    
    def set(self, value: float) -> MomentumFluxSetter:
        """Create a momentum flux setter for this variable with proper type annotation."""
        return MomentumFluxSetter(self, value)


class MomentumFluxModule(VariableModule):
    """MomentumFlux variable module definition."""
    
    def get_variable_class(self):
        return MomentumFlux
    
    def get_setter_class(self):
        return MomentumFluxSetter
    
    def get_expected_dimension(self):
        return PRESSURE


# Register this module for auto-discovery
VARIABLE_MODULE = MomentumFluxModule()