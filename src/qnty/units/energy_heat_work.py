"""
EnergyHeatWork Units Module
===========================

Complete energy, heat, work unit definitions and constants.
"""

from ..dimension import ENERGY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class EnergyHeatWorkUnits:
    """Type-safe energy, heat, work unit constants."""
    # Explicit declarations for type checking
    barrel_oil_equivalent: 'UnitConstant'
    billion_electronvolt: 'UnitConstant'
    british_thermal_unit: 'UnitConstant'
    british_thermal_unit: 'UnitConstant'
    british_thermal_unit_international_steam_tables: 'UnitConstant'
    british_thermal_unit_isotc_12: 'UnitConstant'
    british_thermal_unit_mean: 'UnitConstant'
    british_thermal_unit_thermochemical: 'UnitConstant'
    calorie: 'UnitConstant'
    calorie: 'UnitConstant'
    calorie_international_steam_tables: 'UnitConstant'
    calorie_mean: 'UnitConstant'
    calorie_nutritional: 'UnitConstant'
    calorie_thermochemical: 'UnitConstant'
    celsius: 'UnitConstant'
    celsius: 'UnitConstant'
    electron_volt: 'UnitConstant'
    erg: 'UnitConstant'
    foot_pound_force_duty: 'UnitConstant'
    footpoundal: 'UnitConstant'
    frigorie: 'UnitConstant'
    hartree_atomic_unit_of_energy: 'UnitConstant'
    joule: 'UnitConstant'
    joule_international: 'UnitConstant'
    kilocalorie_thermal: 'UnitConstant'
    kilogram_force_meter: 'UnitConstant'
    kiloton_tnt: 'UnitConstant'
    kilowatt_hour: 'UnitConstant'
    liter_atmosphere: 'UnitConstant'
    megaton_tnt: 'UnitConstant'
    pound_centigrade_unit: 'UnitConstant'
    prout: 'UnitConstant'
    q_unit: 'UnitConstant'
    quad_quadrillion_btu: 'UnitConstant'
    rydberg: 'UnitConstant'
    therm_eeg: 'UnitConstant'
    therm_refineries: 'UnitConstant'
    therm_us: 'UnitConstant'
    ton_coal_equivalent: 'UnitConstant'
    ton_oil_equivalent: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class EnergyHeatWorkUnitModule(UnitModule):
    """EnergyHeatWork unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all energy, heat, work unit definitions."""
        return [
            UnitDefinition("barrel_oil_equivalent", "bboe or boe", ENERGY, 6.12e+09),
            UnitDefinition("billion_electronvolt", "BeV", ENERGY, 1.6022e-10),
            UnitDefinition("british_thermal_unit", "Btu ( 39.2 ° F )", ENERGY, 1059.67),
            UnitDefinition("british_thermal_unit", "Btu ( 60 ° F )", ENERGY, 1054.678),
            UnitDefinition("british_thermal_unit_international_steam_tables", "Btu (IT)", ENERGY, 1055.055853),
            UnitDefinition("british_thermal_unit_isotc_12", "Btu (ISO)", ENERGY, 1055.06),
            UnitDefinition("british_thermal_unit_mean", "Btu (mean) or Btu", ENERGY, 1055.87),
            UnitDefinition("british_thermal_unit_thermochemical", "Btu (therm)", ENERGY, 1054.35),
            UnitDefinition("calorie", "cal ( 20° C )", ENERGY, 4.1819),
            UnitDefinition("calorie", "cal ( 4° C )", ENERGY, 4.2045),
            UnitDefinition("calorie_international_steam_tables", "cal (IT)", ENERGY, 4.18674),
            UnitDefinition("calorie_mean", "cal (mean)", ENERGY, 4.19002),
            UnitDefinition("calorie_nutritional", "Cal (nutr)", ENERGY, 4184),
            UnitDefinition("calorie_thermochemical", "cal (therm)", ENERGY, 4.184),
            UnitDefinition("celsius", "°C", ENERGY, 1899.18),
            UnitDefinition("celsius", "°C", ENERGY, 1899.1),
            UnitDefinition("electron_volt", "eV", ENERGY, 1.6022e-19),
            UnitDefinition("erg", "erg", ENERGY, 1.00e-07),
            UnitDefinition("foot_pound_force_duty", "ft lbf", ENERGY, 1.355818),
            UnitDefinition("footpoundal", "ft pdl", ENERGY, 0.04214),
            UnitDefinition("frigorie", "fg", ENERGY, -4.19e+03),
            UnitDefinition("hartree_atomic_unit_of_energy", "EH a.u.", ENERGY, 4.3597e-18),
            UnitDefinition("joule", "J", ENERGY, 1),
            UnitDefinition("joule_international", "J (intl)", ENERGY, 1.000165),
            UnitDefinition("kilocalorie_thermal", "kcal (therm)", ENERGY, 4184),
            UnitDefinition("kilogram_force_meter", "kgf m", ENERGY, 9.80665),
            UnitDefinition("kiloton_tnt", "kt (TNT)", ENERGY, 4.18e+18),
            UnitDefinition("kilowatt_hour", "kWh", ENERGY, 3.60e+06),
            UnitDefinition("liter_atmosphere", "L atm", ENERGY, 101.325),
            UnitDefinition("megaton_tnt", "Mt (TNT)", ENERGY, 4.18e+21),
            UnitDefinition("pound_centigrade_unit", "pcu ( 15 ° C )", ENERGY, 1899.1),
            UnitDefinition("prout", "prout", ENERGY, 2.9638e-14),
            UnitDefinition("q_unit", "Q", ENERGY, 1.055e+21),
            UnitDefinition("quad_quadrillion_btu", "quad", ENERGY, 1.0551e+18),
            UnitDefinition("rydberg", "Ry", ENERGY, 2.1799e-18),
            UnitDefinition("therm_eeg", "therm (EEG)", ENERGY, 1.0551e+08),
            UnitDefinition("therm_refineries", "therm (refy) or therm", ENERGY, 1.0559e+09),
            UnitDefinition("therm_us", "therm (US) or therm", ENERGY, 1.0548e+08),
            UnitDefinition("ton_coal_equivalent", "tce (tec)", ENERGY, 2.929e+08),
            UnitDefinition("ton_oil_equivalent", "toe (tep)", ENERGY, 4.187e+08),

        ]
    
    def get_units_class(self):
        return EnergyHeatWorkUnits
    


# Register this module for auto-discovery
UNIT_MODULE = EnergyHeatWorkUnitModule()