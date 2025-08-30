"""
ElectricFieldStrength Units Module
==================================

Complete electric field strength unit definitions and constants.
"""

from ..dimension import ELECTRIC_FIELD
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricFieldStrengthUnits:
    """Type-safe electric field strength unit constants."""
    # Explicit declarations for type checking
    volt_per_centimeter: 'UnitConstant'
    volt_per_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricFieldStrengthUnitModule(UnitModule):
    """ElectricFieldStrength unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric field strength unit definitions."""
        return [
            UnitDefinition("volt_per_centimeter", "V/cm", ELECTRIC_FIELD, 100),
            UnitDefinition("volt_per_meter", "V/m", ELECTRIC_FIELD, 1),

        ]
    
    def get_units_class(self):
        return ElectricFieldStrengthUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricFieldStrengthUnitModule()