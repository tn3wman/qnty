"""
TurbulenceEnergyDissipationRate Variable Module
================================================

Type-safe turbulence energy dissipation rate variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import TURBULENCE_ENERGY_DISSIPATION_RATE
from ..units import TurbulenceEnergyDissipationRateUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class TurbulenceEnergyDissipationRateSetter(TypeSafeSetter):
    """TurbulenceEnergyDissipationRate-specific setter with only turbulence energy dissipation rate units."""
    
    def __init__(self, variable: 'TurbulenceEnergyDissipationRate', value: float):
        super().__init__(variable, value)
    
    # Only turbulence energy dissipation rate units available - compile-time safe!
    @property
    def square_foot_per_cubic_seconds(self) -> 'TurbulenceEnergyDissipationRate':
        self.variable.quantity = FastQuantity(self.value, TurbulenceEnergyDissipationRateUnits.square_foot_per_cubic_second)
        return cast('TurbulenceEnergyDissipationRate', self.variable)
    @property
    def square_meter_per_cubic_seconds(self) -> 'TurbulenceEnergyDissipationRate':
        self.variable.quantity = FastQuantity(self.value, TurbulenceEnergyDissipationRateUnits.square_meter_per_cubic_second)
        return cast('TurbulenceEnergyDissipationRate', self.variable)
    
    # Short aliases for convenience
    pass


class TurbulenceEnergyDissipationRate(TypedVariable):
    """Type-safe turbulence energy dissipation rate variable with expression capabilities."""
    
    _setter_class = TurbulenceEnergyDissipationRateSetter
    _expected_dimension = TURBULENCE_ENERGY_DISSIPATION_RATE
    _default_unit_property = "square_meter_per_cubic_seconds"
    
    def set(self, value: float) -> TurbulenceEnergyDissipationRateSetter:
        """Create a turbulence energy dissipation rate setter for this variable with proper type annotation."""
        return TurbulenceEnergyDissipationRateSetter(self, value)


class TurbulenceEnergyDissipationRateModule(VariableModule):
    """TurbulenceEnergyDissipationRate variable module definition."""
    
    def get_variable_class(self):
        return TurbulenceEnergyDissipationRate
    
    def get_setter_class(self):
        return TurbulenceEnergyDissipationRateSetter
    
    def get_expected_dimension(self):
        return TURBULENCE_ENERGY_DISSIPATION_RATE


# Register this module for auto-discovery
VARIABLE_MODULE = TurbulenceEnergyDissipationRateModule()