"""
ActivationEnergy Variable Module
=================================

Type-safe activation energy variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ACTIVATION_ENERGY
from ..units import ActivationEnergyUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ActivationEnergySetter(TypeSafeSetter):
    """ActivationEnergy-specific setter with only activation energy units."""
    
    def __init__(self, variable: 'ActivationEnergy', value: float):
        super().__init__(variable, value)
    
    # Only activation energy units available - compile-time safe!
    @property
    def btu_per_pound_moles(self) -> 'ActivationEnergy':
        self.variable.quantity = FastQuantity(self.value, ActivationEnergyUnits.btu_per_pound_mole)
        return cast('ActivationEnergy', self.variable)
    @property
    def calorie_mean_per_gram_moles(self) -> 'ActivationEnergy':
        self.variable.quantity = FastQuantity(self.value, ActivationEnergyUnits.calorie_mean_per_gram_mole)
        return cast('ActivationEnergy', self.variable)
    @property
    def joule_per_gram_moles(self) -> 'ActivationEnergy':
        self.variable.quantity = FastQuantity(self.value, ActivationEnergyUnits.joule_per_gram_mole)
        return cast('ActivationEnergy', self.variable)
    @property
    def joule_per_kilogram_moles(self) -> 'ActivationEnergy':
        self.variable.quantity = FastQuantity(self.value, ActivationEnergyUnits.joule_per_kilogram_mole)
        return cast('ActivationEnergy', self.variable)
    @property
    def kilocalorie_per_kilogram_moles(self) -> 'ActivationEnergy':
        self.variable.quantity = FastQuantity(self.value, ActivationEnergyUnits.kilocalorie_per_kilogram_mole)
        return cast('ActivationEnergy', self.variable)
    
    # Short aliases for convenience
    pass


class ActivationEnergy(TypedVariable):
    """Type-safe activation energy variable with expression capabilities."""
    
    _setter_class = ActivationEnergySetter
    _expected_dimension = ACTIVATION_ENERGY
    _default_unit_property = "joule_per_gram_moles"
    
    def set(self, value: float) -> ActivationEnergySetter:
        """Create a activation energy setter for this variable with proper type annotation."""
        return ActivationEnergySetter(self, value)


class ActivationEnergyModule(VariableModule):
    """ActivationEnergy variable module definition."""
    
    def get_variable_class(self):
        return ActivationEnergy
    
    def get_setter_class(self):
        return ActivationEnergySetter
    
    def get_expected_dimension(self):
        return ACTIVATION_ENERGY


# Register this module for auto-discovery
VARIABLE_MODULE = ActivationEnergyModule()