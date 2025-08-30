"""
SpecificLength Units Module
===========================

Complete specific length unit definitions and constants.
"""

from ..dimension import SPECIFIC_LENGTH
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SpecificLengthUnits:
    """Type-safe specific length unit constants."""
    # Explicit declarations for type checking
    centimeter_per_gram: 'UnitConstant'
    cotton_count: 'UnitConstant'
    ft_per_pound: 'UnitConstant'
    meters_per_kilogram: 'UnitConstant'
    newton_meter: 'UnitConstant'
    worsted: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SpecificLengthUnitModule(UnitModule):
    """SpecificLength unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all specific length unit definitions."""
        return [
            UnitDefinition("centimeter_per_gram", "cm/g", SPECIFIC_LENGTH, 10),
            UnitDefinition("cotton_count", "cc", SPECIFIC_LENGTH, 5.905e+08),
            UnitDefinition("ft_per_pound", "ft/lb", SPECIFIC_LENGTH, 0.67192),
            UnitDefinition("meters_per_kilogram", "m/kg", SPECIFIC_LENGTH, 1),
            UnitDefinition("newton_meter", "Nm", SPECIFIC_LENGTH, 1000),
            UnitDefinition("worsted", "worsted", SPECIFIC_LENGTH, 8.8868e+08),

        ]
    
    def get_units_class(self):
        return SpecificLengthUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SpecificLengthUnitModule()