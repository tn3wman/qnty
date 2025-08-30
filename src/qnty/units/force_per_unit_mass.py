"""
ForcePerUnitMass Units Module
=============================

Complete force per unit mass unit definitions and constants.
"""

from ..dimension import ACCELERATION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ForcePerUnitMassUnits:
    """Type-safe force per unit mass unit constants."""
    # Explicit declarations for type checking
    dyne_per_gram: 'UnitConstant'
    kilogram_force_per_kilogram: 'UnitConstant'
    newton_per_kilogram: 'UnitConstant'
    pound_force_per_pound_mass: 'UnitConstant'
    pound_force_per_slug: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ForcePerUnitMassUnitModule(UnitModule):
    """ForcePerUnitMass unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all force per unit mass unit definitions."""
        return [
            UnitDefinition("dyne_per_gram", "dyn/g", ACCELERATION, 0.01),
            UnitDefinition("kilogram_force_per_kilogram", "kgf / kg", ACCELERATION, 9.80665),
            UnitDefinition("newton_per_kilogram", "N/kg", ACCELERATION, 1),
            UnitDefinition("pound_force_per_pound_mass", "lbf / lb or lbf / lbm", ACCELERATION, 9.80665),
            UnitDefinition("pound_force_per_slug", "lbf / slug", ACCELERATION, 0.3048),

        ]
    
    def get_units_class(self):
        return ForcePerUnitMassUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ForcePerUnitMassUnitModule()