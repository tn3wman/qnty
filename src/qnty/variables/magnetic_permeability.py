"""
MagneticPermeability Variable Module
=====================================

Type-safe magnetic permeability variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MAGNETIC_PERMEABILITY
from ..units import MagneticPermeabilityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MagneticPermeabilitySetter(TypeSafeSetter):
    """MagneticPermeability-specific setter with only magnetic permeability units."""
    
    def __init__(self, variable: 'MagneticPermeability', value: float):
        super().__init__(variable, value)
    
    # Only magnetic permeability units available - compile-time safe!
    @property
    def henrys_per_meters(self) -> 'MagneticPermeability':
        self.variable.quantity = FastQuantity(self.value, MagneticPermeabilityUnits.henrys_per_meter)
        return cast('MagneticPermeability', self.variable)
    @property
    def newton_per_square_amperes(self) -> 'MagneticPermeability':
        self.variable.quantity = FastQuantity(self.value, MagneticPermeabilityUnits.newton_per_square_ampere)
        return cast('MagneticPermeability', self.variable)
    
    # Short aliases for convenience
    pass


class MagneticPermeability(TypedVariable):
    """Type-safe magnetic permeability variable with expression capabilities."""
    
    _setter_class = MagneticPermeabilitySetter
    _expected_dimension = MAGNETIC_PERMEABILITY
    _default_unit_property = "henrys_per_meters"
    
    def set(self, value: float) -> MagneticPermeabilitySetter:
        """Create a magnetic permeability setter for this variable with proper type annotation."""
        return MagneticPermeabilitySetter(self, value)


class MagneticPermeabilityModule(VariableModule):
    """MagneticPermeability variable module definition."""
    
    def get_variable_class(self):
        return MagneticPermeability
    
    def get_setter_class(self):
        return MagneticPermeabilitySetter
    
    def get_expected_dimension(self):
        return MAGNETIC_PERMEABILITY


# Register this module for auto-discovery
VARIABLE_MODULE = MagneticPermeabilityModule()