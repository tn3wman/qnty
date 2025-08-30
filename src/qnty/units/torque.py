"""
Torque Units Module
===================

Complete torque unit definitions and constants.
"""

from ..dimension import ENERGY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class TorqueUnits:
    """Type-safe torque unit constants."""
    # Explicit declarations for type checking
    centimeter_kilogram_force: 'UnitConstant'
    dyne_centimeter: 'UnitConstant'
    foot_kilogram_force: 'UnitConstant'
    foot_pound_force: 'UnitConstant'
    foot_poundal: 'UnitConstant'
    in_pound_force: 'UnitConstant'
    inch_ounce_force: 'UnitConstant'
    meter_kilogram_force: 'UnitConstant'
    newton_centimeter: 'UnitConstant'
    newton_meter: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class TorqueUnitModule(UnitModule):
    """Torque unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all torque unit definitions."""
        return [
            UnitDefinition("centimeter_kilogram_force", "cm kg  f", ENERGY, 0.098067),
            UnitDefinition("dyne_centimeter", "dyn cm", ENERGY, 1.00e-07),
            UnitDefinition("foot_kilogram_force", "ft kgf", ENERGY, 2.9891),
            UnitDefinition("foot_pound_force", "ft lbf", ENERGY, 1.3558),
            UnitDefinition("foot_poundal", "ft pdl", ENERGY, 0.042140),
            UnitDefinition("in_pound_force", "in lbf", ENERGY, 0.11298),
            UnitDefinition("inch_ounce_force", "in OZf", ENERGY, 0.0070616),
            UnitDefinition("meter_kilogram_force", "m kgf", ENERGY, 9.8067),
            UnitDefinition("newton_centimeter", "N cm", ENERGY, 0.01),
            UnitDefinition("newton_meter", "N m", ENERGY, 1),

        ]
    
    def get_units_class(self):
        return TorqueUnits
    


# Register this module for auto-discovery
UNIT_MODULE = TorqueUnitModule()