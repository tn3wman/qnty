"""
VolumetricCoefficientOfExpansion Units Module
=============================================

Complete volumetric coefficient of expansion unit definitions and constants.
"""

from ..dimension import VOLUMETRIC_COEFFICIENT_OF_EXPANSION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class VolumetricCoefficientOfExpansionUnits:
    """Type-safe volumetric coefficient of expansion unit constants."""
    # Explicit declarations for type checking
    celsius: 'UnitConstant'
    celsius: 'UnitConstant'
    fahrenheit: 'UnitConstant'
    celsius: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class VolumetricCoefficientOfExpansionUnitModule(UnitModule):
    """VolumetricCoefficientOfExpansion unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all volumetric coefficient of expansion unit definitions."""
        return [
            UnitDefinition("celsius", "°C", VOLUMETRIC_COEFFICIENT_OF_EXPANSION, 1000),
            UnitDefinition("celsius", "°C", VOLUMETRIC_COEFFICIENT_OF_EXPANSION, 1),
            UnitDefinition("fahrenheit", "°F", VOLUMETRIC_COEFFICIENT_OF_EXPANSION, 28.833),
            UnitDefinition("celsius", "°C", VOLUMETRIC_COEFFICIENT_OF_EXPANSION, 16.018),

        ]
    
    def get_units_class(self):
        return VolumetricCoefficientOfExpansionUnits
    


# Register this module for auto-discovery
UNIT_MODULE = VolumetricCoefficientOfExpansionUnitModule()