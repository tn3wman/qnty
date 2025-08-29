"""
Absorbed Dose Units Module
==========================

Complete absorbed radiation dose unit definitions and constants.
"""

# No need to import List, use built-in list type

from ..dimension import ABSORBED_DOSE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class AbsorbedDoseUnits:
    """Type-safe absorbed dose unit constants."""
    # Explicit declarations for type checking
    gray: 'UnitConstant'
    rad: 'UnitConstant'
    erg_per_gram: 'UnitConstant'
    gram_rad: 'UnitConstant'
    
    # Common aliases
    Gy: 'UnitConstant'


class AbsorbedDoseUnitModule(UnitModule):
    """Absorbed dose unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all absorbed dose unit definitions."""
        return [
            UnitDefinition("gray", "Gy", ABSORBED_DOSE, 1.0),
            UnitDefinition("rad", "rad", ABSORBED_DOSE, 0.01),
            UnitDefinition("erg_per_gram", "erg/g", ABSORBED_DOSE, 0.0001),
            UnitDefinition("gram_rad", "g-rad", ABSORBED_DOSE, 0.01),
        ]
    
    def get_units_class(self):
        return AbsorbedDoseUnits


# Register this module for auto-discovery
UNIT_MODULE = AbsorbedDoseUnitModule()
