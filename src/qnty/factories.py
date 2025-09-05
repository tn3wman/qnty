"""
Variable Factory System
=======================

Factory methods for creating qnty variables with cleaner, more explicit APIs
that reduce constructor complexity and improve code readability.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .quantities.quantity import Quantity
    from .quantities.unified_variable import UnifiedVariable
    from .units.registry import UnitConstant
    from .variable_spec import VariableSpec

# TypeVar for factory return types
VariableType = TypeVar('VariableType', bound='UnifiedVariable')


class VariableFactory:
    """
    Factory class for creating typed variables with explicit, readable methods.
    
    This factory simplifies variable creation while maintaining all existing
    functionality and performance characteristics.
    """

    @staticmethod
    def from_value_unit(
        variable_class: type[VariableType], 
        value: float, 
        unit: str | UnitConstant,
        name: str = "",
        is_known: bool = True
    ) -> VariableType:
        """
        Create a variable from a value and unit.
        
        Args:
            variable_class: The variable class to create (Length, Pressure, etc.)
            value: Numerical value
            unit: Unit specification (string or UnitConstant)
            name: Variable name for display and equations
            is_known: Whether the variable has a known value
            
        Returns:
            Initialized variable with the specified value and unit
            
        Example:
            >>> length = VariableFactory.from_value_unit(Length, 100.0, "mm", "beam_length")
            >>> pressure = VariableFactory.from_value_unit(Pressure, 150.0, "psi", "design_pressure")
        """
        unit_str = getattr(unit, 'name', str(unit))
        
        # Use existing constructor
        return variable_class(value, unit_str, name, is_known=is_known)

    @staticmethod
    def from_quantity(
        variable_class: type[VariableType], 
        quantity: Quantity,
        name: str = "",
        is_known: bool | None = None
    ) -> VariableType:
        """
        Create a variable from an existing quantity.
        
        Args:
            variable_class: The variable class to create
            quantity: Existing quantity to copy
            name: Variable name (required if not in quantity)
            is_known: Override known state, or infer from quantity if None
            
        Returns:
            Variable wrapping the provided quantity
            
        Example:
            >>> existing_qty = Quantity(5.0, "m")
            >>> length = VariableFactory.from_quantity(Length, existing_qty, "width")
        """
        # Create variable and set quantity directly  
        if is_known is None:
            is_known = True  # Quantities are typically known values
            
        variable = variable_class(name or "unnamed")
        variable.is_known = is_known
        variable.quantity = quantity
        return variable

    @staticmethod
    def unknown(variable_class: type[VariableType], name: str) -> VariableType:
        """
        Create an unknown variable for equation solving.
        
        Args:
            variable_class: The variable class to create
            name: Variable name for equations and display
            
        Returns:
            Variable marked as unknown (no quantity)
            
        Example:
            >>> unknown_length = VariableFactory.unknown(Length, "x")
            >>> unknown_pressure = VariableFactory.unknown(Pressure, "P_design")
        """
        return variable_class(name, is_known=False)

    @staticmethod
    def copy_with_name(source: VariableType, new_name: str) -> VariableType:
        """
        Create a copy of a variable with a different name.
        
        Args:
            source: Variable to copy
            new_name: Name for the new variable
            
        Returns:
            New variable with same quantity but different name
            
        Example:
            >>> original = Length(100.0, "mm", "length1") 
            >>> copy = VariableFactory.copy_with_name(original, "length2")
        """
        variable_class = type(source)
        
        if source.quantity is not None:
            return VariableFactory.from_quantity(
                variable_class, 
                source.quantity, 
                new_name,
                source.is_known
            )
        else:
            return variable_class(new_name, is_known=False)

    @staticmethod
    def with_value(source: VariableType, new_value: float, new_unit: str | None = None) -> VariableType:
        """
        Create a variable based on another but with a different value/unit.
        
        Args:
            source: Source variable for type and name
            new_value: New numerical value
            new_unit: New unit (uses source unit if None)
            
        Returns:
            New variable with same type/name but different value
            
        Example:
            >>> template = Length("beam_length")
            >>> concrete = VariableFactory.with_value(template, 100.0, "mm")
        """
        variable_class = type(source)
        unit = new_unit or (source.quantity.unit.name if source.quantity else "")
        
        return VariableFactory.from_value_unit(
            variable_class,
            new_value,
            unit, 
            source.name,
            True  # New value means it's known
        )


class DimensionlessFactory:
    """
    Specialized factory for Dimensionless variables with their unique syntax.
    
    Dimensionless variables have special constructor behavior that differs
    from other variable types.
    """
    
    @staticmethod
    def from_value(value: float, name: str = "", is_known: bool = True):
        """
        Create a dimensionless variable from a value.
        
        Args:
            value: Numerical value
            name: Variable name
            is_known: Whether the variable has a known value
            
        Returns:
            Dimensionless variable
            
        Example:
            >>> ratio = DimensionlessFactory.from_value(1.5, "safety_factor")
        """
        from .generated.quantities import Dimensionless
        return Dimensionless(value, name, is_known=is_known)
    
    @staticmethod
    def unknown(name: str):
        """
        Create an unknown dimensionless variable.
        
        Args:
            name: Variable name
            
        Returns:
            Unknown dimensionless variable
            
        Example:
            >>> unknown_ratio = DimensionlessFactory.unknown("efficiency")
        """
        from .generated.quantities import Dimensionless
        return Dimensionless(name, is_known=False)


# Convenience functions for common patterns
def make_length(value: float, unit: str, name: str = ""):
    """Convenience function for creating Length variables."""
    from .generated.quantities import Length
    return VariableFactory.from_value_unit(Length, value, unit, name)


def make_pressure(value: float, unit: str, name: str = ""):
    """Convenience function for creating Pressure variables."""
    from .generated.quantities import Pressure
    return VariableFactory.from_value_unit(Pressure, value, unit, name)


def make_temperature(value: float, unit: str, name: str = ""):
    """Convenience function for creating Temperature variables."""
    from .generated.quantities import Temperature
    return VariableFactory.from_value_unit(Temperature, value, unit, name)


def make_unknown(variable_class: type[VariableType], name: str) -> VariableType:
    """Convenience function for creating unknown variables of any type."""
    return VariableFactory.unknown(variable_class, name)


def from_spec(variable_class: type[VariableType], spec) -> VariableType:
    """
    Create variable from VariableSpec.
    
    Args:
        variable_class: The variable class to create
        spec: VariableSpec containing creation parameters
        
    Returns:
        Variable created according to specification
        
    Example:
        >>> spec = VariableSpec.known("pressure", 150.0, "psi")
        >>> pressure = from_spec(Pressure, spec)
    """
    from .variable_spec import VariableSpec
    
    if not isinstance(spec, VariableSpec):
        raise TypeError(f"Expected VariableSpec, got {type(spec)}")
    
    if spec.is_known and spec.has_value() and spec.value is not None:
        if spec.has_unit() and spec.unit is not None:
            return VariableFactory.from_value_unit(
                variable_class, spec.value, spec.unit, spec.name, spec.is_known
            )
        else:
            # Dimensionless case - handle separately
            from .generated.quantities import Dimensionless
            if variable_class == Dimensionless:
                # Use DimensionlessFactory for proper constructor handling
                return DimensionlessFactory.from_value(spec.value, spec.name, spec.is_known)
            else:
                raise ValueError(f"Cannot create {variable_class.__name__} without unit")
    else:
        return VariableFactory.unknown(variable_class, spec.name)