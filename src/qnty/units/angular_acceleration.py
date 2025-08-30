"""
AngularAcceleration Units Module
================================

Complete angular acceleration unit definitions and constants.
"""

from ..dimension import ANGULAR_ACCELERATION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AngularAccelerationUnits:
    """Type-safe angular acceleration unit constants."""
    # Explicit declarations for type checking
    radian_per_second_squared: 'UnitConstant'
    revolution_per_second_squared: 'UnitConstant'
    rpm_or_revolution_per_minute_per_minute: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AngularAccelerationUnitModule(UnitModule):
    """AngularAcceleration unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all angular acceleration unit definitions."""
        return [
            UnitDefinition("radian_per_second_squared", "rad / s2", ANGULAR_ACCELERATION, 1),
            UnitDefinition("revolution_per_second_squared", "rev / sec2", ANGULAR_ACCELERATION, 6.2832),
            UnitDefinition("rpm_or_revolution_per_minute_per_minute", "rev / min2 or rpm/min", ANGULAR_ACCELERATION, 0.001745),

        ]
    
    def get_units_class(self):
        return AngularAccelerationUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AngularAccelerationUnitModule()