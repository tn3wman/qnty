"""
RadiationDoseEquivalent Variable Module
========================================

Type-safe radiation dose equivalent variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ABSORBED_DOSE
from ..units import RadiationDoseEquivalentUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class RadiationDoseEquivalentSetter(TypeSafeSetter):
    """RadiationDoseEquivalent-specific setter with only radiation dose equivalent units."""
    
    def __init__(self, variable: 'RadiationDoseEquivalent', value: float):
        super().__init__(variable, value)
    
    # Only radiation dose equivalent units available - compile-time safe!
    @property
    def rems(self) -> 'RadiationDoseEquivalent':
        self.variable.quantity = FastQuantity(self.value, RadiationDoseEquivalentUnits.rem)
        return cast('RadiationDoseEquivalent', self.variable)
    @property
    def sieverts(self) -> 'RadiationDoseEquivalent':
        self.variable.quantity = FastQuantity(self.value, RadiationDoseEquivalentUnits.sievert)
        return cast('RadiationDoseEquivalent', self.variable)
    
    # Short aliases for convenience
    pass


class RadiationDoseEquivalent(TypedVariable):
    """Type-safe radiation dose equivalent variable with expression capabilities."""
    
    _setter_class = RadiationDoseEquivalentSetter
    _expected_dimension = ABSORBED_DOSE
    _default_unit_property = "sieverts"
    
    def set(self, value: float) -> RadiationDoseEquivalentSetter:
        """Create a radiation dose equivalent setter for this variable with proper type annotation."""
        return RadiationDoseEquivalentSetter(self, value)


class RadiationDoseEquivalentModule(VariableModule):
    """RadiationDoseEquivalent variable module definition."""
    
    def get_variable_class(self):
        return RadiationDoseEquivalent
    
    def get_setter_class(self):
        return RadiationDoseEquivalentSetter
    
    def get_expected_dimension(self):
        return ABSORBED_DOSE


# Register this module for auto-discovery
VARIABLE_MODULE = RadiationDoseEquivalentModule()