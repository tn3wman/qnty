"""
ElectricFieldStrength Variable Module
======================================

Type-safe electric field strength variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_FIELD
from ..units import ElectricFieldStrengthUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricFieldStrengthSetter(TypeSafeSetter):
    """ElectricFieldStrength-specific setter with only electric field strength units."""
    
    def __init__(self, variable: 'ElectricFieldStrength', value: float):
        super().__init__(variable, value)
    
    # Only electric field strength units available - compile-time safe!
    @property
    def volt_per_centimeters(self) -> 'ElectricFieldStrength':
        self.variable.quantity = FastQuantity(self.value, ElectricFieldStrengthUnits.volt_per_centimeter)
        return cast('ElectricFieldStrength', self.variable)
    @property
    def volt_per_meters(self) -> 'ElectricFieldStrength':
        self.variable.quantity = FastQuantity(self.value, ElectricFieldStrengthUnits.volt_per_meter)
        return cast('ElectricFieldStrength', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricFieldStrength(TypedVariable):
    """Type-safe electric field strength variable with expression capabilities."""
    
    _setter_class = ElectricFieldStrengthSetter
    _expected_dimension = ELECTRIC_FIELD
    _default_unit_property = "volt_per_meters"
    
    def set(self, value: float) -> ElectricFieldStrengthSetter:
        """Create a electric field strength setter for this variable with proper type annotation."""
        return ElectricFieldStrengthSetter(self, value)


class ElectricFieldStrengthModule(VariableModule):
    """ElectricFieldStrength variable module definition."""
    
    def get_variable_class(self):
        return ElectricFieldStrength
    
    def get_setter_class(self):
        return ElectricFieldStrengthSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_FIELD


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricFieldStrengthModule()