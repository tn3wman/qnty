"""
EnergyFlux Units Module
=======================

Complete energy flux unit definitions and constants.
"""

from ..dimension import ENERGY_FLUX
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class EnergyFluxUnits:
    """Type-safe energy flux unit constants."""
    # Explicit declarations for type checking
    btu_per_square_foot_per_hour: 'UnitConstant'
    calorie_per_square_centimeter_per_second: 'UnitConstant'
    celsius: 'UnitConstant'
    kilocalorie_per_square_foot_per_hour: 'UnitConstant'
    kilocalorie_per_square_meter_per_hour: 'UnitConstant'
    watt_per_square_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class EnergyFluxUnitModule(UnitModule):
    """EnergyFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all energy flux unit definitions."""
        return [
            UnitDefinition("btu_per_square_foot_per_hour", "Btu / ft2 / hr", ENERGY_FLUX, 3.1546),
            UnitDefinition("calorie_per_square_centimeter_per_second", "cal / cm2 / s or cal / ( cm2 ~s )", ENERGY_FLUX, 41868),
            UnitDefinition("celsius", "°C", ENERGY_FLUX, 5.6784),
            UnitDefinition("kilocalorie_per_square_foot_per_hour", "kcal /left(ft2 hrright)", ENERGY_FLUX, 12.518),
            UnitDefinition("kilocalorie_per_square_meter_per_hour", "kcal /left(m2 hrright)", ENERGY_FLUX, 1.163),
            UnitDefinition("watt_per_square_meter", "W / m2", ENERGY_FLUX, 1),

        ]
    
    def get_units_class(self):
        return EnergyFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = EnergyFluxUnitModule()