from dataclasses import dataclass
from typing import Generic, Self, TypeVar, overload

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
    def set(self, value: float, unit: Unit[D]) -> Self: ...
    @overload
    def set(self, value: float, unit: str) -> Self: ...
    def set(self, value: float, unit: Unit[D] | str | None = None) -> "FieldSetter[D] | Self":
        if unit is None:
            return FieldSetter(self, value)
        if isinstance(unit, str):
            resolved = ureg.resolve(unit)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            self.q = Q(value, resolved)
            return self
        self.q = Q(value, unit)
        return self


    def value_in(self, unit: Unit[D] | None = None) -> float | None:
        if self.q is None:
            return None
        u = unit or self.preferred or ureg.preferred_for(self.q.dim)
        return self.q.value if u is None else self.q.to(u)

    @property
    def to_unit(self) -> "UnitApplier[D]":
        return UnitApplier(self)

    @property
    def as_unit(self) -> "UnitChanger[D]":
        return UnitChanger(self)

    # ---- display ----
    def __str__(self) -> str:  # user-friendly printing
        if self.q is None:
            return f"{self.name} (unknown)"
        unit = self.preferred or ureg.si_unit_for(self.q.dim)  # fallback to a sensible SI unit
        if unit is None:
            return f"{self.q.value:.6g} [Dim={self.q.dim}]"
        return f"{self.q.to(unit):.6g} {unit.symbol}"

    def __repr__(self) -> str:  # mirror __str__ for console/debug parity
        return self.__str__()

class FieldSetter(Generic[D]):
    """
    Returned by FieldQuantity.set(value) when no unit is given.
    Supports .using("mps2"), .in_(u.mps2), and fluent .mps2 / .meter_per_second_squared, etc.
    """
    __slots__ = ("_owner", "_value", "_dim")

    def __init__(self, owner: FieldQuantity[D], value: float, dim: "Dimension | None" = None):
        self._owner = owner
        self._value = float(value)
        # When provided, restrict resolution to this dimension
        self._dim = dim

    # ---- explicit helpers ----
    def using(self, unit_name: str) -> FieldQuantity[D]:
        """Set by unit name/alias string."""
        unit = ureg.resolve(unit_name, dim=self._dim)  # must return a Unit or None
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
        unit = ureg.resolve(name, dim=self._dim)
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
            # Show only names for the expected dimension if known; else show all
            if getattr(self, "_dim", None) is not None:
                names = ureg.names_for(self._dim)  # type: ignore[arg-type]
            else:
                names = ureg.all_names()
            return sorted(set(list(base) + list(names)))
        except Exception:
            return base
        

class UnitApplier(Generic[D]):
    """Helper returned by `.to_unit` for ergonomic conversions via attribute or call.

    Usage:
      q.to_unit.meter_per_square_second
      q.to_unit("m/s²")
    """
    __slots__ = ("_owner", "_dim")

    def __init__(self, owner: "FieldQuantity[D]", dim: "Dimension | None" = None):
        self._owner = owner
        self._dim = dim

    def __call__(self, unit: Unit[D] | str) -> "FieldQuantity[D]":
        if isinstance(unit, str):
            resolved = ureg.resolve(unit, dim=self._dim)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved
        # Validate dimension if known
        if self._owner.q is not None and unit.dim != self._owner.q.dim:
            raise TypeError(f"Cannot prefer unit of dimension {unit.dim} for quantity {self._owner.q.dim}")
        # Return a new instance with the same value but preferred unit set
        cls = type(self._owner)
        return cls(self._owner.name, self._owner.q, unit)

    def __getattr__(self, name: str) -> "FieldQuantity[D]":
        unit = ureg.resolve(name, dim=self._dim)
        if unit is None:
            raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")
        return self(unit)

    def __dir__(self):
        base = super().__dir__()
        try:
            names = ureg.all_names()
            return sorted(set(list(base) + names))
        except Exception:
            return base


class UnitChanger(Generic[D]):
    """Helper returned by `.as_unit` to keep the same numeric value but change the unit.

    - If unknown, just change preferred.
    - If known, compute a new underlying SI value such that the displayed numeric remains the same in the chosen unit.
    """
    __slots__ = ("_owner", "_dim")

    def __init__(self, owner: "FieldQuantity[D]", dim: "Dimension | None" = None):
        self._owner = owner
        self._dim = dim

    def __call__(self, unit: Unit[D] | str) -> "FieldQuantity[D]":
        if isinstance(unit, str):
            resolved = ureg.resolve(unit, dim=self._dim)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved
        if self._owner.q is not None and unit.dim != self._owner.q.dim:
            raise TypeError(f"Cannot change to unit of dimension {unit.dim} from {self._owner.q.dim}")
        # If unknown, only set preferred
        if self._owner.q is None:
            cls = type(self._owner)
            return cls(self._owner.name, None, unit)
        # Determine the currently displayed numeric value
        current_pref = self._owner.preferred or ureg.si_unit_for(self._owner.q.dim)
        if current_pref is not None:
            numeric = self._owner.q.to(current_pref)
        else:
            numeric = self._owner.q.value
        # Build new Quantity that displays the same numeric in the chosen unit
        new_q = Q(numeric, unit)
        cls = type(self._owner)
        return cls(self._owner.name, new_q, unit)

    def __getattr__(self, name: str) -> "FieldQuantity[D]":
        unit = ureg.resolve(name, dim=self._dim)
        if unit is None:
            raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")
        return self(unit)

    def __dir__(self):
        base = super().__dir__()
        try:
            names = ureg.all_names()
            return sorted(set(list(base) + names))
        except Exception:
            return base

# ---- generic binding helpers for any FieldQuantity subclass ----
def _get_namespace_dim(ns_cls: type) -> Dimension:
    for v in vars(ns_cls).values():
        if isinstance(v, Unit):
            return v.dim
    raise RuntimeError("Unit namespace has no Unit attributes to derive dimension")


def bind_quantity_namespace(
    quantity_cls: type[FieldQuantity],
    setter_cls: type[FieldSetter],
    unit_namespace: type,
) -> None:
    """
    Attach canonical unit properties from `unit_namespace` onto the provided
    setter and proxy classes for the given quantity class.
    """
    # Build properties
    def _make_setter_prop(unit_name: str):
        def _prop(self):
            return self.in_(getattr(u, unit_name))
        return property(_prop)

    def _make_proxy_prop(unit_name: str):
        def _prop(self):
            return self(getattr(u, unit_name))
        return property(_prop)

    for name, v in vars(unit_namespace).items():
        if isinstance(v, Unit):
            setattr(setter_cls, name, _make_setter_prop(name))
            # Access nested helper classes on the quantity
            to_cls = quantity_cls.ToUnit  # type: ignore[attr-defined]
            as_cls = quantity_cls.AsUnit  # type: ignore[attr-defined]
            setattr(to_cls, name, _make_proxy_prop(name))
            setattr(as_cls, name, _make_proxy_prop(name))



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
