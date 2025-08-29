"""
Pressure Units Module
====================

Complete pressure unit definitions and constants.
"""

from typing import List

from ..dimension import PRESSURE
from ..unit import UnitDefinition, UnitConstant
from .base import UnitModule


class PressureUnits:
    """Type-safe pressure unit constants."""
    # Explicit declarations for type checking
    pascal: 'UnitConstant'
    kilopascal: 'UnitConstant'
    megapascal: 'UnitConstant'
    psi: 'UnitConstant'
    bar: 'UnitConstant'
    
    # Common aliases
    Pa: 'UnitConstant'
    kPa: 'UnitConstant'
    MPa: 'UnitConstant'


class PressureUnitModule(UnitModule):
    """Pressure unit module definition."""
    
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return all pressure unit definitions."""
        return [
            UnitDefinition("pascal", "Pa", PRESSURE, 1.0),
            UnitDefinition("kilopascal", "kPa", PRESSURE, 1000.0),
            UnitDefinition("megapascal", "MPa", PRESSURE, 1e6),
            UnitDefinition("psi", "psi", PRESSURE, 6894.757),
            UnitDefinition("bar", "bar", PRESSURE, 100000.0),
        ]
    
    def get_units_class(self):
        return PressureUnits


# Register this module for auto-discovery
UNIT_MODULE = PressureUnitModule()