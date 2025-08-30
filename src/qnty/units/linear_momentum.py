"""
LinearMomentum Units Module
===========================

Complete linear momentum unit definitions and constants.
"""

from ..dimension import LINEAR_MOMENTUM
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class LinearMomentumUnits:
    """Type-safe linear momentum unit constants."""
    # Explicit declarations for type checking
    foot_pounds_force_per_hour: 'UnitConstant'
    foot_pounds_force_per_minute: 'UnitConstant'
    foot_pounds_force_per_second: 'UnitConstant'
    gram_centimeters_per_second: 'UnitConstant'
    kilogram_meters_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class LinearMomentumUnitModule(UnitModule):
    """LinearMomentum unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all linear momentum unit definitions."""
        return [
            UnitDefinition("foot_pounds_force_per_hour", "ft lbf/ h or ft-lb / hr", LINEAR_MOMENTUM, 3.84e-05),
            UnitDefinition("foot_pounds_force_per_minute", "ft lbf / min or ft-lb / min", LINEAR_MOMENTUM, 0.0023042),
            UnitDefinition("foot_pounds_force_per_second", "ft lbf / s or ft-lb/sec", LINEAR_MOMENTUM, 0.13825),
            UnitDefinition("gram_centimeters_per_second", "g cm / s", LINEAR_MOMENTUM, 1.00e-05),
            UnitDefinition("kilogram_meters_per_second", "kg m / s", LINEAR_MOMENTUM, 1),

        ]
    
    def get_units_class(self):
        return LinearMomentumUnits
    


# Register this module for auto-discovery
UNIT_MODULE = LinearMomentumUnitModule()