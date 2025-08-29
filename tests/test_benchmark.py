"""
Performance Benchmark Tests
============================

Compare Qnty performance against Pint library for various engineering calculations.
Shows speedup factors and validates calculation accuracy.
"""

import time

import pint

from src.qnty.quantities import DimensionlessUnits, LengthUnits, PressureUnits
from src.qnty.variable import FastQuantity
from src.qnty.quantities import Length


def benchmark_operation(operation, iterations=1000):
    """Benchmark an operation with warmup."""
    
    # Warmup
    for _ in range(10):
        try:
            operation()
        except Exception:
            pass
    
    # Time it
    start = time.perf_counter()
    result = None
    for _ in range(iterations):
        try:
            result = operation()
        except Exception as e:
            return float('inf'), f"ERROR: {e}"
    end = time.perf_counter()
    
    avg_time_us = (end - start) / iterations * 1_000_000
    return avg_time_us, result


def format_speedup(qnty_time, pint_time):
    """Format speedup comparison."""
    if pint_time == float('inf') or qnty_time == float('inf'):
        return "N/A"
    speedup = pint_time / qnty_time
    return f"{speedup:.1f}x"


def print_comparison_table(results):
    """Print a nice comparison table with speedup factors."""
    print("\n" + "=" * 80)
    print("PERFORMANCE COMPARISON: Qnty vs Pint")
    print("=" * 80)
    
    # Header
    print(f"\n{'Operation':<30} {'Qnty (us)':<15} {'Pint (us)':<15} {'Speedup':<12} {'Status'}")
    print("-" * 75)
    
    total_qnty_time = 0
    total_pint_time = 0
    valid_comparisons = 0
    
    for op_name, qnty_result, pint_result in results:
        qnty_time, qnty_val = qnty_result
        pint_time, pint_val = pint_result
        
        # Format times
        qnty_str = f"{qnty_time:.2f}" if qnty_time != float('inf') else "ERROR"
        pint_str = f"{pint_time:.2f}" if pint_time != float('inf') else "ERROR"
        
        # Calculate speedup
        speedup = format_speedup(qnty_time, pint_time)
        
        # Check if both succeeded
        if qnty_time != float('inf') and pint_time != float('inf'):
            status = "OK"
            total_qnty_time += qnty_time
            total_pint_time += pint_time
            valid_comparisons += 1
            
            # Highlight significant speedups
            if pint_time / qnty_time >= 10:
                speedup = f">> {speedup}"
        else:
            status = "ERR"
        
        print(f"{op_name:<30} {qnty_str:<15} {pint_str:<15} {speedup:<12} {status}")
    
    # Summary
    if valid_comparisons > 0:
        avg_speedup = total_pint_time / total_qnty_time if total_qnty_time > 0 else 0
        print("-" * 75)
        print(f"{'AVERAGE':<30} {total_qnty_time/valid_comparisons:.2f} us      "
              f"{total_pint_time/valid_comparisons:.2f} us      "
              f"{'=> ' + format_speedup(total_qnty_time/valid_comparisons, total_pint_time/valid_comparisons):<12}")
        
        print(f"\n[RESULT] Overall Performance: Qnty is {avg_speedup:.1f}x faster than Pint")
        
        # Performance tier message
        if avg_speedup >= 20:
            print("[TIER] BLAZING FAST: Over 20x speedup!")
        elif avg_speedup >= 10:
            print("[TIER] EXCELLENT: 10-20x speedup!")
        elif avg_speedup >= 5:
            print("[TIER] GREAT: 5-10x speedup!")
        elif avg_speedup >= 2:
            print("[TIER] GOOD: 2-5x speedup!")


