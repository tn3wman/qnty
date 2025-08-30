"""
MassFlowRate Units Module
=========================

Complete mass flow rate unit definitions and constants.
"""

from ..dimension import MASS_FLOW_RATE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MassFlowRateUnits:
    """Type-safe mass flow rate unit constants."""
    # Explicit declarations for type checking
    kilograms_per_day: 'UnitConstant'
    kilograms_per_hour: 'UnitConstant'
    kilograms_per_minute: 'UnitConstant'
    kilograms_per_second: 'UnitConstant'
    metric_tons_per_day: 'UnitConstant'
    metric_tons_per_hour: 'UnitConstant'
    metric_tons_per_minute: 'UnitConstant'
    metric_tons_per_second: 'UnitConstant'
    metric_tons_per_year_365_d: 'UnitConstant'
    pounds_per_day: 'UnitConstant'
    pounds_per_hour: 'UnitConstant'
    pounds_per_minute: 'UnitConstant'
    pounds_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MassFlowRateUnitModule(UnitModule):
    """MassFlowRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mass flow rate unit definitions."""
        return [
            UnitDefinition("kilograms_per_day", "kg/d", MASS_FLOW_RATE, 1.1574e-05),
            UnitDefinition("kilograms_per_hour", "kg/h", MASS_FLOW_RATE, 0.00027778),
            UnitDefinition("kilograms_per_minute", "kg/min", MASS_FLOW_RATE, 0.016667),
            UnitDefinition("kilograms_per_second", "kg/s", MASS_FLOW_RATE, 1),
            UnitDefinition("metric_tons_per_day", "MT/d or MTD", MASS_FLOW_RATE, 0.01157),
            UnitDefinition("metric_tons_per_hour", "MT/h or MTD", MASS_FLOW_RATE, 0.2778),
            UnitDefinition("metric_tons_per_minute", "MT/h", MASS_FLOW_RATE, 16.67),
            UnitDefinition("metric_tons_per_second", "MT/s", MASS_FLOW_RATE, 1000),
            UnitDefinition("metric_tons_per_year_365_d", "MT/yr or MTY", MASS_FLOW_RATE, 3.171e-05),
            UnitDefinition("pounds_per_day", "lb / d or lb / da or PPD", MASS_FLOW_RATE, 5.2490e-06),
            UnitDefinition("pounds_per_hour", "lb / h or lb/hr or PPH", MASS_FLOW_RATE, 1.2598e-04),
            UnitDefinition("pounds_per_minute", "lb / min or PPM", MASS_FLOW_RATE, 0.0075586),
            UnitDefinition("pounds_per_second", "lb / s or lb/sec or PPS", MASS_FLOW_RATE, 0.45351),

        ]
    
    def get_units_class(self):
        return MassFlowRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MassFlowRateUnitModule()