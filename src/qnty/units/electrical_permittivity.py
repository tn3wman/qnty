"""
ElectricalPermittivity Units Module
===================================

Complete electrical permittivity unit definitions and constants.
"""

from ..dimension import ELECTRICAL_PERMITTIVITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricalPermittivityUnits:
    """Type-safe electrical permittivity unit constants."""
    # Explicit declarations for type checking
    farad_per_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricalPermittivityUnitModule(UnitModule):
    """ElectricalPermittivity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electrical permittivity unit definitions."""
        return [
            UnitDefinition("farad_per_meter", "F/m", ELECTRICAL_PERMITTIVITY, 1),

        ]
    
    def get_units_class(self):
        return ElectricalPermittivityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricalPermittivityUnitModule()