"""
VolumetricMassFlowRate Variable Module
=======================================

Type-safe volumetric mass flow rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import VOLUMETRIC_MASS_FLOW_RATE
from ..units import VolumetricMassFlowRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumetricMassFlowRateSetter(TypeSafeSetter):
    """VolumetricMassFlowRate-specific setter with only volumetric mass flow rate units."""
    
    def __init__(self, variable: 'VolumetricMassFlowRate', value: float):
        super().__init__(variable, value)
    
    # Only volumetric mass flow rate units available - compile-time safe!
    @property
    def gram_per_second_per_cubic_centimeters(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.gram_per_second_per_cubic_centimeter)
        return cast('VolumetricMassFlowRate', self.variable)
    @property
    def kilogram_per_hour_per_cubic_foots(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.kilogram_per_hour_per_cubic_foot)
        return cast('VolumetricMassFlowRate', self.variable)
    @property
    def kilogram_per_hour_per_cubic_meters(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.kilogram_per_hour_per_cubic_meter)
        return cast('VolumetricMassFlowRate', self.variable)
    @property
    def kilogram_per_second_per_cubic_meters(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.kilogram_per_second_per_cubic_meter)
        return cast('VolumetricMassFlowRate', self.variable)
    @property
    def pound_per_hour_per_cubic_foots(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.pound_per_hour_per_cubic_foot)
        return cast('VolumetricMassFlowRate', self.variable)
    @property
    def pound_per_minute_per_cubic_foots(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.pound_per_minute_per_cubic_foot)
        return cast('VolumetricMassFlowRate', self.variable)
    @property
    def pound_per_second_per_cubic_foots(self) -> 'VolumetricMassFlowRate':
        self.variable.quantity = FastQuantity(self.value, VolumetricMassFlowRateUnits.pound_per_second_per_cubic_foot)
        return cast('VolumetricMassFlowRate', self.variable)
    
    # Short aliases for convenience
    pass


class VolumetricMassFlowRate(TypedVariable):
    """Type-safe volumetric mass flow rate variable with expression capabilities."""
    
    _setter_class = VolumetricMassFlowRateSetter
    _expected_dimension = VOLUMETRIC_MASS_FLOW_RATE
    _default_unit_property = "kilogram_per_second_per_cubic_meters"
    
    def set(self, value: float) -> VolumetricMassFlowRateSetter:
        """Create a volumetric mass flow rate setter for this variable with proper type annotation."""
        return VolumetricMassFlowRateSetter(self, value)


class VolumetricMassFlowRateModule(VariableModule):
    """VolumetricMassFlowRate variable module definition."""
    
    def get_variable_class(self):
        return VolumetricMassFlowRate
    
    def get_setter_class(self):
        return VolumetricMassFlowRateSetter
    
    def get_expected_dimension(self):
        return VOLUMETRIC_MASS_FLOW_RATE


# Register this module for auto-discovery
VARIABLE_MODULE = VolumetricMassFlowRateModule()