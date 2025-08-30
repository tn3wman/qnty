"""
Length Units Module
===================

Complete length unit definitions and constants.
"""

from ..dimension import LENGTH
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class LengthUnits:
    """Type-safe length unit constants."""
    # Explicit declarations for type checking
    ångström: 'UnitConstant'
    arpent_quebec: 'UnitConstant'
    astronomic_unit: 'UnitConstant'
    attometer: 'UnitConstant'
    calibre_centinch: 'UnitConstant'
    centimeter: 'UnitConstant'
    chain_engrs: 'UnitConstant'
    chain_gunters: 'UnitConstant'
    chain_surveyors: 'UnitConstant'
    cubit_uk: 'UnitConstant'
    ell: 'UnitConstant'
    fathom: 'UnitConstant'
    femtometre: 'UnitConstant'
    fermi: 'UnitConstant'
    foot: 'UnitConstant'
    furlong_uk_and_us: 'UnitConstant'
    inch: 'UnitConstant'
    kilometer: 'UnitConstant'
    league_us_statute: 'UnitConstant'
    lieue_metric: 'UnitConstant'
    ligne_metric: 'UnitConstant'
    line_us: 'UnitConstant'
    link_surveyors: 'UnitConstant'
    meter: 'UnitConstant'
    micrometer: 'UnitConstant'
    micron: 'UnitConstant'
    mil: 'UnitConstant'
    mile_geographical: 'UnitConstant'
    mile_us_nautical: 'UnitConstant'
    mile_us_statute: 'UnitConstant'
    mile_us_survey: 'UnitConstant'
    millimeter: 'UnitConstant'
    millimicron: 'UnitConstant'
    nanometer: 'UnitConstant'
    parsec: 'UnitConstant'
    perche: 'UnitConstant'
    pica: 'UnitConstant'
    picometer: 'UnitConstant'
    point_didot: 'UnitConstant'
    point_us: 'UnitConstant'
    rod: 'UnitConstant'
    span: 'UnitConstant'
    thou_millinch: 'UnitConstant'
    toise_metric: 'UnitConstant'
    yard: 'UnitConstant'

    
    # Common aliases for test compatibility
    km: 'UnitConstant'  # kilometer
    m: 'UnitConstant'  # meter
    mm: 'UnitConstant'  # millimeter


class LengthUnitModule(UnitModule):
    """Length unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all length unit definitions."""
        return [
            UnitDefinition("ångström", "AA", LENGTH, 1.00e-10),
            UnitDefinition("arpent_quebec", "arp", LENGTH, 58.47),
            UnitDefinition("astronomic_unit", "AU", LENGTH, 1.4960e+11),
            UnitDefinition("attometer", "am", LENGTH, 1.00e-18),
            UnitDefinition("calibre_centinch", "cin", LENGTH, 0.000254),
            UnitDefinition("centimeter", "cm", LENGTH, 0.01),
            UnitDefinition("chain_engrs", "ch (eng or Rams)", LENGTH, 30.48),
            UnitDefinition("chain_gunters", "ch (Gunt)", LENGTH, 20.1168),
            UnitDefinition("chain_surveyors", "ch (surv)", LENGTH, 20.1168),
            UnitDefinition("cubit_uk", "cu (UK)", LENGTH, 0.4572),
            UnitDefinition("ell", "ell", LENGTH, 1.143),
            UnitDefinition("fathom", "fath", LENGTH, 1.8288),
            UnitDefinition("femtometre", "fm", LENGTH, 1.00e-15),
            UnitDefinition("fermi", "F", LENGTH, 1.00e-15),
            UnitDefinition("foot", "ft", LENGTH, 0.3048),
            UnitDefinition("furlong_uk_and_us", "fur", LENGTH, 201.168),
            UnitDefinition("inch", "in", LENGTH, 0.0254),
            UnitDefinition("kilometer", "km", LENGTH, 1000),
            UnitDefinition("league_us_statute", "lg (US, stat)", LENGTH, 4828),
            UnitDefinition("lieue_metric", "lieue (metric)", LENGTH, 4000),
            UnitDefinition("ligne_metric", "ligne (metric)", LENGTH, 0.0023),
            UnitDefinition("line_us", "li (US)", LENGTH, 0.000635),
            UnitDefinition("link_surveyors", "li (surv)", LENGTH, 0.201168),
            UnitDefinition("meter", "m", LENGTH, 1),
            UnitDefinition("micrometer", "mu m", LENGTH, 0.000001),
            UnitDefinition("micron", "mu", LENGTH, 0.000001),
            UnitDefinition("mil", "mil", LENGTH, 0.0000254),
            UnitDefinition("mile_geographical", "mi", LENGTH, 7421.59),
            UnitDefinition("mile_us_nautical", "mi (US, naut)", LENGTH, 1853.2),
            UnitDefinition("mile_us_statute", "mi", LENGTH, 1609.344),
            UnitDefinition("mile_us_survey", "mi (US, surv)", LENGTH, 1609.3),
            UnitDefinition("millimeter", "mm", LENGTH, 0.001),
            UnitDefinition("millimicron", "m mu", LENGTH, 1.00e-09),
            UnitDefinition("nanometer", "nm", LENGTH, 0.000000001),
            UnitDefinition("parsec", "pc", LENGTH, 3.0860e+16),
            UnitDefinition("perche", "rod", LENGTH, 5.0292),
            UnitDefinition("pica", "pica", LENGTH, 0.0042175),
            UnitDefinition("picometer", "pm", LENGTH, 1.00e-12),
            UnitDefinition("point_didot", "pt (Didot)", LENGTH, 0.00037597),
            UnitDefinition("point_us", "pt (US)", LENGTH, 0.00035146),
            UnitDefinition("rod", "rod", LENGTH, 5.0292),
            UnitDefinition("span", "span", LENGTH, 0.2286),
            UnitDefinition("thou_millinch", "thou", LENGTH, 0.0000254),
            UnitDefinition("toise_metric", "toise (metric)", LENGTH, 2),
            UnitDefinition("yard", "yd", LENGTH, 0.9144),

        ]
    
    def get_units_class(self):
        return LengthUnits
    
    def register_to_registry(self, unit_registry):
        """Register all unit definitions and set up aliases."""
        # First do the standard registration
        super().register_to_registry(unit_registry)
        
        # Then add custom aliases for test compatibility
        units_class = self.get_units_class()
        
        # Set up aliases pointing to existing unit constants
        if hasattr(units_class, 'kilometer'):
            units_class.km = units_class.kilometer
        if hasattr(units_class, 'meter'):
            units_class.m = units_class.meter
        if hasattr(units_class, 'millimeter'):
            units_class.mm = units_class.millimeter


# Register this module for auto-discovery
UNIT_MODULE = LengthUnitModule()