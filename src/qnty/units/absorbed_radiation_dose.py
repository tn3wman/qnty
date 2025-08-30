"""
AbsorbedDose Units Module
=========================

Complete absorbed radiation dose unit definitions and constants.
"""

from ..dimension import ABSORBED_DOSE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AbsorbedDoseUnits:
    """Type-safe absorbed radiation dose unit constants."""
    # Explicit declarations for type checking
    erg_per_gram: 'UnitConstant'
    gramrad: 'UnitConstant'
    gray: 'UnitConstant'
    rad: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class AbsorbedDoseUnitModule(UnitModule):
    """AbsorbedDose unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all absorbed radiation dose unit definitions."""
        return [
            UnitDefinition("erg_per_gram", "erg/g", ABSORBED_DOSE, 0.0001),
            UnitDefinition("gramrad", "g-rad", ABSORBED_DOSE, 0.01),
            UnitDefinition("gray", "Gy", ABSORBED_DOSE, 1),
            UnitDefinition("rad", "rad", ABSORBED_DOSE, 0.01),

        ]
    
    def get_units_class(self):
        return AbsorbedDoseUnits
    


# Register this module for auto-discovery
UNIT_MODULE = AbsorbedDoseUnitModule()