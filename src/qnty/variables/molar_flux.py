"""
MolarFlux Variable Module
==========================

Type-safe molar flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MOLAR_FLUX
from ..units import MolarFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MolarFluxSetter(TypeSafeSetter):
    """MolarFlux-specific setter with only molar flux units."""
    
    def __init__(self, variable: 'MolarFlux', value: float):
        super().__init__(variable, value)
    
    # Only molar flux units available - compile-time safe!
    @property
    def kmol_per_square_meter_per_day(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.kmol_per_square_meter_per_day)
        return cast('MolarFlux', self.variable)
    @property
    def kmol_per_square_meter_per_hours(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.kmol_per_square_meter_per_hour)
        return cast('MolarFlux', self.variable)
    @property
    def kmol_per_square_meter_per_minutes(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.kmol_per_square_meter_per_minute)
        return cast('MolarFlux', self.variable)
    @property
    def kmol_per_square_meter_per_seconds(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.kmol_per_square_meter_per_second)
        return cast('MolarFlux', self.variable)
    @property
    def pound_mole_per_square_foot_per_day(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.pound_mole_per_square_foot_per_day)
        return cast('MolarFlux', self.variable)
    @property
    def pound_mole_per_square_foot_per_hours(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.pound_mole_per_square_foot_per_hour)
        return cast('MolarFlux', self.variable)
    @property
    def pound_mole_per_square_foot_per_minutes(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.pound_mole_per_square_foot_per_minute)
        return cast('MolarFlux', self.variable)
    @property
    def pound_mole_per_square_foot_per_seconds(self) -> 'MolarFlux':
        self.variable.quantity = FastQuantity(self.value, MolarFluxUnits.pound_mole_per_square_foot_per_second)
        return cast('MolarFlux', self.variable)
    
    # Short aliases for convenience
    pass


class MolarFlux(TypedVariable):
    """Type-safe molar flux variable with expression capabilities."""
    
    _setter_class = MolarFluxSetter
    _expected_dimension = MOLAR_FLUX
    _default_unit_property = "kmol_per_square_meter_per_seconds"
    
    def set(self, value: float) -> MolarFluxSetter:
        """Create a molar flux setter for this variable with proper type annotation."""
        return MolarFluxSetter(self, value)


class MolarFluxModule(VariableModule):
    """MolarFlux variable module definition."""
    
    def get_variable_class(self):
        return MolarFlux
    
    def get_setter_class(self):
        return MolarFluxSetter
    
    def get_expected_dimension(self):
        return MOLAR_FLUX


# Register this module for auto-discovery
VARIABLE_MODULE = MolarFluxModule()