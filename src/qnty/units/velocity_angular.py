"""
VelocityAngular Units Module
============================

Complete velocity, angular unit definitions and constants.
"""

from ..dimension import ANGULAR_VELOCITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VelocityAngularUnits:
    """Type-safe velocity, angular unit constants."""
    # Explicit declarations for type checking
    per_minute: 'UnitConstant'
    per_second: 'UnitConstant'
    grade_per_minute: 'UnitConstant'
    radian_per_minute: 'UnitConstant'
    radian_per_second: 'UnitConstant'
    revolution_per_minute: 'UnitConstant'
    revolution_per_second: 'UnitConstant'
    turn_per_minute: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VelocityAngularUnitModule(UnitModule):
    """VelocityAngular unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all velocity, angular unit definitions."""
        return [
            UnitDefinition("per_minute", "deg/min or  ° / min", ANGULAR_VELOCITY, 0.000290888),
            UnitDefinition("per_second", "deg/s or  ° /s", ANGULAR_VELOCITY, 0.0174533),
            UnitDefinition("grade_per_minute", "gon/min or grad/min", ANGULAR_VELOCITY, 0.000261799),
            UnitDefinition("radian_per_minute", "rad / min", ANGULAR_VELOCITY, 0.016667),
            UnitDefinition("radian_per_second", "rad / s", ANGULAR_VELOCITY, 1),
            UnitDefinition("revolution_per_minute", "rev/m or rpm", ANGULAR_VELOCITY, 0.010472),
            UnitDefinition("revolution_per_second", "rev/s or rps", ANGULAR_VELOCITY, 6.283185),
            UnitDefinition("turn_per_minute", "tr/min", ANGULAR_VELOCITY, 0.010472),

        ]
    
    def get_units_class(self):
        return VelocityAngularUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VelocityAngularUnitModule()