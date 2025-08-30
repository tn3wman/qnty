"""
VolumetricFlux Units Module
===========================

Complete volumetric flux unit definitions and constants.
"""

from ..dimension import VOLUMETRIC_FLUX
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumetricFluxUnits:
    """Type-safe volumetric flux unit constants."""
    # Explicit declarations for type checking
    cubic_feet_per_square_foot_per_day: 'UnitConstant'
    cubic_feet_per_square_foot_per_hour: 'UnitConstant'
    cubic_feet_per_square_foot_per_minute: 'UnitConstant'
    cubic_feet_per_square_foot_per_second: 'UnitConstant'
    cubic_meters_per_square_meter_per_day: 'UnitConstant'
    cubic_meters_per_square_meter_per_hour: 'UnitConstant'
    cubic_meters_per_square_meter_per_minute: 'UnitConstant'
    cubic_meters_per_square_meter_per_second: 'UnitConstant'
    gallons_per_square_foot_per_day: 'UnitConstant'
    gallons_per_square_foot_per_hour: 'UnitConstant'
    gallons_per_square_foot_per_minute: 'UnitConstant'
    gallons_per_square_foot_per_second: 'UnitConstant'
    liters_per_square_meter_per_day: 'UnitConstant'
    liters_per_square_meter_per_hour: 'UnitConstant'
    liters_per_square_meter_per_minute: 'UnitConstant'
    liters_per_square_meter_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumetricFluxUnitModule(UnitModule):
    """VolumetricFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volumetric flux unit definitions."""
        return [
            UnitDefinition("cubic_feet_per_square_foot_per_day", "ft3 /left(ft2 ~dright) or cft / sqft / da", VOLUMETRIC_FLUX, 3.5276e-06),
            UnitDefinition("cubic_feet_per_square_foot_per_hour", "ft3 /left(ft2 ~hright) or cft / sqft / hr", VOLUMETRIC_FLUX, 8.4663e-05),
            UnitDefinition("cubic_feet_per_square_foot_per_minute", "ft3 /left(ft2 min right) or cft / sqft/min", VOLUMETRIC_FLUX, 0.0050798),
            UnitDefinition("cubic_feet_per_square_foot_per_second", "ft3 /left(ft2 ~sright) or cft/sqft/ sec", VOLUMETRIC_FLUX, 0.30479),
            UnitDefinition("cubic_meters_per_square_meter_per_day", "m3 /left(m2 ~dright)", VOLUMETRIC_FLUX, 1.1574e-05),
            UnitDefinition("cubic_meters_per_square_meter_per_hour", "m3 /left(m2 ~hright)", VOLUMETRIC_FLUX, 0.00027778),
            UnitDefinition("cubic_meters_per_square_meter_per_minute", "m3 /left(m2 ~minright)", VOLUMETRIC_FLUX, 0.016667),
            UnitDefinition("cubic_meters_per_square_meter_per_second", "m3 /left(m2 ~sright)", VOLUMETRIC_FLUX, 1),
            UnitDefinition("gallons_per_square_foot_per_day", "gal /left(ft2 ~dright) or gal/ sqft/da", VOLUMETRIC_FLUX, 4.7138e-04),
            UnitDefinition("gallons_per_square_foot_per_hour", "gal /left(ft2 ~hright) or gal/ sqft/hr", VOLUMETRIC_FLUX, 0.011313),
            UnitDefinition("gallons_per_square_foot_per_minute", "gal /left(ft2 ~minright) or gal/ sqft/min or gpm/sqft", VOLUMETRIC_FLUX, 0.67878),
            UnitDefinition("gallons_per_square_foot_per_second", "gal /left(ft2 ~sright) or gal/ sqft / sec", VOLUMETRIC_FLUX, 40.727),
            UnitDefinition("liters_per_square_meter_per_day", "1 /left(m2 ~dright)", VOLUMETRIC_FLUX, 1.1574e-05),
            UnitDefinition("liters_per_square_meter_per_hour", "1 /left(m2 ~hright)", VOLUMETRIC_FLUX, 0.00027778),
            UnitDefinition("liters_per_square_meter_per_minute", "1 /left(m2 ~minright)", VOLUMETRIC_FLUX, 0.016667),
            UnitDefinition("liters_per_square_meter_per_second", "1 /left(m2 ~sright)", VOLUMETRIC_FLUX, 1),

        ]
    
    def get_units_class(self):
        return VolumetricFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumetricFluxUnitModule()