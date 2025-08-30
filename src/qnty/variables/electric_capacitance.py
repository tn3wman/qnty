"""
ElectricCapacitance Variable Module
====================================

Type-safe electric capacitance variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_CAPACITANCE
from ..units import ElectricCapacitanceUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricCapacitanceSetter(TypeSafeSetter):
    """ElectricCapacitance-specific setter with only electric capacitance units."""
    
    def __init__(self, variable: 'ElectricCapacitance', value: float):
        super().__init__(variable, value)
    
    # Only electric capacitance units available - compile-time safe!
    @property
    def cms(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.cm)
        return cast('ElectricCapacitance', self.variable)
    @property
    def abfarads(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.abfarad)
        return cast('ElectricCapacitance', self.variable)
    @property
    def farads(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.farad)
        return cast('ElectricCapacitance', self.variable)
    @property
    def farad_intls(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.farad_intl)
        return cast('ElectricCapacitance', self.variable)
    @property
    def jars(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.jar)
        return cast('ElectricCapacitance', self.variable)
    @property
    def puffs(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.puff)
        return cast('ElectricCapacitance', self.variable)
    @property
    def statfarads(self) -> 'ElectricCapacitance':
        self.variable.quantity = FastQuantity(self.value, ElectricCapacitanceUnits.statfarad)
        return cast('ElectricCapacitance', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricCapacitance(TypedVariable):
    """Type-safe electric capacitance variable with expression capabilities."""
    
    _setter_class = ElectricCapacitanceSetter
    _expected_dimension = ELECTRIC_CAPACITANCE
    _default_unit_property = "farads"
    
    def set(self, value: float) -> ElectricCapacitanceSetter:
        """Create a electric capacitance setter for this variable with proper type annotation."""
        return ElectricCapacitanceSetter(self, value)


class ElectricCapacitanceModule(VariableModule):
    """ElectricCapacitance variable module definition."""
    
    def get_variable_class(self):
        return ElectricCapacitance
    
    def get_setter_class(self):
        return ElectricCapacitanceSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_CAPACITANCE


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricCapacitanceModule()