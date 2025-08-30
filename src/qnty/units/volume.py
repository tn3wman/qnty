"""
Volume Units Module
===================

Complete volume unit definitions and constants.
"""

from ..dimension import VOLUME
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumeUnits:
    """Type-safe volume unit constants."""
    # Explicit declarations for type checking
    acre_foot: 'UnitConstant'
    acre_inch: 'UnitConstant'
    barrel_us_liquid: 'UnitConstant'
    barrel_us_petro: 'UnitConstant'
    board_foot_measure: 'UnitConstant'
    bushel_us_dry: 'UnitConstant'
    centiliter: 'UnitConstant'
    cord: 'UnitConstant'
    cord_foot: 'UnitConstant'
    cubic_centimeter: 'UnitConstant'
    cubic_decameter: 'UnitConstant'
    cubic_decimeter: 'UnitConstant'
    cubic_foot: 'UnitConstant'
    cubic_inch: 'UnitConstant'
    cubic_kilometer: 'UnitConstant'
    cubic_meter: 'UnitConstant'
    cubic_micrometer: 'UnitConstant'
    cubic_mile_us_intl: 'UnitConstant'
    cubic_millimeter: 'UnitConstant'
    cubic_yard: 'UnitConstant'
    decastére: 'UnitConstant'
    deciliter: 'UnitConstant'
    fluid_drachm_uk: 'UnitConstant'
    fluid_dram_us: 'UnitConstant'
    fluid_ounce_us: 'UnitConstant'
    gallon_imperial_uk: 'UnitConstant'
    gallon_us_dry: 'UnitConstant'
    gallon_us_liquid: 'UnitConstant'
    last: 'UnitConstant'
    liter: 'UnitConstant'
    microliter: 'UnitConstant'
    milliliter: 'UnitConstant'
    mohr_centicube: 'UnitConstant'
    pint_uk: 'UnitConstant'
    pint_us_dry: 'UnitConstant'
    pint_us_liquid: 'UnitConstant'
    quart_us_dry: 'UnitConstant'
    stére: 'UnitConstant'
    tablespoon_metric: 'UnitConstant'
    tablespoon_us: 'UnitConstant'
    teaspoon_us: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumeUnitModule(UnitModule):
    """Volume unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volume unit definitions."""
        return [
            UnitDefinition("acre_foot", "ac-ft", VOLUME, 1233.48),
            UnitDefinition("acre_inch", "ac-in", VOLUME, 102.79),
            UnitDefinition("barrel_us_liquid", "bbl (US liq)", VOLUME, 0.1192405),
            UnitDefinition("barrel_us_petro", "bbl", VOLUME, 0.158987),
            UnitDefinition("board_foot_measure", "BM or fbm", VOLUME, 0.00235974),
            UnitDefinition("bushel_us_dry", "bu (US dry)", VOLUME, 0.0352391),
            UnitDefinition("centiliter", "cl or cL", VOLUME, 0.00001),
            UnitDefinition("cord", "cord or cd", VOLUME, 3.62456),
            UnitDefinition("cord_foot", "cord-ft", VOLUME, 0.4530695),
            UnitDefinition("cubic_centimeter", "cm3 or cc", VOLUME, 0.000001),
            UnitDefinition("cubic_decameter", "dam  3", VOLUME, 1000),
            UnitDefinition("cubic_decimeter", "dm3", VOLUME, 0.001),
            UnitDefinition("cubic_foot", "cu ft or ft  3", VOLUME, 0.0283168),
            UnitDefinition("cubic_inch", "cu in or in3", VOLUME, 1.63871e-05),
            UnitDefinition("cubic_kilometer", "km3", VOLUME, 1.00e+09),
            UnitDefinition("cubic_meter", "m3", VOLUME, 1),
            UnitDefinition("cubic_micrometer", "mu m3", VOLUME, 1.00e-18),
            UnitDefinition("cubic_mile_us_intl", "cu mi", VOLUME, 4.16818e+09),
            UnitDefinition("cubic_millimeter", "mm3", VOLUME, 1.00e-09),
            UnitDefinition("cubic_yard", "cu yd or yd3", VOLUME, 0.7645549),
            UnitDefinition("decastére", "dast", VOLUME, 10),
            UnitDefinition("deciliter", "dl or dL", VOLUME, 0.0001),
            UnitDefinition("fluid_drachm_uk", "fl dr (UK)", VOLUME, 3.55163e-06),
            UnitDefinition("fluid_dram_us", "fl dr (US liq)", VOLUME, 3.69669e-06),
            UnitDefinition("fluid_ounce_us", "fl oz", VOLUME, 2.95735e-05),
            UnitDefinition("gallon_imperial_uk", "gal (UK) or Imp gal", VOLUME, 0.00454609),
            UnitDefinition("gallon_us_dry", "gal (US dry)", VOLUME, 0.004404884),
            UnitDefinition("gallon_us_liquid", "gal", VOLUME, 0.003785412),
            UnitDefinition("last", "last", VOLUME, 2.9095),
            UnitDefinition("liter", "1 or L", VOLUME, 0.001),
            UnitDefinition("microliter", "mu l or mu L", VOLUME, 1.00e-09),
            UnitDefinition("milliliter", "ml", VOLUME, 0.000001),
            UnitDefinition("mohr_centicube", "cc", VOLUME, 1.00238e-06),
            UnitDefinition("pint_uk", "pt (UK)", VOLUME, 0.000568262),
            UnitDefinition("pint_us_dry", "pt (US dry)", VOLUME, 0.000550611),
            UnitDefinition("pint_us_liquid", "pt", VOLUME, 0.000473176),
            UnitDefinition("quart_us_dry", "qt (US dry)", VOLUME, 0.00110122),
            UnitDefinition("stére", "st", VOLUME, 1),
            UnitDefinition("tablespoon_metric", "tbsp (Metric)", VOLUME, 1.50e-05),
            UnitDefinition("tablespoon_us", "tbsp", VOLUME, 1.47868e-05),
            UnitDefinition("teaspoon_us", "tsp", VOLUME, 4.92892e-06),

        ]
    
    def get_units_class(self):
        return VolumeUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumeUnitModule()