"""
MomentumFlowRate Units Module
=============================

Complete momentum flow rate unit definitions and constants.
"""

from ..dimension import FORCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MomentumFlowRateUnits:
    """Type-safe momentum flow rate unit constants."""
    # Explicit declarations for type checking
    foot_pounds_per_square_hour: 'UnitConstant'
    foot_pounds_per_square_minute: 'UnitConstant'
    foot_pounds_per_square_second: 'UnitConstant'
    gram_centimeters_per_square_second: 'UnitConstant'
    kilogram_meters_per_square_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MomentumFlowRateUnitModule(UnitModule):
    """MomentumFlowRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all momentum flow rate unit definitions."""
        return [
            UnitDefinition("foot_pounds_per_square_hour", "ft lb / h2 or ft lb / hr2", FORCE, 1.0671e-08),
            UnitDefinition("foot_pounds_per_square_minute", "ft lb / min2", FORCE, 3.8417e-05),
            UnitDefinition("foot_pounds_per_square_second", "ft lb / s2 or ft lb/sec  2", FORCE, 0.1383),
            UnitDefinition("gram_centimeters_per_square_second", "g cm / s2", FORCE, 1.00e-05),
            UnitDefinition("kilogram_meters_per_square_second", "kg m / s2", FORCE, 1),

        ]
    
    def get_units_class(self):
        return MomentumFlowRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MomentumFlowRateUnitModule()