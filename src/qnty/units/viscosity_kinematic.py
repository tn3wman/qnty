"""
ViscosityKinematic Units Module
===============================

Complete viscosity, kinematic unit definitions and constants.
"""

from ..dimension import KINEMATIC_VISCOSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ViscosityKinematicUnits:
    """Type-safe viscosity, kinematic unit constants."""
    # Explicit declarations for type checking
    centistokes: 'UnitConstant'
    millistokes: 'UnitConstant'
    square_centimeter_per_second: 'UnitConstant'
    square_foot_per_hour: 'UnitConstant'
    square_foot_per_second: 'UnitConstant'
    square_meters_per_second: 'UnitConstant'
    stokes: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ViscosityKinematicUnitModule(UnitModule):
    """ViscosityKinematic unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all viscosity, kinematic unit definitions."""
        return [
            UnitDefinition("centistokes", "cSt", KINEMATIC_VISCOSITY, 0.000001),
            UnitDefinition("millistokes", "mSt", KINEMATIC_VISCOSITY, 0.0000001),
            UnitDefinition("square_centimeter_per_second", "cm2 / s", KINEMATIC_VISCOSITY, 0.0001),
            UnitDefinition("square_foot_per_hour", "ft2 / h or ft2 / hr", KINEMATIC_VISCOSITY, 2.58064e-05),
            UnitDefinition("square_foot_per_second", "ft2 / s", KINEMATIC_VISCOSITY, 0.092903),
            UnitDefinition("square_meters_per_second", "m2 / s", KINEMATIC_VISCOSITY, 1),
            UnitDefinition("stokes", "St", KINEMATIC_VISCOSITY, 0.0001),

        ]
    
    def get_units_class(self):
        return ViscosityKinematicUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ViscosityKinematicUnitModule()