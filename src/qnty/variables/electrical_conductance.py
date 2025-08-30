"""
ElectricalConductance Variable Module
======================================

Type-safe electrical conductance variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRICAL_CONDUCTANCE
from ..units import ElectricalConductanceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricalConductanceSetter(TypeSafeSetter):
    """ElectricalConductance-specific setter with only electrical conductance units."""
    
    def __init__(self, variable: 'ElectricalConductance', value: float):
        super().__init__(variable, value)
    
    # Only electrical conductance units available - compile-time safe!
    @property
    def emu_cgs(self) -> 'ElectricalConductance':
        self.variable.quantity = FastQuantity(self.value, ElectricalConductanceUnits.emu_cgs)
        return cast('ElectricalConductance', self.variable)
    @property
    def esu_cgs(self) -> 'ElectricalConductance':
        self.variable.quantity = FastQuantity(self.value, ElectricalConductanceUnits.esu_cgs)
        return cast('ElectricalConductance', self.variable)
    @property
    def mhos(self) -> 'ElectricalConductance':
        self.variable.quantity = FastQuantity(self.value, ElectricalConductanceUnits.mho)
        return cast('ElectricalConductance', self.variable)
    @property
    def microsiemens(self) -> 'ElectricalConductance':
        self.variable.quantity = FastQuantity(self.value, ElectricalConductanceUnits.microsiemens)
        return cast('ElectricalConductance', self.variable)
    @property
    def siemens(self) -> 'ElectricalConductance':
        self.variable.quantity = FastQuantity(self.value, ElectricalConductanceUnits.siemens)
        return cast('ElectricalConductance', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricalConductance(TypedVariable):
    """Type-safe electrical conductance variable with expression capabilities."""
    
    _setter_class = ElectricalConductanceSetter
    _expected_dimension = ELECTRICAL_CONDUCTANCE
    _default_unit_property = "mhos"
    
    def set(self, value: float) -> ElectricalConductanceSetter:
        """Create a electrical conductance setter for this variable with proper type annotation."""
        return ElectricalConductanceSetter(self, value)


class ElectricalConductanceModule(VariableModule):
    """ElectricalConductance variable module definition."""
    
    def get_variable_class(self):
        return ElectricalConductance
    
    def get_setter_class(self):
        return ElectricalConductanceSetter
    
    def get_expected_dimension(self):
        return ELECTRICAL_CONDUCTANCE


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricalConductanceModule()