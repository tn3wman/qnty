#!/usr/bin/env python3
"""
ASME Equation Performance Analysis
================================

Detailed profiling of the Complex ASME equation to identify performance bottlenecks
compared to simpler operations that achieve 20-30x speedup.
"""

import cProfile
import pstats
import time
from io import StringIO

import pint

from qnty.quantities import Quantity
from qnty.units import DimensionlessUnits, LengthUnits, PressureUnits

# Initialize Pint registry
ureg = pint.UnitRegistry()

# Create test quantities
qnty_P = Quantity(2900.75, PressureUnits.psi)
qnty_D = Quantity(168.275, LengthUnits.millimeter)
qnty_S = Quantity(137.895, PressureUnits.MPa)
qnty_E = Quantity(0.8, DimensionlessUnits.dimensionless)
qnty_W = Quantity(1.0, DimensionlessUnits.dimensionless)
qnty_Y = Quantity(0.4, DimensionlessUnits.dimensionless)

pint_P = ureg.Quantity(2900.75, "psi")
pint_D = ureg.Quantity(168.275, "mm")
pint_S = ureg.Quantity(137.895, "MPa")

def qnty_simple_multiply():
    """Simple multiplication (Length * Length = Area) - achieves ~25x speedup"""
    length = Quantity(10.0, LengthUnits.meter)
    width = Quantity(5.0, LengthUnits.meter)
    return length * width

def pint_simple_multiply():
    """Pint simple multiplication baseline"""
    length = ureg.Quantity(10.0, "meter")
    width = ureg.Quantity(5.0, "meter")
    return length * width

def qnty_complex_asme():
    """Complex ASME equation - only achieves ~13.7x speedup"""
    return (qnty_P * qnty_D) / (2 * (qnty_S * qnty_E * qnty_W + qnty_P * qnty_Y))

def pint_complex_asme():
    """Pint complex ASME equation baseline"""
    E = 0.8
    W = 1.0
    Y = 0.4
    return (pint_P * pint_D) / (2 * (pint_S * E * W + pint_P * Y))

def detailed_qnty_asme_breakdown():
    """Break down ASME equation step by step for detailed analysis"""
    # Step 1: P * D (Pressure × Length)
    numerator = qnty_P * qnty_D
    
    # Step 2: S * E * W (Pressure × Dimensionless × Dimensionless)
    inner_product = qnty_S * qnty_E * qnty_W
    
    # Step 3: P * Y (Pressure × Dimensionless)
    pressure_term = qnty_P * qnty_Y
    
    # Step 4: Add terms (Pressure + Pressure)
    denominator_inner = inner_product + pressure_term
    
    # Step 5: Multiply by 2 (Dimensionless × Pressure)
    two = Quantity(2, DimensionlessUnits.dimensionless)
    denominator = two * denominator_inner
    
    # Step 6: Final division (Pressure×Length / Pressure)
    return numerator / denominator

def detailed_pint_asme_breakdown():
    """Break down Pint ASME equation step by step"""
    E = 0.8
    W = 1.0
    Y = 0.4
    
    # Step 1: P * D
    numerator = pint_P * pint_D
    
    # Step 2: S * E * W (note: E, W are plain Python scalars)
    inner_product = pint_S * E * W
    
    # Step 3: P * Y
    pressure_term = pint_P * Y
    
    # Step 4: Add terms
    denominator_inner = inner_product + pressure_term
    
    # Step 5: Multiply by 2
    denominator = 2 * denominator_inner
    
    # Step 6: Final division
    return numerator / denominator

def profile_operation(func, name, iterations=1000):
    """Profile an operation and return timing statistics"""
    print(f"\n=== Profiling {name} ===")
    
    # Time the operation
    start_time = time.perf_counter()
    for _ in range(iterations):
        result = func()
    end_time = time.perf_counter()
    
    avg_time_us = (end_time - start_time) / iterations * 1_000_000
    print(f"Average time: {avg_time_us:.2f} μs per operation")
    print(f"Result: {result}")
    
    return avg_time_us

def count_operations():
    """Count the number of operations in each equation"""
    print("\n=== Operation Count Analysis ===")
    
    # Simple multiplication: Length * Length = Area (1 multiplication)
    print("Simple Multiplication Operations:")
    print("  - 1 multiplication (Length × Length)")
    print("  - 1 dimensional signature multiplication")
    print("  - 1 result unit lookup/creation")
    print("  Total: ~3 core operations")
    
    # Complex ASME equation operations
    print("\nComplex ASME Equation Operations:")
    print("  - P * D: Pressure × Length (1 mult)")
    print("  - S * E: Pressure × Dimensionless (1 mult)")
    print("  - (S*E) * W: Result × Dimensionless (1 mult)")
    print("  - P * Y: Pressure × Dimensionless (1 mult)")
    print("  - (S*E*W) + (P*Y): Pressure + Pressure (1 add)")
    print("  - 2 * result: Dimensionless × Pressure (1 mult)")
    print("  - (P*D) / (2*...): Final division (1 div)")
    print("  Total: ~7 arithmetic operations")
    print("  Plus: ~7 dimensional signature operations")
    print("  Plus: ~7 unit lookups/creations")
    print("  Plus: Intermediate object allocations")

def analyze_object_creation():
    """Analyze temporary object creation patterns"""
    print("\n=== Object Creation Analysis ===")
    print("Simple Multiplication:")
    print("  - Input: 2 existing Quantity objects")
    print("  - Output: 1 new Quantity object")
    print("  - Total objects created: 1")
    
    print("\nComplex ASME Equation:")
    print("  - Input: 6 existing Quantity objects")
    print("  - Intermediate results: 6 temporary Quantity objects")
    print("  - Output: 1 final Quantity object")
    print("  - Total objects created: 7")
    print("  - Memory allocation: ~7x more than simple operation")

