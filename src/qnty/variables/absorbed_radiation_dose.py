"""
AbsorbedDose Variable Module
=============================

Type-safe absorbed radiation dose variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ABSORBED_DOSE
from ..units import AbsorbedDoseUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AbsorbedDoseSetter(TypeSafeSetter):
    """AbsorbedDose-specific setter with only absorbed radiation dose units."""
    
    def __init__(self, variable: 'AbsorbedDose', value: float):
        super().__init__(variable, value)
    
    # Only absorbed radiation dose units available - compile-time safe!
    @property
    def erg_per_grams(self) -> 'AbsorbedDose':
        self.variable.quantity = FastQuantity(self.value, AbsorbedDoseUnits.erg_per_gram)
        return cast('AbsorbedDose', self.variable)
    @property
    def gramrads(self) -> 'AbsorbedDose':
        self.variable.quantity = FastQuantity(self.value, AbsorbedDoseUnits.gramrad)
        return cast('AbsorbedDose', self.variable)
    @property
    def gray(self) -> 'AbsorbedDose':
        self.variable.quantity = FastQuantity(self.value, AbsorbedDoseUnits.gray)
        return cast('AbsorbedDose', self.variable)
    @property
    def rads(self) -> 'AbsorbedDose':
        self.variable.quantity = FastQuantity(self.value, AbsorbedDoseUnits.rad)
        return cast('AbsorbedDose', self.variable)
    
    # Short aliases for convenience
    pass


class AbsorbedDose(TypedVariable):
    """Type-safe absorbed radiation dose variable with expression capabilities."""
    
    _setter_class = AbsorbedDoseSetter
    _expected_dimension = ABSORBED_DOSE
    _default_unit_property = "Gy"
    
    def set(self, value: float) -> AbsorbedDoseSetter:
        """Create a absorbed radiation dose setter for this variable with proper type annotation."""
        return AbsorbedDoseSetter(self, value)


class AbsorbedDoseModule(VariableModule):
    """AbsorbedDose variable module definition."""
    
    def get_variable_class(self):
        return AbsorbedDose
    
    def get_setter_class(self):
        return AbsorbedDoseSetter
    
    def get_expected_dimension(self):
        return ABSORBED_DOSE


# Register this module for auto-discovery
VARIABLE_MODULE = AbsorbedDoseModule()