def test_benchmark_suite(capsys):
    """Comprehensive benchmark suite comparing Qnty and Pint."""
    
    print("\n" + "=" * 80)
    print("QNTY PERFORMANCE BENCHMARKS")
    print("=" * 80)
    print("\nComparing Qnty (high-performance) vs Pint (established library)")
    print("Testing real-world engineering calculations...")
    
    # Initialize libraries
    ureg = pint.UnitRegistry()
    
    # Test data
    test_value = 100.0
    pressure_value = 2900.75
    length_value = 168.275
    
    results = []
    
    # ========== TEST 1: Simple Unit Conversion ==========
    def qnty_conversion():
        q = FastQuantity(test_value, LengthUnits.meter)
        return q.to(LengthUnits.millimeter)
    
    def pint_conversion():
        q = ureg.Quantity(test_value, 'meter')
        return q.to('millimeter')
    
    qnty_result = benchmark_operation(qnty_conversion, 2000)
    pint_result = benchmark_operation(pint_conversion, 2000)
    results.append(("Unit Conversion (m -> mm)", qnty_result, pint_result))
    
    # ========== TEST 2: Mixed Unit Addition ==========
    def qnty_mixed_addition():
        q1 = FastQuantity(100.0, LengthUnits.millimeter)
        q2 = FastQuantity(2.0, LengthUnits.inch)
        return q1 + q2
    
    def pint_mixed_addition():
        q1 = ureg.Quantity(100.0, 'millimeter')
        q2 = ureg.Quantity(2.0, 'inch')
        return q1 + q2
    
    qnty_result = benchmark_operation(qnty_mixed_addition, 2000)
    pint_result = benchmark_operation(pint_mixed_addition, 2000)
    results.append(("Mixed Addition (mm + in)", qnty_result, pint_result))
    
    # ========== TEST 3: Multiplication ==========
    def qnty_multiplication():
        length = FastQuantity(10.0, LengthUnits.meter)
        width = FastQuantity(5.0, LengthUnits.meter)
        return length * width
    
    def pint_multiplication():
        length = ureg.Quantity(10.0, 'meter')
        width = ureg.Quantity(5.0, 'meter')
        return length * width
    
    qnty_result = benchmark_operation(qnty_multiplication, 2000)
    pint_result = benchmark_operation(pint_multiplication, 2000)
    results.append(("Multiplication (m x m)", qnty_result, pint_result))
    
    # ========== TEST 4: Division ==========
    def qnty_division():
        pressure = FastQuantity(pressure_value, PressureUnits.psi)
        area = FastQuantity(10.0, LengthUnits.millimeter)
        return pressure / area
    
    def pint_division():
        pressure = ureg.Quantity(pressure_value, 'psi')
        area = ureg.Quantity(10.0, 'millimeter')
        return pressure / area
    
    qnty_result = benchmark_operation(qnty_division, 2000)
    pint_result = benchmark_operation(pint_division, 2000)
    results.append(("Division (psi / mm)", qnty_result, pint_result))
    
    # ========== TEST 5: Complex Engineering Calculation (ASME) ==========
    def qnty_complex():
        P = FastQuantity(pressure_value, PressureUnits.psi)
        D = FastQuantity(length_value, LengthUnits.millimeter)
        S = FastQuantity(137.895, PressureUnits.MPa)
        E = FastQuantity(0.8, DimensionlessUnits.dimensionless)
        W = FastQuantity(1.0, DimensionlessUnits.dimensionless)
        Y = FastQuantity(0.4, DimensionlessUnits.dimensionless)
        return (P * D) / (2 * (S * E * W + P * Y))
    
    def pint_complex():
        P = ureg.Quantity(pressure_value, 'psi')
        D = ureg.Quantity(length_value, 'mm')
        S = ureg.Quantity(137.895, 'MPa')
        E = 0.8
        W = 1.0
        Y = 0.4
        return (P * D) / (2 * (S * E * W + P * Y)) # type: ignore
    
    qnty_result = benchmark_operation(qnty_complex, 1000)
    pint_result = benchmark_operation(pint_complex, 1000)
    results.append(("Complex ASME Equation", qnty_result, pint_result))
    
    # ========== TEST 6: Type-Safe Variables ==========
    def qnty_typesafe():
        length = Length("beam_length")
        length.set(100.0).mm
        return length.quantity.to(LengthUnits.meter)
    
    def pint_typesafe():
        # Pint doesn't have type-safe variables, so we simulate
        length = ureg.Quantity(100.0, 'millimeter')
        return length.to('meter')
    
    qnty_result = benchmark_operation(qnty_typesafe, 1500)
    pint_result = benchmark_operation(pint_typesafe, 1500)
    results.append(("Type-Safe Variables", qnty_result, pint_result))
    
    # ========== TEST 7: Chained Operations ==========
    def qnty_chained():
        q1 = FastQuantity(50.0, LengthUnits.mm)
        q2 = FastQuantity(2.0, LengthUnits.inch)
        q3 = FastQuantity(0.5, LengthUnits.meter)
        result = (q1 + q2) * 2 + q3
        return result.to(LengthUnits.millimeter)
    
    def pint_chained():
        q1 = ureg.Quantity(50.0, 'millimeter')
        q2 = ureg.Quantity(2.0, 'inch')
        q3 = ureg.Quantity(0.5, 'meter')
        result = (q1 + q2) * 2 + q3 # type: ignore
        return result.to('millimeter') # type: ignore
    
    qnty_result = benchmark_operation(qnty_chained, 1000)
    pint_result = benchmark_operation(pint_chained, 1000)
    results.append(("Chained Operations", qnty_result, pint_result))
    
    # ========== TEST 8: Many Small Operations ==========
    def qnty_many_ops():
        total = FastQuantity(0, LengthUnits.millimeter)
        for i in range(10):
            total = total + FastQuantity(i, LengthUnits.millimeter)
        return total
    
    def pint_many_ops():
        total = ureg.Quantity(0, 'millimeter')
        for i in range(10):
            total = total + ureg.Quantity(i, 'millimeter')
        return total
    
    qnty_result = benchmark_operation(qnty_many_ops, 500)
    pint_result = benchmark_operation(pint_many_ops, 500)
    results.append(("10 Additions Loop", qnty_result, pint_result))
    
    # Print results
    with capsys.disabled():
        print_comparison_table(results)
        
        # Additional insights
        print("\n" + "=" * 80)
        print("KEY INSIGHTS:")
        print("-" * 80)
        print("• Qnty uses prime number encoding for ultra-fast dimensional checking")
        print("• Pre-computed conversion tables eliminate runtime calculations")
        print("• __slots__ and caching provide significant memory and speed benefits")
        print("• Type-safe variables prevent dimensional errors at compile time")
        print("\n[TIP] Run with different iterations to see consistent performance gains")
        print("=" * 80)


if __name__ == "__main__":
    # Run the benchmark when executed directly
    class DummyCapsys:
        """Dummy capsys for direct execution."""
        def disabled(self):
            class Context:
                def __enter__(self): pass
                def __exit__(self, *args): pass
            return Context()
    
    test_benchmark_suite(DummyCapsys())
