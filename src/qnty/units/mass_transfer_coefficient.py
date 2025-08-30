"""
MassTransferCoefficient Units Module
====================================

Complete mass transfer coefficient unit definitions and constants.
"""

from ..dimension import MASS_TRANSFER_COEFFICIENT
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MassTransferCoefficientUnits:
    """Type-safe mass transfer coefficient unit constants."""
    # Explicit declarations for type checking
    gram_per_square_centimeter_per_second: 'UnitConstant'
    kilogram_per_square_meter_per_second: 'UnitConstant'
    pounds_force_per_cubic_foot_per_hour: 'UnitConstant'
    pounds_mass_per_square_foot_per_hour: 'UnitConstant'
    pounds_mass_per_square_foot_per_second: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MassTransferCoefficientUnitModule(UnitModule):
    """MassTransferCoefficient unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all mass transfer coefficient unit definitions."""
        return [
            UnitDefinition("gram_per_square_centimeter_per_second", "g / cm2 / s", MASS_TRANSFER_COEFFICIENT, 0.1),
            UnitDefinition("kilogram_per_square_meter_per_second", "kg / m2 / s", MASS_TRANSFER_COEFFICIENT, 1),
            UnitDefinition("pounds_force_per_cubic_foot_per_hour", "lbf / ft3 / h or lbf / cft / hr", MASS_TRANSFER_COEFFICIENT, 15.709),
            UnitDefinition("pounds_mass_per_square_foot_per_hour", "lb/(ft  2 hr ) or lb/sqft/ hr", MASS_TRANSFER_COEFFICIENT, 0.00013562),
            UnitDefinition("pounds_mass_per_square_foot_per_second", "lb /left(ft2 ~sright) or lb/sqft/ sec", MASS_TRANSFER_COEFFICIENT, 0.48824),

        ]
    
    def get_units_class(self):
        return MassTransferCoefficientUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MassTransferCoefficientUnitModule()