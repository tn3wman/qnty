"""
MomentOfInertia Variable Module
================================

Type-safe moment of inertia variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MOMENT_OF_INERTIA
from ..units import MomentOfInertiaUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MomentOfInertiaSetter(TypeSafeSetter):
    """MomentOfInertia-specific setter with only moment of inertia units."""
    
    def __init__(self, variable: 'MomentOfInertia', value: float):
        super().__init__(variable, value)
    
    # Only moment of inertia units available - compile-time safe!
    @property
    def gram_force_centimeter_square_seconds(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.gram_force_centimeter_square_second)
        return cast('MomentOfInertia', self.variable)
    @property
    def gram_square_centimeters(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.gram_square_centimeter)
        return cast('MomentOfInertia', self.variable)
    @property
    def kilogram_force_centimeter_square_seconds(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.kilogram_force_centimeter_square_second)
        return cast('MomentOfInertia', self.variable)
    @property
    def kilogram_force_meter_square_seconds(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.kilogram_force_meter_square_second)
        return cast('MomentOfInertia', self.variable)
    @property
    def kilogram_square_centimeters(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.kilogram_square_centimeter)
        return cast('MomentOfInertia', self.variable)
    @property
    def kilogram_square_meters(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.kilogram_square_meter)
        return cast('MomentOfInertia', self.variable)
    @property
    def ounce_force_inch_square_seconds(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.ounce_force_inch_square_second)
        return cast('MomentOfInertia', self.variable)
    @property
    def ounce_mass_square_inchs(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.ounce_mass_square_inch)
        return cast('MomentOfInertia', self.variable)
    @property
    def pound_mass_square_foots(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.pound_mass_square_foot)
        return cast('MomentOfInertia', self.variable)
    @property
    def pound_mass_square_inchs(self) -> 'MomentOfInertia':
        self.variable.quantity = FastQuantity(self.value, MomentOfInertiaUnits.pound_mass_square_inch)
        return cast('MomentOfInertia', self.variable)
    
    # Short aliases for convenience
    pass


class MomentOfInertia(TypedVariable):
    """Type-safe moment of inertia variable with expression capabilities."""
    
    _setter_class = MomentOfInertiaSetter
    _expected_dimension = MOMENT_OF_INERTIA
    _default_unit_property = "kilogram_square_meters"
    
    def set(self, value: float) -> MomentOfInertiaSetter:
        """Create a moment of inertia setter for this variable with proper type annotation."""
        return MomentOfInertiaSetter(self, value)


class MomentOfInertiaModule(VariableModule):
    """MomentOfInertia variable module definition."""
    
    def get_variable_class(self):
        return MomentOfInertia
    
    def get_setter_class(self):
        return MomentOfInertiaSetter
    
    def get_expected_dimension(self):
        return MOMENT_OF_INERTIA


# Register this module for auto-discovery
VARIABLE_MODULE = MomentOfInertiaModule()