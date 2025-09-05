"""
Variable Specification System
=============================

Data structures for specifying variable creation parameters, eliminating
repeated parameter patterns and improving API consistency.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional, Union

from ..constants import FLOAT_EQUALITY_TOLERANCE


@dataclass(frozen=True, slots=True)
class VariableSpec:
    """
    Specification for creating variables with consistent parameter patterns.
    
    Eliminates the common data clump pattern of (value, unit, name, is_known)
    that appears throughout the codebase, providing a cleaner, more maintainable
    way to specify variable creation parameters.
    """
    
    # Core specification
    name: str = ""
    value: Optional[float] = None
    unit: Optional[str] = None
    is_known: bool = True
    
    # Optional metadata
    description: str = ""
    symbol: str = ""
    
    # Validation constraints
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    def __post_init__(self):
        """Validate the specification after initialization."""
        # If value is provided, unit should typically also be provided
        if self.value is not None and self.unit is None:
            # Allow dimensionless quantities without units
            pass  # This is valid
            
        # Validate constraints
        if self.value is not None and self.min_value is not None:
            if self.value < self.min_value:
                raise ValueError(f"Value {self.value} is below minimum {self.min_value}")
                
        if self.value is not None and self.max_value is not None:
            if self.value > self.max_value:
                raise ValueError(f"Value {self.value} exceeds maximum {self.max_value}")
    
    @classmethod
    def known(
        cls, 
        name: str, 
        value: float, 
        unit: str, 
        description: str = "",
        symbol: str = ""
    ) -> VariableSpec:
        """Create specification for a known variable."""
        return cls(
            name=name,
            value=value,
            unit=unit,
            is_known=True,
            description=description,
            symbol=symbol
        )
    
    @classmethod
    def unknown(
        cls, 
        name: str, 
        description: str = "",
        symbol: str = "",
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> VariableSpec:
        """Create specification for an unknown variable."""
        return cls(
            name=name,
            value=None,
            unit=None,
            is_known=False,
            description=description,
            symbol=symbol,
            min_value=min_value,
            max_value=max_value
        )
    
    @classmethod
    def dimensionless(
        cls, 
        name: str, 
        value: float, 
        description: str = "",
        symbol: str = ""
    ) -> VariableSpec:
        """Create specification for a dimensionless variable."""
        return cls(
            name=name,
            value=value,
            unit=None,  # Dimensionless variables don't need units
            is_known=True,
            description=description,
            symbol=symbol
        )
    
    def has_value(self) -> bool:
        """Check if this specification includes a value."""
        return self.value is not None
    
    def has_unit(self) -> bool:
        """Check if this specification includes a unit."""
        return self.unit is not None and self.unit.strip() != ""
    
    def is_dimensionless(self) -> bool:
        """Check if this is a dimensionless specification."""
        return not self.has_unit()
    
    def is_complete(self) -> bool:
        """Check if specification is complete for creating a known variable."""
        return self.has_value() and (self.has_unit() or self.is_dimensionless())
    
    def to_quantity(self):
        """
        Convert to a Quantity object if specification is complete.
        
        Returns:
            Quantity object if value and unit are specified
            None if specification is incomplete
        """
        if not self.has_value():
            return None
            
        from .quantities.quantity import Quantity
        from .generated.units import DimensionlessUnits
        
        if self.is_dimensionless():
            # Use dimensionless unit
            unit_constant = DimensionlessUnits.dimensionless
        else:
            # Find appropriate unit constant
            # This would need to be expanded based on unit type
            # For now, create a simple quantity
            from ..core.units.registry import registry
            unit_def = registry.get_unit_by_name(self.unit)
            if unit_def is None:
                raise ValueError(f"Unknown unit: {self.unit}")
            unit_constant = unit_def
        
        return Quantity(self.value, unit_constant)
    
    def with_value(self, value: float, unit: str = None) -> VariableSpec:
        """Create a new specification with updated value and optionally unit."""
        return VariableSpec(
            name=self.name,
            value=value,
            unit=unit if unit is not None else self.unit,
            is_known=True,  # Setting value makes it known
            description=self.description,
            symbol=self.symbol,
            min_value=self.min_value,
            max_value=self.max_value
        )
    
    def with_name(self, name: str) -> VariableSpec:
        """Create a new specification with updated name."""
        return VariableSpec(
            name=name,
            value=self.value,
            unit=self.unit,
            is_known=self.is_known,
            description=self.description,
            symbol=self.symbol,
            min_value=self.min_value,
            max_value=self.max_value
        )
    
    def as_unknown(self) -> VariableSpec:
        """Create a new specification marked as unknown."""
        return VariableSpec(
            name=self.name,
            value=None,
            unit=None,
            is_known=False,
            description=self.description,
            symbol=self.symbol,
            min_value=self.min_value,
            max_value=self.max_value
        )
    
    def __str__(self) -> str:
        """String representation of the specification."""
        parts = [f"name='{self.name}'"]
        
        if self.has_value():
            if self.has_unit():
                parts.append(f"value={self.value} {self.unit}")
            else:
                parts.append(f"value={self.value}")
        else:
            parts.append("unknown")
            
        if self.description:
            parts.append(f"description='{self.description}'")
            
        return f"VariableSpec({', '.join(parts)})"


@dataclass(frozen=True, slots=True)
class VariableSpecBatch:
    """
    Collection of variable specifications for batch operations.
    
    Useful for creating multiple variables with consistent patterns.
    """
    
    specs: tuple[VariableSpec, ...]
    
    def __init__(self, *specs: VariableSpec):
        """Create batch from variable specifications."""
        object.__setattr__(self, 'specs', tuple(specs))
    
    @classmethod
    def from_tuples(cls, *tuples) -> VariableSpecBatch:
        """Create batch from (name, value, unit) tuples."""
        specs = []
        for item in tuples:
            if len(item) == 2:
                # (value, name) for dimensionless
                value, name = item
                specs.append(VariableSpec.dimensionless(name, value))
            elif len(item) == 3:
                # (value, unit, name)
                value, unit, name = item
                specs.append(VariableSpec.known(name, value, unit))
            else:
                raise ValueError(f"Expected 2 or 3 items per tuple, got {len(item)}")
        
        return cls(*specs)
    
    def __iter__(self):
        """Allow iteration over specifications."""
        return iter(self.specs)
    
    def __len__(self) -> int:
        """Get number of specifications."""
        return len(self.specs)
    
    def __getitem__(self, index: int) -> VariableSpec:
        """Get specification by index."""
        return self.specs[index]


# Convenience functions for common patterns
def spec(name: str, value: float = None, unit: str = None) -> VariableSpec:
    """Quick specification creation."""
    if value is None:
        return VariableSpec.unknown(name)
    elif unit is None:
        return VariableSpec.dimensionless(name, value)
    else:
        return VariableSpec.known(name, value, unit)


def known_spec(name: str, value: float, unit: str) -> VariableSpec:
    """Create known variable specification."""
    return VariableSpec.known(name, value, unit)


def unknown_spec(name: str) -> VariableSpec:
    """Create unknown variable specification."""
    return VariableSpec.unknown(name)


def dimensionless_spec(name: str, value: float) -> VariableSpec:
    """Create dimensionless variable specification."""
    return VariableSpec.dimensionless(name, value)