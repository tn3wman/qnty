"""
VolumetricCoefficientOfExpansion Variable Module
=================================================

Type-safe volumetric coefficient of expansion variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import VOLUMETRIC_COEFFICIENT_OF_EXPANSION
from ..units import VolumetricCoefficientOfExpansionUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class VolumetricCoefficientOfExpansionSetter(TypeSafeSetter):
    """VolumetricCoefficientOfExpansion-specific setter with only volumetric coefficient of expansion units."""
    
    def __init__(self, variable: 'VolumetricCoefficientOfExpansion', value: float):
        super().__init__(variable, value)
    
    # Only volumetric coefficient of expansion units available - compile-time safe!
    @property
    def celsius(self) -> 'VolumetricCoefficientOfExpansion':
        self.variable.quantity = FastQuantity(self.value, VolumetricCoefficientOfExpansionUnits.celsius)
        return cast('VolumetricCoefficientOfExpansion', self.variable)
    @property
    def celsius(self) -> 'VolumetricCoefficientOfExpansion':
        self.variable.quantity = FastQuantity(self.value, VolumetricCoefficientOfExpansionUnits.celsius)
        return cast('VolumetricCoefficientOfExpansion', self.variable)
    @property
    def fahrenheits(self) -> 'VolumetricCoefficientOfExpansion':
        self.variable.quantity = FastQuantity(self.value, VolumetricCoefficientOfExpansionUnits.fahrenheit)
        return cast('VolumetricCoefficientOfExpansion', self.variable)
    @property
    def celsius(self) -> 'VolumetricCoefficientOfExpansion':
        self.variable.quantity = FastQuantity(self.value, VolumetricCoefficientOfExpansionUnits.celsius)
        return cast('VolumetricCoefficientOfExpansion', self.variable)
    
    # Short aliases for convenience
    pass


class VolumetricCoefficientOfExpansion(TypedVariable):
    """Type-safe volumetric coefficient of expansion variable with expression capabilities."""
    
    _setter_class = VolumetricCoefficientOfExpansionSetter
    _expected_dimension = VOLUMETRIC_COEFFICIENT_OF_EXPANSION
    _default_unit_property = "celsiuss"
    
    def set(self, value: float) -> VolumetricCoefficientOfExpansionSetter:
        """Create a volumetric coefficient of expansion setter for this variable with proper type annotation."""
        return VolumetricCoefficientOfExpansionSetter(self, value)


class VolumetricCoefficientOfExpansionModule(VariableModule):
    """VolumetricCoefficientOfExpansion variable module definition."""
    
    def get_variable_class(self):
        return VolumetricCoefficientOfExpansion
    
    def get_setter_class(self):
        return VolumetricCoefficientOfExpansionSetter
    
    def get_expected_dimension(self):
        return VOLUMETRIC_COEFFICIENT_OF_EXPANSION


# Register this module for auto-discovery
VARIABLE_MODULE = VolumetricCoefficientOfExpansionModule()