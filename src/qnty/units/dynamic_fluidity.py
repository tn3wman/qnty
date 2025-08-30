"""
DynamicFluidity Units Module
============================

Complete dynamic fluidity unit definitions and constants.
"""

from ..dimension import DYNAMIC_FLUIDITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class DynamicFluidityUnits:
    """Type-safe dynamic fluidity unit constants."""
    # Explicit declarations for type checking
    rhe: 'UnitConstant'
    square_foot_per_pound_second: 'UnitConstant'
    square_meters_per_newton_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class DynamicFluidityUnitModule(UnitModule):
    """DynamicFluidity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all dynamic fluidity unit definitions."""
        return [
            UnitDefinition("rhe", "rhe", DYNAMIC_FLUIDITY, 1),
            UnitDefinition("square_foot_per_pound_second", "ft2 /(lb sec)", DYNAMIC_FLUIDITY, 0.002086),
            UnitDefinition("square_meters_per_newton_per_second", "m2 /(N s)", DYNAMIC_FLUIDITY, 1),

        ]
    
    def get_units_class(self):
        return DynamicFluidityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = DynamicFluidityUnitModule()