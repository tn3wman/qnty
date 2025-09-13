#!/usr/bin/env python3
"""Test direct conversion method for maximum performance."""

import time
from qnty.core import Q

def profile_direct_vs_fluent():
    """Compare direct .to() method vs fluent .to_unit.millimeter."""

    # Create the quantity once
    qnty_meter = Q(100.0, 'm')

    def convert_fluent():
        """Fluent conversion using .to_unit.millimeter"""
        return qnty_meter.to_unit.millimeter

    def convert_direct():
        """Direct conversion using .to('mm')"""
        return qnty_meter.to('mm')

    # Test both methods work
    result_fluent = convert_fluent()
    result_direct = convert_direct()
    print(f"Fluent result: {result_fluent}")
    print(f"Direct result: {result_direct}")
    print(f"Results equal: {result_fluent.value == result_direct.value}")

    # Time both methods
    iterations = 10000

    # Time fluent method
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = convert_fluent()
    end_time = time.perf_counter()
    fluent_time = (end_time - start_time) / iterations * 1_000_000

    # Time direct method
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = convert_direct()
    end_time = time.perf_counter()
    direct_time = (end_time - start_time) / iterations * 1_000_000

    print(f"\nPerformance Comparison:")
    print(f"Fluent (.to_unit.millimeter): {fluent_time:.2f} μs")
    print(f"Direct (.to('mm')):           {direct_time:.2f} μs")
    print(f"Speedup: {fluent_time/direct_time:.1f}x")

if __name__ == "__main__":
    profile_direct_vs_fluent()