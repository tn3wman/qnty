"""
MolarConcentrationByMass Variable Module
=========================================

Type-safe molar concentration by mass variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import AMOUNT
from ..units import MolarConcentrationByMassUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MolarConcentrationByMassSetter(TypeSafeSetter):
    """MolarConcentrationByMass-specific setter with only molar concentration by mass units."""
    
    def __init__(self, variable: 'MolarConcentrationByMass', value: float):
        super().__init__(variable, value)
    
    # Only molar concentration by mass units available - compile-time safe!
    @property
    def gram_moles(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.gram_mole)
        return cast('MolarConcentrationByMass', self.variable)
    @property
    def gram_moles(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.gram_mole)
        return cast('MolarConcentrationByMass', self.variable)
    @property
    def kilogram_moles(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.kilogram_mole)
        return cast('MolarConcentrationByMass', self.variable)
    @property
    def micromole_per_grams(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.micromole_per_gram)
        return cast('MolarConcentrationByMass', self.variable)
    @property
    def millimole_per_grams(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.millimole_per_gram)
        return cast('MolarConcentrationByMass', self.variable)
    @property
    def picomole_per_grams(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.picomole_per_gram)
        return cast('MolarConcentrationByMass', self.variable)
    @property
    def pound_mole_per_pounds(self) -> 'MolarConcentrationByMass':
        self.variable.quantity = FastQuantity(self.value, MolarConcentrationByMassUnits.pound_mole_per_pound)
        return cast('MolarConcentrationByMass', self.variable)
    
    # Short aliases for convenience
    pass


class MolarConcentrationByMass(TypedVariable):
    """Type-safe molar concentration by mass variable with expression capabilities."""
    
    _setter_class = MolarConcentrationByMassSetter
    _expected_dimension = AMOUNT
    _default_unit_property = "gram_moles"
    
    def set(self, value: float) -> MolarConcentrationByMassSetter:
        """Create a molar concentration by mass setter for this variable with proper type annotation."""
        return MolarConcentrationByMassSetter(self, value)


class MolarConcentrationByMassModule(VariableModule):
    """MolarConcentrationByMass variable module definition."""
    
    def get_variable_class(self):
        return MolarConcentrationByMass
    
    def get_setter_class(self):
        return MolarConcentrationByMassSetter
    
    def get_expected_dimension(self):
        return AMOUNT


# Register this module for auto-discovery
VARIABLE_MODULE = MolarConcentrationByMassModule()