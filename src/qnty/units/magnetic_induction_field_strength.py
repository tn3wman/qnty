"""
MagneticInductionFieldStrength Units Module
===========================================

Complete magnetic induction field strength unit definitions and constants.
"""

from ..dimension import MAGNETIC_INDUCTION_FIELD_STRENGTH
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class MagneticInductionFieldStrengthUnits:
    """Type-safe magnetic induction field strength unit constants."""
    # Explicit declarations for type checking
    gamma: 'UnitConstant'
    gauss: 'UnitConstant'
    line_per_square_centimeter: 'UnitConstant'
    maxwell_per_square_centimeter: 'UnitConstant'
    tesla: 'UnitConstant'
    ua: 'UnitConstant'
    weber_per_square_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class MagneticInductionFieldStrengthUnitModule(UnitModule):
    """MagneticInductionFieldStrength unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all magnetic induction field strength unit definitions."""
        return [
            UnitDefinition("gamma", "gamma", MAGNETIC_INDUCTION_FIELD_STRENGTH, 1.00e-09),
            UnitDefinition("gauss", "G", MAGNETIC_INDUCTION_FIELD_STRENGTH, 1.00e-04),
            UnitDefinition("line_per_square_centimeter", "line / cm2", MAGNETIC_INDUCTION_FIELD_STRENGTH, 1.00e-04),
            UnitDefinition("maxwell_per_square_centimeter", "Mx / cm2", MAGNETIC_INDUCTION_FIELD_STRENGTH, 1.00e-04),
            UnitDefinition("tesla", "T", MAGNETIC_INDUCTION_FIELD_STRENGTH, 1),
            UnitDefinition("ua", "u.a.", MAGNETIC_INDUCTION_FIELD_STRENGTH, 2.35052e+15),
            UnitDefinition("weber_per_square_meter", "Wb / m2", MAGNETIC_INDUCTION_FIELD_STRENGTH, 1),

        ]
    
    def get_units_class(self):
        return MagneticInductionFieldStrengthUnits
    


# Register this module for auto-discovery
UNIT_MODULE = MagneticInductionFieldStrengthUnitModule()