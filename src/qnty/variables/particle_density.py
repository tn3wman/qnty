"""
ParticleDensity Variable Module
================================

Type-safe particle density variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import PARTICLE_DENSITY
from ..units import ParticleDensityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ParticleDensitySetter(TypeSafeSetter):
    """ParticleDensity-specific setter with only particle density units."""
    
    def __init__(self, variable: 'ParticleDensity', value: float):
        super().__init__(variable, value)
    
    # Only particle density units available - compile-time safe!
    @property
    def particles_per_cubic_centimeters(self) -> 'ParticleDensity':
        self.variable.quantity = FastQuantity(self.value, ParticleDensityUnits.particles_per_cubic_centimeter)
        return cast('ParticleDensity', self.variable)
    @property
    def particles_per_cubic_foots(self) -> 'ParticleDensity':
        self.variable.quantity = FastQuantity(self.value, ParticleDensityUnits.particles_per_cubic_foot)
        return cast('ParticleDensity', self.variable)
    @property
    def particles_per_cubic_meters(self) -> 'ParticleDensity':
        self.variable.quantity = FastQuantity(self.value, ParticleDensityUnits.particles_per_cubic_meter)
        return cast('ParticleDensity', self.variable)
    @property
    def particles_per_gallon_us(self) -> 'ParticleDensity':
        self.variable.quantity = FastQuantity(self.value, ParticleDensityUnits.particles_per_gallon_us)
        return cast('ParticleDensity', self.variable)
    @property
    def particles_per_liters(self) -> 'ParticleDensity':
        self.variable.quantity = FastQuantity(self.value, ParticleDensityUnits.particles_per_liter)
        return cast('ParticleDensity', self.variable)
    @property
    def particles_per_milliliters(self) -> 'ParticleDensity':
        self.variable.quantity = FastQuantity(self.value, ParticleDensityUnits.particles_per_milliliter)
        return cast('ParticleDensity', self.variable)
    
    # Short aliases for convenience
    pass


class ParticleDensity(TypedVariable):
    """Type-safe particle density variable with expression capabilities."""
    
    _setter_class = ParticleDensitySetter
    _expected_dimension = PARTICLE_DENSITY
    _default_unit_property = "particles_per_cubic_meters"
    
    def set(self, value: float) -> ParticleDensitySetter:
        """Create a particle density setter for this variable with proper type annotation."""
        return ParticleDensitySetter(self, value)


class ParticleDensityModule(VariableModule):
    """ParticleDensity variable module definition."""
    
    def get_variable_class(self):
        return ParticleDensity
    
    def get_setter_class(self):
        return ParticleDensitySetter
    
    def get_expected_dimension(self):
        return PARTICLE_DENSITY


# Register this module for auto-discovery
VARIABLE_MODULE = ParticleDensityModule()