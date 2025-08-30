"""
SecondRadiationConstantplanck Units Module
==========================================

Complete second radiation constant (planck) unit definitions and constants.
"""

from ..dimension import SECOND_RADIATION_CONSTANT_PLANCK
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SecondRadiationConstantplanckUnits:
    """Type-safe second radiation constant (planck) unit constants."""
    # Explicit declarations for type checking
    kelvin: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SecondRadiationConstantplanckUnitModule(UnitModule):
    """SecondRadiationConstantplanck unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all second radiation constant (planck) unit definitions."""
        return [
            UnitDefinition("kelvin", "K", SECOND_RADIATION_CONSTANT_PLANCK, 1),

        ]
    
    def get_units_class(self):
        return SecondRadiationConstantplanckUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SecondRadiationConstantplanckUnitModule()