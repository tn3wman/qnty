"""
ElectricCurrentIntensity Units Module
=====================================

Complete electric current intensity unit definitions and constants.
"""

from ..dimension import CURRENT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricCurrentIntensityUnits:
    """Type-safe electric current intensity unit constants."""
    # Explicit declarations for type checking
    abampere: 'UnitConstant'
    ampere_intl_mean: 'UnitConstant'
    ampere_intl_us: 'UnitConstant'
    ampere: 'UnitConstant'
    biot: 'UnitConstant'
    statampere: 'UnitConstant'
    ua: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricCurrentIntensityUnitModule(UnitModule):
    """ElectricCurrentIntensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric current intensity unit definitions."""
        return [
            UnitDefinition("abampere", "emu cgs", CURRENT, 10),
            UnitDefinition("ampere_intl_mean", "A (int mean)", CURRENT, 0.99985),
            UnitDefinition("ampere_intl_us", "A (int US)", CURRENT, 0.999835),
            UnitDefinition("ampere", "A", CURRENT, 1),
            UnitDefinition("biot", "biot", CURRENT, 10),
            UnitDefinition("statampere", "esu cgs", CURRENT, 3.33564e-10),
            UnitDefinition("ua", "u.a.", CURRENT, 0.00662362),

        ]
    
    def get_units_class(self):
        return ElectricCurrentIntensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricCurrentIntensityUnitModule()