from dataclasses import dataclass

from ..dimensions import Dimension
from ..units import Unit, ureg


@dataclass(frozen=True, slots=True)
class Quantity:
    """
    Immutable physical quantity stored in SI units.
    Supports arithmetic and automatic pretty-printing
    using preferred units from the UnitRegistry.
    """
    value: float         # numerical value in SI base units
    dim: Dimension       # physical dimension (e.g., M*L/T^2)

    # ----- arithmetic -----
    def __mul__(self, other: "Quantity | float | int") -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.dim * other.dim)
        return Quantity(self.value * float(other), self.dim)

    def __truediv__(self, other: "Quantity | float | int") -> "Quantity":
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.dim / other.dim)
        return Quantity(self.value / float(other), self.dim)

    def __pow__(self, k: int) -> "Quantity":
        return Quantity(self.value ** k, self.dim ** k)

    def __add__(self, other: "Quantity") -> "Quantity":
        if self.dim != other.dim:
            raise TypeError("Dimension mismatch in addition")
        return Quantity(self.value + other.value, self.dim)

    def __sub__(self, other: "Quantity") -> "Quantity":
        if self.dim != other.dim:
            raise TypeError("Dimension mismatch in subtraction")
        return Quantity(self.value - other.value, self.dim)

    # ----- conversion & display -----
    def to(self, unit: Unit) -> float:
        """
        Convert to the given unit and return the numerical value.
        Raises TypeError if the unit dimension is incompatible.
        """
        if unit.dim != self.dim:
            raise TypeError(f"Cannot convert {self.dim} to {unit.dim}")
        return (self.value - unit.si_offset) / unit.si_factor

    def __repr__(self) -> str:
        """
        Pretty-print in the preferred unit if one is registered;
        otherwise show the raw SI value and dimension.
        """
        pref = ureg.preferred_for(self.dim)
        if pref:
            return f"{self.to(pref):.6g} {pref.symbol}"
        return f"{self.value:.6g} [Dim={self.dim}]"


def Q(val: float, unit: Unit) -> Quantity:
    """Create an immutable Quantity from a value in the given unit."""
    return Quantity(unit.si_factor * val + unit.si_offset, unit.dim)



# class BooleanQuantity(Quantity):
#     """A quantity that represents a boolean value but maintains Quantity compatibility.

#     This class is used for comparison operations that need to return boolean results
#     while maintaining the Expression interface requirement of returning Quantity objects.
#     """

#     __slots__ = ("_boolean_value",)

#     def __init__(self, boolean_value: bool):
#         """Initialize with a boolean value."""
#         # Store the actual boolean value
#         self._boolean_value = boolean_value

#         # Initialize parent with numeric representation
#         super().__init__(1.0 if boolean_value else 0.0, DIMENSIONLESS)

#     def __str__(self) -> str:
#         """Display as True/False instead of 1.0/0.0."""
#         return str(self._boolean_value)

#     def __repr__(self) -> str:
#         """Display as BooleanQuantity(True/False)."""
#         return f"BooleanQuantity({self._boolean_value})"

#     def __bool__(self) -> bool:
#         """Return the actual boolean value."""
#         return self._boolean_value

#     @property
#     def boolean_value(self) -> bool:
#         """Access the boolean value directly."""
#         return self._boolean_value


# class TypeSafeSetter:
#     """Base class for type-safe setter objects."""
    
#     __slots__ = ("variable", "value")
    
#     def __init__(self, variable, value: float):
#         """Initialize setter with variable and value."""
#         self.variable = variable
#         self.value = value