def compare_dimensional_complexity():
    """Compare dimensional signature complexity"""
    print("\n=== Dimensional Signature Complexity ===")
    
    print("Simple Multiplication (Length × Length):")
    print(f"  - Input dimensions: {LengthUnits.meter.dimension._signature} × {LengthUnits.meter.dimension._signature}")
    print(f"  - Result dimension: {LengthUnits.meter.dimension._signature * LengthUnits.meter.dimension._signature}")
    print("  - Cache lookup: Likely cached (common area operation)")
    
    print("\nComplex ASME Equation:")
    print(f"  - Pressure: {PressureUnits.psi.dimension._signature}")
    print(f"  - Length: {LengthUnits.millimeter.dimension._signature}")
    print(f"  - Dimensionless: {DimensionlessUnits.dimensionless.dimension._signature}")
    print("  - Multiple mixed-dimension operations")
    print("  - Complex result dimensions requiring new unit creation")
    print("  - Less likely to hit cache for intermediate results")

def performance_breakdown_analysis():
    """Analyze where performance is lost in complex operations"""
    print("\n" + "="*80)
    print("PERFORMANCE BREAKDOWN ANALYSIS")
    print("="*80)
    
    # Run timing comparisons
    simple_qnty_time = profile_operation(qnty_simple_multiply, "Qnty Simple Multiplication", 2000)
    simple_pint_time = profile_operation(pint_simple_multiply, "Pint Simple Multiplication", 2000)
    
    complex_qnty_time = profile_operation(qnty_complex_asme, "Qnty Complex ASME", 1000)
    complex_pint_time = profile_operation(pint_complex_asme, "Pint Complex ASME", 1000)
    
    # Calculate speedups
    simple_speedup = simple_pint_time / simple_qnty_time
    complex_speedup = complex_pint_time / complex_qnty_time
    
    print(f"\n=== SPEEDUP COMPARISON ===")
    print(f"Simple Multiplication Speedup: {simple_speedup:.1f}x")
    print(f"Complex ASME Speedup: {complex_speedup:.1f}x")
    print(f"Performance Loss: {simple_speedup / complex_speedup:.1f}x slower than expected")
    
    # Analyze per-operation overhead
    operations_per_simple = 3  # Estimated core operations
    operations_per_complex = 21  # Estimated total operations (7 arithmetic + 7 dimensional + 7 unit)
    
    qnty_per_op_simple = simple_qnty_time / operations_per_simple
    qnty_per_op_complex = complex_qnty_time / operations_per_complex
    
    print(f"\n=== PER-OPERATION ANALYSIS ===")
    print(f"Qnty time per operation (simple): {qnty_per_op_simple:.2f} μs")
    print(f"Qnty time per operation (complex): {qnty_per_op_complex:.2f} μs")
    print(f"Overhead increase: {qnty_per_op_complex / qnty_per_op_simple:.1f}x per operation")
    
    # Identify bottlenecks
    print(f"\n=== BOTTLENECK IDENTIFICATION ===")
    overhead_ratio = qnty_per_op_complex / qnty_per_op_simple
    if overhead_ratio > 1.5:
        print("❌ Significant per-operation overhead detected")
        print("   Potential causes:")
        print("   - Cache misses for complex dimensional combinations")
        print("   - Excessive object creation and garbage collection")
        print("   - Complex unit resolution for mixed dimensions")
        print("   - Repeated dimensional signature calculations")
    else:
        print("✅ Per-operation overhead within acceptable range")
        print("   Performance loss is primarily due to operation count")

def optimization_recommendations():
    """Provide specific optimization recommendations"""
    print("\n" + "="*80)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("="*80)
    
    print("\n1. DIMENSIONAL SIGNATURE CACHING")
    print("   - Pre-cache common engineering combinations")
    print("   - Implement LRU cache for mixed-dimension results")
    print("   - Priority: HIGH (estimated 15-25% improvement)")
    
    print("\n2. OBJECT POOLING")
    print("   - Reuse intermediate Quantity objects")
    print("   - Implement object pool for common operations")
    print("   - Priority: MEDIUM (estimated 10-15% improvement)")
    
    print("\n3. OPERATION FUSION")
    print("   - Detect common expression patterns")
    print("   - Fuse multiple operations into single optimized functions")
    print("   - Priority: HIGH (estimated 20-30% improvement)")
    
    print("\n4. LAZY EVALUATION")
    print("   - Defer intermediate calculations")
    print("   - Only evaluate when final result is needed")
    print("   - Priority: LOW (complex to implement)")
    
    print("\n5. SPECIALIZED ARITHMETIC PATHS")
    print("   - Fast paths for mixed scalar/quantity operations")
    print("   - Optimize dimensionless quantity handling")
    print("   - Priority: MEDIUM (estimated 8-12% improvement)")
    
    print("\n6. UNIT RESOLUTION OPTIMIZATION")
    print("   - Pre-compute common engineering unit combinations")
    print("   - Optimize unit lookup tables")
    print("   - Priority: HIGH (estimated 10-20% improvement)")

if __name__ == "__main__":
    print("ASME Equation Performance Analysis")
    print("=" * 50)
    
    # Count operations
    count_operations()
    
    # Analyze object creation
    analyze_object_creation()
    
    # Compare dimensional complexity
    compare_dimensional_complexity()
    
    # Performance breakdown
    performance_breakdown_analysis()
    
    # Optimization recommendations
    optimization_recommendations()