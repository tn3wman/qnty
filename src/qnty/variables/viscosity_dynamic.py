"""
ViscosityDynamic Variable Module
=================================

Type-safe viscosity, dynamic variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DYNAMIC_VISCOSITY
from ..units import ViscosityDynamicUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ViscosityDynamicSetter(TypeSafeSetter):
    """ViscosityDynamic-specific setter with only viscosity, dynamic units."""
    
    def __init__(self, variable: 'ViscosityDynamic', value: float):
        super().__init__(variable, value)
    
    # Only viscosity, dynamic units available - compile-time safe!
    @property
    def centipoises(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.centipoise)
        return cast('ViscosityDynamic', self.variable)
    @property
    def dyne_second_per_square_centimeters(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.dyne_second_per_square_centimeter)
        return cast('ViscosityDynamic', self.variable)
    @property
    def kilopound_second_per_square_meters(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.kilopound_second_per_square_meter)
        return cast('ViscosityDynamic', self.variable)
    @property
    def millipoises(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.millipoise)
        return cast('ViscosityDynamic', self.variable)
    @property
    def newton_second_per_square_meters(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.newton_second_per_square_meter)
        return cast('ViscosityDynamic', self.variable)
    @property
    def pascal_seconds(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.pascal_second)
        return cast('ViscosityDynamic', self.variable)
    @property
    def poises(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.poise)
        return cast('ViscosityDynamic', self.variable)
    @property
    def pound_force_hour_per_square_foots(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.pound_force_hour_per_square_foot)
        return cast('ViscosityDynamic', self.variable)
    @property
    def pound_force_second_per_square_foots(self) -> 'ViscosityDynamic':
        self.variable.quantity = FastQuantity(self.value, ViscosityDynamicUnits.pound_force_second_per_square_foot)
        return cast('ViscosityDynamic', self.variable)
    
    # Short aliases for convenience
    pass


class ViscosityDynamic(TypedVariable):
    """Type-safe viscosity, dynamic variable with expression capabilities."""
    
    _setter_class = ViscosityDynamicSetter
    _expected_dimension = DYNAMIC_VISCOSITY
    _default_unit_property = "dyne_second_per_square_centimeters"
    
    def set(self, value: float) -> ViscosityDynamicSetter:
        """Create a viscosity, dynamic setter for this variable with proper type annotation."""
        return ViscosityDynamicSetter(self, value)


class ViscosityDynamicModule(VariableModule):
    """ViscosityDynamic variable module definition."""
    
    def get_variable_class(self):
        return ViscosityDynamic
    
    def get_setter_class(self):
        return ViscosityDynamicSetter
    
    def get_expected_dimension(self):
        return DYNAMIC_VISCOSITY


# Register this module for auto-discovery
VARIABLE_MODULE = ViscosityDynamicModule()