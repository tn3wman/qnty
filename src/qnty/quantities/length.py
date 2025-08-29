"""
Length Quantity Module
======================

Complete length quantity system containing unit definitions, constants,
variable class, and setter class in one integrated module.
"""

from typing import TYPE_CHECKING, cast, List

from ..dimension import LENGTH
from ..unit import UnitDefinition, UnitConstant
from ..variable import FastQuantity, TypeSafeSetter
from .typed_variable import TypedVariable
from .base import QuantityModule

if TYPE_CHECKING:
    pass


# =====================================================================
# Unit Definitions and Constants
# =====================================================================

class LengthUnits:
    """Type-safe length unit constants."""
    # Explicit declarations for type checking
    meter: 'UnitConstant'
    millimeter: 'UnitConstant'
    centimeter: 'UnitConstant'
    inch: 'UnitConstant'
    foot: 'UnitConstant'
    
    # Common aliases
    m: 'UnitConstant'
    mm: 'UnitConstant'
    cm: 'UnitConstant'
    in_: 'UnitConstant'
    ft: 'UnitConstant'


# =====================================================================
# Variable Setter
# =====================================================================

class LengthSetter(TypeSafeSetter):
    """Length-specific setter with only length units."""
    
    def __init__(self, variable: 'Length', value: float):
        super().__init__(variable, value)
    
    # Only length units available - compile-time safe!
    @property
    def meters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.meter)
        return cast('Length', self.variable)
    
    @property
    def millimeters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.millimeter)
        return cast('Length', self.variable)
    
    @property
    def centimeters(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.centimeter)
        return cast('Length', self.variable)
    
    @property
    def inches(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.inch)
        return cast('Length', self.variable)
    
    @property
    def feet(self) -> 'Length':
        self.variable.quantity = FastQuantity(self.value, LengthUnits.foot)
        return cast('Length', self.variable)
    
    # Short aliases for convenience
    @property
    def m(self) -> 'Length':
        return self.meters
    
    @property
    def mm(self) -> 'Length':
        return self.millimeters
    
    @property
    def cm(self) -> 'Length':
        return self.centimeters
    
    @property
    def in_(self) -> 'Length':
        return self.inches
    
    @property
    def ft(self) -> 'Length':
        return self.feet


# =====================================================================
# Variable Class
# =====================================================================

class Length(TypedVariable):
    """Type-safe length variable with expression capabilities."""
    
    _setter_class = LengthSetter
    _expected_dimension = LENGTH
    _default_unit_property = "meters"
    
    def set(self, value: float) -> LengthSetter:
        """Create a length setter for this variable with proper type annotation."""
        return LengthSetter(self, value)


# =====================================================================
# Quantity Module Definition
# =====================================================================

class LengthQuantityModule(QuantityModule):
    """Complete length quantity module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all length unit definitions."""
        return [
            UnitDefinition("meter", "m", LENGTH, 1.0),
            UnitDefinition("millimeter", "mm", LENGTH, 0.001),
            UnitDefinition("centimeter", "cm", LENGTH, 0.01),
            UnitDefinition("inch", "in", LENGTH, 0.0254),
            UnitDefinition("foot", "ft", LENGTH, 0.3048),
        ]
    
    def get_variable_class(self):
        return Length
    
    def get_setter_class(self):
        return LengthSetter
    
    def get_units_class(self):
        return LengthUnits
    
    def get_expected_dimension(self):
        return LENGTH


# Register this quantity module for auto-discovery
QUANTITY_MODULE = LengthQuantityModule()