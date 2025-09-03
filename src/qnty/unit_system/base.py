"""
Base Unit Module Definition
===========================

Provides abstract base class for unit modules and registration functionality.
"""

from abc import ABC, abstractmethod
from typing import Any

from .core import UnitConstant, UnitDefinition


class UnitModule(ABC):
    """Abstract base class for unit modules."""
    
    @abstractmethod
    def get_unit_definitions(self) -> list[UnitDefinition]:
        """Return list of unit definitions for this module."""
        pass
    
    @abstractmethod
    def get_units_class(self) -> type[Any]:
        """Return the units class for this module."""
        pass
    
    def register_to_registry(self, unit_registry):
        """Register all unit definitions to the given registry."""
        
        unit_definitions = self.get_unit_definitions()
        units_class = self.get_units_class()
        
        # Phase 1: Register all units first (batch operation)
        for unit_def in unit_definitions:
            if unit_def.name not in unit_registry.units:
                unit_registry.register_unit(unit_def)
        
        # Phase 2: Batch create unit constants with caching
        unit_constants = {}
        for unit_def in unit_definitions:
            unit_constants[unit_def.name] = UnitConstant(unit_registry.units[unit_def.name])
        
        # Phase 3: Batch set all attributes
        for unit_def in unit_definitions:
            unit_constant = unit_constants[unit_def.name]
            setattr(units_class, unit_def.name, unit_constant)
            
            # Add symbol alias if different from name
            if unit_def.symbol and unit_def.symbol != unit_def.name:
                setattr(units_class, unit_def.symbol, unit_constant)
            
            # Special case for inch - add in_ alias since 'in' is a Python keyword
            if unit_def.name == "inch":
                units_class.in_ = unit_constant
