"""
MolarFlowRate Units Module
==========================

Complete molar flow rate unit definitions and constants.
"""

from ..dimension import MOLAR_FLOW_RATE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MolarFlowRateUnits:
    """Type-safe molar flow rate unit constants."""
    # Explicit declarations for type checking
    gram_mole_per_day: 'UnitConstant'
    gram_mole_per_hour: 'UnitConstant'
    gram_mole_per_minute: 'UnitConstant'
    gram_mole_per_second: 'UnitConstant'
    kilogram_mole: 'UnitConstant'
    kilogram_mole: 'UnitConstant'
    kilogram_mole: 'UnitConstant'
    kilogram_mole: 'UnitConstant'
    pound_mole: 'UnitConstant'
    pound_mole: 'UnitConstant'
    pound_mole: 'UnitConstant'
    pound_mole: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MolarFlowRateUnitModule(UnitModule):
    """MolarFlowRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all molar flow rate unit definitions."""
        return [
            UnitDefinition("gram_mole_per_day", "mol/d", MOLAR_FLOW_RATE, 4.167e-05),
            UnitDefinition("gram_mole_per_hour", "mol/h", MOLAR_FLOW_RATE, 0.001),
            UnitDefinition("gram_mole_per_minute", "mol/min", MOLAR_FLOW_RATE, 0.06),
            UnitDefinition("gram_mole_per_second", "mol/s", MOLAR_FLOW_RATE, 3.6),
            UnitDefinition("kilogram_mole", "kmol/d", MOLAR_FLOW_RATE, 0.04167),
            UnitDefinition("kilogram_mole", "kmol/h", MOLAR_FLOW_RATE, 1),
            UnitDefinition("kilogram_mole", "kmol/min", MOLAR_FLOW_RATE, 60),
            UnitDefinition("kilogram_mole", "kmol/s", MOLAR_FLOW_RATE, 3600),
            UnitDefinition("pound_mole", "lb-mol/d or mole/da", MOLAR_FLOW_RATE, 0.01890),
            UnitDefinition("pound_mole", "lb-mol/h or mole/hr", MOLAR_FLOW_RATE, 0.4535),
            UnitDefinition("pound_mole", "lb-mol/min or mole/ min", MOLAR_FLOW_RATE, 27.21),
            UnitDefinition("pound_mole", "lb-mol / s or mole/sec", MOLAR_FLOW_RATE, 1633),

        ]
    
    def get_units_class(self):
        return MolarFlowRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MolarFlowRateUnitModule()