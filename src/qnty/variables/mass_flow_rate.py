"""
MassFlowRate Variable Module
=============================

Type-safe mass flow rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MASS_FLOW_RATE
from ..units import MassFlowRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MassFlowRateSetter(TypeSafeSetter):
    """MassFlowRate-specific setter with only mass flow rate units."""
    
    def __init__(self, variable: 'MassFlowRate', value: float):
        super().__init__(variable, value)
    
    # Only mass flow rate units available - compile-time safe!
    @property
    def kilograms_per_day(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.kilograms_per_day)
        return cast('MassFlowRate', self.variable)
    @property
    def kilograms_per_hours(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.kilograms_per_hour)
        return cast('MassFlowRate', self.variable)
    @property
    def kilograms_per_minutes(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.kilograms_per_minute)
        return cast('MassFlowRate', self.variable)
    @property
    def kilograms_per_seconds(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.kilograms_per_second)
        return cast('MassFlowRate', self.variable)
    @property
    def metric_tons_per_day(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.metric_tons_per_day)
        return cast('MassFlowRate', self.variable)
    @property
    def metric_tons_per_hours(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.metric_tons_per_hour)
        return cast('MassFlowRate', self.variable)
    @property
    def metric_tons_per_minutes(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.metric_tons_per_minute)
        return cast('MassFlowRate', self.variable)
    @property
    def metric_tons_per_seconds(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.metric_tons_per_second)
        return cast('MassFlowRate', self.variable)
    @property
    def metric_tons_per_year_365_ds(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.metric_tons_per_year_365_d)
        return cast('MassFlowRate', self.variable)
    @property
    def pounds_per_day(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.pounds_per_day)
        return cast('MassFlowRate', self.variable)
    @property
    def pounds_per_hours(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.pounds_per_hour)
        return cast('MassFlowRate', self.variable)
    @property
    def pounds_per_minutes(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.pounds_per_minute)
        return cast('MassFlowRate', self.variable)
    @property
    def pounds_per_seconds(self) -> 'MassFlowRate':
        self.variable.quantity = FastQuantity(self.value, MassFlowRateUnits.pounds_per_second)
        return cast('MassFlowRate', self.variable)
    
    # Short aliases for convenience
    pass


class MassFlowRate(TypedVariable):
    """Type-safe mass flow rate variable with expression capabilities."""
    
    _setter_class = MassFlowRateSetter
    _expected_dimension = MASS_FLOW_RATE
    _default_unit_property = "kilograms_per_seconds"
    
    def set(self, value: float) -> MassFlowRateSetter:
        """Create a mass flow rate setter for this variable with proper type annotation."""
        return MassFlowRateSetter(self, value)


class MassFlowRateModule(VariableModule):
    """MassFlowRate variable module definition."""
    
    def get_variable_class(self):
        return MassFlowRate
    
    def get_setter_class(self):
        return MassFlowRateSetter
    
    def get_expected_dimension(self):
        return MASS_FLOW_RATE


# Register this module for auto-discovery
VARIABLE_MODULE = MassFlowRateModule()