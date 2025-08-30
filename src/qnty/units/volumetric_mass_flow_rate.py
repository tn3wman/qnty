"""
VolumetricMassFlowRate Units Module
===================================

Complete volumetric mass flow rate unit definitions and constants.
"""

from ..dimension import VOLUMETRIC_MASS_FLOW_RATE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumetricMassFlowRateUnits:
    """Type-safe volumetric mass flow rate unit constants."""
    # Explicit declarations for type checking
    gram_per_second_per_cubic_centimeter: 'UnitConstant'
    kilogram_per_hour_per_cubic_foot: 'UnitConstant'
    kilogram_per_hour_per_cubic_meter: 'UnitConstant'
    kilogram_per_second_per_cubic_meter: 'UnitConstant'
    pound_per_hour_per_cubic_foot: 'UnitConstant'
    pound_per_minute_per_cubic_foot: 'UnitConstant'
    pound_per_second_per_cubic_foot: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumetricMassFlowRateUnitModule(UnitModule):
    """VolumetricMassFlowRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volumetric mass flow rate unit definitions."""
        return [
            UnitDefinition("gram_per_second_per_cubic_centimeter", "g /left(s cm3right) or g/s/cc or g / cc / sec", VOLUMETRIC_MASS_FLOW_RATE, 1000),
            UnitDefinition("kilogram_per_hour_per_cubic_foot", "kg/(h ft  3 ) or kg/hr/ cft", VOLUMETRIC_MASS_FLOW_RATE, 0.0098096),
            UnitDefinition("kilogram_per_hour_per_cubic_meter", "kg/(h m3) or kg/hr/ cu.m", VOLUMETRIC_MASS_FLOW_RATE, 2.7778e-04),
            UnitDefinition("kilogram_per_second_per_cubic_meter", "kg /left(s m3right) or kg/sec/ cu.m", VOLUMETRIC_MASS_FLOW_RATE, 1),
            UnitDefinition("pound_per_hour_per_cubic_foot", "lb /left(h ft3right) or lb / hr / cft or PPH/cft", VOLUMETRIC_MASS_FLOW_RATE, 0.0044496),
            UnitDefinition("pound_per_minute_per_cubic_foot", "lb/(min ft3 ) or lb/ min / cft", VOLUMETRIC_MASS_FLOW_RATE, 0.26697),
            UnitDefinition("pound_per_second_per_cubic_foot", "b/(s ft  3 ) or lb/sec/cft", VOLUMETRIC_MASS_FLOW_RATE, 16.018),

        ]
    
    def get_units_class(self):
        return VolumetricMassFlowRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumetricMassFlowRateUnitModule()