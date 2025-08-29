"""
Dimensionless Quantity Module
=============================

Complete dimensionless quantity system containing unit definitions, constants,
variable class, and setter class in one integrated module.
"""

from typing import TYPE_CHECKING, cast, List

from ..dimension import DIMENSIONLESS
from ..unit import UnitDefinition, UnitConstant
from ..variable import FastQuantity, TypeSafeSetter
from .typed_variable import TypedVariable
from .base import QuantityModule

if TYPE_CHECKING:
    pass


# =====================================================================
# Unit Definitions and Constants
# =====================================================================

class DimensionlessUnits:
    """Type-safe dimensionless unit constants."""
    # Explicit declarations for type checking
    dimensionless: 'UnitConstant'


# =====================================================================
# Variable Setter
# =====================================================================

class DimensionlessSetter(TypeSafeSetter):
    """Dimensionless-specific setter with only dimensionless units."""
    
    def __init__(self, variable: 'Dimensionless', value: float):
        super().__init__(variable, value)
    
    # Dimensionless units
    @property
    def dimensionless(self) -> 'Dimensionless':
        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)
        return cast('Dimensionless', self.variable)
    
    # Common alias for no units
    @property
    def unitless(self) -> 'Dimensionless':
        self.variable.quantity = FastQuantity(self.value, DimensionlessUnits.dimensionless)
        return cast('Dimensionless', self.variable)


# =====================================================================
# Variable Class
# =====================================================================

class Dimensionless(TypedVariable):
    """Type-safe dimensionless variable with expression capabilities."""

    _setter_class = DimensionlessSetter
    _expected_dimension = DIMENSIONLESS
    _default_unit_property = "dimensionless"
    
    def set(self, value: float) -> DimensionlessSetter:
        """Create a dimensionless setter for this variable with proper type annotation."""
        return DimensionlessSetter(self, value)


# =====================================================================
# Quantity Module Definition
# =====================================================================

class DimensionlessQuantityModule(QuantityModule):
    """Complete dimensionless quantity module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all dimensionless unit definitions."""
        return [
            UnitDefinition("dimensionless", "", DIMENSIONLESS, 1.0),
        ]
    
    def get_variable_class(self):
        return Dimensionless
    
    def get_setter_class(self):
        return DimensionlessSetter
    
    def get_units_class(self):
        return DimensionlessUnits
    
    def get_expected_dimension(self):
        return DIMENSIONLESS


# Register this quantity module for auto-discovery
QUANTITY_MODULE = DimensionlessQuantityModule()