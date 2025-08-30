"""
AnglePlane Units Module
=======================

Complete angle, plane unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AnglePlaneUnits:
    """Type-safe angle, plane unit constants."""
    # Explicit declarations for type checking
    degree: 'UnitConstant'
    gon: 'UnitConstant'
    grade: 'UnitConstant'
    minute_new: 'UnitConstant'
    minute_of_angle: 'UnitConstant'
    percent: 'UnitConstant'
    plane_angle: 'UnitConstant'
    quadrant: 'UnitConstant'
    radian: 'UnitConstant'
    right_angle: 'UnitConstant'
    round_unit: 'UnitConstant'
    second_new: 'UnitConstant'
    second_of_angle: 'UnitConstant'
    thousandth_us: 'UnitConstant'
    turn: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AnglePlaneUnitModule(UnitModule):
    """AnglePlane unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all angle, plane unit definitions."""
        return [
            UnitDefinition("degree", "°", DIMENSIONLESS, 0.0174533),
            UnitDefinition("gon", "g or gon", DIMENSIONLESS, 0.015708),
            UnitDefinition("grade", "g or grad", DIMENSIONLESS, 0.015708),
            UnitDefinition("minute_new", "c", DIMENSIONLESS, 0.00015708),
            UnitDefinition("minute_of_angle", "'", DIMENSIONLESS, 0.000290888),
            UnitDefinition("percent", "%", DIMENSIONLESS, 0.062832),
            UnitDefinition("plane_angle", "-", DIMENSIONLESS, 3.141593),
            UnitDefinition("quadrant", "quadr", DIMENSIONLESS, 1.570796),
            UnitDefinition("radian", "rad", DIMENSIONLESS, 1),
            UnitDefinition("right_angle", "perp", DIMENSIONLESS, 1.570796),
            UnitDefinition("round_unit", "tr or r", DIMENSIONLESS, 6.283185),
            UnitDefinition("second_new", "cc", DIMENSIONLESS, 1.5708e-06),
            UnitDefinition("second_of_angle", "\"", DIMENSIONLESS, 4.8481e-06),
            UnitDefinition("thousandth_us", "% (US)", DIMENSIONLESS, 0.0015708),
            UnitDefinition("turn", "turn or rev", DIMENSIONLESS, 6.283185),

        ]
    
    def get_units_class(self):
        return AnglePlaneUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AnglePlaneUnitModule()