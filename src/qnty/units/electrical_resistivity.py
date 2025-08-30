"""
ElectricalResistivity Units Module
==================================

Complete electrical resistivity unit definitions and constants.
"""

from ..dimension import ELECTRICAL_RESISTIVITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricalResistivityUnits:
    """Type-safe electrical resistivity unit constants."""
    # Explicit declarations for type checking
    circular_milohm_per_foot: 'UnitConstant'
    emu_cgs: 'UnitConstant'
    microhminch: 'UnitConstant'
    ohmcentimeter: 'UnitConstant'
    ohmmeter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricalResistivityUnitModule(UnitModule):
    """ElectricalResistivity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electrical resistivity unit definitions."""
        return [
            UnitDefinition("circular_milohm_per_foot", "°mil Omega / ft", ELECTRICAL_RESISTIVITY, 1.6624e-09),
            UnitDefinition("emu_cgs", "abohm cm", ELECTRICAL_RESISTIVITY, 1.00e-11),
            UnitDefinition("microhminch", "mu Omega in", ELECTRICAL_RESISTIVITY, 2.5400e-08),
            UnitDefinition("ohmcentimeter", "boldsymbolOmega mathbfc m", ELECTRICAL_RESISTIVITY, 0.01),
            UnitDefinition("ohmmeter", "Omega m", ELECTRICAL_RESISTIVITY, 1),

        ]
    
    def get_units_class(self):
        return ElectricalResistivityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricalResistivityUnitModule()