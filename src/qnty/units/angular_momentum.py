"""
AngularMomentum Units Module
============================

Complete angular momentum unit definitions and constants.
"""

from ..dimension import ANGULAR_MOMENTUM
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AngularMomentumUnits:
    """Type-safe angular momentum unit constants."""
    # Explicit declarations for type checking
    gram_centimeter_squared_per_second: 'UnitConstant'
    kilogram_meter_squared_per_second: 'UnitConstant'
    pound_force_square_foot_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AngularMomentumUnitModule(UnitModule):
    """AngularMomentum unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all angular momentum unit definitions."""
        return [
            UnitDefinition("gram_centimeter_squared_per_second", "g cm2 / s", ANGULAR_MOMENTUM, 1.00e-07),
            UnitDefinition("kilogram_meter_squared_per_second", "kg m2 / s", ANGULAR_MOMENTUM, 1),
            UnitDefinition("pound_force_square_foot_per_second", "lb ft  2 / sec", ANGULAR_MOMENTUM, 0.04214),

        ]
    
    def get_units_class(self):
        return AngularMomentumUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AngularMomentumUnitModule()