"""
VelocityLinear Units Module
===========================

Complete velocity, linear unit definitions and constants.
"""

from ..dimension import VELOCITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VelocityLinearUnits:
    """Type-safe velocity, linear unit constants."""
    # Explicit declarations for type checking
    foot_per_hour: 'UnitConstant'
    foot_per_minute: 'UnitConstant'
    foot_per_second: 'UnitConstant'
    inch_per_second: 'UnitConstant'
    international_knot: 'UnitConstant'
    kilometer_per_hour: 'UnitConstant'
    kilometer_per_second: 'UnitConstant'
    meter_per_second: 'UnitConstant'
    mile_per_hour: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VelocityLinearUnitModule(UnitModule):
    """VelocityLinear unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all velocity, linear unit definitions."""
        return [
            UnitDefinition("foot_per_hour", "ft/h or ft/hr or fph", VELOCITY, 0.000084667),
            UnitDefinition("foot_per_minute", "ft/min or fpm", VELOCITY, 0.00508),
            UnitDefinition("foot_per_second", "ft/s or fps", VELOCITY, 0.3048),
            UnitDefinition("inch_per_second", "in/s or ips", VELOCITY, 0.0254),
            UnitDefinition("international_knot", "knot", VELOCITY, 0.0514444),
            UnitDefinition("kilometer_per_hour", "km/h ot kph", VELOCITY, 0.027778),
            UnitDefinition("kilometer_per_second", "km/s", VELOCITY, 1000),
            UnitDefinition("meter_per_second", "m / s", VELOCITY, 1),
            UnitDefinition("mile_per_hour", "mi / h or mi / hr or mph", VELOCITY, 0.0444704),

        ]
    
    def get_units_class(self):
        return VelocityLinearUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VelocityLinearUnitModule()