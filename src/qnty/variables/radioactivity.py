"""
Radioactivity Variable Module
==============================

Type-safe radioactivity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import RADIOACTIVITY
from ..units import RadioactivityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class RadioactivitySetter(TypeSafeSetter):
    """Radioactivity-specific setter with only radioactivity units."""
    
    def __init__(self, variable: 'Radioactivity', value: float):
        super().__init__(variable, value)
    
    # Only radioactivity units available - compile-time safe!
    @property
    def becquerels(self) -> 'Radioactivity':
        self.variable.quantity = FastQuantity(self.value, RadioactivityUnits.becquerel)
        return cast('Radioactivity', self.variable)
    @property
    def curies(self) -> 'Radioactivity':
        self.variable.quantity = FastQuantity(self.value, RadioactivityUnits.curie)
        return cast('Radioactivity', self.variable)
    @property
    def mache_units(self) -> 'Radioactivity':
        self.variable.quantity = FastQuantity(self.value, RadioactivityUnits.mache_unit)
        return cast('Radioactivity', self.variable)
    @property
    def rutherfords(self) -> 'Radioactivity':
        self.variable.quantity = FastQuantity(self.value, RadioactivityUnits.rutherford)
        return cast('Radioactivity', self.variable)
    @property
    def stats(self) -> 'Radioactivity':
        self.variable.quantity = FastQuantity(self.value, RadioactivityUnits.stat)
        return cast('Radioactivity', self.variable)
    
    # Short aliases for convenience
    pass


class Radioactivity(TypedVariable):
    """Type-safe radioactivity variable with expression capabilities."""
    
    _setter_class = RadioactivitySetter
    _expected_dimension = RADIOACTIVITY
    _default_unit_property = "becquerels"
    
    def set(self, value: float) -> RadioactivitySetter:
        """Create a radioactivity setter for this variable with proper type annotation."""
        return RadioactivitySetter(self, value)


class RadioactivityModule(VariableModule):
    """Radioactivity variable module definition."""
    
    def get_variable_class(self):
        return Radioactivity
    
    def get_setter_class(self):
        return RadioactivitySetter
    
    def get_expected_dimension(self):
        return RADIOACTIVITY


# Register this module for auto-discovery
VARIABLE_MODULE = RadioactivityModule()