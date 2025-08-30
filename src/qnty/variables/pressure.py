"""
Pressure Variable Module
=========================

Type-safe pressure variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import PRESSURE
from ..units import PressureUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class PressureSetter(TypeSafeSetter):
    """Pressure-specific setter with only pressure units."""
    
    def __init__(self, variable: 'Pressure', value: float):
        super().__init__(variable, value)
    
    # Only pressure units available - compile-time safe!
    @property
    def atmosphere_standards(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.atmosphere_standard)
        return cast('Pressure', self.variable)
    @property
    def bars(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.bar)
        return cast('Pressure', self.variable)
    @property
    def baryes(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.barye)
        return cast('Pressure', self.variable)
    @property
    def dyne_per_square_centimeters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.dyne_per_square_centimeter)
        return cast('Pressure', self.variable)
    @property
    def foot_of_mercury(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.foot_of_mercury)
        return cast('Pressure', self.variable)
    @property
    def foot_of_waters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.foot_of_water)
        return cast('Pressure', self.variable)
    @property
    def gigapascals(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.gigapascal)
        return cast('Pressure', self.variable)
    @property
    def hectopascals(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.hectopascal)
        return cast('Pressure', self.variable)
    @property
    def inch_of_mercury(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.inch_of_mercury)
        return cast('Pressure', self.variable)
    @property
    def inch_of_waters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.inch_of_water)
        return cast('Pressure', self.variable)
    @property
    def kilogram_force_per_square_centimeters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.kilogram_force_per_square_centimeter)
        return cast('Pressure', self.variable)
    @property
    def kilogram_force_per_square_meters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.kilogram_force_per_square_meter)
        return cast('Pressure', self.variable)
    @property
    def kip_force_per_square_inchs(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.kip_force_per_square_inch)
        return cast('Pressure', self.variable)
    @property
    def megapascals(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.megapascal)
        return cast('Pressure', self.variable)
    @property
    def meter_of_waters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.meter_of_water)
        return cast('Pressure', self.variable)
    @property
    def microbars(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.microbar)
        return cast('Pressure', self.variable)
    @property
    def millibars(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.millibar)
        return cast('Pressure', self.variable)
    @property
    def millimeter_of_mercury(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.millimeter_of_mercury)
        return cast('Pressure', self.variable)
    @property
    def millimeter_of_waters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.millimeter_of_water)
        return cast('Pressure', self.variable)
    @property
    def newton_per_square_meters(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.newton_per_square_meter)
        return cast('Pressure', self.variable)
    @property
    def ounce_force_per_square_inchs(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.ounce_force_per_square_inch)
        return cast('Pressure', self.variable)
    @property
    def pascals(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.pascal)
        return cast('Pressure', self.variable)
    @property
    def pièzes(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.pièze)
        return cast('Pressure', self.variable)
    @property
    def pound_force_per_square_foots(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.pound_force_per_square_foot)
        return cast('Pressure', self.variable)
    @property
    def pound_force_per_square_inchs(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.pound_force_per_square_inch)
        return cast('Pressure', self.variable)
    @property
    def torrs(self) -> 'Pressure':
        self.variable.quantity = FastQuantity(self.value, PressureUnits.torr)
        return cast('Pressure', self.variable)
    
    # Short aliases for convenience
    @property
    def bar(self) -> 'Pressure':
        """Bar alias."""
        self.variable.quantity = FastQuantity(self.value, PressureUnits.bar)
        return cast('Pressure', self.variable)
    @property
    def MPa(self) -> 'Pressure':
        """Megapascal alias."""
        self.variable.quantity = FastQuantity(self.value, PressureUnits.MPa)
        return cast('Pressure', self.variable)
    @property
    def psi(self) -> 'Pressure':
        """Alias for pound force per square inch."""
        self.variable.quantity = FastQuantity(self.value, PressureUnits.psi)
        return cast('Pressure', self.variable)
    @property
    def kPa(self) -> 'Pressure':
        """Kilopascal alias."""
        self.variable.quantity = FastQuantity(self.value, PressureUnits.kPa)
        return cast('Pressure', self.variable)


class Pressure(TypedVariable):
    """Type-safe pressure variable with expression capabilities."""
    
    _setter_class = PressureSetter
    _expected_dimension = PRESSURE
    _default_unit_property = "pascals"
    
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