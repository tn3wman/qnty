from dataclasses import dataclass
from typing import Generic, TypeVar, cast, overload

from ..dimensions import Dimension
from ..units import u
from ..units.core import Unit, ureg

D = TypeVar("D")

@dataclass(frozen=True, slots=True)
class Quantity(Generic[D]):
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
    def to(self, unit: Unit[D]) -> float:
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


def Q(val: float, unit: Unit[D]) -> Quantity[D]:
    return Quantity(unit.si_factor * val + unit.si_offset, unit.dim)


# =========================
# FieldQuantity + Setter
# =========================
class FieldQuantity(Generic[D]):
    """
    A named quantity (optionally unknown) with an optional preferred display unit.
    """
    __slots__ = ("name", "q", "preferred")

    def __init__(self, name: str, q: Quantity[D] | None = None, preferred: Unit[D] | None = None):
        self.name = name
        self.q = q
        self.preferred = preferred

    @property
    def is_known(self) -> bool:
        return self.q is not None

    def prefer(self, unit: Unit[D]) -> "FieldQuantity[D]":
        self.preferred = unit
        return self

    @overload
    def set(self, value: float) -> "FieldSetter[D]": ...
    @overload
    def set(self, value: float, unit: Unit[D]) -> "FieldQuantity[D]": ...
    def set(self, value: float, unit: Unit[D] | None = None) -> "FieldSetter[D] | FieldQuantity[D]":
        if unit is None:
            return FieldSetter(self, value)
        self.q = Q(value, unit)
        return self


    def value_in(self, unit: Unit[D] | None = None) -> float | None:
        if self.q is None:
            return None
        u = unit or self.preferred or ureg.preferred_for(self.q.dim)
        return self.q.value if u is None else self.q.to(u)

class FieldSetter(Generic[D]):
    """
    Returned by FieldQuantity.set(value) when no unit is given.
    Supports .using("mps2"), .in_(u.mps2), and fluent .mps2 / .meter_per_second_squared, etc.
    """
    __slots__ = ("_owner", "_value")

    def __init__(self, owner: FieldQuantity[D], value: float):
        self._owner = owner
        self._value = float(value)

    # ---- explicit helpers ----
    def using(self, unit_name: str) -> FieldQuantity[D]:
        """Set by unit name/alias string."""
        unit = ureg.resolve(unit_name)  # must return a Unit or None
        if unit is None:
            raise AttributeError(f"Unknown unit '{unit_name}'")
        self._owner.set(self._value, unit)
        return self._owner

    def in_(self, unit: Unit[D]) -> "FieldQuantity[D]":
        self._owner.set(self._value, unit)
        return self._owner

    # ---- fluent attributes: .mps2, .meter_per_second_squared, etc. ----
    def __getattr__(self, name: str) -> FieldQuantity[D]:
        """
        Resolve attribute name to a Unit (via registry) and apply immediately.
        Returns the FieldQuantity so the chain can continue.
        """
        unit = ureg.resolve(name)
        if unit is None:
            raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")
        self._owner.set(self._value, unit)  # dimension mismatch handled in Q/Quantity.to if needed
        return self._owner

    def __dir__(self):
        """
        Improve IDE autocompletion by exposing known names/aliases
        (if your editor uses __dir__). This is optional but nice.
        """
        base = super().__dir__()
        try:
            # Show all unit names; or restrict to most-relevant for owner.q/preferred
            names = ureg.all_names()  # see registry notes below
            return sorted(set(list(base) + names))
        except Exception:
            return base
        

class AccelerationSetter(FieldSetter["Acceleration"]):
    __slots__ = ()
    @property
    def meter_per_square_second(self) -> "FieldQuantity['Acceleration']":
        return self.in_(u.meter_per_square_second)  # property returns owner (no parens)
    meter_per_second_squared = meter_per_square_second


class Acceleration(FieldQuantity["Acceleration"]):
    __slots__ = ()

    @overload
    def set(self, value: float) -> AccelerationSetter: ...
    @overload
    def set(self, value: float, unit: Unit["Acceleration"]) -> "Acceleration": ...

    def set(
        self,
        value: float,
        unit: Unit["Acceleration"] | None = None,
    ) -> "Acceleration | AccelerationSetter":
        # Match the correct overload: if unit is None, call the 1-arg overload; otherwise the 2-arg overload
        if unit is None:
            return cast("Acceleration | AccelerationSetter", super().set(value))
        return cast("Acceleration | AccelerationSetter", super().set(value, unit))








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
