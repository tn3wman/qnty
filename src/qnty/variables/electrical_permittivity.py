"""
ElectricalPermittivity Variable Module
=======================================

Type-safe electrical permittivity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRICAL_PERMITTIVITY
from ..units import ElectricalPermittivityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricalPermittivitySetter(TypeSafeSetter):
    """ElectricalPermittivity-specific setter with only electrical permittivity units."""
    
    def __init__(self, variable: 'ElectricalPermittivity', value: float):
        super().__init__(variable, value)
    
    # Only electrical permittivity units available - compile-time safe!
    @property
    def farad_per_meters(self) -> 'ElectricalPermittivity':
        self.variable.quantity = FastQuantity(self.value, ElectricalPermittivityUnits.farad_per_meter)
        return cast('ElectricalPermittivity', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricalPermittivity(TypedVariable):
    """Type-safe electrical permittivity variable with expression capabilities."""
    
    _setter_class = ElectricalPermittivitySetter
    _expected_dimension = ELECTRICAL_PERMITTIVITY
    _default_unit_property = "farad_per_meters"
    
    def set(self, value: float) -> ElectricalPermittivitySetter:
        """Create a electrical permittivity setter for this variable with proper type annotation."""
        return ElectricalPermittivitySetter(self, value)


class ElectricalPermittivityModule(VariableModule):
    """ElectricalPermittivity variable module definition."""
    
    def get_variable_class(self):
        return ElectricalPermittivity
    
    def get_setter_class(self):
        return ElectricalPermittivitySetter
    
    def get_expected_dimension(self):
        return ELECTRICAL_PERMITTIVITY


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricalPermittivityModule()