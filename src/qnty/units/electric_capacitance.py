"""
ElectricCapacitance Units Module
================================

Complete electric capacitance unit definitions and constants.
"""

from ..dimension import ELECTRIC_CAPACITANCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricCapacitanceUnits:
    """Type-safe electric capacitance unit constants."""
    # Explicit declarations for type checking
    cm: 'UnitConstant'
    abfarad: 'UnitConstant'
    farad: 'UnitConstant'
    farad_intl: 'UnitConstant'
    jar: 'UnitConstant'
    puff: 'UnitConstant'
    statfarad: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricCapacitanceUnitModule(UnitModule):
    """ElectricCapacitance unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric capacitance unit definitions."""
        return [
            UnitDefinition("cm", "cm", ELECTRIC_CAPACITANCE, 1.1111e-12),
            UnitDefinition("abfarad", "emu cgs", ELECTRIC_CAPACITANCE, 1.00e+09),
            UnitDefinition("farad", "F", ELECTRIC_CAPACITANCE, 1),
            UnitDefinition("farad_intl", "F (int)", ELECTRIC_CAPACITANCE, 0.99951),
            UnitDefinition("jar", "jar", ELECTRIC_CAPACITANCE, 1.1111e-09),
            UnitDefinition("puff", "puff", ELECTRIC_CAPACITANCE, 1.00e-12),
            UnitDefinition("statfarad", "esu cgs", ELECTRIC_CAPACITANCE, 1.1130e-12),

        ]
    
    def get_units_class(self):
        return ElectricCapacitanceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricCapacitanceUnitModule()