"""
ViscosityKinematic Variable Module
===================================

Type-safe viscosity, kinematic variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import KINEMATIC_VISCOSITY
from ..units import ViscosityKinematicUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ViscosityKinematicSetter(TypeSafeSetter):
    """ViscosityKinematic-specific setter with only viscosity, kinematic units."""
    
    def __init__(self, variable: 'ViscosityKinematic', value: float):
        super().__init__(variable, value)
    
    # Only viscosity, kinematic units available - compile-time safe!
    @property
    def centistokes(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.centistokes)
        return cast('ViscosityKinematic', self.variable)
    @property
    def millistokes(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.millistokes)
        return cast('ViscosityKinematic', self.variable)
    @property
    def square_centimeter_per_seconds(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.square_centimeter_per_second)
        return cast('ViscosityKinematic', self.variable)
    @property
    def square_foot_per_hours(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.square_foot_per_hour)
        return cast('ViscosityKinematic', self.variable)
    @property
    def square_foot_per_seconds(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.square_foot_per_second)
        return cast('ViscosityKinematic', self.variable)
    @property
    def square_meters_per_seconds(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.square_meters_per_second)
        return cast('ViscosityKinematic', self.variable)
    @property
    def stokes(self) -> 'ViscosityKinematic':
        self.variable.quantity = FastQuantity(self.value, ViscosityKinematicUnits.stokes)
        return cast('ViscosityKinematic', self.variable)
    
    # Short aliases for convenience
    pass


class ViscosityKinematic(TypedVariable):
    """Type-safe viscosity, kinematic variable with expression capabilities."""
    
    _setter_class = ViscosityKinematicSetter
    _expected_dimension = KINEMATIC_VISCOSITY
    _default_unit_property = "square_meters_per_seconds"
    
    def set(self, value: float) -> ViscosityKinematicSetter:
        """Create a viscosity, kinematic setter for this variable with proper type annotation."""
        return ViscosityKinematicSetter(self, value)


class ViscosityKinematicModule(VariableModule):
    """ViscosityKinematic variable module definition."""
    
    def get_variable_class(self):
        return ViscosityKinematic
    
    def get_setter_class(self):
        return ViscosityKinematicSetter
    
    def get_expected_dimension(self):
        return KINEMATIC_VISCOSITY


# Register this module for auto-discovery
VARIABLE_MODULE = ViscosityKinematicModule()