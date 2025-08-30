"""
ThermalConductivity Units Module
================================

Complete thermal conductivity unit definitions and constants.
"""

from ..dimension import THERMAL_CONDUCTIVITY
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class ThermalConductivityUnits:
    """Type-safe thermal conductivity unit constants."""
    # Explicit declarations for type checking
    fahrenheit: 'UnitConstant'
    fahrenheit: 'UnitConstant'
    fahrenheit: 'UnitConstant'
    celsius: 'UnitConstant'
    kelvin: 'UnitConstant'
    kelvin: 'UnitConstant'
    kelvin: 'UnitConstant'

    
    # Common aliases for test compatibility
    pass


class ThermalConductivityUnitModule(UnitModule):
    """ThermalConductivity unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all thermal conductivity unit definitions."""
        return [
            UnitDefinition("fahrenheit", "°F", THERMAL_CONDUCTIVITY, 0.207688),
            UnitDefinition("fahrenheit", "°F", THERMAL_CONDUCTIVITY, 0.017296),
            UnitDefinition("fahrenheit", "°F", THERMAL_CONDUCTIVITY, 0.207549),
            UnitDefinition("celsius", "°C", THERMAL_CONDUCTIVITY, 4.184),
            UnitDefinition("kelvin", "K", THERMAL_CONDUCTIVITY, 0.01),
            UnitDefinition("kelvin", "K", THERMAL_CONDUCTIVITY, 1),
            UnitDefinition("kelvin", "K", THERMAL_CONDUCTIVITY, 0.01),

        ]
    
    def get_units_class(self):
        return ThermalConductivityUnits
    


# Register this module for auto-discovery
UNIT_MODULE = ThermalConductivityUnitModule()