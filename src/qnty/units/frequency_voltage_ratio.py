"""
FrequencyVoltageRatio Units Module
==================================

Complete frequency voltage ratio unit definitions and constants.
"""

from ..dimension import FREQUENCY_VOLTAGE_RATIO
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class FrequencyVoltageRatioUnits:
    """Type-safe frequency voltage ratio unit constants."""
    # Explicit declarations for type checking
    cycles_per_second_per_volt: 'UnitConstant'
    hertz_per_volt: 'UnitConstant'
    terahertz_per_volt: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class FrequencyVoltageRatioUnitModule(UnitModule):
    """FrequencyVoltageRatio unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all frequency voltage ratio unit definitions."""
        return [
            UnitDefinition("cycles_per_second_per_volt", "cycle/(sec V)", FREQUENCY_VOLTAGE_RATIO, 1),
            UnitDefinition("hertz_per_volt", "Hz/V", FREQUENCY_VOLTAGE_RATIO, 1),
            UnitDefinition("terahertz_per_volt", "THz/V", FREQUENCY_VOLTAGE_RATIO, 1.00e+12),

        ]
    
    def get_units_class(self):
        return FrequencyVoltageRatioUnits
    


# Register this module for auto-discovery
UNIT_MODULE = FrequencyVoltageRatioUnitModule()