"""
Permeability Variable Module
=============================

Type-safe permeability variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import AREA
from ..units import PermeabilityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class PermeabilitySetter(TypeSafeSetter):
    """Permeability-specific setter with only permeability units."""
    
    def __init__(self, variable: 'Permeability', value: float):
        super().__init__(variable, value)
    
    # Only permeability units available - compile-time safe!
    @property
    def darcy(self) -> 'Permeability':
        self.variable.quantity = FastQuantity(self.value, PermeabilityUnits.darcy)
        return cast('Permeability', self.variable)
    @property
    def square_feets(self) -> 'Permeability':
        self.variable.quantity = FastQuantity(self.value, PermeabilityUnits.square_feet)
        return cast('Permeability', self.variable)
    @property
    def square_meters(self) -> 'Permeability':
        self.variable.quantity = FastQuantity(self.value, PermeabilityUnits.square_meters)
        return cast('Permeability', self.variable)
    
    # Short aliases for convenience
    pass


class Permeability(TypedVariable):
    """Type-safe permeability variable with expression capabilities."""
    
    _setter_class = PermeabilitySetter
    _expected_dimension = AREA
    _default_unit_property = "square_meters"
    
    def set(self, value: float) -> PermeabilitySetter:
        """Create a permeability setter for this variable with proper type annotation."""
        return PermeabilitySetter(self, value)


class PermeabilityModule(VariableModule):
    """Permeability variable module definition."""
    
    def get_variable_class(self):
        return Permeability
    
    def get_setter_class(self):
        return PermeabilitySetter
    
    def get_expected_dimension(self):
        return AREA


# Register this module for auto-discovery
VARIABLE_MODULE = PermeabilityModule()