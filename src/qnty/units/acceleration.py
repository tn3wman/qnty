"""
Acceleration Units Module
=========================

Complete acceleration unit definitions and constants.
"""

from ..dimension import ACCELERATION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AccelerationUnits:
    """Type-safe acceleration unit constants."""
    # Explicit declarations for type checking
    foot_per_second_squared: 'UnitConstant'
    meter_per_second_squared: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AccelerationUnitModule(UnitModule):
    """Acceleration unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all acceleration unit definitions."""
        return [
            UnitDefinition("foot_per_second_squared", "ft / s2 or ft / sec2", ACCELERATION, 0.3048),
            UnitDefinition("meter_per_second_squared", "m / s2", ACCELERATION, 1),

        ]
    
    def get_units_class(self):
        return AccelerationUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AccelerationUnitModule()