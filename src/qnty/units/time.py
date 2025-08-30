"""
Time Units Module
=================

Complete time unit definitions and constants.
"""

from ..dimension import TIME
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class TimeUnits:
    """Type-safe time unit constants."""
    # Explicit declarations for type checking
    blink: 'UnitConstant'
    century: 'UnitConstant'
    chronon: 'UnitConstant'
    gigan: 'UnitConstant'
    hour: 'UnitConstant'
    julian_year: 'UnitConstant'
    mean_solar_day: 'UnitConstant'
    millenium: 'UnitConstant'
    minute: 'UnitConstant'
    second: 'UnitConstant'
    shake: 'UnitConstant'
    sidereal_year_1900_ad: 'UnitConstant'
    tropical_year: 'UnitConstant'
    wink: 'UnitConstant'
    year: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class TimeUnitModule(UnitModule):
    """Time unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all time unit definitions."""
        return [
            UnitDefinition("blink", "blink", TIME, 0.864),
            UnitDefinition("century", "-", TIME, 3.1558e+09),
            UnitDefinition("chronon", "-", TIME, 1.00e-23),
            UnitDefinition("gigan", "Ga or eon", TIME, 3.1558e+16),
            UnitDefinition("hour", "h or hr", TIME, 3600),
            UnitDefinition("julian_year", "a (jul) or yr", TIME, 3.1557e+07),
            UnitDefinition("mean_solar_day", "da or d", TIME, 86400),
            UnitDefinition("millenium", "-", TIME, 3.1558e+10),
            UnitDefinition("minute", "min", TIME, 60),
            UnitDefinition("second", "s", TIME, 1),
            UnitDefinition("shake", "shake", TIME, 1.0000e-08),
            UnitDefinition("sidereal_year_1900_ad", "a (sider) or yr", TIME, 3.1552e+07),
            UnitDefinition("tropical_year", "a (trop)", TIME, 3.1557e+07),
            UnitDefinition("wink", "wink", TIME, 3.33333e-12),
            UnitDefinition("year", "a or y or yr", TIME, 3.1558e+07),

        ]
    
    def get_units_class(self):
        return TimeUnits
    


# Register this module for auto-discovery
UNIT_MODULE = TimeUnitModule()