"""
ElectricDipoleMoment Variable Module
=====================================

Type-safe electric dipole moment variables with specialized setter and fluent API.
"""

from typing import cast

from ..dimension import ELECTRIC_DIPOLE_MOMENT
from ..units import ElectricDipoleMomentUnits
from ..variable import FastQuantity, TypeSafeSetter
from .base import VariableModule
from .typed_variable import TypedVariable


class ElectricDipoleMomentSetter(TypeSafeSetter):
    """ElectricDipoleMoment-specific setter with only electric dipole moment units."""
    
    def __init__(self, variable: 'ElectricDipoleMoment', value: float):
        super().__init__(variable, value)
    
    # Only electric dipole moment units available - compile-time safe!
    @property
    def ampere_meter_seconds(self) -> 'ElectricDipoleMoment':
        self.variable.quantity = FastQuantity(self.value, ElectricDipoleMomentUnits.ampere_meter_second)
        return cast('ElectricDipoleMoment', self.variable)
    @property
    def coulomb_meters(self) -> 'ElectricDipoleMoment':
        self.variable.quantity = FastQuantity(self.value, ElectricDipoleMomentUnits.coulomb_meter)
        return cast('ElectricDipoleMoment', self.variable)
    @property
    def debyes(self) -> 'ElectricDipoleMoment':
        self.variable.quantity = FastQuantity(self.value, ElectricDipoleMomentUnits.debye)
        return cast('ElectricDipoleMoment', self.variable)
    @property
    def electron_meters(self) -> 'ElectricDipoleMoment':
        self.variable.quantity = FastQuantity(self.value, ElectricDipoleMomentUnits.electron_meter)
        return cast('ElectricDipoleMoment', self.variable)
    
    # Short aliases for convenience
    pass


class ElectricDipoleMoment(TypedVariable):
    """Type-safe electric dipole moment variable with expression capabilities."""
    
    _setter_class = ElectricDipoleMomentSetter
    _expected_dimension = ELECTRIC_DIPOLE_MOMENT
    _default_unit_property = "ampere_meter_seconds"
    
    def set(self, value: float) -> ElectricDipoleMomentSetter:
        """Create a electric dipole moment setter for this variable with proper type annotation."""
        return ElectricDipoleMomentSetter(self, value)


class ElectricDipoleMomentModule(VariableModule):
    """ElectricDipoleMoment variable module definition."""
    
    def get_variable_class(self):
        return ElectricDipoleMoment
    
    def get_setter_class(self):
        return ElectricDipoleMomentSetter
    
    def get_expected_dimension(self):
        return ELECTRIC_DIPOLE_MOMENT


# Register this module for auto-discovery
VARIABLE_MODULE = ElectricDipoleMomentModule()