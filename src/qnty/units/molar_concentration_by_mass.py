"""
MolarConcentrationByMass Units Module
=====================================

Complete molar concentration by mass unit definitions and constants.
"""

from ..dimension import AMOUNT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MolarConcentrationByMassUnits:
    """Type-safe molar concentration by mass unit constants."""
    # Explicit declarations for type checking
    gram_mole: 'UnitConstant'
    gram_mole: 'UnitConstant'
    kilogram_mole: 'UnitConstant'
    micromole_per_gram: 'UnitConstant'
    millimole_per_gram: 'UnitConstant'
    picomole_per_gram: 'UnitConstant'
    pound_mole_per_pound: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MolarConcentrationByMassUnitModule(UnitModule):
    """MolarConcentrationByMass unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all molar concentration by mass unit definitions."""
        return [
            UnitDefinition("gram_mole", "mol/g", AMOUNT, 1),
            UnitDefinition("gram_mole", "mol/kg", AMOUNT, 0.001),
            UnitDefinition("kilogram_mole", "kmol/kg", AMOUNT, 1),
            UnitDefinition("micromole_per_gram", "mu mol / g", AMOUNT, 1.00e-06),
            UnitDefinition("millimole_per_gram", "mmol/g", AMOUNT, 0.001),
            UnitDefinition("picomole_per_gram", "pmol/g", AMOUNT, 1.00e-12),
            UnitDefinition("pound_mole_per_pound", "lb-mol / lb or mole/lb", AMOUNT, 1),

        ]
    
    def get_units_class(self):
        return MolarConcentrationByMassUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MolarConcentrationByMassUnitModule()