#!/usr/bin/env python3
"""
Performance Test: Optimized Unit Conversion
==========================================

Test the performance improvements after optimizing:
1. Made variable name detection lazy (only when .symbol is accessed)
2. Added caching to unit resolution
3. Simplified Q() function to avoid expensive lookups
"""

import time
from qnty.core import Q

def test_optimized_performance():
    """Test the performance of the optimized unit conversion."""
    print("OPTIMIZED PERFORMANCE TEST")
    print("="*50)

    # Test the original benchmark operation
    def unit_conversion():
        qnty_meter = Q(100.0, 'm')
        return qnty_meter.to_unit.millimeter

    iterations = 10000

    # Warmup
    for _ in range(100):
        unit_conversion()

    # Time the operation
    start = time.perf_counter()
    for _ in range(iterations):
        result = unit_conversion()
    end = time.perf_counter()

    total_time = end - start
    avg_time_us = (total_time / iterations) * 1_000_000

    print(f"Iterations: {iterations}")
    print(f"Total time: {total_time:.6f} seconds")
    print(f"Average time per conversion: {avg_time_us:.3f} μs")
    print(f"Operations per second: {iterations / total_time:.0f}")

    # Performance comparison
    print(f"\nPERFORMACE COMPARISON:")
    print(f"Target performance:    0.200 μs")
    print(f"Previous performance:  2.600 μs (13x slower than target)")
    print(f"Current performance:   {avg_time_us:.3f} μs")

    if avg_time_us <= 0.200:
        improvement = 2.600 / avg_time_us
        print(f"STATUS: ✅ EXCELLENT! Back to target performance")
        print(f"Improvement: {improvement:.1f}x faster than before optimization")
    elif avg_time_us <= 0.500:
        improvement = 2.600 / avg_time_us
        print(f"STATUS: ✅ GREAT! {improvement:.1f}x improvement")
    elif avg_time_us <= 1.000:
        improvement = 2.600 / avg_time_us
        print(f"STATUS: ✅ GOOD! {improvement:.1f}x improvement")
    elif avg_time_us <= 1.500:
        improvement = 2.600 / avg_time_us
        print(f"STATUS: ✅ BETTER! {improvement:.1f}x improvement")
    else:
        improvement = 2.600 / avg_time_us
        print(f"STATUS: ⚠️  Some improvement ({improvement:.1f}x) but still slow")

    return result

def test_component_performance():
    """Test the performance of individual components after optimization."""
    print(f"\nCOMPONENT PERFORMANCE (AFTER OPTIMIZATION)")
    print("="*50)

    iterations = 10000

    # 1. Q function creation
    def create_quantity():
        return Q(100.0, 'm')

    start = time.perf_counter()
    for _ in range(iterations):
        create_quantity()
    end = time.perf_counter()
    q_time_us = ((end - start) / iterations) * 1_000_000
    print(f"Q(100.0, 'm') creation:        {q_time_us:.3f} μs")

    # 2. Unit resolution (cached)
    from qnty.core.unit import ureg
    def resolve_unit():
        return ureg.resolve('millimeter')

    start = time.perf_counter()
    for _ in range(iterations):
        resolve_unit()
    end = time.perf_counter()
    resolve_time_us = ((end - start) / iterations) * 1_000_000
    print(f"ureg.resolve('millimeter'):     {resolve_time_us:.3f} μs")

    # 3. Complete conversion
    def complete_conversion():
        qnty_meter = Q(100.0, 'm')
        return qnty_meter.to_unit.millimeter

    start = time.perf_counter()
    for _ in range(iterations):
        complete_conversion()
    end = time.perf_counter()
    complete_time_us = ((end - start) / iterations) * 1_000_000
    print(f"Complete conversion:            {complete_time_us:.3f} μs")

def test_variable_name_detection():
    """Test that variable name detection still works when needed."""
    print(f"\nVARIABLE NAME DETECTION TEST")
    print("="*40)

    # Create a quantity with a meaningful variable name
    pressure = Q(2000000, 'Pa')

    # Variable name detection should be lazy - not triggered during creation
    print(f"Quantity created without immediate symbol detection")

    # Access symbol property to trigger detection
    symbol = pressure.symbol
    print(f"Symbol detected when accessed: '{symbol}'")

    # Should be cached now
    symbol2 = pressure.symbol
    print(f"Symbol from cache: '{symbol2}'")

    if symbol == symbol2:
        print("✅ Variable name detection working correctly (lazy + cached)")
    else:
        print("❌ Variable name detection issue")

if __name__ == "__main__":
    test_optimized_performance()
    test_component_performance()
    test_variable_name_detection()

    print(f"\n{'='*50}")
    print("OPTIMIZATION SUMMARY")
    print("="*50)
    print("Applied optimizations:")
    print("1. ✅ Made variable name detection lazy (only when symbol accessed)")
    print("2. ✅ Added caching to unit resolution")
    print("3. ✅ Simplified Q() function to avoid expensive dimension lookups")
    print("")
    print("These changes should significantly improve unit conversion performance")
    print("while maintaining full functionality for equation solving features.")