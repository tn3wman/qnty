"""
ViscosityDynamic Units Module
=============================

Complete viscosity, dynamic unit definitions and constants.
"""

from ..dimension import DYNAMIC_VISCOSITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ViscosityDynamicUnits:
    """Type-safe viscosity, dynamic unit constants."""
    # Explicit declarations for type checking
    centipoise: 'UnitConstant'
    dyne_second_per_square_centimeter: 'UnitConstant'
    kilopound_second_per_square_meter: 'UnitConstant'
    millipoise: 'UnitConstant'
    newton_second_per_square_meter: 'UnitConstant'
    pascal_second: 'UnitConstant'
    poise: 'UnitConstant'
    pound_force_hour_per_square_foot: 'UnitConstant'
    pound_force_second_per_square_foot: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ViscosityDynamicUnitModule(UnitModule):
    """ViscosityDynamic unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all viscosity, dynamic unit definitions."""
        return [
            UnitDefinition("centipoise", "cP or cPo", DYNAMIC_VISCOSITY, 0.01),
            UnitDefinition("dyne_second_per_square_centimeter", "dyn s/ cm2", DYNAMIC_VISCOSITY, 1),
            UnitDefinition("kilopound_second_per_square_meter", "kip s / m2", DYNAMIC_VISCOSITY, 98.0665),
            UnitDefinition("millipoise", "mP or mPo", DYNAMIC_VISCOSITY, 0.001),
            UnitDefinition("newton_second_per_square_meter", "N s / m2", DYNAMIC_VISCOSITY, 10),
            UnitDefinition("pascal_second", "Pa s or PI", DYNAMIC_VISCOSITY, 10),
            UnitDefinition("poise", "P or Po", DYNAMIC_VISCOSITY, 1),
            UnitDefinition("pound_force_hour_per_square_foot", "lbf h / ft2 or lb hr / sq ft", DYNAMIC_VISCOSITY, 1.72369e+06),
            UnitDefinition("pound_force_second_per_square_foot", "lbf s / ft2 or lb sec / sq ft", DYNAMIC_VISCOSITY, 478.803),

        ]
    
    def get_units_class(self):
        return ViscosityDynamicUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ViscosityDynamicUnitModule()