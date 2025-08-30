"""
MagneticFlux Units Module
=========================

Complete magnetic flux unit definitions and constants.
"""

from ..dimension import MAGNETIC_FLUX
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MagneticFluxUnits:
    """Type-safe magnetic flux unit constants."""
    # Explicit declarations for type checking
    kapp_line: 'UnitConstant'
    line: 'UnitConstant'
    maxwell: 'UnitConstant'
    unit_pole: 'UnitConstant'
    weber: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MagneticFluxUnitModule(UnitModule):
    """MagneticFlux unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all magnetic flux unit definitions."""
        return [
            UnitDefinition("kapp_line", "-", MAGNETIC_FLUX, 6.00e-05),
            UnitDefinition("line", "line", MAGNETIC_FLUX, 1.00e-08),
            UnitDefinition("maxwell", "Mx", MAGNETIC_FLUX, 1.00e-08),
            UnitDefinition("unit_pole", "unit pole", MAGNETIC_FLUX, 1.2566e-07),
            UnitDefinition("weber", "Wb", MAGNETIC_FLUX, 1),

        ]
    
    def get_units_class(self):
        return MagneticFluxUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MagneticFluxUnitModule()