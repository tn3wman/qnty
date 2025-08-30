"""
ActivationEnergy Units Module
=============================

Complete activation energy unit definitions and constants.
"""

from ..dimension import ACTIVATION_ENERGY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ActivationEnergyUnits:
    """Type-safe activation energy unit constants."""
    # Explicit declarations for type checking
    btu_per_pound_mole: 'UnitConstant'
    calorie_mean_per_gram_mole: 'UnitConstant'
    joule_per_gram_mole: 'UnitConstant'
    joule_per_kilogram_mole: 'UnitConstant'
    kilocalorie_per_kilogram_mole: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ActivationEnergyUnitModule(UnitModule):
    """ActivationEnergy unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all activation energy unit definitions."""
        return [
            UnitDefinition("btu_per_pound_mole", "Btu/lb-mol", ACTIVATION_ENERGY, 2326),
            UnitDefinition("calorie_mean_per_gram_mole", "cal/mol", ACTIVATION_ENERGY, 4.18675),
            UnitDefinition("joule_per_gram_mole", "J/mol", ACTIVATION_ENERGY, 1),
            UnitDefinition("joule_per_kilogram_mole", "J/kmol", ACTIVATION_ENERGY, 1000),
            UnitDefinition("kilocalorie_per_kilogram_mole", "kcal/kmol", ACTIVATION_ENERGY, 4.18675),

        ]
    
    def get_units_class(self):
        return ActivationEnergyUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ActivationEnergyUnitModule()