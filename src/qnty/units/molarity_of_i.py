"""
MolarityOfI Units Module
========================

Complete molarity of "i" unit definitions and constants.
"""

from ..dimension import MOLARITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MolarityOfIUnits:
    """Type-safe molarity of "i" unit constants."""
    # Explicit declarations for type checking
    gram_moles_of_i_per_cubic_meter: 'UnitConstant'
    gram_moles_of_i_per_liter: 'UnitConstant'
    kilogram_moles_of_i_per_cubic_meter: 'UnitConstant'
    kilogram_moles_of_i_per_liter: 'UnitConstant'
    pound_moles_of_i_per_cubic_foot: 'UnitConstant'
    pound_moles_of_per_gallon_us: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MolarityOfIUnitModule(UnitModule):
    """MolarityOfI unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all molarity of "i" unit definitions."""
        return [
            UnitDefinition("gram_moles_of_i_per_cubic_meter", "moli / m3 or ci", MOLARITY, 1),
            UnitDefinition("gram_moles_of_i_per_liter", "moli / l", MOLARITY, 1000),
            UnitDefinition("kilogram_moles_of_i_per_cubic_meter", "kmoli / m3", MOLARITY, 1000),
            UnitDefinition("kilogram_moles_of_i_per_liter", "kmoli / l", MOLARITY, 1000000),
            UnitDefinition("pound_moles_of_i_per_cubic_foot", "lb moli / ft3 or molei / cft", MOLARITY, 77844),
            UnitDefinition("pound_moles_of_per_gallon_us", "lb moli / gal or molei / gal", MOLARITY, 10406),

        ]
    
    def get_units_class(self):
        return MolarityOfIUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MolarityOfIUnitModule()