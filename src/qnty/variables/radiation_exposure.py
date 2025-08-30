"""
RadiationExposure Variable Module
==================================

Type-safe radiation exposure variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import RADIATION_EXPOSURE
from ..units import RadiationExposureUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class RadiationExposureSetter(TypeSafeSetter):
    """RadiationExposure-specific setter with only radiation exposure units."""
    
    def __init__(self, variable: 'RadiationExposure', value: float):
        super().__init__(variable, value)
    
    # Only radiation exposure units available - compile-time safe!
    @property
    def coulomb_per_kilograms(self) -> 'RadiationExposure':
        self.variable.quantity = FastQuantity(self.value, RadiationExposureUnits.coulomb_per_kilogram)
        return cast('RadiationExposure', self.variable)
    @property
    def d_units(self) -> 'RadiationExposure':
        self.variable.quantity = FastQuantity(self.value, RadiationExposureUnits.d_unit)
        return cast('RadiationExposure', self.variable)
    @property
    def pastille_dose_b_units(self) -> 'RadiationExposure':
        self.variable.quantity = FastQuantity(self.value, RadiationExposureUnits.pastille_dose_b_unit)
        return cast('RadiationExposure', self.variable)
    @property
    def röentgens(self) -> 'RadiationExposure':
        self.variable.quantity = FastQuantity(self.value, RadiationExposureUnits.röentgen)
        return cast('RadiationExposure', self.variable)
    
    # Short aliases for convenience
    pass


class RadiationExposure(TypedVariable):
    """Type-safe radiation exposure variable with expression capabilities."""
    
    _setter_class = RadiationExposureSetter
    _expected_dimension = RADIATION_EXPOSURE
    _default_unit_property = "coulomb_per_kilograms"
    
    def set(self, value: float) -> RadiationExposureSetter:
        """Create a radiation exposure setter for this variable with proper type annotation."""
        return RadiationExposureSetter(self, value)


class RadiationExposureModule(VariableModule):
    """RadiationExposure variable module definition."""
    
    def get_variable_class(self):
        return RadiationExposure
    
    def get_setter_class(self):
        return RadiationExposureSetter
    
    def get_expected_dimension(self):
        return RADIATION_EXPOSURE


# Register this module for auto-discovery
VARIABLE_MODULE = RadiationExposureModule()