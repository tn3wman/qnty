"""
Time Units Module
=================

Complete time unit definitions and constants.
"""

from typing import List

from ..dimension import TIME
from ..unit import UnitDefinition, UnitConstant
from .base import UnitModule


class TimeUnits:
    """Type-safe time unit constants."""
    # Explicit declarations for type checking
    second: 'UnitConstant'
    minute: 'UnitConstant'
    hour: 'UnitConstant'
    day: 'UnitConstant'
    year: 'UnitConstant'
    julian_year: 'UnitConstant'
    century: 'UnitConstant'
    millennium: 'UnitConstant'
    
    # Common aliases
    s: 'UnitConstant'
    min: 'UnitConstant'
    h: 'UnitConstant'
    hr: 'UnitConstant'
    d: 'UnitConstant'
    yr: 'UnitConstant'
    a: 'UnitConstant'


class TimeUnitModule(UnitModule):
    """Time unit module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all time unit definitions."""
        return [
            UnitDefinition("second", "s", TIME, 1.0),
            UnitDefinition("minute", "min", TIME, 60.0),
            UnitDefinition("hour", "h", TIME, 3600.0),
            UnitDefinition("day", "d", TIME, 86400.0),
            UnitDefinition("year", "yr", TIME, 3.1558e7),
            UnitDefinition("julian_year", "a", TIME, 3.1557e7),
            UnitDefinition("century", "century", TIME, 3.1558e9),
            UnitDefinition("millennium", "millennium", TIME, 3.1558e10),
        ]
    
    def get_units_class(self):
        return TimeUnits


# Register this module for auto-discovery
UNIT_MODULE = TimeUnitModule()