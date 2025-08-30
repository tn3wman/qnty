"""
SurfaceTension Units Module
===========================

Complete surface tension unit definitions and constants.
"""

from ..dimension import SURFACE_TENSION
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SurfaceTensionUnits:
    """Type-safe surface tension unit constants."""
    # Explicit declarations for type checking
    dyne_per_centimeter: 'UnitConstant'
    gram_force_per_centimeter: 'UnitConstant'
    newton_per_meter: 'UnitConstant'
    pound_force_per_foot: 'UnitConstant'
    pound_force_per_inch: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class SurfaceTensionUnitModule(UnitModule):
    """SurfaceTension unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all surface tension unit definitions."""
        return [
            UnitDefinition("dyne_per_centimeter", "dyn/cm", SURFACE_TENSION, 0.001),
            UnitDefinition("gram_force_per_centimeter", "gf / cm", SURFACE_TENSION, 0.0102),
            UnitDefinition("newton_per_meter", "N/m", SURFACE_TENSION, 1),
            UnitDefinition("pound_force_per_foot", "lbf / ft", SURFACE_TENSION, 14.594),
            UnitDefinition("pound_force_per_inch", "lbf / in", SURFACE_TENSION, 175.13),

        ]
    
    def get_units_class(self):
        return SurfaceTensionUnits
    


# Register this module for auto-discovery
UNIT_MODULE = SurfaceTensionUnitModule()