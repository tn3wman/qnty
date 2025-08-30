"""
ElectricDipoleMoment Units Module
=================================

Complete electric dipole moment unit definitions and constants.
"""

from ..dimension import ELECTRIC_DIPOLE_MOMENT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricDipoleMomentUnits:
    """Type-safe electric dipole moment unit constants."""
    # Explicit declarations for type checking
    ampere_meter_second: 'UnitConstant'
    coulomb_meter: 'UnitConstant'
    debye: 'UnitConstant'
    electron_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricDipoleMomentUnitModule(UnitModule):
    """ElectricDipoleMoment unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric dipole moment unit definitions."""
        return [
            UnitDefinition("ampere_meter_second", "A m s", ELECTRIC_DIPOLE_MOMENT, 1),
            UnitDefinition("coulomb_meter", "C m", ELECTRIC_DIPOLE_MOMENT, 1),
            UnitDefinition("debye", "D", ELECTRIC_DIPOLE_MOMENT, 3.3356e-30),
            UnitDefinition("electron_meter", "e m", ELECTRIC_DIPOLE_MOMENT, 1.6022e-19),

        ]
    
    def get_units_class(self):
        return ElectricDipoleMomentUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricDipoleMomentUnitModule()