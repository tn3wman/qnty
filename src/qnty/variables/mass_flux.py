"""
MassFlux Variable Module
=========================

Type-safe mass flux variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS_FLUX
from ..units import MassFluxUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MassFluxSetter(TypeSafeSetter):
    """MassFlux-specific setter with only mass flux units."""
    
    def __init__(self, variable: 'MassFlux', value: float):
        super().__init__(variable, value)
    
    # Only mass flux units available - compile-time safe!
    @property
    def kilogram_per_square_meter_per_day(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.kilogram_per_square_meter_per_day)
        return cast('MassFlux', self.variable)
    @property
    def kilogram_per_square_meter_per_hours(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.kilogram_per_square_meter_per_hour)
        return cast('MassFlux', self.variable)
    @property
    def kilogram_per_square_meter_per_minutes(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.kilogram_per_square_meter_per_minute)
        return cast('MassFlux', self.variable)
    @property
    def kilogram_per_square_meter_per_seconds(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.kilogram_per_square_meter_per_second)
        return cast('MassFlux', self.variable)
    @property
    def pound_per_square_foot_per_day(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.pound_per_square_foot_per_day)
        return cast('MassFlux', self.variable)
    @property
    def pound_per_square_foot_per_hours(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.pound_per_square_foot_per_hour)
        return cast('MassFlux', self.variable)
    @property
    def pound_per_square_foot_per_minutes(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.pound_per_square_foot_per_minute)
        return cast('MassFlux', self.variable)
    @property
    def pound_per_square_foot_per_seconds(self) -> 'MassFlux':
        self.variable.quantity = FastQuantity(self.value, MassFluxUnits.pound_per_square_foot_per_second)
        return cast('MassFlux', self.variable)
    
    # Short aliases for convenience
    pass


class MassFlux(TypedVariable):
    """Type-safe mass flux variable with expression capabilities."""
    
    _setter_class = MassFluxSetter
    _expected_dimension = MASS_FLUX
    _default_unit_property = "kilogram_per_square_meter_per_seconds"
    
    def set(self, value: float) -> MassFluxSetter:
        """Create a mass flux setter for this variable with proper type annotation."""
        return MassFluxSetter(self, value)


class MassFluxModule(VariableModule):
    """MassFlux variable module definition."""
    
    def get_variable_class(self):
        return MassFlux
    
    def get_setter_class(self):
        return MassFluxSetter
    
    def get_expected_dimension(self):
        return MASS_FLUX


# Register this module for auto-discovery
VARIABLE_MODULE = MassFluxModule()