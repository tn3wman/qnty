"""
RadiationDoseEquivalent Units Module
====================================

Complete radiation dose equivalent unit definitions and constants.
"""

from ..dimension import ABSORBED_DOSE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class RadiationDoseEquivalentUnits:
    """Type-safe radiation dose equivalent unit constants."""
    # Explicit declarations for type checking
    rem: 'UnitConstant'
    sievert: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class RadiationDoseEquivalentUnitModule(UnitModule):
    """RadiationDoseEquivalent unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all radiation dose equivalent unit definitions."""
        return [
            UnitDefinition("rem", "rem", ABSORBED_DOSE, 0.01),
            UnitDefinition("sievert", "Sv", ABSORBED_DOSE, 1),

        ]
    
    def get_units_class(self):
        return RadiationDoseEquivalentUnits
    


# Register this module for auto-discovery
UNIT_MODULE = RadiationDoseEquivalentUnitModule()