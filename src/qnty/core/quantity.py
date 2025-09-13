"""
Unified Quantity class that combines the functionality of both Quantity and FieldQuantity.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar, cast, overload

from .dimension import Dimension
from .unit import Unit, ureg

if TYPE_CHECKING:
    from . import quantity_catalog

D = TypeVar("D")

@dataclass
class Quantity(Generic[D]):
    """
    A unified quantity that can be either:
    - A concrete value with dimension (when value is set)
    - A named placeholder (when value is None)

    Supports arithmetic, unit conversions, and all FieldQuantity features.
    """
    name: str
    dim: Dimension
    value: float | None = None
    preferred: Unit[D] | None = None

    # Factory methods for different use cases
    @classmethod
    def from_value(cls, value: float, unit: Unit[D], name: str = "unnamed") -> Quantity[D]:
        """Create a quantity from a value and unit (replaces Q function)."""
        return cls(
            name=name,
            dim=unit.dim,
            value=unit.si_factor * value + unit.si_offset
        )

    @classmethod
    def unknown(cls, name: str, dim: Dimension, preferred: Unit[D] | None = None) -> Quantity[D]:
        """Create an unknown/placeholder quantity."""
        return cls(name=name, dim=dim, preferred=preferred)

    # ---- Properties ----
    @property
    def is_known(self) -> bool:
        return self.value is not None

    @property
    def quantity(self) -> Quantity[D] | None:
        """Compatibility property for code expecting .q"""
        return self if self.value is not None else None

    # ---- Setting values ----
    @overload
    def set(self, value: float) -> QuantitySetter[D]: ...
    @overload
    def set(self, value: float, unit: Unit[D]) -> Self: ...
    @overload
    def set(self, value: float, unit: str) -> Self: ...

    def set(self, value: float, unit: Unit[D] | str | None = None) -> QuantitySetter[D] | Self:
        """Set the value of this quantity."""
        if unit is None:
            return QuantitySetter(self, value)

        if isinstance(unit, str):
            resolved = ureg.resolve(unit)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved

        # Create new instance with value set
        new_q = Quantity(
            name=self.name,
            dim=self.dim,
            value=unit.si_factor * value + unit.si_offset,
            preferred=self.preferred or unit
        )
        return new_q  # type: ignore

    def prefer(self, unit: Unit[D]) -> Quantity[D]:
        """Set preferred display unit."""
        return Quantity(
            name=self.name,
            dim=self.dim,
            value=self.value,
            preferred=unit
        )

    @property
    def to_unit(self) -> UnitApplier[D]:
        """Convert to different unit via attribute access."""
        return UnitApplier(self)

    @property
    def as_unit(self) -> UnitChanger[D]:
        """Change display unit via attribute access."""
        return UnitChanger(self)

    # ----- arithmetic -----
    def __mul__(self, other: Quantity | float | int) -> Quantity:
        if isinstance(other, Quantity):
            if self.value is None or other.value is None:
                raise ValueError("Cannot perform arithmetic on unknown quantities")
            result_value = self.value * other.value
            return Quantity(name=f"{result_value}", dim=self.dim * other.dim, value=result_value)
        if self.value is None:
            raise ValueError("Cannot perform arithmetic on unknown quantities")
        result_value = self.value * float(other)
        return Quantity(name=f"{result_value}", dim=self.dim, value=result_value)

    def __truediv__(self, other: Quantity | float | int) -> Quantity:
        if isinstance(other, Quantity):
            if self.value is None or other.value is None:
                raise ValueError("Cannot perform arithmetic on unknown quantities")
            result_value = self.value / other.value
            return Quantity(name=f"{result_value}", dim=self.dim / other.dim, value=result_value)
        if self.value is None:
            raise ValueError("Cannot perform arithmetic on unknown quantities")
        result_value = self.value / float(other)
        return Quantity(name=f"{result_value}", dim=self.dim, value=result_value)

    def __pow__(self, k: int) -> Quantity:
        if self.value is None:
            raise ValueError("Cannot perform arithmetic on unknown quantities")
        result_value = self.value ** k
        return Quantity(name=f"{result_value}", dim=self.dim ** k, value=result_value)

    def __add__(self, other: Quantity) -> Quantity:
        if self.dim != other.dim:
            raise TypeError("Dimension mismatch in addition")
        if self.value is None or other.value is None:
            raise ValueError("Cannot perform arithmetic on unknown quantities")
        result_value = self.value + other.value
        return Quantity(name=f"{result_value}", dim=self.dim, value=result_value)

    def __sub__(self, other: Quantity) -> Quantity:
        if self.dim != other.dim:
            raise TypeError("Dimension mismatch in subtraction")
        if self.value is None or other.value is None:
            raise ValueError("Cannot perform arithmetic on unknown quantities")
        result_value = self.value - other.value
        return Quantity(name=f"{result_value}", dim=self.dim, value=result_value)

    # ---- Comparison operators ----
    def __eq__(self, other: object) -> bool:
        """Check equality between quantities, accounting for units."""
        if not isinstance(other, Quantity):
            return NotImplemented

        # Check dimension compatibility
        if self.dim != other.dim:
            return False

        # If either value is unknown, they're not equal
        if self.value is None or other.value is None:
            return False

        # Compare SI values (both are stored in SI units internally)
        # Use a small tolerance for floating point comparison
        return abs(self.value - other.value) < 1e-10

    def __ne__(self, other: object) -> bool:
        """Check inequality between quantities."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other: Quantity) -> bool:
        """Check if this quantity is less than another."""
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dim != other.dim:
            raise TypeError(f"Cannot compare quantities with different dimensions: {self.dim} vs {other.dim}")

        if self.value is None or other.value is None:
            raise ValueError("Cannot compare unknown quantities")

        # Compare SI values
        return self.value < other.value

    def __le__(self, other: Quantity) -> bool:
        """Check if this quantity is less than or equal to another."""
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dim != other.dim:
            raise TypeError(f"Cannot compare quantities with different dimensions: {self.dim} vs {other.dim}")

        if self.value is None or other.value is None:
            raise ValueError("Cannot compare unknown quantities")

        # Compare SI values
        return self.value <= other.value

    def __gt__(self, other: Quantity) -> bool:
        """Check if this quantity is greater than another."""
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dim != other.dim:
            raise TypeError(f"Cannot compare quantities with different dimensions: {self.dim} vs {other.dim}")

        if self.value is None or other.value is None:
            raise ValueError("Cannot compare unknown quantities")

        # Compare SI values
        return self.value > other.value

    def __ge__(self, other: Quantity) -> bool:
        """Check if this quantity is greater than or equal to another."""
        if not isinstance(other, Quantity):
            return NotImplemented

        if self.dim != other.dim:
            raise TypeError(f"Cannot compare quantities with different dimensions: {self.dim} vs {other.dim}")

        if self.value is None or other.value is None:
            raise ValueError("Cannot compare unknown quantities")

        # Compare SI values
        return self.value >= other.value

    def __float__(self) -> float:
        if not self.dim.is_dimensionless():
            raise TypeError("Cannot convert non-dimensionless quantity to float")
        if self.dim.is_angle():
            raise TypeError("NOT IMPLEMENTED YET")
        if self.value is None:
            raise ValueError("Cannot convert unknown quantity to float")
        return self.value

    # ---- Display ----
    def __str__(self) -> str:
        if self.value is None:
            return f"{self.name} (unknown)" if self.name else "Unknown quantity"

        unit = self.preferred or ureg.preferred_for(self.dim) or ureg.si_unit_for(self.dim)
        if unit is None:
            return f"{self.value:.6g} [Dim={self.dim}]"
        converted_quantity = self.to_unit(unit)
        return f"{converted_quantity.value:.6g} {unit.symbol}"

    def __repr__(self) -> str:
        return self.__str__()


