"""
SpecificHeatCapacityconstantPressure Units Module
=================================================

Complete specific heat capacity (constant pressure) unit definitions and constants.
"""

from ..dimension import SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE
from ..unit import UnitConstant, UnitDefinition
from .base import UnitModule


class SpecificHeatCapacityconstantPressureUnits:
    """Type-safe specific heat capacity (constant pressure) unit constants."""
    # Explicit declarations for type checking
    fahrenheit: 'UnitConstant'
    celsius: 'UnitConstant'
    celsius: 'UnitConstant'
    kilopascal: 'UnitConstant'
    kPa: 'UnitConstant'
    
    # Common aliases for test compatibility
    kPa: 'UnitConstant'  # kilopascal


class SpecificHeatCapacityconstantPressureUnitModule(UnitModule):
    """SpecificHeatCapacityconstantPressure unit module definition."""
    
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return all specific heat capacity (constant pressure) unit definitions."""
        return [
            UnitDefinition("fahrenheit", "°F", SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE, 4186.8),
            UnitDefinition("celsius", "°C", SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE, 4186.8),
            UnitDefinition("celsius", "°C", SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE, 1),
            UnitDefinition("kilopascal", "kPa", SPECIFIC_HEAT_CAPACITY_CONSTANT_PRESSURE, 1000),

        ]
    
    def get_units_class(self):
        return SpecificHeatCapacityconstantPressureUnits
    
    def register_to_registry(self, unit_registry):
        """Register all unit definitions and set up aliases."""
        # First do the standard registration
        super().register_to_registry(unit_registry)
        
        # Then add custom aliases for test compatibility
        units_class = self.get_units_class()
        
        # Set up aliases pointing to existing unit constants
        if hasattr(units_class, 'kilopascal'):
            units_class.kPa = units_class.kilopascal


# Register this module for auto-discovery
UNIT_MODULE = SpecificHeatCapacityconstantPressureUnitModule()