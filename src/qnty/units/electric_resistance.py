"""
ElectricResistance Units Module
===============================

Complete electric resistance unit definitions and constants.
"""

from ..dimension import ELECTRIC_RESISTANCE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ElectricResistanceUnits:
    """Type-safe electric resistance unit constants."""
    # Explicit declarations for type checking
    abohm: 'UnitConstant'
    jacobi: 'UnitConstant'
    lenz: 'UnitConstant'
    ohm: 'UnitConstant'
    ohm_intl_mean: 'UnitConstant'
    ohm_intl_us: 'UnitConstant'
    ohm_legal: 'UnitConstant'
    preece: 'UnitConstant'
    statohm: 'UnitConstant'
    wheatstone: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ElectricResistanceUnitModule(UnitModule):
    """ElectricResistance unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all electric resistance unit definitions."""
        return [
            UnitDefinition("abohm", "emu cgs", ELECTRIC_RESISTANCE, 1.00e-09),
            UnitDefinition("jacobi", "-", ELECTRIC_RESISTANCE, 0.64),
            UnitDefinition("lenz", "Metric", ELECTRIC_RESISTANCE, 8.00e+04),
            UnitDefinition("ohm", "Omega", ELECTRIC_RESISTANCE, 1),
            UnitDefinition("ohm_intl_mean", "Omega (int mean)", ELECTRIC_RESISTANCE, 1.00049),
            UnitDefinition("ohm_intl_us", "Omega (int US)", ELECTRIC_RESISTANCE, 1.000495),
            UnitDefinition("ohm_legal", "Omega (legal)", ELECTRIC_RESISTANCE, 0.9972),
            UnitDefinition("preece", "preece", ELECTRIC_RESISTANCE, 1.00e+06),
            UnitDefinition("statohm", "csu cgs", ELECTRIC_RESISTANCE, 8.987552),
            UnitDefinition("wheatstone", "-", ELECTRIC_RESISTANCE, 0.0025),

        ]
    
    def get_units_class(self):
        return ElectricResistanceUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ElectricResistanceUnitModule()