"""
PhotonEmissionRate Units Module
===============================

Complete photon emission rate unit definitions and constants.
"""

from ..dimension import PHOTON_EMISSION_RATE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class PhotonEmissionRateUnits:
    """Type-safe photon emission rate unit constants."""
    # Explicit declarations for type checking
    rayleigh: 'UnitConstant'
    reciprocal_square_meter_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class PhotonEmissionRateUnitModule(UnitModule):
    """PhotonEmissionRate unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all photon emission rate unit definitions."""
        return [
            UnitDefinition("rayleigh", "R", PHOTON_EMISSION_RATE, 1.00e+10),
            UnitDefinition("reciprocal_square_meter_second", "1 /left(m2 secright)", PHOTON_EMISSION_RATE, 1),

        ]
    
    def get_units_class(self):
        return PhotonEmissionRateUnits
    


# Register this module for auto-discovery
UNIT_MODULE = PhotonEmissionRateUnitModule()