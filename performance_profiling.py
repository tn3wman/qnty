#!/usr/bin/env python3
"""
Performance Profiling for Qnty Unit Conversion
==============================================

This script profiles the specific unit conversion operation that has regressed from 0.2 μs to 2.6-2.7 μs.
We'll use cProfile and line-by-line profiling to identify the bottleneck.
"""

import cProfile
import io
import pstats
import time
from typing import Callable

from qnty.core import Q
from qnty.core.unit import ureg

# Test constants
TEST_VALUE = 100.0
ITERATIONS = 10000  # More iterations for better profiling

def profile_with_cprofile(func: Callable, name: str, iterations: int = ITERATIONS):
    """Profile a function using cProfile."""
    print(f"\n{'='*60}")
    print(f"cProfile Analysis: {name}")
    print(f"{'='*60}")

    # Create profiler
    pr = cProfile.Profile()

    # Profile the function
    pr.enable()
    for _ in range(iterations):
        result = func()
    pr.disable()

    # Print results
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(20)  # Show top 20 functions

    print(s.getvalue())

    # Also show time per operation
    total_time = sum(stat[2] for stat in ps.stats.values())
    avg_time_us = (total_time / iterations) * 1_000_000
    print(f"\nAverage time per operation: {avg_time_us:.3f} μs")

    return result

def time_operation(func: Callable, name: str, iterations: int = ITERATIONS):
    """Time an operation precisely."""
    print(f"\n{'-'*40}")
    print(f"Timing: {name}")
    print(f"{'-'*40}")

    # Warmup
    for _ in range(100):
        func()

    # Time the operation
    start = time.perf_counter()
    for _ in range(iterations):
        result = func()
    end = time.perf_counter()

    total_time = end - start
    avg_time_us = (total_time / iterations) * 1_000_000

    print(f"Total time: {total_time:.6f} seconds")
    print(f"Average time per operation: {avg_time_us:.3f} μs")
    print(f"Operations per second: {iterations / total_time:.0f}")

    return result

def analyze_conversion_components():
    """Analyze individual components of the conversion process."""
    print(f"\n{'='*80}")
    print("COMPONENT ANALYSIS: Breaking down the conversion process")
    print(f"{'='*80}")

    # 1. Q function creation
    def create_quantity():
        return Q(TEST_VALUE, 'm')

    time_operation(create_quantity, "Q(100.0, 'm') - Quantity Creation")

    # 2. Access .to_unit property
    qnty_meter = Q(TEST_VALUE, 'm')
    def access_to_unit():
        return qnty_meter.to_unit

    time_operation(access_to_unit, ".to_unit property access")

    # 3. Access .millimeter attribute
    to_unit_obj = qnty_meter.to_unit
    def access_millimeter():
        return to_unit_obj.millimeter

    time_operation(access_millimeter, ".millimeter attribute access")

    # 4. Complete conversion (baseline)
    def complete_conversion():
        qnty_meter = Q(TEST_VALUE, 'm')
        return qnty_meter.to_unit.millimeter

    time_operation(complete_conversion, "Complete conversion (Q + to_unit + millimeter)")

    # 5. Unit resolution by name
    def resolve_unit():
        return ureg.resolve('millimeter')

    time_operation(resolve_unit, "ureg.resolve('millimeter')")

    # 6. Unit resolution by name with dimension hint
    meter_unit = ureg.resolve('m')
    def resolve_unit_with_dim():
        return ureg.resolve('millimeter', dim=meter_unit.dim)

    time_operation(resolve_unit_with_dim, "ureg.resolve('millimeter', dim=length_dim)")

def profile_main_operation():
    """Profile the main operation that has regressed."""
    def unit_conversion():
        qnty_meter = Q(TEST_VALUE, 'm')
        return qnty_meter.to_unit.millimeter

    # Profile with cProfile
    result = profile_with_cprofile(unit_conversion, "Unit Conversion (Q(100.0, 'm').to_unit.millimeter)")

    # Also time it precisely
    time_operation(unit_conversion, "Unit Conversion (Precise Timing)")

    return result

def analyze_object_creation_overhead():
    """Analyze potential object creation overhead."""
    print(f"\n{'='*80}")
    print("OBJECT CREATION ANALYSIS")
    print(f"{'='*80}")

    # Pre-create objects to test reuse
    qnty_meter = Q(TEST_VALUE, 'm')
    meter_unit = ureg.resolve('m')
    mm_unit = ureg.resolve('millimeter')

    # Test conversion with pre-created objects
    def conversion_with_precreated():
        # Convert from SI to target unit: (si_value - offset) / factor
        converted_value = (qnty_meter.value - mm_unit.si_offset) / mm_unit.si_factor
        from qnty.core.quantity import Quantity
        return Quantity(
            name="converted",
            dim=qnty_meter.dim,
            value=converted_value,
            preferred=mm_unit
        )

    time_operation(conversion_with_precreated, "Direct conversion (pre-created objects)")

    # Test UnitApplier creation
    def unit_applier_creation():
        from qnty.core.quantity import UnitApplier
        return UnitApplier(qnty_meter)

    time_operation(unit_applier_creation, "UnitApplier creation")

def analyze_string_processing():
    """Analyze string processing overhead in unit resolution."""
    print(f"\n{'='*80}")
    print("STRING PROCESSING ANALYSIS")
    print(f"{'='*80}")

    # Test _norm function
    from qnty.core.unit import _norm

    def norm_millimeter():
        return _norm('millimeter')

    time_operation(norm_millimeter, "_norm('millimeter') - String normalization")

    # Test dictionary lookup
    normalized = _norm('millimeter')
    def dict_lookup():
        return ureg._by_name.get(normalized)

    time_operation(dict_lookup, "ureg._by_name.get(normalized_key)")

def memory_analysis():
    """Analyze memory allocations."""
    print(f"\n{'='*80}")
    print("MEMORY ALLOCATION ANALYSIS")
    print(f"{'='*80}")

    import tracemalloc

    # Start tracing
    tracemalloc.start()

    # Take snapshot before
    snapshot1 = tracemalloc.take_snapshot()

    # Run the operation multiple times
    for _ in range(1000):
        qnty_meter = Q(TEST_VALUE, 'm')
        result = qnty_meter.to_unit.millimeter

    # Take snapshot after
    snapshot2 = tracemalloc.take_snapshot()

    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("\nTop 10 memory allocations:")
    for stat in top_stats[:10]:
        print(stat)

    tracemalloc.stop()

if __name__ == "__main__":
    print("QNTY PERFORMANCE PROFILING")
    print("="*80)
    print("Analyzing unit conversion regression from 0.2 μs to 2.6-2.7 μs")

    # 1. Profile the main operation
    profile_main_operation()

    # 2. Analyze components
    analyze_conversion_components()

    # 3. Analyze object creation
    analyze_object_creation_overhead()

    # 4. Analyze string processing
    analyze_string_processing()

    # 5. Memory analysis
    memory_analysis()

    print(f"\n{'='*80}")
    print("PROFILING COMPLETE")
    print("="*80)
    print("Review the cProfile output above to identify the bottleneck.")
    print("Look for:")
    print("- High cumulative time in specific functions")
    print("- Excessive function calls")
    print("- String processing overhead")
    print("- Object creation patterns")