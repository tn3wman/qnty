#!/usr/bin/env python3
"""
Optimized unit lookup strategies focusing on caching and fast resolution.
No pre-computed conversion tables - just optimized lookup mechanisms.
"""

import functools
from typing import Final

from .dimension import Dimension
from .unit import Unit, _norm

# Optimization Strategy 1: Cached normalization
@functools.lru_cache(maxsize=512)
def _cached_norm(s: str) -> str:
    """Cached version of _norm for frequently used unit names."""
    return _norm(s)


class OptimizedUnitRegistry:
    """
    Enhanced unit registry with optimized lookup strategies:
    1. Multi-level caching (symbol -> normalized -> fallback)
    2. Cached normalization for repeated lookups
    3. Dimension-aware fast paths
    4. Optimized attribute access
    """

    __slots__ = (
        "_by_name", "_by_symbol", "_intern_by_symbol", "_by_dim",
        "_preferred", "_resolve_cache", "_attr_cache", "_norm_cache",
        "_dimension_units", "_common_units"
    )

    def __init__(self):
        # Existing structures (maintain compatibility)
        self._by_name = {}
        self._by_symbol = {}
        self._intern_by_symbol = {}
        self._by_dim = {}
        self._preferred = {}

        # Enhanced caching
        self._resolve_cache = {}
        self._attr_cache = {}  # For __getattr__ performance
        self._norm_cache = {}  # Cache normalized strings

        # Dimension-specific optimization
        self._dimension_units = {}  # dim -> list of units (for fast iteration)
        self._common_units = set()  # Track frequently accessed units

    def register(self, unit: Unit, *, name: str | None = None, aliases: list[str] = None):
        """Enhanced registration with optimization tracking."""
        # Standard registration logic (maintain compatibility)
        actual_name = name or unit.name
        nk = _cached_norm(actual_name)

        self._by_name[nk] = unit
        self._by_symbol[unit.symbol] = unit
        self._intern_by_symbol.setdefault(unit.symbol, unit)

        # Dimension indexing for fast lookup
        dim_units = self._by_dim.setdefault(unit.dim, {})
        dim_units[nk] = unit

        # Track units by dimension for optimization
        if unit.dim not in self._dimension_units:
            self._dimension_units[unit.dim] = []
        self._dimension_units[unit.dim].append(unit)

        # Register aliases
        if aliases:
            for alias in aliases:
                alias_nk = _cached_norm(alias)
                self._by_name[alias_nk] = unit
                dim_units[alias_nk] = unit

    def resolve_fast(self, name_or_symbol: str, *, dim: Dimension | None = None) -> Unit | None:
        """
        Optimized resolution with multiple fast paths:
        1. Direct symbol lookup (fastest)
        2. Cached resolve result
        3. Dimension-specific lookup
        4. Standard normalization fallback
        """

        # Fast Path 1: Direct symbol lookup (no normalization needed)
        if dim is None:  # Only when dimension not specified
            unit = self._intern_by_symbol.get(name_or_symbol)
            if unit is not None:
                self._track_common_unit(name_or_symbol)
                return unit

            unit = self._by_symbol.get(name_or_symbol)
            if unit is not None:
                self._track_common_unit(name_or_symbol)
                return unit

        # Fast Path 2: Check resolve cache
        cache_key = (name_or_symbol, dim)
        if cache_key in self._resolve_cache:
            result = self._resolve_cache[cache_key]
            if result is not None:
                self._track_common_unit(name_or_symbol)
            return result

        # Fast Path 3: Dimension-specific lookup (when dim is specified)
        if dim is not None and dim in self._by_dim:
            # Try direct symbol lookup in dimension-specific units first
            unit = self._intern_by_symbol.get(name_or_symbol)
            if unit is not None and unit.dim == dim:
                self._resolve_cache[cache_key] = unit
                self._track_common_unit(name_or_symbol)
                return unit

            # Then normalized lookup within dimension
            nk = _cached_norm(name_or_symbol)
            dim_units = self._by_dim[dim]
            unit = dim_units.get(nk)
            if unit is not None:
                self._resolve_cache[cache_key] = unit
                self._track_common_unit(name_or_symbol)
                return unit

        # Fast Path 4: Standard normalization lookup
        nk = _cached_norm(name_or_symbol)
        unit = self._by_name.get(nk)
        if unit is not None:
            if dim is None or unit.dim == dim:
                self._resolve_cache[cache_key] = unit
                self._track_common_unit(name_or_symbol)
                return unit

        # Cache miss
        self._resolve_cache[cache_key] = None
        return None

    def _track_common_unit(self, name: str):
        """Track commonly accessed units for future optimization."""
        self._common_units.add(name)

        # Limit tracking to prevent memory bloat
        if len(self._common_units) > 200:
            # Keep most recent half
            common_list = list(self._common_units)
            self._common_units = set(common_list[-100:])

    def __getattr__(self, name: str) -> Unit:
        """Optimized attribute access with caching."""

        # Check attribute cache first
        if name in self._attr_cache:
            return self._attr_cache[name]

        # Try resolution
        unit = self.resolve_fast(name)
        if unit is not None:
            # Cache successful lookups (limit cache size)
            if len(self._attr_cache) < 100:
                self._attr_cache[name] = unit
            return unit

        # Enhanced error message with suggestions
        suggestions = self._get_suggestions(name)
        if suggestions:
            suggestion_str = f". Did you mean: {', '.join(suggestions[:3])}?"
        else:
            suggestion_str = ""

        raise AttributeError(f"{type(self).__name__} has no attribute '{name}'{suggestion_str}")

    def _get_suggestions(self, name: str) -> list[str]:
        """Get suggestions for unknown unit names."""
        nk = _cached_norm(name)
        suggestions = []

        # Find similar normalized names
        for known_name in self._by_name.keys():
            if len(known_name) >= 2 and (
                known_name.startswith(nk[:2]) or
                nk.startswith(known_name[:2]) or
                known_name in nk or
                nk in known_name
            ):
                # Try to get original name from unit
                unit = self._by_name[known_name]
                suggestions.append(unit.name)

        return suggestions[:5]  # Limit suggestions

    def clear_caches(self):
        """Clear all caches (useful for testing or memory management)."""
        self._resolve_cache.clear()
        self._attr_cache.clear()
        self._norm_cache.clear()
        _cached_norm.cache_clear()

    def get_cache_stats(self) -> dict:
        """Get cache performance statistics."""
        return {
            "resolve_cache_size": len(self._resolve_cache),
            "attr_cache_size": len(self._attr_cache),
            "norm_cache_info": _cached_norm.cache_info(),
            "common_units_tracked": len(self._common_units),
            "dimension_count": len(self._dimension_units)
        }


