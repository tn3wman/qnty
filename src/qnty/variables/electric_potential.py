"""
ElectricPotential Variable Module
==================================

Type-safe electric potential variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_POTENTIAL
from ..units import ElectricPotentialUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricPotentialSetter(TypeSafeSetter):
    """ElectricPotential-specific setter with only electric potential units."""
    
    def __init__(self, variable: 'ElectricPotential', value: float):
        super().__init__(variable, value)
    
    # Only electric potential units available - compile-time safe!
    @property
    def abvolts(self) -> 'ElectricPotential':
        self.variable.quantity = FastQuantity(self.value, ElectricPotentialUnits.abvolt)
        return cast('ElectricPotential', self.variable)
    @property
    def statvolts(self) -> 'ElectricPotential':
        self.variable.quantity = FastQuantity(self.value, ElectricPotentialUnits.statvolt)
        return cast('ElectricPotential', self.variable)
    @property
    def ua_potentials(self) -> 'ElectricPotential':
        self.variable.quantity = FastQuantity(self.value, ElectricPotentialUnits.ua_potential)
        return cast('ElectricPotential', self.variable)
    @property
    def volts(self) -> 'ElectricPotential':
        self.variable.quantity = FastQuantity(self.value, ElectricPotentialUnits.volt)
        return cast('ElectricPotential', self.variable)
    @property
    def volt_intl_means(self) -> 'ElectricPotential':
        self.variable.quantity = FastQuantity(self.value, ElectricPotentialUnits.volt_intl_mean)
        return cast('ElectricPotential', self.variable)
    @property
    def volt_us(self) -> 'ElectricPotential':
        self.variable.quantity = FastQuantity(self.value, ElectricPotentialUnits.volt_us)
        return cast('ElectricPotential', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricPotential(TypedVariable):
    """Type-safe electric potential variable with expression capabilities."""
    
    _setter_class = ElectricPotentialSetter
    _expected_dimension = ELECTRIC_POTENTIAL
    _default_unit_property = "volts"
    
    def set(self, value: float) -> ElectricPotentialSetter:
        """Create a electric potential setter for this variable with proper type annotation."""
        return ElectricPotentialSetter(self, value)


class ElectricPotentialModule(VariableModule):
    """ElectricPotential variable module definition."""
    
    def get_variable_class(self):
        return ElectricPotential
    
    def get_setter_class(self):
        return ElectricPotentialSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_POTENTIAL


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricPotentialModule()