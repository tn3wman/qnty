"""
Base classes for integrated quantity modules with auto-registration.
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Type

from ..dimension import DimensionSignature
from ..unit import UnitConstant, UnitDefinition
from ..unit import registry as unit_registry

if TYPE_CHECKING:
    from ..variable import TypeSafeSetter, TypeSafeVariable


class QuantityModule(ABC):
    """
    Base class for integrated quantity modules containing units, variables, and setters.
    
    Each quantity module provides everything needed for a physical quantity:
    - Unit definitions and constants
    - Variable class
    - Setter class  
    - Auto-registration logic
    """
    
    @abstractmethod
    def get_unit_definitions(self) -> List[UnitDefinition]:
        """Return list of unit definitions for this quantity."""
        pass
    
    @abstractmethod
    def get_variable_class(self) -> Type['TypeSafeVariable']:
        """Return the variable class for this quantity."""
        pass
    
    @abstractmethod  
    def get_setter_class(self) -> Type['TypeSafeSetter']:
        """Return the setter class for this quantity."""
        pass
    
    @abstractmethod
    def get_units_class(self) -> Type:
        """Return the units constants class for this quantity."""
        pass
    
    @abstractmethod
    def get_expected_dimension(self) -> DimensionSignature:
        """Return the expected dimension for this quantity type."""
        pass
    
    def register_units(self):
        """Register all unit definitions to the global unit registry."""
        for unit_def in self.get_unit_definitions():
            # Check if unit already exists to avoid double registration
            if unit_def.name not in unit_registry.units:
                try:
                    unit_registry.register_unit(unit_def)
                except RuntimeError:
                    # Registry is finalized, but we can still add units directly
                    unit_registry.units[unit_def.name] = unit_def
                    
                    # Group by dimension
                    dim_sig = unit_def.dimension._signature
                    if dim_sig not in unit_registry.dimensional_groups:
                        unit_registry.dimensional_groups[dim_sig] = []
                    unit_registry.dimensional_groups[dim_sig].append(unit_def)
                    
                    # Update conversion table for this unit
                    unit_registry._precompute_conversions()
    
    def populate_units_class(self):
        """Auto-populate the units constants class with UnitConstant instances."""
        units_class = self.get_units_class()
        
        for unit_def in self.get_unit_definitions():
            constant = UnitConstant(unit_def)
            setattr(units_class, unit_def.name, constant)
            
            # Add common aliases based on symbol
            if unit_def.symbol and unit_def.symbol != unit_def.name:
                # Handle special cases for Python reserved words
                symbol = unit_def.symbol
                if symbol == "in":
                    symbol = "in_"
                setattr(units_class, symbol, constant)
    
    def register_to_registries(self):
        """Register this quantity to all relevant registries."""
        # Register units to unit registry
        self.register_units()
        
        # Populate units class
        self.populate_units_class()


class QuantityRegistry:
    """Registry for quantity types with factory methods."""
    
    def __init__(self):
        self.quantities = {}
    
    def register_quantity(self, name: str, quantity_module: QuantityModule):
        """Register a complete quantity module."""
        self.quantities[name] = quantity_module
        
        # Perform all registrations
        quantity_module.register_to_registries()
    
    def create_variable(self, quantity_name: str, *args, **kwargs):
        """Factory method to create variables by quantity name."""
        if quantity_name in self.quantities:
            var_class = self.quantities[quantity_name].get_variable_class()
            return var_class(*args, **kwargs)
        raise ValueError(f"Unknown quantity type: {quantity_name}")
    
    def get_available_quantities(self) -> list[str]:
        """Get list of available quantity types."""
        return list(self.quantities.keys())
    
    def get_units_for_quantity(self, quantity_name: str):
        """Get the units class for a specific quantity."""
        if quantity_name in self.quantities:
            return self.quantities[quantity_name].get_units_class()
        raise ValueError(f"Unknown quantity type: {quantity_name}")


# Global quantity registry
quantity_registry = QuantityRegistry()