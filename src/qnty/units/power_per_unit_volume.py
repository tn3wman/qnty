"""
PowerPerUnitVolumeOrPowerDensity Units Module
=============================================

Complete power per unit volume or power density unit definitions and constants.
"""

from ..dimension import POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class PowerPerUnitVolumeOrPowerDensityUnits:
    """Type-safe power per unit volume or power density unit constants."""
    # Explicit declarations for type checking
    british_thermal_unit_per_hour_per_cubic_foot: 'UnitConstant'
    calorie_per_second_per_cubic_centimeter: 'UnitConstant'
    chu_per_hour_per_cubic_foot: 'UnitConstant'
    kilocalorie_per_hour_per_cubic_centimeter: 'UnitConstant'
    kilocalorie_per_hour_per_cubic_foot: 'UnitConstant'
    kilocalorie_per_second_per_cubic_centimeter: 'UnitConstant'
    watt_per_cubic_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class PowerPerUnitVolumeOrPowerDensityUnitModule(UnitModule):
    """PowerPerUnitVolumeOrPowerDensity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all power per unit volume or power density unit definitions."""
        return [
            UnitDefinition("british_thermal_unit_per_hour_per_cubic_foot", "Btu / h / ft3 or Btu / hr / cft", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 10.35),
            UnitDefinition("calorie_per_second_per_cubic_centimeter", "cal / s / cm3 or cal / s / cc", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 4.1868e+06),
            UnitDefinition("chu_per_hour_per_cubic_foot", "Chu/h/ft3 or Chu/hr/ cft", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 18.63),
            UnitDefinition("kilocalorie_per_hour_per_cubic_centimeter", "kcal / h / cm3 or kcal / hr/cc", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 1.163),
            UnitDefinition("kilocalorie_per_hour_per_cubic_foot", "kcal / h / ft3 or kcal / hr / cft", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 41.071),
            UnitDefinition("kilocalorie_per_second_per_cubic_centimeter", "kcal/s/cm  3 or kcal/s/ cc", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 4.1868e+09),
            UnitDefinition("watt_per_cubic_meter", "W / m3", POWER_PER_UNIT_VOLUME_OR_POWER_DENSITY, 1),

        ]
    
    def get_units_class(self):
        return PowerPerUnitVolumeOrPowerDensityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = PowerPerUnitVolumeOrPowerDensityUnitModule()