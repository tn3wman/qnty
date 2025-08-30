"""
ElectricPotential Units Module
==============================

Complete electric potential unit definitions and constants.
"""

from ..dimension import ELECTRIC_POTENTIAL
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricPotentialUnits:
    """Type-safe electric potential unit constants."""
    # Explicit declarations for type checking
    abvolt: 'UnitConstant'
    statvolt: 'UnitConstant'
    ua_potential: 'UnitConstant'
    volt: 'UnitConstant'
    volt_intl_mean: 'UnitConstant'
    volt_us: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricPotentialUnitModule(UnitModule):
    """ElectricPotential unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric potential unit definitions."""
        return [
            UnitDefinition("abvolt", "emu cgs", ELECTRIC_POTENTIAL, 1.00e-08),
            UnitDefinition("statvolt", "esu cgs", ELECTRIC_POTENTIAL, 299.792),
            UnitDefinition("ua_potential", "u.a.", ELECTRIC_POTENTIAL, 27.2114),
            UnitDefinition("volt", "V", ELECTRIC_POTENTIAL, 1),
            UnitDefinition("volt_intl_mean", "V (int mean)", ELECTRIC_POTENTIAL, 1.00034),
            UnitDefinition("volt_us", "V (int US)", ELECTRIC_POTENTIAL, 1.00033),

        ]
    
    def get_units_class(self):
        return ElectricPotentialUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricPotentialUnitModule()