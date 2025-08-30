"""
AtomicWeight Variable Module
=============================

Type-safe atomic weight variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ATOMIC_WEIGHT
from ..units import AtomicWeightUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class AtomicWeightSetter(TypeSafeSetter):
    """AtomicWeight-specific setter with only atomic weight units."""
    
    def __init__(self, variable: 'AtomicWeight', value: float):
        super().__init__(variable, value)
    
    # Only atomic weight units available - compile-time safe!
    @property
    def atomic_mass_unit_12cs(self) -> 'AtomicWeight':
        self.variable.quantity = FastQuantity(self.value, AtomicWeightUnits.atomic_mass_unit_12c)
        return cast('AtomicWeight', self.variable)
    @property
    def grams_per_moles(self) -> 'AtomicWeight':
        self.variable.quantity = FastQuantity(self.value, AtomicWeightUnits.grams_per_mole)
        return cast('AtomicWeight', self.variable)
    @property
    def kilograms_per_kilomoles(self) -> 'AtomicWeight':
        self.variable.quantity = FastQuantity(self.value, AtomicWeightUnits.kilograms_per_kilomole)
        return cast('AtomicWeight', self.variable)
    @property
    def pounds_per_pound_moles(self) -> 'AtomicWeight':
        self.variable.quantity = FastQuantity(self.value, AtomicWeightUnits.pounds_per_pound_mole)
        return cast('AtomicWeight', self.variable)
    
    # Short aliases for convenience
    pass


class AtomicWeight(TypedVariable):
    """Type-safe atomic weight variable with expression capabilities."""
    
    _setter_class = AtomicWeightSetter
    _expected_dimension = ATOMIC_WEIGHT
    _default_unit_property = "atomic_mass_unit_12cs"
    
    def set(self, value: float) -> AtomicWeightSetter:
        """Create a atomic weight setter for this variable with proper type annotation."""
        return AtomicWeightSetter(self, value)


class AtomicWeightModule(VariableModule):
    """AtomicWeight variable module definition."""
    
    def get_variable_class(self):
        return AtomicWeight
    
    def get_setter_class(self):
        return AtomicWeightSetter
    
    def get_expected_dimension(self):
        return ATOMIC_WEIGHT


# Register this module for auto-discovery
VARIABLE_MODULE = AtomicWeightModule()