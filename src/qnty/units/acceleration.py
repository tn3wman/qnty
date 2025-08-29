"""
Acceleration Units Module
=========================

Complete acceleration unit definitions and constants.
"""

from typing import List

from ..dimension import ACCELERATION
from ..unit import UnitDefinition, UnitConstant
from .base import UnitModule


class AccelerationUnits:
    """Type-safe acceleration unit constants."""
    # Explicit declarations for type checking
    meter_per_second_squared: 'UnitConstant'
    foot_per_second_squared: 'UnitConstant'
    
    # Common aliases
    mps2: 'UnitConstant'
    fps2: 'UnitConstant'


class AccelerationUnitModule(UnitModule):
    """Acceleration unit module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all acceleration unit definitions."""
        return [
            UnitDefinition("meter_per_second_squared", "m/s^2", ACCELERATION, 1.0),
            UnitDefinition("foot_per_second_squared", "ft/s^2", ACCELERATION, 0.3048),
        ]
    
    def get_units_class(self):
        return AccelerationUnits


# Register this module for auto-discovery
UNIT_MODULE = AccelerationUnitModule()