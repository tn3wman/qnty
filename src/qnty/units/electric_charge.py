"""
ElectricCharge Units Module
===========================

Complete electric charge unit definitions and constants.
"""

from ..dimension import ELECTRIC_CHARGE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricChargeUnits:
    """Type-safe electric charge unit constants."""
    # Explicit declarations for type checking
    abcoulomb: 'UnitConstant'
    amperehour: 'UnitConstant'
    coulomb: 'UnitConstant'
    faraday_c12: 'UnitConstant'
    franklin: 'UnitConstant'
    statcoulomb: 'UnitConstant'
    ua_charge: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricChargeUnitModule(UnitModule):
    """ElectricCharge unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric charge unit definitions."""
        return [
            UnitDefinition("abcoulomb", "emu cgs", ELECTRIC_CHARGE, 0.000103643),
            UnitDefinition("amperehour", "Ah", ELECTRIC_CHARGE, 0.03731138),
            UnitDefinition("coulomb", "C", ELECTRIC_CHARGE, 1.0364e-05),
            UnitDefinition("faraday_c12", "F", ELECTRIC_CHARGE, 1),
            UnitDefinition("franklin", "Fr", ELECTRIC_CHARGE, 3.45715e-15),
            UnitDefinition("statcoulomb", "esu cgs", ELECTRIC_CHARGE, 3.45715e-15),
            UnitDefinition("ua_charge", "u.a.", ELECTRIC_CHARGE, 1.66054e-24),

        ]
    
    def get_units_class(self):
        return ElectricChargeUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricChargeUnitModule()