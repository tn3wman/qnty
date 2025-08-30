"""
ElectricCharge Variable Module
===============================

Type-safe electric charge variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_CHARGE
from ..units import ElectricChargeUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricChargeSetter(TypeSafeSetter):
    """ElectricCharge-specific setter with only electric charge units."""
    
    def __init__(self, variable: 'ElectricCharge', value: float):
        super().__init__(variable, value)
    
    # Only electric charge units available - compile-time safe!
    @property
    def abcoulombs(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.abcoulomb)
        return cast('ElectricCharge', self.variable)
    @property
    def amperehours(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.amperehour)
        return cast('ElectricCharge', self.variable)
    @property
    def coulombs(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.coulomb)
        return cast('ElectricCharge', self.variable)
    @property
    def faraday_c12s(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.faraday_c12)
        return cast('ElectricCharge', self.variable)
    @property
    def franklins(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.franklin)
        return cast('ElectricCharge', self.variable)
    @property
    def statcoulombs(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.statcoulomb)
        return cast('ElectricCharge', self.variable)
    @property
    def ua_charges(self) -> 'ElectricCharge':
        self.variable.quantity = FastQuantity(self.value, ElectricChargeUnits.ua_charge)
        return cast('ElectricCharge', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricCharge(TypedVariable):
    """Type-safe electric charge variable with expression capabilities."""
    
    _setter_class = ElectricChargeSetter
    _expected_dimension = ELECTRIC_CHARGE
    _default_unit_property = "faraday_c12s"
    
    def set(self, value: float) -> ElectricChargeSetter:
        """Create a electric charge setter for this variable with proper type annotation."""
        return ElectricChargeSetter(self, value)


class ElectricChargeModule(VariableModule):
    """ElectricCharge variable module definition."""
    
    def get_variable_class(self):
        return ElectricCharge
    
    def get_setter_class(self):
        return ElectricChargeSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_CHARGE


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricChargeModule()