"""
SecondMomentOfArea Variable Module
===================================

Type-safe second moment of area variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import SECOND_MOMENT_OF_AREA
from ..units import SecondMomentOfAreaUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class SecondMomentOfAreaSetter(TypeSafeSetter):
    """SecondMomentOfArea-specific setter with only second moment of area units."""
    
    def __init__(self, variable: 'SecondMomentOfArea', value: float):
        super().__init__(variable, value)
    
    # Only second moment of area units available - compile-time safe!
    @property
    def inch_quadrupleds(self) -> 'SecondMomentOfArea':
        self.variable.quantity = FastQuantity(self.value, SecondMomentOfAreaUnits.inch_quadrupled)
        return cast('SecondMomentOfArea', self.variable)
    @property
    def centimeter_quadrupleds(self) -> 'SecondMomentOfArea':
        self.variable.quantity = FastQuantity(self.value, SecondMomentOfAreaUnits.centimeter_quadrupled)
        return cast('SecondMomentOfArea', self.variable)
    @property
    def foot_quadrupleds(self) -> 'SecondMomentOfArea':
        self.variable.quantity = FastQuantity(self.value, SecondMomentOfAreaUnits.foot_quadrupled)
        return cast('SecondMomentOfArea', self.variable)
    @property
    def meter_quadrupleds(self) -> 'SecondMomentOfArea':
        self.variable.quantity = FastQuantity(self.value, SecondMomentOfAreaUnits.meter_quadrupled)
        return cast('SecondMomentOfArea', self.variable)
    
    # Short aliases for convenience
    pass


class SecondMomentOfArea(TypedVariable):
    """Type-safe second moment of area variable with expression capabilities."""
    
    _setter_class = SecondMomentOfAreaSetter
    _expected_dimension = SECOND_MOMENT_OF_AREA
    _default_unit_property = "meter_quadrupleds"
    
    def set(self, value: float) -> SecondMomentOfAreaSetter:
        """Create a second moment of area setter for this variable with proper type annotation."""
        return SecondMomentOfAreaSetter(self, value)


class SecondMomentOfAreaModule(VariableModule):
    """SecondMomentOfArea variable module definition."""
    
    def get_variable_class(self):
        return SecondMomentOfArea
    
    def get_setter_class(self):
        return SecondMomentOfAreaSetter
    
    def get_expected_dimension(self):
        return SECOND_MOMENT_OF_AREA


# Register this module for auto-discovery
VARIABLE_MODULE = SecondMomentOfAreaModule()