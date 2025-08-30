"""
PowerThermalDuty Units Module
=============================

Complete power, thermal duty unit definitions and constants.
"""

from ..dimension import POWER
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class PowerThermalDutyUnits:
    """Type-safe power, thermal duty unit constants."""
    # Explicit declarations for type checking
    abwatt_emu_of_power: 'UnitConstant'
    boiler_horsepower: 'UnitConstant'
    british_thermal_unit_mean_per_hour: 'UnitConstant'
    british_thermal_unit_mean_per_minute: 'UnitConstant'
    british_thermal_unit_thermochemical_per_hour: 'UnitConstant'
    british_thermal_unit_thermochemical_per_minute: 'UnitConstant'
    calorie_mean_per_hour: 'UnitConstant'
    calorie_thermochemical_per_hour: 'UnitConstant'
    donkey: 'UnitConstant'
    erg_per_second: 'UnitConstant'
    foot_pondal_per_second: 'UnitConstant'
    foot_pound_force_per_hour: 'UnitConstant'
    foot_pound_force_per_minute: 'UnitConstant'
    foot_pound_force_per_second: 'UnitConstant'
    horsepower: 'UnitConstant'
    horsepower_electric: 'UnitConstant'
    horsepower_uk: 'UnitConstant'
    kcal_per_hour: 'UnitConstant'
    kilogram_force_meter_per_second: 'UnitConstant'
    kilowatt: 'UnitConstant'
    megawatt: 'UnitConstant'
    metric_horsepower: 'UnitConstant'
    million_british_thermal_units_per_hour_petroleum: 'UnitConstant'
    million_kilocalorie_per_hour: 'UnitConstant'
    prony: 'UnitConstant'
    ton_of_refrigeration_us: 'UnitConstant'
    ton: 'UnitConstant'
    voltampere: 'UnitConstant'
    water_horsepower: 'UnitConstant'
    watt: 'UnitConstant'
    watt_international_mean: 'UnitConstant'
    watt_international_us: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class PowerThermalDutyUnitModule(UnitModule):
    """PowerThermalDuty unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all power, thermal duty unit definitions."""
        return [
            UnitDefinition("abwatt_emu_of_power", "emu", POWER, 1.00e-08),
            UnitDefinition("boiler_horsepower", "HP (boiler)", POWER, 9809.5),
            UnitDefinition("british_thermal_unit_mean_per_hour", "Btu (mean)/hr or Btu/hr", POWER, 0.293297),
            UnitDefinition("british_thermal_unit_mean_per_minute", "Btu/min or Btu (mean)/min", POWER, 17.597833),
            UnitDefinition("british_thermal_unit_thermochemical_per_hour", "Btu (therm)/hr or Btu/hr", POWER, 0.292875),
            UnitDefinition("british_thermal_unit_thermochemical_per_minute", "Btu / min or Btu (therm)/min", POWER, 17.5725),
            UnitDefinition("calorie_mean_per_hour", "cal (mean)/hr", POWER, 0.00116389),
            UnitDefinition("calorie_thermochemical_per_hour", "cal (therm)/hr", POWER, 0.00116222),
            UnitDefinition("donkey", "donkey", POWER, 250),
            UnitDefinition("erg_per_second", "erg/s", POWER, 1.00e-07),
            UnitDefinition("foot_pondal_per_second", "ft pdl/s", POWER, 0.04214),
            UnitDefinition("foot_pound_force_per_hour", "ft lbf / hr", POWER, 3.7044e-04),
            UnitDefinition("foot_pound_force_per_minute", "ft lbf / min", POWER, 0.022597),
            UnitDefinition("foot_pound_force_per_second", "ft lbf / s", POWER, 1.355818),
            UnitDefinition("horsepower", "HP", POWER, 745.7),
            UnitDefinition("horsepower_electric", "HP (elect)", POWER, 746),
            UnitDefinition("horsepower_uk", "HP (UK)", POWER, 745.7),
            UnitDefinition("kcal_per_hour", "kcal/hr", POWER, 1.16389),
            UnitDefinition("kilogram_force_meter_per_second", "kgf m / s", POWER, 9.80665),
            UnitDefinition("kilowatt", "kW", POWER, 1000),
            UnitDefinition("megawatt", "MW", POWER, 1000000),
            UnitDefinition("metric_horsepower", "HP (metric)", POWER, 735.499),
            UnitDefinition("million_british_thermal_units_per_hour_petroleum", "MMBtu/hr", POWER, 293297),
            UnitDefinition("million_kilocalorie_per_hour", "MM kcal/hr", POWER, 1163890),
            UnitDefinition("prony", "prony", POWER, 98.0665),
            UnitDefinition("ton_of_refrigeration_us", "CTR (US)", POWER, 3516.8),
            UnitDefinition("ton", "CTR (UK)", POWER, 3922.7),
            UnitDefinition("voltampere", "VA", POWER, 1),
            UnitDefinition("water_horsepower", "HP (water)", POWER, 746.043),
            UnitDefinition("watt", "W", POWER, 1),
            UnitDefinition("watt_international_mean", "W (int, mean)", POWER, 1.00019),
            UnitDefinition("watt_international_us", "watt (int, US)", POWER, 1.000165),

        ]
    
    def get_units_class(self):
        return PowerThermalDutyUnits
    


# Register this module for auto-discovery
UNIT_MODULE = PowerThermalDutyUnitModule()