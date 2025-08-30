"""
Mass Units Module
=================

Complete mass unit definitions and constants.
"""

from ..dimension import MASS
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MassUnits:
    """Type-safe mass unit constants."""
    # Explicit declarations for type checking
    slug: 'UnitConstant'
    atomic_mass_unit: 'UnitConstant'
    carat_metric: 'UnitConstant'
    cental: 'UnitConstant'
    centigram: 'UnitConstant'
    clove_uk: 'UnitConstant'
    drachm_apothecary: 'UnitConstant'
    dram_avoirdupois: 'UnitConstant'
    dram_troy: 'UnitConstant'
    grain: 'UnitConstant'
    gram: 'UnitConstant'
    hundredweight_long: 'UnitConstant'
    hundredweight_short: 'UnitConstant'
    kilogram: 'UnitConstant'
    kip: 'UnitConstant'
    microgram: 'UnitConstant'
    milligram: 'UnitConstant'
    ounce_apothecary: 'UnitConstant'
    ounce_avoirdupois: 'UnitConstant'
    ounce_troy: 'UnitConstant'
    pennyweight_troy: 'UnitConstant'
    pood_russia: 'UnitConstant'
    pound_apothecary: 'UnitConstant'
    pound_avoirdupois: 'UnitConstant'
    pound_troy: 'UnitConstant'
    pound_mass: 'UnitConstant'
    quarter_uk: 'UnitConstant'
    quintal_metric: 'UnitConstant'
    quital_us: 'UnitConstant'
    scruple_avoirdupois: 'UnitConstant'
    stone_uk: 'UnitConstant'
    ton_metric: 'UnitConstant'
    ton_us_long: 'UnitConstant'
    ton_us_short: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MassUnitModule(UnitModule):
    """Mass unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mass unit definitions."""
        return [
            UnitDefinition("slug", "sl", MASS, 14.594),
            UnitDefinition("atomic_mass_unit", "uleft( 12 Cright) or amu", MASS, 1.66050e-27),
            UnitDefinition("carat_metric", "ct", MASS, 0.0002),
            UnitDefinition("cental", "sh cwt, cH", MASS, 45.359),
            UnitDefinition("centigram", "cg", MASS, 0.00001),
            UnitDefinition("clove_uk", "cl", MASS, 3.6287),
            UnitDefinition("drachm_apothecary", "dr (ap)", MASS, 0.0038879),
            UnitDefinition("dram_avoirdupois", "dr (av)", MASS, 0.0017718),
            UnitDefinition("dram_troy", "dr (troy)", MASS, 0.0038879),
            UnitDefinition("grain", "gr", MASS, 0.000064799),
            UnitDefinition("gram", "g", MASS, 0.001),
            UnitDefinition("hundredweight_long", "cwt, lg cwt", MASS, 50.802),
            UnitDefinition("hundredweight_short", "sh cwt", MASS, 45.359),
            UnitDefinition("kilogram", "kg", MASS, 1),
            UnitDefinition("kip", "kip", MASS, 453.59),
            UnitDefinition("microgram", "mu g", MASS, 0.000000001),
            UnitDefinition("milligram", "mg", MASS, 0.000001),
            UnitDefinition("ounce_apothecary", "oz (ap)", MASS, 0.031103),
            UnitDefinition("ounce_avoirdupois", "oz", MASS, 0.02835),
            UnitDefinition("ounce_troy", "oz (troy)", MASS, 0.031103),
            UnitDefinition("pennyweight_troy", "dwt (troy)", MASS, 0.0015552),
            UnitDefinition("pood_russia", "pood", MASS, 16.38),
            UnitDefinition("pound_apothecary", "lb (ap)", MASS, 0.37324),
            UnitDefinition("pound_avoirdupois", "lb (av)", MASS, 0.45359),
            UnitDefinition("pound_troy", "lb (troy)", MASS, 0.37324),
            UnitDefinition("pound_mass", "lbm", MASS, 0.45359),
            UnitDefinition("quarter_uk", "qt", MASS, 12.7),
            UnitDefinition("quintal_metric", "q, dt", MASS, 100),
            UnitDefinition("quital_us", "quint (US)", MASS, 45.359),
            UnitDefinition("scruple_avoirdupois", "scf", MASS, 0.001575),
            UnitDefinition("stone_uk", "st", MASS, 6.3503),
            UnitDefinition("ton_metric", "t", MASS, 1000),
            UnitDefinition("ton_us_long", "lg ton", MASS, 1016),
            UnitDefinition("ton_us_short", "sh ton", MASS, 907.18),

        ]
    
    def get_units_class(self):
        return MassUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MassUnitModule()