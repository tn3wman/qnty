"""
Parameter Objects for Simplifying Long Parameter Lists.

This module provides parameter objects to replace long parameter lists
with cohesive data structures, improving code readability and maintainability.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class VariableInitParams:
    """
    Parameter object for variable initialization to replace long parameter lists.
    
    Replaces the common pattern of:
    __init__(self, name_or_value, unit=None, name=None, is_known=True)
    
    With a single cohesive parameter object.
    """
    name_or_value: str | int | float
    unit: str | None = None
    name: str | None = None
    is_known: bool = True
    
    @classmethod
    def from_name(cls, name: str, is_known: bool = False) -> "VariableInitParams":
        """Create parameters for a named unknown variable."""
        return cls(name_or_value=name, unit=None, name=None, is_known=is_known)
    
    @classmethod
    def from_value_unit(cls, value: int | float, unit: str, name: str | None = None) -> "VariableInitParams":
        """Create parameters for a variable with value and unit."""
        return cls(name_or_value=value, unit=unit, name=name, is_known=True)
    
    @classmethod
    def from_name_with_value(cls, name: str, value: int | float, unit: str) -> "VariableInitParams":
        """Create parameters for a named variable with value and unit."""
        return cls(name_or_value=value, unit=unit, name=name, is_known=True)


@dataclass 
class DimensionCreateParams:
    """
    Parameter object for DimensionSignature creation to replace 7-parameter method.
    
    Replaces:
    create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0)
    
    With a single parameter object containing dimension exponents.
    """
    length: int | float = 0
    mass: int | float = 0 
    time: int | float = 0
    current: int | float = 0
    temp: int | float = 0
    amount: int | float = 0
    luminosity: int | float = 0
    
    @classmethod
    def dimensionless(cls) -> "DimensionCreateParams":
        """Create parameters for dimensionless quantity."""
        return cls()
    
    @classmethod
    def length_dimension(cls, exponent: int | float = 1) -> "DimensionCreateParams":
        """Create parameters for length dimension."""
        return cls(length=exponent)
        
    @classmethod
    def mass_dimension(cls, exponent: int | float = 1) -> "DimensionCreateParams":
        """Create parameters for mass dimension."""
        return cls(mass=exponent)
    
    @classmethod
    def time_dimension(cls, exponent: int | float = 1) -> "DimensionCreateParams":
        """Create parameters for time dimension."""
        return cls(time=exponent)
        
    @classmethod
    def area_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for area dimension (length²)."""
        return cls(length=2)
        
    @classmethod
    def volume_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for volume dimension (length³)."""
        return cls(length=3)
        
    @classmethod
    def velocity_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for velocity dimension (length/time)."""
        return cls(length=1, time=-1)
        
    @classmethod
    def acceleration_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for acceleration dimension (length/time²)."""
        return cls(length=1, time=-2)
        
    @classmethod 
    def force_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for force dimension (mass×length/time²)."""
        return cls(mass=1, length=1, time=-2)
        
    @classmethod
    def pressure_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for pressure dimension (mass/(length×time²))."""
        return cls(mass=1, length=-1, time=-2)
        
    @classmethod
    def energy_dimension(cls) -> "DimensionCreateParams":
        """Create parameters for energy dimension (mass×length²/time²)."""
        return cls(mass=1, length=2, time=-2)
    
    def to_tuple(self) -> tuple[int | float, ...]:
        """Convert to tuple for use with existing code."""
        return (self.length, self.mass, self.time, self.current, 
                self.temp, self.amount, self.luminosity)
    
    def is_dimensionless(self) -> bool:
        """Check if this represents a dimensionless quantity."""
        return not any([self.length, self.mass, self.time, self.current, 
                       self.temp, self.amount, self.luminosity])


@dataclass
class ExpressionEvaluationParams:
    """
    Parameter object for expression evaluation contexts.
    
    Consolidates parameters commonly passed together for expression evaluation.
    """
    variable_values: dict[str, Any]
    enable_caching: bool = True
    tolerance: float = 1e-10
    max_depth: int = 100
    
    @classmethod
    def simple(cls, variable_values: dict[str, Any]) -> "ExpressionEvaluationParams":
        """Create simple evaluation parameters with just variable values."""
        return cls(variable_values=variable_values)
    
    @classmethod
    def with_tolerance(cls, variable_values: dict[str, Any], tolerance: float) -> "ExpressionEvaluationParams":
        """Create evaluation parameters with custom tolerance."""
        return cls(variable_values=variable_values, tolerance=tolerance)


@dataclass
class UnitConversionParams:
    """
    Parameter object for unit conversion operations.
    
    Consolidates parameters for unit conversion to improve readability.
    """
    source_unit: str
    target_unit: str
    value: int | float
    check_compatibility: bool = True
    allow_offset: bool = True
    
    @classmethod
    def simple(cls, value: int | float, from_unit: str, to_unit: str) -> "UnitConversionParams":
        """Create simple conversion parameters."""
        return cls(source_unit=from_unit, target_unit=to_unit, value=value)


@dataclass
class CacheParams:
    """
    Parameter object for cache configuration.
    
    Consolidates cache-related parameters to avoid passing many boolean flags.
    """
    enable_caching: bool = True
    max_size: int = 1000
    clear_on_update: bool = False
    enable_statistics: bool = False
    
    @classmethod
    def disabled(cls) -> "CacheParams":
        """Create parameters with caching disabled."""
        return cls(enable_caching=False)
    
    @classmethod
    def high_performance(cls) -> "CacheParams":
        """Create parameters optimized for high performance."""
        return cls(enable_caching=True, max_size=10000, enable_statistics=True)