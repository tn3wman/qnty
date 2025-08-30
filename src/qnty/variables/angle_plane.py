"""
AnglePlane Variable Module
===========================

Type-safe angle, plane variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import DIMENSIONLESS
from ..units import AnglePlaneUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AnglePlaneSetter(TypeSafeSetter):
    """AnglePlane-specific setter with only angle, plane units."""
    
    def __init__(self, variable: 'AnglePlane', value: float):
        super().__init__(variable, value)
    
    # Only angle, plane units available - compile-time safe!
    @property
    def degrees(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.degree)
        return cast('AnglePlane', self.variable)
    @property
    def gons(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.gon)
        return cast('AnglePlane', self.variable)
    @property
    def grades(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.grade)
        return cast('AnglePlane', self.variable)
    @property
    def minute_news(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.minute_new)
        return cast('AnglePlane', self.variable)
    @property
    def minute_of_angles(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.minute_of_angle)
        return cast('AnglePlane', self.variable)
    @property
    def percents(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.percent)
        return cast('AnglePlane', self.variable)
    @property
    def plane_angles(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.plane_angle)
        return cast('AnglePlane', self.variable)
    @property
    def quadrants(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.quadrant)
        return cast('AnglePlane', self.variable)
    @property
    def radians(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.radian)
        return cast('AnglePlane', self.variable)
    @property
    def right_angles(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.right_angle)
        return cast('AnglePlane', self.variable)
    @property
    def round_units(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.round_unit)
        return cast('AnglePlane', self.variable)
    @property
    def second_news(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.second_new)
        return cast('AnglePlane', self.variable)
    @property
    def second_of_angles(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.second_of_angle)
        return cast('AnglePlane', self.variable)
    @property
    def thousandth_us(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.thousandth_us)
        return cast('AnglePlane', self.variable)
    @property
    def turns(self) -> 'AnglePlane':
        self.variable.quantity = FastQuantity(self.value, AnglePlaneUnits.turn)
        return cast('AnglePlane', self.variable)
    
    # Short aliases for convenience
    pass


class AnglePlane(TypedVariable):
    """Type-safe angle, plane variable with expression capabilities."""
    
    _setter_class = AnglePlaneSetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "radians"
    
    def set(self, value: float) -> AnglePlaneSetter:
        """Create a angle, plane setter for this variable with proper type annotation."""
        return AnglePlaneSetter(self, value)


class AnglePlaneModule(VariableModule):
    """AnglePlane variable module definition."""
    
    def get_variable_class(self):
        return AnglePlane
    
    def get_setter_class(self):
        return AnglePlaneSetter
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this module for auto-discovery
VARIABLE_MODULE = AnglePlaneModule()