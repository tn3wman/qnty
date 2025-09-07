"""Test multiplication cache effectiveness."""
from qnty.quantities import Quantity
from qnty.units import LengthUnits
from qnty.quantities.base_qnty import _cache_manager

# Create test quantities
length_10 = Quantity(10.0, LengthUnits.meter)
width_5 = Quantity(5.0, LengthUnits.meter)

print("=== MULTIPLICATION CACHE ANALYSIS ===")
print(f"Initial cache size: {len(_cache_manager.multiplication_cache)}")
print(f"Cache contents: {list(_cache_manager.multiplication_cache.keys())}")

# Test dimension signatures
print(f"\nLength dimension signature: {length_10._dimension_sig}")
print(f"Cache key would be: ({length_10._dimension_sig}, {width_5._dimension_sig})")

# Check if this combination is cached
cache_key = (length_10._dimension_sig, width_5._dimension_sig)
is_cached = cache_key in _cache_manager.multiplication_cache

print(f"Is length × length cached? {is_cached}")

# Perform multiplication
result = length_10 * width_5
print(f"\nResult: {result}")
print(f"Cache size after multiplication: {len(_cache_manager.multiplication_cache)}")
print(f"New cache contents: {list(_cache_manager.multiplication_cache.keys())}")

# Test if it's cached for second multiplication
print(f"\nIs now cached? {cache_key in _cache_manager.multiplication_cache}")

# Test registry dimension cache
from qnty.units.registry import registry
print(f"\nRegistry dimension cache size: {len(registry._dimension_cache)}")
print(f"Area dimension in registry cache: {result._dimension_sig in registry._dimension_cache}")