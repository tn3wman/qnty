"""
Forcebody Units Module
======================

Complete force (body) unit definitions and constants.
"""

from ..dimension import FORCE_BODY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ForcebodyUnits:
    """Type-safe force (body) unit constants."""
    # Explicit declarations for type checking
    dyne_per_cubic_centimeter: 'UnitConstant'
    kilogram_force_per_cubic_centimeter: 'UnitConstant'
    kilogram_force_per_cubic_meter: 'UnitConstant'
    newton_per_cubic_meter: 'UnitConstant'
    pound_force_per_cubic_foot: 'UnitConstant'
    pound_force_per_cubic_inch: 'UnitConstant'
    ton_force_per_cubic_foot: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ForcebodyUnitModule(UnitModule):
    """Forcebody unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all force (body) unit definitions."""
        return [
            UnitDefinition("dyne_per_cubic_centimeter", "dyn/cc or dyn/ cm3", FORCE_BODY, 10),
            UnitDefinition("kilogram_force_per_cubic_centimeter", "kgf / cm3", FORCE_BODY, 9.8067e+06),
            UnitDefinition("kilogram_force_per_cubic_meter", "kgf / m3", FORCE_BODY, 9.80665),
            UnitDefinition("newton_per_cubic_meter", "N / m3", FORCE_BODY, 1),
            UnitDefinition("pound_force_per_cubic_foot", "lbf / cft", FORCE_BODY, 157.087),
            UnitDefinition("pound_force_per_cubic_inch", "lbf / cu . in.", FORCE_BODY, 2.7145e+05),
            UnitDefinition("ton_force_per_cubic_foot", "ton f / cft", FORCE_BODY, 3.5188e+05),

        ]
    
    def get_units_class(self):
        return ForcebodyUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ForcebodyUnitModule()