"""
Dimension Signatures
====================

Immutable dimension signatures for ultra-fast dimensional analysis using prime number encoding.

This file contains the core DimensionSignature class that provides zero-cost dimensional
compatibility checking through compile-time type system integration.
"""

from dataclasses import dataclass
from typing import ClassVar, final

from .base import BaseDimension


@final
@dataclass(frozen=True, slots=True)
class DimensionSignature:
    """Immutable dimension signature for zero-cost dimensional analysis."""

    # Store as bit pattern for ultra-fast comparison
    _signature: int | float = 1

    # Pre-computed signature cache for common dimensions
    _COMMON_SIGNATURES: ClassVar[dict[tuple[int, ...], int | float]] = {
        (0, 0, 0, 0, 0, 0, 0): 1,  # Dimensionless
        (-1, 0, 0, 0, 0, 0, 0): 0.5,  # L^-1
        (0, 0, -1, 0, 0, 0, 0): 0.2,  # T^-1
        (0, 0, 0, 0, 0, 0, 1): 17,  # J
        (0, 0, 0, 0, 0, 1, 0): 13,  # N
        (0, 0, 0, 0, 1, 0, 0): 11,  # Θ
        (0, 0, 0, 1, 0, 0, 0): 7,  # A
        (0, 0, 1, 0, 0, 0, 0): 5,  # T
        (0, 1, 0, 0, 0, 0, 0): 3,  # M
        (1, 0, 0, 0, 0, 0, 0): 2,  # L
        (-2, 0, 0, 0, 0, 0, 0): 0.25,  # L^-2 L
        (-1, 0, 0, 1, 0, 0, 0): 3.5,  # A L^-1
        (-1, 1, 0, 0, 0, 0, 0): 1.5,  # L^-1 M
        (0, -1, 0, 0, 0, 1, 0): 4.333333333,  # N M^-1
        (0, 0, -2, 0, 0, 0, 0): 0.04,  # T^-2
        (0, 0, -1, 0, 0, 1, 0): 2.6,  # N T^-1
        (0, 1, -1, 0, 0, 0, 0): 0.6,  # M T^-1
        (0, 1, 0, 0, 0, -1, 0): 0.2307692308,  # N^-1 M
        (1, -1, 0, 0, 0, 0, 0): 0.6666666667,  # L M^-1
        (1, 0, -1, 0, 0, 0, 0): 0.4,  # L T^-1
        (1, 0, 0, 0, 1, 0, 0): 22,  # L Θ
        (2, 0, 0, 0, 0, 0, 0): 4,  # L^2
        (-3, 0, 0, 0, 0, 0, 0): 0.125,  # L^-3
        (-2, 0, -1, 0, 0, 0, 0): 0.05,  # L^-2 T^-1
        (-2, 1, 0, 0, 0, 0, 0): 0.75,  # L^-2 M
        (-1, 1, -1, 0, 0, 0, 0): 0.3,  # L^-1 M T^-1
        (0, -1, 1, 1, 0, 0, 0): 11.66666667,  # A M^-1 T
        (0, 0, 1, 1, 0, -1, 0): 2.692307692,  # N^-1 A T
        (0, 1, -2, 0, 0, 0, 0): 0.12,  # M T^-2
        (1, -1, 1, 0, 0, 0, 0): 3.333333333,  # L M^-1 T
        (1, 0, -2, 0, 0, 0, 0): 0.08,  # L T^-2
        (1, 0, 1, 1, 0, 0, 0): 70,  # A L T
        (1, 1, -1, 0, 0, 0, 0): 1.2,  # L M T^-1
        (2, -1, 0, 0, 0, 0, 0): 1.333333333,  # L^2 M^-1
        (2, 0, -1, 0, 0, 0, 0): 0.8,  # L^2 T^-1
        (2, 0, 0, 1, 0, 0, 0): 28,  # A L^2
        (2, 1, 0, 0, 0, 0, 0): 12,  # L^2 M
        (3, 0, 0, 0, 0, 0, 0): 8,  # L^3
        (-3, 0, 0, 0, 0, 1, 0): 1.625,  # N L^-3
        (-3, 1, 0, 0, 0, 0, 0): 0.375,  # L^-3 M
        (-2, 0, -1, 0, 0, 1, 0): 0.65,  # N L^-2 T^-1
        (-2, 1, -1, 0, 0, 0, 0): 0.15,  # L^-2 M T^-1
        (-1, 1, -2, 0, 0, 0, 0): 0.06,  # L^-1 M T^-2
        (0, 1, -3, 0, 0, 0, 0): 0.024,  # M T^-3
        (0, 1, -2, -1, 0, 0, 0): 0.01714285714,  # A^-1 M T^-2
        (1, 1, -2, 0, 0, 0, 0): 0.24,  # L M T^-2
        (2, 0, -2, 0, 0, 0, 0): 0.16,  # L^2 T^-2
        (2, 1, -1, 0, 0, 0, 0): 2.4,  # L^2 M T^-1
        (3, -1, 0, 0, 0, 0, 0): 2.666666667,  # L^3 M^-1
        (3, 0, -1, 0, 0, 0, 0): 1.6,  # L^3 T^-1
    }

    # Instance cache for interning common dimensions
    _INSTANCE_CACHE: ClassVar[dict[int | float, "DimensionSignature"]] = {}

    def __new__(cls, signature: int | float = 1):
        """Optimized constructor with instance interning."""
        if signature in cls._INSTANCE_CACHE:
            return cls._INSTANCE_CACHE[signature]

        instance = object.__new__(cls)

        # Cache common signatures
        if len(cls._INSTANCE_CACHE) < 100:  # Limit cache size
            cls._INSTANCE_CACHE[signature] = instance

        return instance

    @classmethod
    def create(cls, length=0, mass=0, time=0, current=0, temp=0, amount=0, luminosity=0):
        """Create dimension from exponents with optimized lookup."""
        # Check cache first
        key = (length, mass, time, current, temp, amount, luminosity)
        if key in cls._COMMON_SIGNATURES:
            return cls(cls._COMMON_SIGNATURES[key])

        # Fast path for dimensionless
        if not any([length, mass, time, current, temp, amount, luminosity]):
            return cls(1)

        # Compute signature
        signature = 1
        if length != 0:
            signature *= BaseDimension.LENGTH**length
        if mass != 0:
            signature *= BaseDimension.MASS**mass
        if time != 0:
            signature *= BaseDimension.TIME**time
        if current != 0:
            signature *= BaseDimension.CURRENT**current
        if temp != 0:
            signature *= BaseDimension.TEMPERATURE**temp
        if amount != 0:
            signature *= BaseDimension.AMOUNT**amount
        if luminosity != 0:
            signature *= BaseDimension.LUMINOSITY**luminosity

        return cls(signature)

    def __mul__(self, other):
        """Multiply dimensions."""
        return DimensionSignature(self._signature * other._signature)

    def __truediv__(self, other):
        """Divide dimensions."""
        return DimensionSignature(self._signature / other._signature)

    def __pow__(self, power):
        """Raise dimension to a power."""
        if power == 1:
            return self
        if power == 0:
            return DimensionSignature(1)
        return DimensionSignature(self._signature**power)

    def is_compatible(self, other):
        """Check dimensional compatibility."""
        return self._signature == other._signature

    def __eq__(self, other):
        """Check equality."""
        if self is other:
            return True
        return isinstance(other, DimensionSignature) and self._signature == other._signature

    def __hash__(self):
        """Hash based on signature."""
        return hash(self._signature)
