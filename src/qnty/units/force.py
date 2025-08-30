"""
Force Units Module
==================

Complete force unit definitions and constants.
"""

from ..dimension import FORCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ForceUnits:
    """Type-safe force unit constants."""
    # Explicit declarations for type checking
    crinal: 'UnitConstant'
    dyne: 'UnitConstant'
    funal: 'UnitConstant'
    kilogram_force: 'UnitConstant'
    kip_force: 'UnitConstant'
    newton: 'UnitConstant'
    ounce_force: 'UnitConstant'
    pond: 'UnitConstant'
    pound_force: 'UnitConstant'
    poundal: 'UnitConstant'
    slug_force: 'UnitConstant'
    sthène: 'UnitConstant'
    ton_force_long: 'UnitConstant'
    ton_force_metric: 'UnitConstant'
    ton_force_short: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ForceUnitModule(UnitModule):
    """Force unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all force unit definitions."""
        return [
            UnitDefinition("crinal", "crinal", FORCE, 0.1),
            UnitDefinition("dyne", "dyn", FORCE, 0.00001),
            UnitDefinition("funal", "funal", FORCE, 1000),
            UnitDefinition("kilogram_force", "kgf", FORCE, 9.80665),
            UnitDefinition("kip_force", "operatornamekipf", FORCE, 4448.22),
            UnitDefinition("newton", "N", FORCE, 1),
            UnitDefinition("ounce_force", "ozf or oz", FORCE, 0.27801385),
            UnitDefinition("pond", "p", FORCE, 0.0098066),
            UnitDefinition("pound_force", "lbf or lb", FORCE, 4.4482216),
            UnitDefinition("poundal", "pdl", FORCE, 0.13825495),
            UnitDefinition("slug_force", "operatornameslugf", FORCE, 143.117),
            UnitDefinition("sthène", "sn", FORCE, 1000),
            UnitDefinition("ton_force_long", "LT", FORCE, 9964.016),
            UnitDefinition("ton_force_metric", "MT", FORCE, 9806.65),
            UnitDefinition("ton_force_short", "T", FORCE, 8896.44),

        ]
    
    def get_units_class(self):
        return ForceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ForceUnitModule()