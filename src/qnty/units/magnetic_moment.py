"""
MagneticMoment Units Module
===========================

Complete magnetic moment unit definitions and constants.
"""

from ..dimension import MAGNETIC_MOMENT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MagneticMomentUnits:
    """Type-safe magnetic moment unit constants."""
    # Explicit declarations for type checking
    bohr_magneton: 'UnitConstant'
    joule_per_tesla: 'UnitConstant'
    nuclear_magneton: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MagneticMomentUnitModule(UnitModule):
    """MagneticMoment unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all magnetic moment unit definitions."""
        return [
            UnitDefinition("bohr_magneton", "Bohr magneton", MAGNETIC_MOMENT, 9.2740e-24),
            UnitDefinition("joule_per_tesla", "J/T", MAGNETIC_MOMENT, 1),
            UnitDefinition("nuclear_magneton", "nucl. Magneton", MAGNETIC_MOMENT, 5.0508e-27),

        ]
    
    def get_units_class(self):
        return MagneticMomentUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MagneticMomentUnitModule()