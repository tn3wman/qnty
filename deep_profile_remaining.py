#!/usr/bin/env python3
"""
Deep Profile: Remaining Performance Bottlenecks
===============================================

After our optimizations, we've improved from 2.6 μs to 0.85 μs (3x improvement).
Let's profile what's still taking time to get closer to the 0.2 μs target.
"""

import cProfile
import io
import pstats
import time
from qnty.core import Q

def deep_profile_remaining():
    """Profile the remaining bottlenecks in unit conversion."""
    print("DEEP PROFILING: Remaining Performance Issues")
    print("="*60)

    def unit_conversion():
        qnty_meter = Q(100.0, 'm')
        return qnty_meter.to_unit.millimeter

    # Profile with higher resolution
    pr = cProfile.Profile()
    iterations = 50000  # More iterations for better granularity

    pr.enable()
    for _ in range(iterations):
        result = unit_conversion()
    pr.disable()

    # Analyze results
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('tottime')  # Sort by total time
    ps.print_stats(30)  # Show top 30 functions

    print(s.getvalue())

    # Calculate per-operation time
    total_time = sum(stat[1] for stat in ps.stats.values())
    avg_time_us = (total_time / iterations) * 1_000_000
    print(f"\nAverage time per operation (from tottime): {avg_time_us:.3f} μs")

def analyze_object_creation_cost():
    """Analyze the cost of object creation vs direct computation."""
    print(f"\n{'='*60}")
    print("OBJECT CREATION ANALYSIS")
    print("="*60)

    iterations = 100000

    # Test 1: Current implementation
    def current():
        qnty_meter = Q(100.0, 'm')
        return qnty_meter.to_unit.millimeter

    start = time.perf_counter()
    for _ in range(iterations):
        current()
    end = time.perf_counter()
    current_time_us = ((end - start) / iterations) * 1_000_000

    # Test 2: Direct conversion without UnitApplier
    from qnty.core.unit import ureg
    meter_unit = ureg.resolve('m')
    mm_unit = ureg.resolve('millimeter')

    def direct_conversion():
        from qnty.core.quantity import Quantity
        # Create quantity directly
        si_value = meter_unit.si_factor * 100.0 + meter_unit.si_offset
        qnty = Quantity(name="Q", dim=meter_unit.dim, value=si_value)
        # Convert directly
        converted_value = (qnty.value - mm_unit.si_offset) / mm_unit.si_factor
        return Quantity(name="converted", dim=meter_unit.dim, value=converted_value, preferred=mm_unit)

    start = time.perf_counter()
    for _ in range(iterations):
        direct_conversion()
    end = time.perf_counter()
    direct_time_us = ((end - start) / iterations) * 1_000_000

    # Test 3: Just the math (no objects)
    conversion_factor = mm_unit.si_factor / meter_unit.si_factor

    def just_math():
        si_value = 100.0  # Already in SI (meters)
        return si_value / mm_unit.si_factor  # Convert to mm

    start = time.perf_counter()
    for _ in range(iterations):
        just_math()
    end = time.perf_counter()
    math_time_us = ((end - start) / iterations) * 1_000_000

    print(f"Current implementation:  {current_time_us:.3f} μs")
    print(f"Direct conversion:       {direct_time_us:.3f} μs")
    print(f"Just math (no objects):  {math_time_us:.3f} μs")

    object_overhead = current_time_us - math_time_us
    print(f"Object creation overhead: {object_overhead:.3f} μs ({object_overhead/current_time_us*100:.1f}%)")

def analyze_string_operations():
    """Analyze remaining string operation costs."""
    print(f"\n{'='*60}")
    print("STRING OPERATION ANALYSIS")
    print("="*60)

    from qnty.core.unit import _norm

    iterations = 100000

    # Test string normalization
    def test_norm():
        return _norm('millimeter')

    start = time.perf_counter()
    for _ in range(iterations):
        test_norm()
    end = time.perf_counter()
    norm_time_us = ((end - start) / iterations) * 1_000_000

    print(f"_norm('millimeter'):     {norm_time_us:.3f} μs per call")

    # Test if we can pre-compute common normalizations
    normalized_mm = _norm('millimeter')
    def test_precomputed():
        return normalized_mm

    start = time.perf_counter()
    for _ in range(iterations):
        test_precomputed()
    end = time.perf_counter()
    precomputed_time_us = ((end - start) / iterations) * 1_000_000

    print(f"Pre-computed result:     {precomputed_time_us:.3f} μs per call")
    print(f"Normalization overhead:  {norm_time_us - precomputed_time_us:.3f} μs")

def find_fastest_possible():
    """Find the absolute fastest possible conversion."""
    print(f"\n{'='*60}")
    print("FASTEST POSSIBLE CONVERSION")
    print("="*60)

    # Pre-compute everything
    from qnty.core.unit import ureg
    m_unit = ureg.resolve('m')
    mm_unit = ureg.resolve('millimeter')

    # Since both are SI base units with simple factors:
    # meter: si_factor = 1.0
    # millimeter: si_factor = 0.001
    # So conversion factor = 1000.0
    CONVERSION_FACTOR = 1000.0

    iterations = 100000

    def fastest_conversion():
        # Input: 100 meters
        # Output: value in millimeters
        return 100.0 * CONVERSION_FACTOR

    start = time.perf_counter()
    for _ in range(iterations):
        result = fastest_conversion()
    end = time.perf_counter()
    fastest_time_us = ((end - start) / iterations) * 1_000_000

    print(f"Fastest possible (pure math): {fastest_time_us:.3f} μs")
    print(f"Result: {result}")

    # This shows us the absolute minimum time for the conversion
    # Everything above this is framework overhead

if __name__ == "__main__":
    deep_profile_remaining()
    analyze_object_creation_cost()
    analyze_string_operations()
    find_fastest_possible()

    print(f"\n{'='*60}")
    print("REMAINING OPTIMIZATION OPPORTUNITIES")
    print("="*60)
    print("Current performance: ~0.85 μs")
    print("Target performance:   0.20 μs")
    print("Gap to close:        ~0.65 μs")
    print("")
    print("Next optimization targets:")
    print("1. Reduce object creation overhead")
    print("2. Cache common unit pairs (m->mm)")
    print("3. Special-case SI prefix conversions")
    print("4. Consider return value optimization")