"""
Angle Units Module
==================

Complete angle (plane) unit definitions and constants.
"""

from ..dimension import DIMENSIONLESS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AngleUnits:
    """Type-safe angle unit constants."""
    # Explicit declarations for type checking
    radian: 'UnitConstant'
    degree: 'UnitConstant'
    gradian: 'UnitConstant'
    turn: 'UnitConstant'
    arc_minute: 'UnitConstant'
    arc_second: 'UnitConstant'
    
    # Common aliases
    rad: 'UnitConstant'
    deg: 'UnitConstant'
    grad: 'UnitConstant'
    arcmin: 'UnitConstant'
    arcsec: 'UnitConstant'


class AngleUnitModule(UnitModule):
    """Angle unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all angle unit definitions."""
        return [
            UnitDefinition("radian", "rad", DIMENSIONLESS, 1.0),
            UnitDefinition("degree", "deg", DIMENSIONLESS, 0.0174533),
            UnitDefinition("gradian", "grad", DIMENSIONLESS, 0.015708),
            UnitDefinition("turn", "turn", DIMENSIONLESS, 6.283185),
            UnitDefinition("arc_minute", "arcmin", DIMENSIONLESS, 0.000290888),
            UnitDefinition("arc_second", "arcsec", DIMENSIONLESS, 4.8481e-6),
        ]
    
    def get_units_class(self):
        return AngleUnits


# Register this module for auto-discovery
UNIT_MODULE = AngleUnitModule()
