"""
Pressure Variable Module
=======================

Type-safe pressure variables with specialized setter and fluent API.
"""

from typing import TYPE_CHECKING, cast

from ..dimension import PRESSURE
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable

from ..units import PressureUnits


class PressureSetter(TypeSafeSetter):
    """Pressure-specific setter with only pressure units."""
    
    def __init__(self, variable: 'Pressure', value: float):
        super().__init__(variable, value)
    
    # Only pressure units available - compile-time safe!
    @property
    def pascal(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.pascal)
        return cast('Pressure', self.variable)
    
    @property
    def pascals(self) -> 'Pressure':
        return self.pascal
    
    @property
    def kilopascal(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.kilopascal)
        return cast('Pressure', self.variable)
    
    @property
    def kilopascals(self) -> 'Pressure':
        return self.kilopascal
    
    @property
    def megapascal(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.megapascal)
        return cast('Pressure', self.variable)
    
    @property
    def megapascals(self) -> 'Pressure':
        return self.megapascal
    
    @property
    def psi(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.psi)
        return cast('Pressure', self.variable)
    
    @property
    def bar(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.bar)
        return cast('Pressure', self.variable)
    
    # Short aliases
    @property
    def Pa(self) -> 'Pressure':
        return self.pascal
    
    @property
    def kPa(self) -> 'Pressure':
        return self.kilopascal
    
    @property
    def MPa(self) -> 'Pressure':
        return self.megapascal


class Pressure(TypedVariable):
    """Type-safe pressure variable with expression capabilities."""
    
    _setter_class = PressureSetter
    _expected_dimension = PRESSURE
    _default_unit_property = "psi"
    
    def set(self, value: float) -> PressureSetter:
        """Create a pressure setter for this variable with proper type annotation."""
        return PressureSetter(self, value)


class PressureModule(VariableModule):
    """Pressure variable module definition."""
    
    def get_variable_class(self):
        return Pressure
    
    def get_setter_class(self):
        return PressureSetter
    
    def get_expected_dimension(self):
        return PRESSURE


# Register this module for auto-discovery
VARIABLE_MODULE = PressureModule()