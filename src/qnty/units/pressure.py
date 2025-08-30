"""
Pressure Units Module
=====================

Complete pressure unit definitions and constants.
"""

from ..dimension import PRESSURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class PressureUnits:
    """Type-safe pressure unit constants."""
    # Explicit declarations for type checking
    atmosphere_standard: 'UnitConstant'
    bar: 'UnitConstant'
    barye: 'UnitConstant'
    dyne_per_square_centimeter: 'UnitConstant'
    foot_of_mercury: 'UnitConstant'
    foot_of_water: 'UnitConstant'
    gigapascal: 'UnitConstant'
    hectopascal: 'UnitConstant'
    inch_of_mercury: 'UnitConstant'
    inch_of_water: 'UnitConstant'
    kilogram_force_per_square_centimeter: 'UnitConstant'
    kilogram_force_per_square_meter: 'UnitConstant'
    kip_force_per_square_inch: 'UnitConstant'
    megapascal: 'UnitConstant'
    meter_of_water: 'UnitConstant'
    microbar: 'UnitConstant'
    millibar: 'UnitConstant'
    millimeter_of_mercury: 'UnitConstant'
    millimeter_of_water: 'UnitConstant'
    newton_per_square_meter: 'UnitConstant'
    ounce_force_per_square_inch: 'UnitConstant'
    pascal: 'UnitConstant'
    pièze: 'UnitConstant'
    pound_force_per_square_foot: 'UnitConstant'
    pound_force_per_square_inch: 'UnitConstant'
    torr: 'UnitConstant'
    kilopascal: 'UnitConstant'
    psi: 'UnitConstant'
    kPa: 'UnitConstant'
    
    # Common aliases for test compatibility
    bar: 'UnitConstant'  # bar
    MPa: 'UnitConstant'  # megapascal
    kPa: 'UnitConstant'  # kilopascal


class PressureUnitModule(UnitModule):
    """Pressure unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all pressure unit definitions."""
        return [
            UnitDefinition("atmosphere_standard", "atm", PRESSURE, 101325),
            UnitDefinition("bar", "bar", PRESSURE, 1.00e+05),
            UnitDefinition("barye", "barye", PRESSURE, 0.1),
            UnitDefinition("dyne_per_square_centimeter", "dyn / cm2", PRESSURE, 0.1),
            UnitDefinition("foot_of_mercury", "ft Hg ( 60 ° F )", PRESSURE, 4.0526e+04),
            UnitDefinition("foot_of_water", "ft H2 Oleft(60° Fright)", PRESSURE, 2.9890e+03),
            UnitDefinition("gigapascal", "GPa", PRESSURE, 1.00e+09),
            UnitDefinition("hectopascal", "hPa", PRESSURE, 100),
            UnitDefinition("inch_of_mercury", "in Hgleft(60 ° Fright)", PRESSURE, 3.3864e+03),
            UnitDefinition("inch_of_water", "in H2 Oleft(60° Fright)", PRESSURE, 248.845),
            UnitDefinition("kilogram_force_per_square_centimeter", "at or kgf / cm2", PRESSURE, 9.8067e+04),
            UnitDefinition("kilogram_force_per_square_meter", "kgf / m2", PRESSURE, 9.80665),
            UnitDefinition("kip_force_per_square_inch", "KSI or ksi or kip  f / in2", PRESSURE, 6.8948e+06),
            UnitDefinition("megapascal", "MPa", PRESSURE, 1.00e+06),
            UnitDefinition("meter_of_water", "m H2 Oleft(4° Cright)", PRESSURE, 9.8064e+03),
            UnitDefinition("microbar", "mu bar", PRESSURE, 0.1),
            UnitDefinition("millibar", "mbar", PRESSURE, 100),
            UnitDefinition("millimeter_of_mercury", "mm Hgleft(4° Cright)", PRESSURE, 133.322),
            UnitDefinition("millimeter_of_water", "mm H2 Oleft(4° Cright)", PRESSURE, 9.806375),
            UnitDefinition("newton_per_square_meter", "N / m2", PRESSURE, 1),
            UnitDefinition("ounce_force_per_square_inch", "OSI or osi or ozf / in2", PRESSURE, 430.922),
            UnitDefinition("pascal", "Pa", PRESSURE, 1),
            UnitDefinition("pièze", "pz", PRESSURE, 1000),
            UnitDefinition("pound_force_per_square_foot", "PSF or psf or lbf / ft2", PRESSURE, 47.880259),
            UnitDefinition("pound_force_per_square_inch", "PSI or psi or lbf / in2", PRESSURE, 6.8948e+03),
            UnitDefinition("torr", "torr or mm Hg ( 0 ° C)", PRESSURE, 133.322),
            UnitDefinition("kilopascal", "kPa", PRESSURE, 1000),
            # Test-expected alias as separate unit
            UnitDefinition("psi", "psi", PRESSURE, 6894.757),
        ]
    
    def get_units_class(self):
        return PressureUnits
    
    def register_to_registry(self, unit_registry):
        """Register all unit definitions and set up aliases."""
        # First do the standard registration
        super().register_to_registry(unit_registry)
        
        # Then add custom aliases for test compatibility
        units_class = self.get_units_class()
        
        # Set up aliases pointing to existing unit constants
        if hasattr(units_class, 'bar'):
            units_class.bar = units_class.bar
        if hasattr(units_class, 'megapascal'):
            units_class.MPa = units_class.megapascal
        if hasattr(units_class, 'kilopascal'):
            units_class.kPa = units_class.kilopascal


# Register this module for auto-discovery
UNIT_MODULE = PressureUnitModule()