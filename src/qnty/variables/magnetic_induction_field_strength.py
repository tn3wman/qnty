"""
MagneticInductionFieldStrength Variable Module
===============================================

Type-safe magnetic induction field strength variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import MAGNETIC_INDUCTION_FIELD_STRENGTH
from ..units import MagneticInductionFieldStrengthUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class MagneticInductionFieldStrengthSetter(TypeSafeSetter):
    """MagneticInductionFieldStrength-specific setter with only magnetic induction field strength units."""
    
    def __init__(self, variable: 'MagneticInductionFieldStrength', value: float):
        super().__init__(variable, value)
    
    # Only magnetic induction field strength units available - compile-time safe!
    @property
    def gammas(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.gamma)
        return cast('MagneticInductionFieldStrength', self.variable)
    @property
    def gauss(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.gauss)
        return cast('MagneticInductionFieldStrength', self.variable)
    @property
    def line_per_square_centimeters(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.line_per_square_centimeter)
        return cast('MagneticInductionFieldStrength', self.variable)
    @property
    def maxwell_per_square_centimeters(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.maxwell_per_square_centimeter)
        return cast('MagneticInductionFieldStrength', self.variable)
    @property
    def teslas(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.tesla)
        return cast('MagneticInductionFieldStrength', self.variable)
    @property
    def uas(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.ua)
        return cast('MagneticInductionFieldStrength', self.variable)
    @property
    def weber_per_square_meters(self) -> 'MagneticInductionFieldStrength':
        self.variable.quantity = FastQuantity(self.value, MagneticInductionFieldStrengthUnits.weber_per_square_meter)
        return cast('MagneticInductionFieldStrength', self.variable)
    
    # Short aliases for convenience
    pass


class MagneticInductionFieldStrength(TypedVariable):
    """Type-safe magnetic induction field strength variable with expression capabilities."""
    
    _setter_class = MagneticInductionFieldStrengthSetter
    _expected_dimension = MAGNETIC_INDUCTION_FIELD_STRENGTH
    _default_unit_property = "teslas"
    
    def set(self, value: float) -> MagneticInductionFieldStrengthSetter:
        """Create a magnetic induction field strength setter for this variable with proper type annotation."""
        return MagneticInductionFieldStrengthSetter(self, value)


class MagneticInductionFieldStrengthModule(VariableModule):
    """MagneticInductionFieldStrength variable module definition."""
    
    def get_variable_class(self):
        return MagneticInductionFieldStrength
    
    def get_setter_class(self):
        return MagneticInductionFieldStrengthSetter
    
    def get_expected_dimension(self):
        return MAGNETIC_INDUCTION_FIELD_STRENGTH


# Register this module for auto-discovery
VARIABLE_MODULE = MagneticInductionFieldStrengthModule()