"""
ElectricalResistivity Variable Module
======================================

Type-safe electrical resistivity variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRICAL_RESISTIVITY
from ..units import ElectricalResistivityUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricalResistivitySetter(TypeSafeSetter):
    """ElectricalResistivity-specific setter with only electrical resistivity units."""
    
    def __init__(self, variable: 'ElectricalResistivity', value: float):
        super().__init__(variable, value)
    
    # Only electrical resistivity units available - compile-time safe!
    @property
    def circular_milohm_per_foots(self) -> 'ElectricalResistivity':
        self.variable.quantity = FastQuantity(self.value, ElectricalResistivityUnits.circular_milohm_per_foot)
        return cast('ElectricalResistivity', self.variable)
    @property
    def emu_cgs(self) -> 'ElectricalResistivity':
        self.variable.quantity = FastQuantity(self.value, ElectricalResistivityUnits.emu_cgs)
        return cast('ElectricalResistivity', self.variable)
    @property
    def microhminchs(self) -> 'ElectricalResistivity':
        self.variable.quantity = FastQuantity(self.value, ElectricalResistivityUnits.microhminch)
        return cast('ElectricalResistivity', self.variable)
    @property
    def ohmcentimeters(self) -> 'ElectricalResistivity':
        self.variable.quantity = FastQuantity(self.value, ElectricalResistivityUnits.ohmcentimeter)
        return cast('ElectricalResistivity', self.variable)
    @property
    def ohmmeters(self) -> 'ElectricalResistivity':
        self.variable.quantity = FastQuantity(self.value, ElectricalResistivityUnits.ohmmeter)
        return cast('ElectricalResistivity', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricalResistivity(TypedVariable):
    """Type-safe electrical resistivity variable with expression capabilities."""
    
    _setter_class = ElectricalResistivitySetter
    _expected_dimension = ELECTRICAL_RESISTIVITY
    _default_unit_property = "ohmmeters"
    
    def set(self, value: float) -> ElectricalResistivitySetter:
        """Create a electrical resistivity setter for this variable with proper type annotation."""
        return ElectricalResistivitySetter(self, value)


class ElectricalResistivityModule(VariableModule):
    """ElectricalResistivity variable module definition."""
    
    def get_variable_class(self):
        return ElectricalResistivity
    
    def get_setter_class(self):
        return ElectricalResistivitySetter
    
    def get_expected_dimension(self):
        return ELECTRICAL_RESISTIVITY


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricalResistivityModule()