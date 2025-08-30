"""
MolarFlowRate Variable Module
==============================

Type-safe molar flow rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MOLAR_FLOW_RATE
from ..units import MolarFlowRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MolarFlowRateSetter(TypeSafeSetter):
    """MolarFlowRate-specific setter with only molar flow rate units."""
    
    def __init__(self, variable: 'MolarFlowRate', value: float):
        super().__init__(variable, value)
    
    # Only molar flow rate units available - compile-time safe!
    @property
    def gram_mole_per_day(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.gram_mole_per_day)
        return cast('MolarFlowRate', self.variable)
    @property
    def gram_mole_per_hours(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.gram_mole_per_hour)
        return cast('MolarFlowRate', self.variable)
    @property
    def gram_mole_per_minutes(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.gram_mole_per_minute)
        return cast('MolarFlowRate', self.variable)
    @property
    def gram_mole_per_seconds(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.gram_mole_per_second)
        return cast('MolarFlowRate', self.variable)
    @property
    def kilogram_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.kilogram_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def kilogram_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.kilogram_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def kilogram_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.kilogram_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def kilogram_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.kilogram_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def pound_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.pound_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def pound_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.pound_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def pound_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.pound_mole)
        return cast('MolarFlowRate', self.variable)
    @property
    def pound_moles(self) -> 'MolarFlowRate':
        self.variable.quantity = FastQuantity(self.value, MolarFlowRateUnits.pound_mole)
        return cast('MolarFlowRate', self.variable)
    
    # Short aliases for convenience
    pass


class MolarFlowRate(TypedVariable):
    """Type-safe molar flow rate variable with expression capabilities."""
    
    _setter_class = MolarFlowRateSetter
    _expected_dimension = MOLAR_FLOW_RATE
    _default_unit_property = "kilogram_moles"
    
    def set(self, value: float) -> MolarFlowRateSetter:
        """Create a molar flow rate setter for this variable with proper type annotation."""
        return MolarFlowRateSetter(self, value)


class MolarFlowRateModule(VariableModule):
    """MolarFlowRate variable module definition."""
    
    def get_variable_class(self):
        return MolarFlowRate
    
    def get_setter_class(self):
        return MolarFlowRateSetter
    
    def get_expected_dimension(self):
        return MOLAR_FLOW_RATE


# Register this module for auto-discovery
VARIABLE_MODULE = MolarFlowRateModule()