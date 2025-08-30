"""
HeatTransferCoefficient Units Module
====================================

Complete heat transfer coefficient unit definitions and constants.
"""

from ..dimension import HEAT_TRANSFER_COEFFICIENT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class HeatTransferCoefficientUnits:
    """Type-safe heat transfer coefficient unit constants."""
    # Explicit declarations for type checking
    fahrenheit: 'UnitConstant'
    celsius: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class HeatTransferCoefficientUnitModule(UnitModule):
    """HeatTransferCoefficient unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all heat transfer coefficient unit definitions."""
        return [
            UnitDefinition("fahrenheit", "°F", HEAT_TRANSFER_COEFFICIENT, 5.679),
            UnitDefinition("celsius", "°C", HEAT_TRANSFER_COEFFICIENT, 1),

        ]
    
    def get_units_class(self):
        return HeatTransferCoefficientUnits
    


# Register this module for auto-discovery
UNIT_MODULE = HeatTransferCoefficientUnitModule()