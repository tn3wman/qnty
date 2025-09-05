"""
High-Performance Quantity and Variables
========================================

FastQuantity class and type-safe variables optimized for engineering calculations
with dimensional safety.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, Self, TypeVar

from ...constants import FLOAT_EQUALITY_TOLERANCE
from ...generated.dimensions import (
    AREA,
    DIMENSIONLESS,
    ENERGY_PER_UNIT_AREA,
    FORCE,
    LENGTH,
    PRESSURE,
    SURFACE_TENSION,
    VOLUME,
    DimensionSignature,
)
from ...generated.dimensions import (
    ENERGY_HEAT_WORK as ENERGY,
)
from ...generated.units import AreaUnits, DimensionlessUnits, LengthUnits, PressureUnits, VolumeUnits
from ..units.registry import UnitConstant, UnitDefinition, registry

if TYPE_CHECKING:
    from ...domain.problems.problem import Problem

# TypeVar for generic dimensional types
DimensionType = TypeVar("DimensionType", bound="Quantity")


# Removed object pool system - benchmarking showed it was counter-productive
# Simple cache for small integer values only (most common case)
_SMALL_INTEGER_CACHE: dict[tuple[int, str], Quantity] = {}

# Pre-computed error message templates to eliminate f-string overhead
ERROR_TEMPLATES = {
    "incompatible_add": "Cannot add {} and {}",
    "incompatible_subtract": "Cannot subtract {} from {}",
    "incompatible_dimension": "Unit {} incompatible with expected dimension",
    "unit_not_found": "Unit '{}' not found for {}. Available units: {}",
    "unknown_function": "Unknown function: {}",
    "incompatible_comparison": "Cannot compare incompatible dimensions",
}

# Cache for multiplication/division results - keyed by dimension signature pairs
_MULTIPLICATION_CACHE = {}
_DIVISION_CACHE = {}


# Pre-initialize common dimension cache for performance
def _initialize_dimension_cache():
    """Initialize dimension cache at module load to avoid runtime checks."""
    if not registry._dimension_cache:
        registry._dimension_cache = {
            DIMENSIONLESS._signature: DimensionlessUnits.dimensionless,
            LENGTH._signature: LengthUnits.millimeter,
            PRESSURE._signature: PressureUnits.Pa,
            AREA._signature: AreaUnits.square_millimeter,
            VOLUME._signature: VolumeUnits.cubic_millimeter,  # mm³
            FORCE._signature: UnitConstant(UnitDefinition("newton", "N", FORCE, 1.0)),
            ENERGY._signature: UnitConstant(UnitDefinition("joule", "J", ENERGY, 1.0)),
            SURFACE_TENSION._signature: UnitConstant(UnitDefinition("newton_per_meter", "N/m", SURFACE_TENSION, 1.0)),
            ENERGY_PER_UNIT_AREA._signature: UnitConstant(UnitDefinition("joule_per_square_meter", "J/m²", ENERGY_PER_UNIT_AREA, 1.0)),
        }

    # Pre-populate multiplication cache with comprehensive engineering combinations
    global _MULTIPLICATION_CACHE, _DIVISION_CACHE

    # Create basic unit constants for common results
    force_unit = UnitConstant(UnitDefinition("newton", "N", FORCE, 1.0))
    energy_unit = UnitConstant(UnitDefinition("joule", "J", ENERGY, 1.0))

    _MULTIPLICATION_CACHE = {
        # Basic geometric combinations
        (LENGTH._signature, LENGTH._signature): AreaUnits.square_millimeter,
        (LENGTH._signature, AREA._signature): VolumeUnits.cubic_millimeter,
        (AREA._signature, LENGTH._signature): VolumeUnits.cubic_millimeter,
        # Force and pressure combinations
        (PRESSURE._signature, AREA._signature): force_unit,
        (AREA._signature, PRESSURE._signature): force_unit,
        # Energy combinations
        (FORCE._signature, LENGTH._signature): energy_unit,
        (LENGTH._signature, FORCE._signature): energy_unit,
    }

    _DIVISION_CACHE = {
        # Basic geometric divisions
        (AREA._signature, LENGTH._signature): LengthUnits.millimeter,
        (VOLUME._signature, AREA._signature): LengthUnits.millimeter,
        (VOLUME._signature, LENGTH._signature): AreaUnits.square_millimeter,
        # Force and pressure divisions
        (FORCE._signature, AREA._signature): PressureUnits.Pa,
        # Energy divisions
        (ENERGY._signature, FORCE._signature): LengthUnits.meter,
        (ENERGY._signature, LENGTH._signature): force_unit,
    }


# Component classes for separation of concerns
class ArithmeticOperations:
    """Handles arithmetic operations for quantities."""
    
    @staticmethod
    def add(quantity, other):
        """Add two quantities with dimensional checking."""
        # Optimized addition with early exit and bulk operations
        self_sig, other_sig = quantity._dimension_sig, other._dimension_sig
        if self_sig != other_sig:
            raise ValueError(ERROR_TEMPLATES["incompatible_add"].format(quantity.unit.name, other.unit.name))

        # Ultra-fast path: compare unit names directly
        if quantity.unit.name == other.unit.name:
            return Quantity(quantity.value + other.value, quantity.unit)

        # Convert using cached SI factors (avoid repeated attribute access)
        self_si, other_si = quantity._si_factor, other._si_factor
        other_value = other.value * other_si / self_si
        return Quantity(quantity.value + other_value, quantity.unit)
    
    @staticmethod
    def subtract(quantity, other):
        """Subtract two quantities with dimensional checking."""
        # Optimized subtraction with early exit and bulk operations
        self_sig, other_sig = quantity._dimension_sig, other._dimension_sig
        if self_sig != other_sig:
            raise ValueError(ERROR_TEMPLATES["incompatible_subtract"].format(other.unit.name, quantity.unit.name))

        # Ultra-fast path: compare unit names directly
        if quantity.unit.name == other.unit.name:
            return Quantity(quantity.value - other.value, quantity.unit)

        # Convert using cached SI factors (avoid repeated attribute access)
        self_si, other_si = quantity._si_factor, other._si_factor
        other_value = other.value * other_si / self_si
        return Quantity(quantity.value - other_value, quantity.unit)
    
    @staticmethod
    def multiply(quantity, other):
        """Multiply quantity by another quantity or scalar."""
        # Fast path for numeric types - use type() for speed
        if isinstance(other, int | float):
            return Quantity(quantity.value * other, quantity.unit)

        # Handle UnifiedVariable objects by using their quantity
        # Check for quantity attribute without importing (duck typing)
        if hasattr(other, "quantity") and getattr(other, "quantity", None) is not None:
            other = other.quantity  # type: ignore

        # Type narrowing: at this point other should be Quantity
        if not isinstance(other, Quantity):
            raise TypeError(f"Expected Quantity, got {type(other)}")

        # Check multiplication cache first
        cache_key = (quantity._dimension_sig, other._dimension_sig)
        if cache_key in _MULTIPLICATION_CACHE:
            result_unit = _MULTIPLICATION_CACHE[cache_key]
            # Fast computation with cached unit
            result_si_value = (quantity.value * quantity._si_factor) * (other.value * other._si_factor)
            return Quantity(result_si_value / result_unit.si_factor, result_unit)

        # Fast dimensional analysis using cached signatures
        result_dimension_sig = quantity._dimension_sig * other._dimension_sig

        # Use cached SI factors for conversion (bulk operations)
        self_si, other_si = quantity._si_factor, other._si_factor
        result_si_value = (quantity.value * self_si) * (other.value * other_si)

        # Fast path for common dimension combinations
        result_unit = UnitResolution.find_result_unit_fast(quantity, result_dimension_sig)
        result_value = result_si_value / result_unit.si_factor

        # Cache the result for future use (limit cache size)
        if len(_MULTIPLICATION_CACHE) < 100:
            _MULTIPLICATION_CACHE[cache_key] = result_unit

        return Quantity(result_value, result_unit)
    
    @staticmethod
    def divide(quantity, other):
        """Divide quantity by another quantity or scalar."""
        # Fast path for numeric types - use type() for speed
        if isinstance(other, int | float):
            return Quantity(quantity.value / other, quantity.unit)

        # Handle UnifiedVariable objects by using their quantity
        if hasattr(other, "quantity") and getattr(other, "quantity", None) is not None:
            other = other.quantity  # type: ignore

        # Type narrowing: at this point other should be Quantity
        if not isinstance(other, Quantity):
            raise TypeError(f"Expected Quantity, got {type(other)}")

        # Check division cache first
        cache_key = (quantity._dimension_sig, other._dimension_sig)
        if cache_key in _DIVISION_CACHE:
            result_unit = _DIVISION_CACHE[cache_key]
            # Fast computation with cached unit
            result_si_value = (quantity.value * quantity._si_factor) / (other.value * other._si_factor)
            return Quantity(result_si_value / result_unit.si_factor, result_unit)

        # Fast dimensional analysis using cached signatures
        result_dimension_sig = quantity._dimension_sig / other._dimension_sig

        # Use cached SI factors for conversion (bulk operations)
        self_si, other_si = quantity._si_factor, other._si_factor
        result_si_value = (quantity.value * self_si) / (other.value * other_si)

        # Fast path for common dimension combinations
        result_unit = UnitResolution.find_result_unit_fast(quantity, result_dimension_sig)
        result_value = result_si_value / result_unit.si_factor

        # Cache the result for future use (limit cache size)
        if len(_DIVISION_CACHE) < 100:
            _DIVISION_CACHE[cache_key] = result_unit

        return Quantity(result_value, result_unit)


class ComparisonOperations:
    """Handles comparison operations for quantities."""
    
    @staticmethod
    def less_than(quantity, other):
        """Compare if this quantity is less than another."""
        # Optimized comparison with bulk operations
        if quantity._dimension_sig != other._dimension_sig:
            raise ValueError(ERROR_TEMPLATES["incompatible_comparison"])

        # Fast path for same units (use name comparison for speed)
        if quantity.unit.name == other.unit.name:
            return quantity.value < other.value

        # Convert using cached SI factors (bulk assignment)
        self_si, other_si = quantity._si_factor, other._si_factor
        return quantity.value < (other.value * other_si / self_si)
    
    @staticmethod
    def equals(quantity, other):
        """Check equality between quantities."""
        if not isinstance(other, Quantity):
            return False
        if quantity._dimension_sig != other._dimension_sig:
            return False

        # Fast path for same units (use name comparison)
        if quantity.unit.name == other.unit.name:
            return abs(quantity.value - other.value) < FLOAT_EQUALITY_TOLERANCE

        # Convert using cached SI factors (bulk assignment)
        self_si, other_si = quantity._si_factor, other._si_factor
        return abs(quantity.value - (other.value * other_si / self_si)) < FLOAT_EQUALITY_TOLERANCE


class UnitConversions:
    """Handles unit conversion operations."""
    
    @staticmethod
    def to(quantity, target_unit):
        """Convert quantity to target unit."""
        # Ultra-fast same unit check using name comparison
        if quantity.unit.name == target_unit.name:
            return Quantity(quantity.value, target_unit)

        # Direct SI factor conversion - avoid registry lookup
        converted_value = quantity.value * quantity._si_factor / target_unit.si_factor
        return Quantity(converted_value, target_unit)


class QuantityFormatting:
    """Handles string formatting for quantities."""
    
    @staticmethod
    def to_string(quantity):
        """String representation of the quantity."""
        # Optimized string representation (caching removed for simplicity)
        return f"{quantity.value} {quantity.unit.symbol}"
    
    @staticmethod
    def to_repr(quantity):
        """Detailed representation of the quantity."""
        return f"Quantity({quantity.value}, {quantity.unit.name})"


class UnitResolution:
    """Handles unit resolution for dimensional operations."""
    
    @staticmethod
    def find_result_unit_fast(quantity, result_dimension_sig: int | float) -> UnitConstant:
        """Ultra-fast unit finding using pre-cached dimension signatures."""
        # O(1) lookup for common dimensions (cache initialized at module load)
        if result_dimension_sig in registry._dimension_cache:
            return registry._dimension_cache[result_dimension_sig]

        # For rare combined dimensions, create SI base unit with descriptive name
        result_dimension = DimensionSignature(result_dimension_sig)

        # Create descriptive name based on dimensional analysis
        si_name = UnitResolution.create_si_unit_name(quantity, result_dimension)
        si_symbol = UnitResolution.create_si_unit_symbol(quantity, result_dimension)

        temp_unit = UnitDefinition(name=si_name, symbol=si_symbol, dimension=result_dimension, si_factor=1.0)
        result_unit = UnitConstant(temp_unit)

        # Cache for future use
        registry._dimension_cache[result_dimension_sig] = result_unit
        return result_unit
    
    @staticmethod
    def create_si_unit_name(_quantity, dimension: DimensionSignature) -> str:
        """Create descriptive SI unit name based on dimensional analysis."""
        # For now, return a generic SI unit name. In the future, this could be enhanced
        # to parse the dimension signature and create descriptive names like "newton_per_meter"
        return f"si_derived_unit_{abs(hash(dimension._signature)) % 10000}"
    
    @staticmethod
    def create_si_unit_symbol(_quantity, dimension: DimensionSignature) -> str:
        """Create SI unit symbol based on dimensional analysis."""
        # For complex units, return descriptive symbol based on common engineering units
        # Use dimension signature for unique symbol generation
        return f"SI_{abs(hash(dimension._signature)) % 1000}"
    
    @staticmethod
    def find_result_unit(quantity, result_dimension: DimensionSignature) -> UnitConstant:
        """Legacy method - kept for compatibility."""
        return UnitResolution.find_result_unit_fast(quantity, result_dimension._signature)


class TypeSafeSetter:
    """Basic type-safe setter that accepts compatible units."""

    def __init__(self, variable, value: float):
        self.variable = variable
        self.value = value

    def with_unit(self, unit: UnitConstant):
        """Set with type-safe unit constant."""
        if not self.variable.expected_dimension.is_compatible(unit.dimension):
            raise TypeError(ERROR_TEMPLATES["incompatible_dimension"].format(unit.name))

        self.variable.quantity = Quantity(self.value, unit)
        return self.variable


class Quantity:
    """High-performance quantity optimized for engineering calculations."""

    __slots__ = ("value", "unit", "dimension", "_si_factor", "_dimension_sig")

    def __init__(self, value: float, unit: UnitConstant):
        # Optimized initialization with cached values for performance
        self.value = value if isinstance(value, float) else float(value)
        self.unit = unit
        self.dimension = unit.dimension
        # Cache commonly used values to avoid repeated attribute access
        self._si_factor = unit.si_factor
        self._dimension_sig = unit.dimension._signature

    @classmethod
    def get_cached(cls, value: int | float, unit: UnitConstant):
        """Get cached instance for small integers, otherwise create new."""
        # Only cache small integers (most common case in engineering)
        if isinstance(value, int | float) and -10 <= value <= 10 and value == int(value):
            cache_key = (int(value), unit.name)
            if cache_key in _SMALL_INTEGER_CACHE:
                return _SMALL_INTEGER_CACHE[cache_key]

            # Create and cache if under limit
            if len(_SMALL_INTEGER_CACHE) < 100:  # Small cache limit
                obj = cls(float(value), unit)
                _SMALL_INTEGER_CACHE[cache_key] = obj
                return obj

        # Regular creation for everything else
        return cls(value, unit)

    def __str__(self) -> str:
        return QuantityFormatting.to_string(self)

    def __repr__(self) -> str:
        return QuantityFormatting.to_repr(self)

    # Ultra-fast arithmetic with dimensional checking
    def __add__(self, other: Quantity) -> Quantity:
        return ArithmeticOperations.add(self, other)

    def __sub__(self, other: Quantity) -> Quantity:
        return ArithmeticOperations.subtract(self, other)

    def __mul__(self, other: Quantity | float | int) -> Quantity:
        return ArithmeticOperations.multiply(self, other)

    def __rmul__(self, other: float | int) -> Quantity:
        """Reverse multiplication for cases like 2 * quantity."""
        if isinstance(other, int | float):
            return Quantity(other * self.value, self.unit)
        return NotImplemented

    def __truediv__(self, other: Quantity | float | int) -> Quantity:
        return ArithmeticOperations.divide(self, other)

    def _find_result_unit_fast(self, result_dimension_sig: int | float) -> UnitConstant:
        """Delegate to unit resolution component."""
        return UnitResolution.find_result_unit_fast(self, result_dimension_sig)
    
    def _create_si_unit_name(self, dimension: DimensionSignature) -> str:
        """Delegate to unit resolution component."""
        return UnitResolution.create_si_unit_name(self, dimension)
    
    def _create_si_unit_symbol(self, dimension: DimensionSignature) -> str:
        """Delegate to unit resolution component."""
        return UnitResolution.create_si_unit_symbol(self, dimension)
    
    def _find_result_unit(self, result_dimension: DimensionSignature) -> UnitConstant:
        """Legacy method - kept for compatibility."""
        return UnitResolution.find_result_unit(self, result_dimension)

    # Ultra-fast comparisons
    def __lt__(self, other: Quantity) -> bool:
        return ComparisonOperations.less_than(self, other)

    def __eq__(self, other) -> bool:
        return ComparisonOperations.equals(self, other)

    def to(self, target_unit: UnitConstant) -> Quantity:
        """Ultra-fast unit conversion with optimized same-unit check."""
        return UnitConversions.to(self, target_unit)




# Initialize dimension cache at module load for performance
_initialize_dimension_cache()
