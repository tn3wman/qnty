"""
FrequencyVoltageRatio Variable Module
======================================

Type-safe frequency voltage ratio variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import FREQUENCY_VOLTAGE_RATIO
from ..units import FrequencyVoltageRatioUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class FrequencyVoltageRatioSetter(TypeSafeSetter):
    """FrequencyVoltageRatio-specific setter with only frequency voltage ratio units."""
    
    def __init__(self, variable: 'FrequencyVoltageRatio', value: float):
        super().__init__(variable, value)
    
    # Only frequency voltage ratio units available - compile-time safe!
    @property
    def cycles_per_second_per_volts(self) -> 'FrequencyVoltageRatio':
        self.variable.quantity = FastQuantity(self.value, FrequencyVoltageRatioUnits.cycles_per_second_per_volt)
        return cast('FrequencyVoltageRatio', self.variable)
    @property
    def hertz_per_volts(self) -> 'FrequencyVoltageRatio':
        self.variable.quantity = FastQuantity(self.value, FrequencyVoltageRatioUnits.hertz_per_volt)
        return cast('FrequencyVoltageRatio', self.variable)
    @property
    def terahertz_per_volts(self) -> 'FrequencyVoltageRatio':
        self.variable.quantity = FastQuantity(self.value, FrequencyVoltageRatioUnits.terahertz_per_volt)
        return cast('FrequencyVoltageRatio', self.variable)
    
    # Short aliases for convenience
    pass


class FrequencyVoltageRatio(TypedVariable):
    """Type-safe frequency voltage ratio variable with expression capabilities."""
    
    _setter_class = FrequencyVoltageRatioSetter
    _expected_dimension = FREQUENCY_VOLTAGE_RATIO
    _default_unit_property = "cycles_per_second_per_volts"
    
    def set(self, value: float) -> FrequencyVoltageRatioSetter:
        """Create a frequency voltage ratio setter for this variable with proper type annotation."""
        return FrequencyVoltageRatioSetter(self, value)


class FrequencyVoltageRatioModule(VariableModule):
    """FrequencyVoltageRatio variable module definition."""
    
    def get_variable_class(self):
        return FrequencyVoltageRatio
    
    def get_setter_class(self):
        return FrequencyVoltageRatioSetter
    
    def get_expected_dimension(self):
        return FREQUENCY_VOLTAGE_RATIO


# Register this module for auto-discovery
VARIABLE_MODULE = FrequencyVoltageRatioModule()