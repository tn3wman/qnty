"""
Specialized Variables
=====================

Dimension-specific variable classes with type safety.
"""

from .dimension import DIMENSIONLESS, LENGTH, PRESSURE
from .setters import DimensionlessSetter, LengthSetter, PressureSetter
from .types import TypeSafeVariable


# Specialized variable types
class Length(TypeSafeVariable):
    """Type-safe length variable."""
    def __init__(self, *args, is_known: bool = True):
        if len(args) == 1:
            # Length("name") - original syntax
            super().__init__(args[0], LENGTH, is_known=is_known)
        elif len(args) == 3:
            # Length(value, "unit", "name") - new syntax
            value, unit, name = args
            super().__init__(name, LENGTH, is_known=is_known)
            # Auto-set the value with the specified unit
            setter = LengthSetter(self, value)
            # Get the unit setter method dynamically
            if unit == "in":  # Handle "in" alias for inches
                setter.inches
            elif hasattr(setter, unit):
                getattr(setter, unit)
            elif hasattr(setter, unit + 's'):  # Handle singular/plural
                getattr(setter, unit + 's')
            else:
                # Default to meters if unit not recognized
                setter.meters
        else:
            raise ValueError("Length expects either 1 argument (name) or 3 arguments (value, unit, name)")
    
    def set(self, value: float) -> 'LengthSetter':
        return LengthSetter(self, value)


class Pressure(TypeSafeVariable):
    """Type-safe pressure variable."""
    
    def __init__(self, *args, is_known: bool = True):
        if len(args) == 1:
            # Pressure("name") - original syntax
            super().__init__(args[0], PRESSURE, is_known=is_known)
        elif len(args) == 3:
            # Pressure(value, "unit", "name") - new syntax
            value, unit, name = args
            super().__init__(name, PRESSURE, is_known=is_known)
            # Auto-set the value with the specified unit
            setter = PressureSetter(self, value)
            # Get the unit setter method dynamically
            if unit == "psi":
                setter.psi
            elif unit == "kPa":
                setter.kPa
            elif unit == "MPa":
                setter.MPa
            elif unit == "bar":
                setter.bar
            else:
                # Default to psi if unit not recognized
                setter.psi
        else:
            raise ValueError("Pressure expects either 1 argument (name) or 3 arguments (value, unit, name)")
    
    def set(self, value: float) -> 'PressureSetter':
        return PressureSetter(self, value)


class Dimensionless(TypeSafeVariable):
    """Type-safe dimensionless variable."""

    def __init__(self, *args, is_known: bool = True):
        if len(args) == 1:
            # Dimensionless("name") - original syntax
            super().__init__(args[0], DIMENSIONLESS, is_known=is_known)
        elif len(args) == 2:
            # Dimensionless(value, "name") - new syntax
            value, name = args
            super().__init__(name, DIMENSIONLESS, is_known=is_known)
            # Auto-set the value as dimensionless
            setter = DimensionlessSetter(self, value)
            setter.dimensionless
        else:
            raise ValueError("Dimensionless expects either 1 argument (name) or 2 arguments (value, name)")

    def set(self, value: float) -> 'DimensionlessSetter':
        return DimensionlessSetter(self, value)
