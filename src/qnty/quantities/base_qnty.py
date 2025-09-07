"""
High-Performance Quantity and Variables
========================================

FastQuantity class and type-safe variables optimized for engineering calculations
with dimensional safety.
"""

from __future__ import annotations

from typing import TypeVar

from ..constants import FLOAT_EQUALITY_TOLERANCE
from ..dimensions.field_dims import (
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
from ..dimensions.field_dims import (
    ENERGY_HEAT_WORK as ENERGY,
)
from ..units.field_units import AreaUnits, DimensionlessUnits, LengthUnits, PressureUnits, VolumeUnits
from ..units.registry import UnitConstant, UnitDefinition, registry

# TypeVar for generic dimensional types
DimensionType = TypeVar("DimensionType", bound="Quantity")


# Global state management and caching system
class CacheManager:
    """Centralized cache management for better encapsulation and control."""

    def __init__(self):
        self.small_integer_cache: dict[tuple[int, str], Quantity] = {}
        self.multiplication_cache: dict[tuple[int | float, int | float], UnitConstant] = {}
        self.division_cache: dict[tuple[int | float, int | float], UnitConstant] = {}
        self.max_cache_size = 100

    def get_cached_quantity(self, value: int | float, unit: UnitConstant) -> Quantity | None:
        """Get cached quantity for small integers."""
        if isinstance(value, int | float) and -10 <= value <= 10 and value == int(value):
            cache_key = (int(value), unit.name)
            return self.small_integer_cache.get(cache_key)
        return None

    def cache_quantity(self, value: int | float, unit: UnitConstant, quantity: Quantity) -> None:
        """Cache quantity if under size limit."""
        if len(self.small_integer_cache) < self.max_cache_size:
            cache_key = (int(value), unit.name)
            self.small_integer_cache[cache_key] = quantity

    def get_multiplication_result(self, left_sig: int | float, right_sig: int | float) -> UnitConstant | None:
        """Get cached multiplication result."""
        return self.multiplication_cache.get((left_sig, right_sig))

    def cache_multiplication_result(self, left_sig: int | float, right_sig: int | float, result_unit: UnitConstant) -> None:
        """Cache multiplication result if under size limit."""
        if len(self.multiplication_cache) < self.max_cache_size:
            self.multiplication_cache[(left_sig, right_sig)] = result_unit

    def get_division_result(self, left_sig: int | float, right_sig: int | float) -> UnitConstant | None:
        """Get cached division result."""
        return self.division_cache.get((left_sig, right_sig))

    def cache_division_result(self, left_sig: int | float, right_sig: int | float, result_unit: UnitConstant) -> None:
        """Cache division result if under size limit."""
        if len(self.division_cache) < self.max_cache_size:
            self.division_cache[(left_sig, right_sig)] = result_unit

    def initialize_common_operations(self) -> None:
        """Initialize common dimensional operations cache."""
        if not registry._dimension_cache:
            registry._dimension_cache = {
                DIMENSIONLESS._signature: DimensionlessUnits.dimensionless,
                LENGTH._signature: LengthUnits.millimeter,
                PRESSURE._signature: PressureUnits.Pa,
                AREA._signature: AreaUnits.square_millimeter,
                VOLUME._signature: VolumeUnits.cubic_millimeter,
                FORCE._signature: UnitConstant(UnitDefinition("newton", "N", FORCE, 1.0)),
                ENERGY._signature: UnitConstant(UnitDefinition("joule", "J", ENERGY, 1.0)),
                SURFACE_TENSION._signature: UnitConstant(UnitDefinition("newton_per_meter", "N/m", SURFACE_TENSION, 1.0)),
                ENERGY_PER_UNIT_AREA._signature: UnitConstant(UnitDefinition("joule_per_square_meter", "J/m²", ENERGY_PER_UNIT_AREA, 1.0)),
            }

        # Pre-populate common engineering combinations with extensive coverage
        force_unit = UnitConstant(UnitDefinition("newton", "N", FORCE, 1.0))
        energy_unit = UnitConstant(UnitDefinition("joule", "J", ENERGY, 1.0))
        surface_tension_unit = UnitConstant(UnitDefinition("newton_per_meter", "N/m", SURFACE_TENSION, 1.0))
        energy_per_area_unit = UnitConstant(UnitDefinition("joule_per_square_meter", "J/m²", ENERGY_PER_UNIT_AREA, 1.0))

        # Create comprehensive multiplication cache with all common engineering patterns
        multiplication_patterns = {
            # Basic geometric operations (most common)
            (LENGTH._signature, LENGTH._signature): AreaUnits.square_millimeter,
            (LENGTH._signature, AREA._signature): VolumeUnits.cubic_millimeter,
            (AREA._signature, LENGTH._signature): VolumeUnits.cubic_millimeter,
            (AREA._signature, AREA._signature): UnitConstant(UnitDefinition("m4", "m⁴", 
                DimensionSignature(AREA._signature * AREA._signature), 1e-12)),  # mm⁴
            
            # Force and pressure operations (ASME common)
            (PRESSURE._signature, AREA._signature): force_unit,
            (AREA._signature, PRESSURE._signature): force_unit,
            (FORCE._signature, LENGTH._signature): energy_unit,
            (LENGTH._signature, FORCE._signature): energy_unit,
            (FORCE._signature, FORCE._signature): UnitConstant(UnitDefinition("N2", "N²", 
                DimensionSignature(FORCE._signature * FORCE._signature), 1.0)),
            
            # ASME-specific: Pressure × Length = Force (P×D term in hoop stress)
            (PRESSURE._signature, LENGTH._signature): force_unit,
            (LENGTH._signature, PRESSURE._signature): force_unit,
            (PRESSURE._signature, PRESSURE._signature): UnitConstant(UnitDefinition("Pa2", "Pa²", 
                DimensionSignature(PRESSURE._signature * PRESSURE._signature), 1.0)),
            
            # Advanced engineering combinations
            (PRESSURE._signature, VOLUME._signature): energy_unit,  # PV work
            (VOLUME._signature, PRESSURE._signature): energy_unit,
            (FORCE._signature, AREA._signature): energy_unit,  # Force × Area = Energy
            (AREA._signature, FORCE._signature): energy_unit,
            (ENERGY._signature, LENGTH._signature): force_unit,  # Energy/Length = Force
            (LENGTH._signature, ENERGY._signature): force_unit,
            (ENERGY._signature, AREA._signature): energy_per_area_unit,
            (AREA._signature, ENERGY._signature): energy_per_area_unit,
            (FORCE._signature, LENGTH._signature * LENGTH._signature): energy_unit,  # Moment × Length = Energy
            
            # Surface tension operations
            (SURFACE_TENSION._signature, LENGTH._signature): force_unit,
            (LENGTH._signature, SURFACE_TENSION._signature): force_unit,
            
            # Dimensionless combinations (extremely common in ASME equations - factor of safety, ratios, etc.)
            (PRESSURE._signature, DIMENSIONLESS._signature): PressureUnits.Pa,
            (DIMENSIONLESS._signature, PRESSURE._signature): PressureUnits.Pa,
            (LENGTH._signature, DIMENSIONLESS._signature): LengthUnits.millimeter,
            (DIMENSIONLESS._signature, LENGTH._signature): LengthUnits.millimeter,
            (AREA._signature, DIMENSIONLESS._signature): AreaUnits.square_millimeter,
            (DIMENSIONLESS._signature, AREA._signature): AreaUnits.square_millimeter,
            (VOLUME._signature, DIMENSIONLESS._signature): VolumeUnits.cubic_millimeter,
            (DIMENSIONLESS._signature, VOLUME._signature): VolumeUnits.cubic_millimeter,
            (FORCE._signature, DIMENSIONLESS._signature): force_unit,
            (DIMENSIONLESS._signature, FORCE._signature): force_unit,
            (ENERGY._signature, DIMENSIONLESS._signature): energy_unit,
            (DIMENSIONLESS._signature, ENERGY._signature): energy_unit,
            (DIMENSIONLESS._signature, DIMENSIONLESS._signature): DimensionlessUnits.dimensionless,
        }

        self.multiplication_cache.update(multiplication_patterns)

        self.division_cache.update(
            {
                # Basic geometric divisions
                (AREA._signature, LENGTH._signature): LengthUnits.millimeter,
                (VOLUME._signature, AREA._signature): LengthUnits.millimeter,
                (VOLUME._signature, LENGTH._signature): AreaUnits.square_millimeter,
                
                # Force and pressure divisions
                (FORCE._signature, AREA._signature): PressureUnits.Pa,
                (ENERGY._signature, FORCE._signature): LengthUnits.meter,
                (ENERGY._signature, LENGTH._signature): force_unit,
                
                # ASME-specific: Force ÷ Length = Pressure (common in final result)
                (FORCE._signature, LENGTH._signature): PressureUnits.Pa,
                
                # Dimensionless divisions (maintain original units)
                (PRESSURE._signature, DIMENSIONLESS._signature): PressureUnits.Pa,
                (LENGTH._signature, DIMENSIONLESS._signature): LengthUnits.millimeter,
                (FORCE._signature, DIMENSIONLESS._signature): force_unit,
                
                # Combined unit divisions (P×D ÷ P = D pattern in ASME)
                (force_unit.dimension._signature, PRESSURE._signature): LengthUnits.millimeter,
            }
        )


# Global cache manager instance
_cache_manager = CacheManager()


# Error message constants for better maintainability
class ErrorMessages:
    """Centralized error message templates."""

    INCOMPATIBLE_ADD = "Cannot add {} and {}"
    INCOMPATIBLE_SUBTRACT = "Cannot subtract {} from {}"
    INCOMPATIBLE_DIMENSION = "Unit {} incompatible with expected dimension"
    UNIT_NOT_FOUND = "Unit '{}' not found for {}. Available units: {}"
    UNKNOWN_FUNCTION = "Unknown function: {}"
    INCOMPATIBLE_COMPARISON = "Cannot compare incompatible dimensions"


# Component classes for separation of concerns
class ArithmeticOperations:
    """Handles arithmetic operations for quantities."""

    @staticmethod
    def add(quantity, other):
        """Add two quantities with dimensional checking."""
        if quantity._dimension_sig != other._dimension_sig:
            raise ValueError(ErrorMessages.INCOMPATIBLE_ADD.format(quantity.unit.name, other.unit.name))

        # Fast path for same units
        if quantity.unit.name == other.unit.name:
            return Quantity(quantity.value + other.value, quantity.unit)

        # Convert using cached SI factors
        converted_value = other.value * other._si_factor / quantity._si_factor
        return Quantity(quantity.value + converted_value, quantity.unit)

    @staticmethod
    def subtract(quantity, other):
        """Subtract two quantities with dimensional checking."""
        if quantity._dimension_sig != other._dimension_sig:
            raise ValueError(ErrorMessages.INCOMPATIBLE_SUBTRACT.format(other.unit.name, quantity.unit.name))

        # Fast path for same units
        if quantity.unit.name == other.unit.name:
            return Quantity(quantity.value - other.value, quantity.unit)

        # Convert using cached SI factors
        converted_value = other.value * other._si_factor / quantity._si_factor
        return Quantity(quantity.value - converted_value, quantity.unit)

    @staticmethod
    def multiply(quantity, other):
        """Multiply quantity by another quantity or scalar with ultra-fast optimizations."""
        # CRITICAL FAST PATH: Numeric types (most common case for scaling)
        if isinstance(other, int | float):
            return Quantity(quantity.value * other, quantity.unit)

        # Handle UnifiedVariable objects by using their quantity - duck typing for performance
        if hasattr(other, "quantity") and getattr(other, "quantity", None) is not None:
            other = other.quantity  # type: ignore

        # Type narrowing: at this point other should be Quantity
        if not isinstance(other, Quantity):
            raise TypeError(f"Expected Quantity, got {type(other)}")

        # PERFORMANCE OPTIMIZATIONS: Extract frequently accessed attributes once
        quantity_value = quantity.value
        quantity_si = quantity._si_factor
        quantity_dim = quantity._dimension_sig
        other_value = other.value
        other_si = other._si_factor
        other_dim = other._dimension_sig

        # ULTRA-FAST PATH: Special values (identity, zero) - checked first for maximum impact
        if quantity_value == 1.0 and quantity_dim == 1:  # 1.0 * dimensionless
            return Quantity(other_value * quantity_si, other.unit)
        elif other_value == 1.0 and other_dim == 1:  # something * 1.0 dimensionless
            return Quantity(quantity_value * other_si, quantity.unit)
        elif quantity_value == 0.0:
            return Quantity(0.0, quantity.unit)
        elif other_value == 0.0:
            return Quantity(0.0, other.unit)

        # ENHANCED DIMENSIONLESS FAST PATHS: Handle like scalars with minimal overhead
        if other_dim == 1:  # DIMENSIONLESS right operand
            # Dimensionless multiplication: just scale, keep original unit - avoid complex operations
            return Quantity(quantity_value * other_value * other_si, quantity.unit)
        elif quantity_dim == 1:  # DIMENSIONLESS left operand
            # Dimensionless left operand: scale the right operand - avoid complex operations
            return Quantity(quantity_value * quantity_si * other_value, other.unit)

        # STREAMLINED CACHE LOOKUP: Direct dictionary access instead of method calls
        cache_key = (quantity_dim, other_dim)
        if cache_key in _cache_manager.multiplication_cache:
            cached_unit = _cache_manager.multiplication_cache[cache_key]
            # BATCHED SI CALCULATIONS: Combine operations to reduce attribute access
            result_si_value = (quantity_value * quantity_si) * (other_value * other_si)
            return Quantity(result_si_value / cached_unit.si_factor, cached_unit)

        # OPTIMIZED GENERAL CASE: Pre-calculate result dimension
        result_dimension_sig = quantity_dim * other_dim
        result_si_value = (quantity_value * quantity_si) * (other_value * other_si)

        # Find appropriate result unit using fast path
        result_unit = UnitResolution.find_result_unit_fast(quantity, result_dimension_sig)
        result_value = result_si_value / result_unit.si_factor

        # Cache the result for future use - direct dictionary assignment for speed
        if len(_cache_manager.multiplication_cache) < _cache_manager.max_cache_size:
            _cache_manager.multiplication_cache[cache_key] = result_unit
        
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

        # OPTIMIZATION: Fast path for dimensionless divisor (signature = 1)
        # Treat dimensionless quantities more like scalars to reduce overhead
        if other._dimension_sig == 1:  # DIMENSIONLESS divisor
            # Division by dimensionless: just scale the value, keep original unit
            divisor = other.value * other._si_factor
            return Quantity(quantity.value / divisor, quantity.unit)

        # Check division cache first
        cached_unit = _cache_manager.get_division_result(quantity._dimension_sig, other._dimension_sig)
        if cached_unit:
            result_si_value = (quantity.value * quantity._si_factor) / (other.value * other._si_factor)
            return Quantity(result_si_value / cached_unit.si_factor, cached_unit)

        # Calculate result dimension and value
        result_dimension_sig = quantity._dimension_sig / other._dimension_sig
        result_si_value = (quantity.value * quantity._si_factor) / (other.value * other._si_factor)

        # Find appropriate result unit
        result_unit = UnitResolution.find_result_unit_fast(quantity, result_dimension_sig)
        result_value = result_si_value / result_unit.si_factor

        # Cache the result for future use
        _cache_manager.cache_division_result(quantity._dimension_sig, other._dimension_sig, result_unit)
        return Quantity(result_value, result_unit)


class ComparisonOperations:
    """Handles comparison operations for quantities."""

    @staticmethod
    def less_than(quantity, other):
        """Compare if this quantity is less than another."""
        # Optimized comparison with bulk operations
        if quantity._dimension_sig != other._dimension_sig:
            raise ValueError(ErrorMessages.INCOMPATIBLE_COMPARISON)

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
        # CRITICAL OPTIMIZATION: Direct dictionary access (O(1)) for common dimensions
        dimension_cache = registry._dimension_cache
        if result_dimension_sig in dimension_cache:
            return dimension_cache[result_dimension_sig]

        # OPTIMIZED PATH: For rare combined dimensions, create SI base unit efficiently
        result_dimension = DimensionSignature(result_dimension_sig)

        # FAST CREATION: Minimize string operations for performance
        sig_hash = abs(hash(result_dimension_sig)) % 10000
        si_name = f"si_derived_{sig_hash}"
        si_symbol = f"SI_{sig_hash % 1000}"

        # STREAMLINED CREATION: Avoid unnecessary method calls
        temp_unit = UnitDefinition(name=si_name, symbol=si_symbol, dimension=result_dimension, si_factor=1.0)
        result_unit = UnitConstant(temp_unit)

        # DIRECT CACHE ASSIGNMENT: Bypass cache size checks for dimension cache
        dimension_cache[result_dimension_sig] = result_unit
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
            raise TypeError(ErrorMessages.INCOMPATIBLE_DIMENSION.format(unit.name))

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
        # Check cache for small integers
        cached = _cache_manager.get_cached_quantity(value, unit)
        if cached:
            return cached

        # Create new quantity
        obj = cls(value, unit)

        # Cache if it qualifies
        _cache_manager.cache_quantity(value, unit, obj)
        return obj

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


# Initialize cache manager at module load
_cache_manager.initialize_common_operations()
