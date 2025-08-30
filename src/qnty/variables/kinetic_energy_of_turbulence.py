"""
KineticEnergyOfTurbulence Variable Module
==========================================

Type-safe kinetic energy of turbulence variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import KineticEnergyOfTurbulenceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class KineticEnergyOfTurbulenceSetter(TypeSafeSetter):
    """KineticEnergyOfTurbulence-specific setter with only kinetic energy of turbulence units."""
    
    def __init__(self, variable: 'KineticEnergyOfTurbulence', value: float):
        super().__init__(variable, value)
    
    # Only kinetic energy of turbulence units available - compile-time safe!
    @property
    def square_foot_per_second_squareds(self) -> 'KineticEnergyOfTurbulence':
        self.variable.quantity = FastQuantity(self.value, KineticEnergyOfTurbulenceUnits.square_foot_per_second_squared)
        return cast('KineticEnergyOfTurbulence', self.variable)
    @property
    def square_meters_per_second_squareds(self) -> 'KineticEnergyOfTurbulence':
        self.variable.quantity = FastQuantity(self.value, KineticEnergyOfTurbulenceUnits.square_meters_per_second_squared)
        return cast('KineticEnergyOfTurbulence', self.variable)
    
    # Short aliases for convenience
    pass


class KineticEnergyOfTurbulence(TypedVariable):
    """Type-safe kinetic energy of turbulence variable with expression capabilities."""
    
    _setter_class = KineticEnergyOfTurbulenceSetter
    _expected_dimension = ENERGY
    _default_unit_property = "square_meters_per_second_squareds"
    
    def set(self, value: float) -> KineticEnergyOfTurbulenceSetter:
        """Create a kinetic energy of turbulence setter for this variable with proper type annotation."""
        return KineticEnergyOfTurbulenceSetter(self, value)


class KineticEnergyOfTurbulenceModule(VariableModule):
    """KineticEnergyOfTurbulence variable module definition."""
    
    def get_variable_class(self):
        return KineticEnergyOfTurbulence
    
    def get_setter_class(self):
        return KineticEnergyOfTurbulenceSetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = KineticEnergyOfTurbulenceModule()