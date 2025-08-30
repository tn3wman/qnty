"""
PhotonEmissionRate Variable Module
===================================

Type-safe photon emission rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import PHOTON_EMISSION_RATE
from ..units import PhotonEmissionRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class PhotonEmissionRateSetter(TypeSafeSetter):
    """PhotonEmissionRate-specific setter with only photon emission rate units."""
    
    def __init__(self, variable: 'PhotonEmissionRate', value: float):
        super().__init__(variable, value)
    
    # Only photon emission rate units available - compile-time safe!
    @property
    def rayleighs(self) -> 'PhotonEmissionRate':
        self.variable.quantity = FastQuantity(self.value, PhotonEmissionRateUnits.rayleigh)
        return cast('PhotonEmissionRate', self.variable)
    @property
    def reciprocal_square_meter_seconds(self) -> 'PhotonEmissionRate':
        self.variable.quantity = FastQuantity(self.value, PhotonEmissionRateUnits.reciprocal_square_meter_second)
        return cast('PhotonEmissionRate', self.variable)
    
    # Short aliases for convenience
    pass


class PhotonEmissionRate(TypedVariable):
    """Type-safe photon emission rate variable with expression capabilities."""
    
    _setter_class = PhotonEmissionRateSetter
    _expected_dimension = PHOTON_EMISSION_RATE
    _default_unit_property = "reciprocal_square_meter_seconds"
    
    def set(self, value: float) -> PhotonEmissionRateSetter:
        """Create a photon emission rate setter for this variable with proper type annotation."""
        return PhotonEmissionRateSetter(self, value)


class PhotonEmissionRateModule(VariableModule):
    """PhotonEmissionRate variable module definition."""
    
    def get_variable_class(self):
        return PhotonEmissionRate
    
    def get_setter_class(self):
        return PhotonEmissionRateSetter
    
    def get_expected_dimension(self):
        return PHOTON_EMISSION_RATE


# Register this module for auto-discovery
VARIABLE_MODULE = PhotonEmissionRateModule()