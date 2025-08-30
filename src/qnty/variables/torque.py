"""
Torque Variable Module
=======================

Type-safe torque variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ENERGY
from ..units import TorqueUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class TorqueSetter(TypeSafeSetter):
    """Torque-specific setter with only torque units."""
    
    def __init__(self, variable: 'Torque', value: float):
        super().__init__(variable, value)
    
    # Only torque units available - compile-time safe!
    @property
    def centimeter_kilogram_forces(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.centimeter_kilogram_force)
        return cast('Torque', self.variable)
    @property
    def dyne_centimeters(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.dyne_centimeter)
        return cast('Torque', self.variable)
    @property
    def foot_kilogram_forces(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.foot_kilogram_force)
        return cast('Torque', self.variable)
    @property
    def foot_pound_forces(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.foot_pound_force)
        return cast('Torque', self.variable)
    @property
    def foot_poundals(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.foot_poundal)
        return cast('Torque', self.variable)
    @property
    def in_pound_forces(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.in_pound_force)
        return cast('Torque', self.variable)
    @property
    def inch_ounce_forces(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.inch_ounce_force)
        return cast('Torque', self.variable)
    @property
    def meter_kilogram_forces(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.meter_kilogram_force)
        return cast('Torque', self.variable)
    @property
    def newton_centimeters(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.newton_centimeter)
        return cast('Torque', self.variable)
    @property
    def newton_meters(self) -> 'Torque':
        self.variable.quantity = FastQuantity(self.value, TorqueUnits.newton_meter)
        return cast('Torque', self.variable)
    
    # Short aliases for convenience
    pass


class Torque(TypedVariable):
    """Type-safe torque variable with expression capabilities."""
    
    _setter_class = TorqueSetter
    _expected_dimension = ENERGY
    _default_unit_property = "centimeter_kilogram_forces"
    
    def set(self, value: float) -> TorqueSetter:
        """Create a torque setter for this variable with proper type annotation."""
        return TorqueSetter(self, value)


class TorqueModule(VariableModule):
    """Torque variable module definition."""
    
    def get_variable_class(self):
        return Torque
    
    def get_setter_class(self):
        return TorqueSetter
    
    def get_expected_dimension(self):
        return ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = TorqueModule()