# Compatibility function with automatic dimension detection and proper typing
@overload
def Q(val: float, unit: str) -> Quantity: ...

@overload
def Q(val: float, unit: Unit[D]) -> Quantity[D]: ...

if TYPE_CHECKING:
    from .unit_catalog import AccelerationUnits, DimensionlessUnits, LengthUnits

    @overload
    def Q(val: float, unit: type[AccelerationUnits]) -> quantity_catalog.Acceleration: ...

    @overload
    def Q(val: float, unit: type[LengthUnits]) -> quantity_catalog.Length: ...

    @overload
    def Q(val: float, unit: type[DimensionlessUnits]) -> quantity_catalog.Dimensionless: ...

def Q(val: float, unit: Unit[D] | str | type) -> Quantity:
    """Create a quantity from value and unit string with automatic dimension detection and proper quantity type."""
    if isinstance(unit, str):
        resolved_unit = ureg.resolve(unit)
        if resolved_unit is None:
            raise ValueError(f"Unknown unit '{unit}'")
        unit = resolved_unit
    elif isinstance(unit, type):
        # Check if it's a UnitNamespace class
        from .unit import UnitNamespace
        if issubclass(unit, UnitNamespace):
            # Get the preferred unit from the UnitNamespace class
            preferred_name = getattr(unit, '__preferred__', None)
            if preferred_name is None:
                raise ValueError(f"UnitNamespace {unit.__name__} has no __preferred__ attribute")
            unit = getattr(unit, preferred_name)
        else:
            raise ValueError(f"Invalid unit type: {type(unit)}")

    # Import quantity classes here to avoid circular imports
    from . import quantity_catalog

    # At this point, unit is guaranteed to be a Unit object, not a string or type
    assert not isinstance(unit, str | type)

    # Create a registry mapping dimensions to quantity classes
    dimension_to_class = {
        quantity_catalog.Acceleration('').dim: quantity_catalog.Acceleration,
        quantity_catalog.Length('').dim: quantity_catalog.Length,
        quantity_catalog.Dimensionless('').dim: quantity_catalog.Dimensionless,
    }

    # Check if we have a specialized quantity class for this dimension
    quantity_class = dimension_to_class.get(unit.dim)
    if quantity_class:
        # Create instance of the specialized class with value converted to SI
        si_value = unit.si_factor * val + unit.si_offset
        return quantity_class(
            name="Q",
            value=si_value,
            preferred=unit
        )

    # Fallback to generic Quantity
    si_value = unit.si_factor * val + unit.si_offset
    return Quantity(
        name="Q",
        dim=unit.dim,
        value=si_value,
        preferred=unit
    )


# ---- Setter classes ----
class QuantitySetter(Generic[D]):
    """Fluent setter for quantities when unit not specified."""
    __slots__ = ("_owner", "_value", "_dim")

    def __init__(self, owner: Quantity[D], value: float):
        self._owner = owner
        self._value = float(value)
        self._dim = owner.dim

    def using(self, unit_name: str) -> Quantity[D]:
        """Set by unit name/alias string."""
        unit = ureg.resolve(unit_name, dim=self._dim)
        if unit is None:
            raise AttributeError(f"Unknown unit '{unit_name}'")
        return self._owner.set(self._value, unit)

    def in_(self, unit: Unit[D]) -> Quantity[D]:
        return self._owner.set(self._value, unit)

    def __getattr__(self, name: str) -> Quantity[D]:
        """Resolve attribute name to a Unit and apply."""
        unit = ureg.resolve(name, dim=self._dim)
        if unit is None:
            raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")
        return self._owner.set(self._value, unit)

    def __dir__(self):
        base = super().__dir__()
        try:
            if self._dim is not None:
                names = ureg.names_for(self._dim)
            else:
                names = ureg.all_names()
            return sorted(set(list(base) + list(names)))
        except Exception:
            return base


class UnitApplier(Generic[D]):
    """Helper for .to_unit property."""
    __slots__ = ("_q", "_dim")

    def __init__(self, q: Quantity[D]):
        self._q = q
        self._dim = q.dim

    def __call__(self, unit: Unit[D] | str) -> Quantity[D]:
        if isinstance(unit, str):
            resolved = ureg.resolve(unit, dim=self._dim)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved

        # Convert from SI to target unit: (si_value - offset) / factor
        if self._q.value is None:
            raise ValueError(f"Cannot convert unknown quantity '{self._q.name}' to unit")
        converted_value = (self._q.value - unit.si_offset) / unit.si_factor
        return Quantity(
            name="converted",
            dim=self._dim,
            value=converted_value,
            preferred=unit
        )

    def __getattr__(self, name: str) -> Quantity[D]:
        unit = ureg.resolve(name, dim=self._dim)
        if unit is None:
            raise AttributeError(f"No unit '{name}' for dimension {self._dim}")
        return self(unit)


class UnitChanger(Generic[D]):
    """Helper for .as_unit property."""
    __slots__ = ("_q", "_dim")

    def __init__(self, q: Quantity[D]):
        self._q = q
        self._dim = q.dim

    def __call__(self, unit: Unit[D] | str) -> Quantity[D]:
        if isinstance(unit, str):
            resolved = ureg.resolve(unit, dim=self._dim)
            if resolved is None:
                raise ValueError(f"Unknown unit '{unit}'")
            unit = resolved

        # For as_unit, we want to keep the display value the same
        # So if current display is "25 ft/s²", we want new display to be "25 m/s²"
        if self._q.value is None:
            raise ValueError(f"Cannot change unit of unknown quantity '{self._q.name}'")

        current_unit = self._q.preferred or ureg.preferred_for(self._dim) or ureg.si_unit_for(self._dim)
        if current_unit:
            # Convert from SI to current display unit: (si_value - offset) / factor
            display_value = (self._q.value - current_unit.si_offset) / current_unit.si_factor
        else:
            display_value = self._q.value

        # Convert this display value to SI for storage
        si_value = unit.si_factor * display_value + unit.si_offset

        return Quantity(
            name=self._q.name,
            dim=self._dim,
            value=si_value,
            preferred=unit
        )

    def __getattr__(self, name: str) -> Quantity[D]:
        unit = ureg.resolve(name, dim=self._dim)
        if unit is None:
            raise AttributeError(f"No unit '{name}' for dimension {self._dim}")
        return self(unit)


# For backwards compatibility
FieldQuantity = Quantity
FieldSetter = QuantitySetter
