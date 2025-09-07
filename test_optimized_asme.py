#!/usr/bin/env python3
"""
Test Optimized ASME Equation Performance
========================================

Test the performance improvements from dimensionless quantity optimizations.
"""

import time
import pint

from qnty.quantities import Quantity
from qnty.units import DimensionlessUnits, LengthUnits, PressureUnits

# Initialize Pint registry
ureg = pint.UnitRegistry()

# Create test quantities - same as benchmark
qnty_P = Quantity(2900.75, PressureUnits.psi)
qnty_D = Quantity(168.275, LengthUnits.millimeter)
qnty_S = Quantity(137.895, PressureUnits.MPa)
qnty_E = Quantity(0.8, DimensionlessUnits.dimensionless)
qnty_W = Quantity(1.0, DimensionlessUnits.dimensionless)
qnty_Y = Quantity(0.4, DimensionlessUnits.dimensionless)

pint_P = ureg.Quantity(2900.75, "psi")
pint_D = ureg.Quantity(168.275, "mm")
pint_S = ureg.Quantity(137.895, "MPa")

def benchmark_operation(func, name: str, iterations: int = 1000) -> float:
    """Benchmark an operation and return average time in microseconds"""
    # Warmup
    for _ in range(10):
        func()
    
    # Time the operations
    start = time.perf_counter()
    for _ in range(iterations):
        result = func()
    end = time.perf_counter()
    
    avg_time_us = (end - start) / iterations * 1_000_000
    print(f"{name:<35}: {avg_time_us:.2f} μs | Result: {result}")
    return avg_time_us

def main():
    print("OPTIMIZED ASME EQUATION PERFORMANCE TEST")
    print("=" * 60)
    
    # Original ASME equation with dimensionless quantities
    def original_asme():
        return (qnty_P * qnty_D) / (2 * (qnty_S * qnty_E * qnty_W + qnty_P * qnty_Y))
    
    # ASME with scalar approach (like Pint)
    def scalar_asme():
        E, W, Y = 0.8, 1.0, 0.4  # Plain scalars
        return (qnty_P * qnty_D) / (2 * (qnty_S * E * W + qnty_P * Y))
    
    # Pint baseline
    def pint_asme():
        E, W, Y = 0.8, 1.0, 0.4
        return (pint_P * pint_D) / (2 * (pint_S * E * W + pint_P * Y))
    
    # Simple multiplication baseline
    def simple_multiply():
        return Quantity(10.0, LengthUnits.meter) * Quantity(5.0, LengthUnits.meter)
    
    def pint_simple_multiply():
        return ureg.Quantity(10.0, "meter") * ureg.Quantity(5.0, "meter")
    
    print("\n--- BASELINE SIMPLE OPERATIONS ---")
    simple_qnty_time = benchmark_operation(simple_multiply, "Qnty Simple Multiply", 2000)
    simple_pint_time = benchmark_operation(pint_simple_multiply, "Pint Simple Multiply", 2000)
    simple_speedup = simple_pint_time / simple_qnty_time
    print(f"Simple operation speedup: {simple_speedup:.1f}x")
    
    print("\n--- COMPLEX ASME EQUATION TESTS ---")
    original_time = benchmark_operation(original_asme, "Original ASME (dimensionless)", 1000)
    scalar_time = benchmark_operation(scalar_asme, "Optimized ASME (scalars)", 1000)
    pint_time = benchmark_operation(pint_asme, "Pint ASME", 1000)
    
    print("\n--- PERFORMANCE ANALYSIS ---")
    original_speedup = pint_time / original_time
    scalar_speedup = pint_time / scalar_time
    optimization_improvement = original_time / scalar_time
    
    print(f"Original ASME speedup vs Pint:      {original_speedup:.1f}x")
    print(f"Optimized ASME speedup vs Pint:     {scalar_speedup:.1f}x")
    print(f"Optimization improvement:           {optimization_improvement:.1f}x faster")
    
    # Compare to simple operation efficiency
    per_op_original = original_time / 7  # ~7 operations in ASME equation
    per_op_scalar = scalar_time / 7
    per_op_simple = simple_qnty_time / 1  # 1 operation
    
    print(f"\nPer-operation efficiency:")
    print(f"Simple operation:                   {per_op_simple:.2f} μs/op")
    print(f"Original ASME per-operation:        {per_op_original:.2f} μs/op")
    print(f"Optimized ASME per-operation:       {per_op_scalar:.2f} μs/op")
    print(f"Efficiency improvement:             {per_op_original / per_op_scalar:.1f}x")
    
    # Target achievement analysis
    target_speedup = 20.0
    print(f"\n--- TARGET ACHIEVEMENT ---")
    print(f"Target speedup:                     {target_speedup:.1f}x")
    if scalar_speedup >= target_speedup:
        print(f"✅ TARGET ACHIEVED! ({scalar_speedup:.1f}x >= {target_speedup:.1f}x)")
    else:
        remaining_gap = target_speedup / scalar_speedup
        print(f"🔧 Remaining gap: {remaining_gap:.1f}x improvement needed")
        print(f"   Current progress: {(scalar_speedup/target_speedup)*100:.1f}% of target")

if __name__ == "__main__":
    main()