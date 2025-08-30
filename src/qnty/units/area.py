"""
Area Units Module
=================

Complete area unit definitions and constants.
"""

from ..dimension import AREA
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AreaUnits:
    """Type-safe area unit constants."""
    # Explicit declarations for type checking
    acre_general: 'UnitConstant'
    are: 'UnitConstant'
    arpent_quebec: 'UnitConstant'
    barn: 'UnitConstant'
    circular_inch: 'UnitConstant'
    circular_mil: 'UnitConstant'
    hectare: 'UnitConstant'
    shed: 'UnitConstant'
    square_centimeter: 'UnitConstant'
    square_chain_ramsden: 'UnitConstant'
    square_chain_survey_gunters: 'UnitConstant'
    square_decimeter: 'UnitConstant'
    square_fermi: 'UnitConstant'
    square_foot: 'UnitConstant'
    square_hectometer: 'UnitConstant'
    square_inch: 'UnitConstant'
    square_kilometer: 'UnitConstant'
    square_league_statute: 'UnitConstant'
    square_meter: 'UnitConstant'
    square_micron: 'UnitConstant'
    square_mile_statute: 'UnitConstant'
    square_mile_us_survey: 'UnitConstant'
    square_millimeter: 'UnitConstant'
    square_nanometer: 'UnitConstant'
    square_yard: 'UnitConstant'
    township_us: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AreaUnitModule(UnitModule):
    """Area unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all area unit definitions."""
        return [
            UnitDefinition("acre_general", "ac", AREA, 4046.856),
            UnitDefinition("are", "a", AREA, 100),
            UnitDefinition("arpent_quebec", "arp", AREA, 3418.89),
            UnitDefinition("barn", "b", AREA, 1.00e-28),
            UnitDefinition("circular_inch", "cin", AREA, 0.000506707),
            UnitDefinition("circular_mil", "cmil", AREA, 5.07e-10),
            UnitDefinition("hectare", "ha", AREA, 10000),
            UnitDefinition("shed", "shed", AREA, 1.00e-52),
            UnitDefinition("square_centimeter", "cm2", AREA, 0.0001),
            UnitDefinition("square_chain_ramsden", "sq ch (Rams)", AREA, 929.03),
            UnitDefinition("square_chain_survey_gunters", "sq ch (surv)", AREA, 404.6856),
            UnitDefinition("square_decimeter", "dm2", AREA, 0.01),
            UnitDefinition("square_fermi", "F2", AREA, 1.00e-30),
            UnitDefinition("square_foot", "sq ft or ft  2", AREA, 0.092903),
            UnitDefinition("square_hectometer", "hm2", AREA, 10000),
            UnitDefinition("square_inch", "sq in or in  2", AREA, 0.00064516),
            UnitDefinition("square_kilometer", "km2", AREA, 1000000),
            UnitDefinition("square_league_statute", "sq lg (stat)", AREA, 2.3310e+07),
            UnitDefinition("square_meter", "m2", AREA, 1),
            UnitDefinition("square_micron", "mu m2 or mu2", AREA, 1.00e-12),
            UnitDefinition("square_mile_statute", "sq mi (stat)", AREA, 2.5900e+06),
            UnitDefinition("square_mile_us_survey", "sq mi (US Surv)", AREA, 2.5900e+06),
            UnitDefinition("square_millimeter", "mm2", AREA, 0.000001),
            UnitDefinition("square_nanometer", "nm2", AREA, 1.00e-18),
            UnitDefinition("square_yard", "sq yd", AREA, 0.836131),
            UnitDefinition("township_us", "twshp", AREA, 9.3240e+07),

        ]
    
    def get_units_class(self):
        return AreaUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AreaUnitModule()