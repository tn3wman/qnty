"""
ElectricalConductance Units Module
==================================

Complete electrical conductance unit definitions and constants.
"""

from ..dimension import ELECTRICAL_CONDUCTANCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricalConductanceUnits:
    """Type-safe electrical conductance unit constants."""
    # Explicit declarations for type checking
    emu_cgs: 'UnitConstant'
    esu_cgs: 'UnitConstant'
    mho: 'UnitConstant'
    microsiemens: 'UnitConstant'
    siemens: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricalConductanceUnitModule(UnitModule):
    """ElectricalConductance unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electrical conductance unit definitions."""
        return [
            UnitDefinition("emu_cgs", "abmho", ELECTRICAL_CONDUCTANCE, 1.00e+09),
            UnitDefinition("esu_cgs", "statmho", ELECTRICAL_CONDUCTANCE, 1.1127e-12),
            UnitDefinition("mho", "mho", ELECTRICAL_CONDUCTANCE, 1),
            UnitDefinition("microsiemens", "mu S", ELECTRICAL_CONDUCTANCE, 1.00e-06),
            UnitDefinition("siemens", "S", ELECTRICAL_CONDUCTANCE, 1),

        ]
    
    def get_units_class(self):
        return ElectricalConductanceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricalConductanceUnitModule()