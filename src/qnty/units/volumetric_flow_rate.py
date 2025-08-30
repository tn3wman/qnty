"""
VolumetricFlowRate Units Module
===============================

Complete volumetric flow rate unit definitions and constants.
"""

from ..dimension import VOLUMETRIC_FLOW_RATE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumetricFlowRateUnits:
    """Type-safe volumetric flow rate unit constants."""
    # Explicit declarations for type checking
    cubic_feet_per_day: 'UnitConstant'
    cubic_feet_per_hour: 'UnitConstant'
    cubic_feet_per_minute: 'UnitConstant'
    cubic_feet_per_second: 'UnitConstant'
    cubic_meters_per_day: 'UnitConstant'
    cubic_meters_per_hour: 'UnitConstant'
    cubic_meters_per_minute: 'UnitConstant'
    cubic_meters_per_second: 'UnitConstant'
    gallons_per_day: 'UnitConstant'
    gallons_per_hour: 'UnitConstant'
    gallons_per_minute: 'UnitConstant'
    gallons_per_second: 'UnitConstant'
    liters_per_day: 'UnitConstant'
    liters_per_hour: 'UnitConstant'
    liters_per_minute: 'UnitConstant'
    liters_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumetricFlowRateUnitModule(UnitModule):
    """VolumetricFlowRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volumetric flow rate unit definitions."""
        return [
            UnitDefinition("cubic_feet_per_day", "ft3 / d or cft / da or cfd", VOLUMETRIC_FLOW_RATE, 3.2778e-07),
            UnitDefinition("cubic_feet_per_hour", "ft3 / h or cft / hr or cfh", VOLUMETRIC_FLOW_RATE, 7.8667e-06),
            UnitDefinition("cubic_feet_per_minute", "ft3 / min or cft / min or cfm", VOLUMETRIC_FLOW_RATE, 0.0004720),
            UnitDefinition("cubic_feet_per_second", "ft3 / s or cft/sec or cfs", VOLUMETRIC_FLOW_RATE, 0.02832),
            UnitDefinition("cubic_meters_per_day", "m3 / d", VOLUMETRIC_FLOW_RATE, 1.1574e-05),
            UnitDefinition("cubic_meters_per_hour", "m3 / h", VOLUMETRIC_FLOW_RATE, 0.00027778),
            UnitDefinition("cubic_meters_per_minute", "m3 / min", VOLUMETRIC_FLOW_RATE, 0.016667),
            UnitDefinition("cubic_meters_per_second", "m3 / s", VOLUMETRIC_FLOW_RATE, 1),
            UnitDefinition("gallons_per_day", "gal/d or gpd or gal/ da", VOLUMETRIC_FLOW_RATE, 0.002628),
            UnitDefinition("gallons_per_hour", "gal/h or gph or gal/ hr", VOLUMETRIC_FLOW_RATE, 0.06308),
            UnitDefinition("gallons_per_minute", "gal/min or gpm", VOLUMETRIC_FLOW_RATE, 3.785),
            UnitDefinition("gallons_per_second", "gal/s or gps or gal/ sec", VOLUMETRIC_FLOW_RATE, 227.1),
            UnitDefinition("liters_per_day", "1/d", VOLUMETRIC_FLOW_RATE, 0.00069444),
            UnitDefinition("liters_per_hour", "1/h", VOLUMETRIC_FLOW_RATE, 0.016667),
            UnitDefinition("liters_per_minute", "1 / min", VOLUMETRIC_FLOW_RATE, 1),
            UnitDefinition("liters_per_second", "1/s", VOLUMETRIC_FLOW_RATE, 60),

        ]
    
    def get_units_class(self):
        return VolumetricFlowRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumetricFlowRateUnitModule()