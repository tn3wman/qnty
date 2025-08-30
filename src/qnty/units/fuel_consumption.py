"""
FuelConsumption Units Module
============================

Complete fuel consumption unit definitions and constants.
"""

from ..dimension import FUEL_CONSUMPTION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class FuelConsumptionUnits:
    """Type-safe fuel consumption unit constants."""
    # Explicit declarations for type checking
    unit_100_km_per_liter: 'UnitConstant'
    gallons_uk_per_100_miles: 'UnitConstant'
    gallons_us_per_100_miles: 'UnitConstant'
    kilometers_per_gallon_uk: 'UnitConstant'
    kilometers_per_gallon_us: 'UnitConstant'
    kilometers_per_liter: 'UnitConstant'
    liters_per_100_km: 'UnitConstant'
    liters_per_kilometer: 'UnitConstant'
    meters_per_gallon_uk: 'UnitConstant'
    meters_per_gallon_us: 'UnitConstant'
    miles_per_gallon_uk: 'UnitConstant'
    miles_per_gallon_us: 'UnitConstant'
    miles_per_liter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class FuelConsumptionUnitModule(UnitModule):
    """FuelConsumption unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all fuel consumption unit definitions."""
        return [
            UnitDefinition("unit_100_km_per_liter", "100 ~km / l", FUEL_CONSUMPTION, 100),
            UnitDefinition("gallons_uk_per_100_miles", "gal (UK)/ 100 mi", FUEL_CONSUMPTION, 35.4),
            UnitDefinition("gallons_us_per_100_miles", "gal (US)/ 100 mi", FUEL_CONSUMPTION, 42.51),
            UnitDefinition("kilometers_per_gallon_uk", "km/gal (UK)", FUEL_CONSUMPTION, 0.21997),
            UnitDefinition("kilometers_per_gallon_us", "km/gal(US)", FUEL_CONSUMPTION, 0.26417),
            UnitDefinition("kilometers_per_liter", "km/l", FUEL_CONSUMPTION, 1),
            UnitDefinition("liters_per_100_km", "1 / 100 ~km", FUEL_CONSUMPTION, 100),
            UnitDefinition("liters_per_kilometer", "1/km", FUEL_CONSUMPTION, 1),
            UnitDefinition("meters_per_gallon_uk", "m/gal (UK)", FUEL_CONSUMPTION, 2.1997e-04),
            UnitDefinition("meters_per_gallon_us", "1/gal (US)", FUEL_CONSUMPTION, 2.2642e-04),
            UnitDefinition("miles_per_gallon_uk", "mi/gal (UK) or mpg (UK)", FUEL_CONSUMPTION, 0.35401),
            UnitDefinition("miles_per_gallon_us", "mi/gal (US) or mpg (US)", FUEL_CONSUMPTION, 0.42514),
            UnitDefinition("miles_per_liter", "mi/l", FUEL_CONSUMPTION, 1.6093),

        ]
    
    def get_units_class(self):
        return FuelConsumptionUnits
    


# Register this module for auto-discovery
UNIT_MODULE = FuelConsumptionUnitModule()