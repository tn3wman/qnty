"""
ElectricInductance Units Module
===============================

Complete electric inductance unit definitions and constants.
"""

from ..dimension import ELECTRIC_INDUCTANCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricInductanceUnits:
    """Type-safe electric inductance unit constants."""
    # Explicit declarations for type checking
    abhenry: 'UnitConstant'
    cm: 'UnitConstant'
    henry: 'UnitConstant'
    henry_intl_mean: 'UnitConstant'
    henry_intl_us: 'UnitConstant'
    mic: 'UnitConstant'
    stathenry: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricInductanceUnitModule(UnitModule):
    """ElectricInductance unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric inductance unit definitions."""
        return [
            UnitDefinition("abhenry", "emu cgs", ELECTRIC_INDUCTANCE, 1.00e-09),
            UnitDefinition("cm", "cm", ELECTRIC_INDUCTANCE, 1.00e-09),
            UnitDefinition("henry", "H", ELECTRIC_INDUCTANCE, 1),
            UnitDefinition("henry_intl_mean", "H (int mean)", ELECTRIC_INDUCTANCE, 1.00049),
            UnitDefinition("henry_intl_us", "H (int US)", ELECTRIC_INDUCTANCE, 1.000495),
            UnitDefinition("mic", "mic", ELECTRIC_INDUCTANCE, 1.00e-06),
            UnitDefinition("stathenry", "esu cgs", ELECTRIC_INDUCTANCE, 8.9876e+11),

        ]
    
    def get_units_class(self):
        return ElectricInductanceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricInductanceUnitModule()