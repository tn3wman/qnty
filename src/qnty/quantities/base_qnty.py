from dataclasses import dataclass

from ..dimensions import Dimension, DIMENSIONLESS
from ..units import Unit, ureg

# ---------- Quantity (stored in SI) ----------
@dataclass(frozen=True)
class Quantity:
    value: float
    dim: Dimension
    def __mul__(self, o: "Quantity|float") -> "Quantity":
        if isinstance(o, Quantity):
            return Quantity(self.value*o.value, self.dim*o.dim)
        return Quantity(self.value*float(o), self.dim)
    def __truediv__(self, o: "Quantity|float") -> "Quantity":
        if isinstance(o, Quantity):
            return Quantity(self.value/o.value, self.dim/o.dim)
        return Quantity(self.value/float(o), self.dim)
    def __pow__(self, p: int) -> "Quantity":
        return Quantity(self.value**p, self.dim**p)
    def __add__(self, o: "Quantity") -> "Quantity":
        if self.dim != o.dim: raise TypeError("Dimension mismatch in addition")
        return Quantity(self.value + o.value, self.dim)
    def __sub__(self, o: "Quantity") -> "Quantity":
        if self.dim != o.dim: raise TypeError("Dimension mismatch in subtraction")
        return Quantity(self.value - o.value, self.dim)
    def to(self, unit: Unit) -> float:
        if unit.dimension != self.dim: raise TypeError("Conversion dimension mismatch")
        return (self.value - unit.si_offset)/unit.si_factor
    def __repr__(self) -> str:
        pu = ureg.preferred_for(self.dim)
        if pu:
            return f"{self.to(pu):.6g} {pu.symbol}"
        return f"{self.value:.6g} [Dim={self.dim.exps}]"

def Q(val: float, unit: Unit) -> Quantity:
    return Quantity(unit.si_factor*val + unit.si_offset, unit.dimension)


class BooleanQuantity(Quantity):
    """A quantity that represents a boolean value but maintains Quantity compatibility.

    This class is used for comparison operations that need to return boolean results
    while maintaining the Expression interface requirement of returning Quantity objects.
    """

    __slots__ = ("_boolean_value",)

    def __init__(self, boolean_value: bool):
        """Initialize with a boolean value."""
        # Store the actual boolean value
        self._boolean_value = boolean_value

        # Initialize parent with numeric representation
        super().__init__(1.0 if boolean_value else 0.0, DIMENSIONLESS)

    def __str__(self) -> str:
        """Display as True/False instead of 1.0/0.0."""
        return str(self._boolean_value)

    def __repr__(self) -> str:
        """Display as BooleanQuantity(True/False)."""
        return f"BooleanQuantity({self._boolean_value})"

    def __bool__(self) -> bool:
        """Return the actual boolean value."""
        return self._boolean_value

    @property
    def boolean_value(self) -> bool:
        """Access the boolean value directly."""
        return self._boolean_value


class TypeSafeSetter:
    """Base class for type-safe setter objects."""
    
    __slots__ = ("variable", "value")
    
    def __init__(self, variable, value: float):
        """Initialize setter with variable and value."""
        self.variable = variable
        self.value = value