"""
Pressure Quantity Module
========================

Complete pressure quantity system containing unit definitions, constants,
variable class, and setter class in one integrated module.
"""

from typing import TYPE_CHECKING, cast, List

from ..dimension import PRESSURE
from ..unit import UnitDefinition, UnitConstant
from ..variable import FastQuantity, TypeSafeSetter
from .typed_variable import TypedVariable
from .base import QuantityModule

if TYPE_CHECKING:
    pass


# =====================================================================
# Unit Definitions and Constants
# =====================================================================

class PressureUnits:
    """Type-safe pressure unit constants."""
    # Explicit declarations for type checking
    pascal: 'UnitConstant'
    kilopascal: 'UnitConstant'
    megapascal: 'UnitConstant'
    psi: 'UnitConstant'
    bar: 'UnitConstant'
    
    # Common aliases
    Pa: 'UnitConstant'
    kPa: 'UnitConstant'
    MPa: 'UnitConstant'


# =====================================================================
# Variable Setter
# =====================================================================

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


# =====================================================================
# Variable Class
# =====================================================================

class Pressure(TypedVariable):
    """Type-safe pressure variable with expression capabilities."""
    
    _setter_class = PressureSetter
    _expected_dimension = PRESSURE
    _default_unit_property = "psi"
    
    def set(self, value: float) -> PressureSetter:
        """Create a pressure setter for this variable with proper type annotation."""
        return PressureSetter(self, value)


# =====================================================================
# Quantity Module Definition
# =====================================================================

class PressureQuantityModule(QuantityModule):
    """Complete pressure quantity module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all pressure unit definitions."""
        return [
            UnitDefinition("pascal", "Pa", PRESSURE, 1.0),
            UnitDefinition("kilopascal", "kPa", PRESSURE, 1000.0),
            UnitDefinition("megapascal", "MPa", PRESSURE, 1e6),
            UnitDefinition("psi", "psi", PRESSURE, 6894.757),
            UnitDefinition("bar", "bar", PRESSURE, 100000.0),
        ]
    
    def get_variable_class(self):
        return Pressure
    
    def get_setter_class(self):
        return PressureSetter
    
    def get_units_class(self):
        return PressureUnits
    
    def get_expected_dimension(self):
        return PRESSURE


# Register this quantity module for auto-discovery
QUANTITY_MODULE = PressureQuantityModule()