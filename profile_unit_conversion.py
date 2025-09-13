#!/usr/bin/env python3
"""Profile unit conversion to identify performance bottlenecks."""

import cProfile
import io
import pstats
import time
from qnty.core import Q

def profile_unit_conversion():
    """Profile the unit conversion operation that used to take 0.2μs but now takes 2.6μs."""

    # Create the quantity once outside the loop
    qnty_meter = Q(100.0, 'm')

    def convert_once():
        """Single unit conversion operation."""
        return qnty_meter.to_unit.millimeter

    # Test the operation works
    result = convert_once()
    print(f"Conversion result: {result}")

    # Time it manually first
    iterations = 10000
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = convert_once()
    end_time = time.perf_counter()

    avg_time_us = (end_time - start_time) / iterations * 1_000_000
    print(f"Manual timing: {avg_time_us:.2f} μs per conversion")

    # Now profile it
    pr = cProfile.Profile()
    pr.enable()

    # Run the operation many times
    for _ in range(1000):
        result = convert_once()

    pr.disable()

    # Analyze results
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(20)  # Show top 20 functions

    print("\n" + "="*80)
    print("PROFILING RESULTS")
    print("="*80)
    print(s.getvalue())

    # Also show by total time
    s2 = io.StringIO()
    ps2 = pstats.Stats(pr, stream=s2)
    ps2.sort_stats('tottime')
    ps2.print_stats(10)  # Show top 10 by total time

    print("\n" + "="*80)
    print("BY TOTAL TIME")
    print("="*80)
    print(s2.getvalue())

def profile_q_creation():
    """Profile Q() creation separately."""

    def create_q():
        return Q(100.0, 'm')

    # Time it manually
    iterations = 10000
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = create_q()
    end_time = time.perf_counter()

    avg_time_us = (end_time - start_time) / iterations * 1_000_000
    print(f"\nQ() creation timing: {avg_time_us:.2f} μs per creation")

def profile_to_unit_access():
    """Profile just the .to_unit property access."""
    qnty_meter = Q(100.0, 'm')

    def access_to_unit():
        return qnty_meter.to_unit

    # Time it manually
    iterations = 10000
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = access_to_unit()
    end_time = time.perf_counter()

    avg_time_us = (end_time - start_time) / iterations * 1_000_000
    print(f".to_unit access timing: {avg_time_us:.2f} μs per access")

def profile_millimeter_access():
    """Profile just the .millimeter attribute access on UnitApplier."""
    qnty_meter = Q(100.0, 'm')
    to_unit_obj = qnty_meter.to_unit

    def access_millimeter():
        return to_unit_obj.millimeter

    # Time it manually
    iterations = 10000
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = access_millimeter()
    end_time = time.perf_counter()

    avg_time_us = (end_time - start_time) / iterations * 1_000_000
    print(f".millimeter access timing: {avg_time_us:.2f} μs per access")

if __name__ == "__main__":
    print("Profiling unit conversion performance bottlenecks...")

    # Break down the operation into components
    profile_q_creation()
    profile_to_unit_access()
    profile_millimeter_access()

    print("\nFull conversion profiling:")
    profile_unit_conversion()