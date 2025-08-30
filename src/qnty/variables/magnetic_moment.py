"""
MagneticMoment Variable Module
===============================

Type-safe magnetic moment variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MAGNETIC_MOMENT
from ..units import MagneticMomentUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MagneticMomentSetter(TypeSafeSetter):
    """MagneticMoment-specific setter with only magnetic moment units."""
    
    def __init__(self, variable: 'MagneticMoment', value: float):
        super().__init__(variable, value)
    
    # Only magnetic moment units available - compile-time safe!
    @property
    def bohr_magnetons(self) -> 'MagneticMoment':
        self.variable.quantity = FastQuantity(self.value, MagneticMomentUnits.bohr_magneton)
        return cast('MagneticMoment', self.variable)
    @property
    def joule_per_teslas(self) -> 'MagneticMoment':
        self.variable.quantity = FastQuantity(self.value, MagneticMomentUnits.joule_per_tesla)
        return cast('MagneticMoment', self.variable)
    @property
    def nuclear_magnetons(self) -> 'MagneticMoment':
        self.variable.quantity = FastQuantity(self.value, MagneticMomentUnits.nuclear_magneton)
        return cast('MagneticMoment', self.variable)
    
    # Short aliases for convenience
    pass


class MagneticMoment(TypedVariable):
    """Type-safe magnetic moment variable with expression capabilities."""
    
    _setter_class = MagneticMomentSetter
    _expected_dimension = MAGNETIC_MOMENT
    _default_unit_property = "joule_per_teslas"
    
    def set(self, value: float) -> MagneticMomentSetter:
        """Create a magnetic moment setter for this variable with proper type annotation."""
        return MagneticMomentSetter(self, value)


class MagneticMomentModule(VariableModule):
    """MagneticMoment variable module definition."""
    
    def get_variable_class(self):
        return MagneticMoment
    
    def get_setter_class(self):
        return MagneticMomentSetter
    
    def get_expected_dimension(self):
        return MAGNETIC_MOMENT


# Register this module for auto-discovery
VARIABLE_MODULE = MagneticMomentModule()