def benchmark_optimizations():
    """Benchmark the optimized lookup strategies."""
    import time
    from .unit import ureg  # Original registry
    from .unit_catalog import LengthUnits  # For testing

    print("Unit Lookup Optimization Benchmark")
    print("=" * 50)

    # Create optimized registry and populate with same data
    opt_registry = OptimizedUnitRegistry()

    # We'd need to copy units from original registry
    # For now, just benchmark the resolve methods

    test_units = ["ft", "m", "in", "mm", "meter", "feet", "inches"]
    iterations = 10000

    print(f"Testing {len(test_units)} units x {iterations} iterations")
    print()

    # Benchmark original resolution
    start = time.perf_counter()
    for _ in range(iterations):
        for unit_name in test_units:
            result = ureg.resolve(unit_name)
    end = time.perf_counter()
    original_time = end - start

    # Since we can't easily populate the optimized registry,
    # let's profile the normalization function separately

    print(f"Original resolve time: {original_time:.4f}s")
    print(f"Per lookup: {(original_time / (len(test_units) * iterations)) * 1e6:.1f} μs")

    # Test cached normalization impact
    start = time.perf_counter()
    for _ in range(iterations * 10):  # More iterations for micro-benchmark
        for unit_name in test_units:
            _cached_norm(unit_name)
    end = time.perf_counter()
    cached_norm_time = end - start

    start = time.perf_counter()
    for _ in range(iterations * 10):
        for unit_name in test_units:
            _norm(unit_name)  # Original normalization
    end = time.perf_counter()
    orig_norm_time = end - start

    print(f"\nNormalization comparison:")
    print(f"Original _norm: {orig_norm_time:.4f}s")
    print(f"Cached _norm: {cached_norm_time:.4f}s")
    print(f"Speedup: {orig_norm_time/cached_norm_time:.1f}x")

    print(f"\nCache info: {_cached_norm.cache_info()}")


if __name__ == "__main__":
    benchmark_optimizations()