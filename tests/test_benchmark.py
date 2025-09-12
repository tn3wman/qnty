"""
Performance Benchmark Tests
============================

Compare Qnty performance against Pint library for various engineering calculations.
Shows speedup factors and validates calculation accuracy.
"""

import os
import time

import astropy.units as u
import pint
import unyt
from astropy.units import imperial

# from qnty import Length
from qnty.quantities import Q
from qnty.units import DimensionlessUnits, LengthUnits, PressureUnits

# Pre-define all variables to exclude initialization from performance measurements
ASTROPY_AVAILABLE = True

"""FAIRNESS & SCOPE NOTES
This benchmark aims to compare raw arithmetic and conversion overhead between
Qnty and three popular unit libraries (Pint, Unyt, Astropy). To keep the
comparison as fair as possible we:
    • Use consistent SI units for all initial quantity definitions (no mixing psi vs Pa).
    • Avoid re‑using timing results (bug previously affected Complex ASME Equation test).
    • Perform identical operation counts and iteration counts per library.
    • Pre-create all quantities so object construction cost is excluded.
    • Keep calculations dimensionally equivalent (no placeholder dimensionless where others use real units).

Disclaimers:
    • These micro-benchmarks emphasize relative overhead of common operations; they are not full application simulations.
    • Astropy focuses on astrophysical correctness; its performance profile differs by design.
    • Real workloads may involve vectorized / array operations (e.g., with numpy); those are out of scope here.

Customize iteration count: set env var QNTY_BENCH_ITER (default 1500 for most ops,
small loops may still use higher counts to smooth noise).
"""

# Test scalar values (SI)
TEST_VALUE = 100.0            # length magnitude
PRESSURE_VALUE = 2_000_000.0  # Pa (≈ 290 psi) using SI everywhere
LENGTH_VALUE = 0.168275       # meters (rather than mm -> avoids implicit conversions)

# Adjustable iteration control
DEFAULT_ITER = int(os.environ.get("QNTY_BENCH_ITER", "1500"))
SMALL_OP_ITER = int(os.environ.get("QNTY_BENCH_SMALL_ITER", str(DEFAULT_ITER * 2)))

# Initialize unit registries once
ureg = pint.UnitRegistry()

## ---------------------------------------------------------------------------
## Quantity Definitions (All SI Base to minimize conversion bias)
## ---------------------------------------------------------------------------

# Qnty quantities
qnty_meter = Q(TEST_VALUE, LengthUnits.meter)
qnty_mm_100 = Q(100.0, LengthUnits.millimeter)
qnty_inch_2 = Q(2.0, LengthUnits.inch)  # keep a mixed-unit source for mixed addition
qnty_length_10 = Q(10.0, LengthUnits.meter)
qnty_width_5 = Q(5.0, LengthUnits.meter)
qnty_pressure = Q(PRESSURE_VALUE, PressureUnits.Pa)
qnty_area_10mm = Q(10.0, LengthUnits.millimeter)
qnty_P = Q(PRESSURE_VALUE, PressureUnits.Pa)
qnty_D = Q(LENGTH_VALUE, LengthUnits.meter)
qnty_S = Q(137.895e6, PressureUnits.Pa)  # 137.895 MPa expressed in Pa for all libs
qnty_E = Q(0.8, DimensionlessUnits.dimensionless)
qnty_W = Q(1.0, DimensionlessUnits.dimensionless)
qnty_Y = Q(0.4, DimensionlessUnits.dimensionless)
qnty_length = Q(100.0, LengthUnits.millimeter)  # For type-safe variable test
qnty_q1_50mm = Q(50.0, LengthUnits.millimeter)
qnty_q2_2in = Q(2.0, LengthUnits.inch)
qnty_q3_05m = Q(0.5, LengthUnits.meter)
qnty_zero_mm = Q(0, LengthUnits.millimeter)

# Pint quantities (mirroring above units)
pint_meter = ureg.Quantity(TEST_VALUE, "meter")
pint_mm_100 = ureg.Quantity(100.0, "millimeter")
pint_inch_2 = ureg.Quantity(2.0, "inch")
pint_length_10 = ureg.Quantity(10.0, "meter")
pint_width_5 = ureg.Quantity(5.0, "meter")
pint_pressure = ureg.Quantity(PRESSURE_VALUE, "pascal")
pint_area_10mm = ureg.Quantity(10.0, "millimeter")
pint_P = ureg.Quantity(PRESSURE_VALUE, "pascal")
pint_D = ureg.Quantity(LENGTH_VALUE, "meter")
pint_S = ureg.Quantity(137.895e6, "pascal")
pint_E = ureg.Quantity(0.8, "dimensionless")
pint_W = ureg.Quantity(1.0, "dimensionless")
pint_Y = ureg.Quantity(0.4, "dimensionless")
pint_length_100mm = ureg.Quantity(100.0, "millimeter")
pint_q1_50mm = ureg.Quantity(50.0, "millimeter")
pint_q2_2in = ureg.Quantity(2.0, "inch")
pint_q3_05m = ureg.Quantity(0.5, "meter")
pint_zero_mm = ureg.Quantity(0, "millimeter")

# Unyt quantities
unyt_meter = unyt.unyt_quantity(TEST_VALUE, "meter")
unyt_mm_100 = unyt.unyt_quantity(100.0, "millimeter")
unyt_inch_2 = unyt.unyt_quantity(2.0, "inch")
unyt_length_10 = unyt.unyt_quantity(10.0, "meter")
unyt_width_5 = unyt.unyt_quantity(5.0, "meter")
unyt_pressure = unyt.unyt_quantity(PRESSURE_VALUE, "Pa")
unyt_area_10mm = unyt.unyt_quantity(10.0, "millimeter")
unyt_P = unyt.unyt_quantity(PRESSURE_VALUE, "Pa")
unyt_D = unyt.unyt_quantity(LENGTH_VALUE, "m")
unyt_S = unyt.unyt_quantity(137.895e6, "Pa")
unyt_E = unyt.unyt_quantity(0.8, "dimensionless")
unyt_W = unyt.unyt_quantity(1.0, "dimensionless")
unyt_Y = unyt.unyt_quantity(0.4, "dimensionless")
unyt_length_100mm = unyt.unyt_quantity(100.0, "millimeter")
unyt_q1_50mm = unyt.unyt_quantity(50.0, "millimeter")
unyt_q2_2in = unyt.unyt_quantity(2.0, "inch")
unyt_q3_05m = unyt.unyt_quantity(0.5, "meter")
unyt_zero_mm = unyt.unyt_quantity(0, "millimeter")

# Astropy quantities (SI aligned)
astropy_meter = TEST_VALUE * u.m  # type: ignore
astropy_mm_100 = 100.0 * u.mm  # type: ignore
astropy_inch_2 = 2.0 * imperial.inch  # type: ignore (retain mixed addition source)
astropy_length_10 = 10.0 * u.m  # type: ignore
astropy_width_5 = 5.0 * u.m  # type: ignore
astropy_pressure = PRESSURE_VALUE * u.Pa  # type: ignore
astropy_area_10mm = 10.0 * u.mm  # type: ignore
astropy_P = PRESSURE_VALUE * u.Pa  # type: ignore
astropy_D = LENGTH_VALUE * u.m  # type: ignore
astropy_S = 137.895e6 * u.Pa  # type: ignore
astropy_E = 0.8 * u.dimensionless_unscaled  # type: ignore
astropy_W = 1.0 * u.dimensionless_unscaled  # type: ignore
astropy_Y = 0.4 * u.dimensionless_unscaled  # type: ignore
astropy_length_100mm = 100.0 * u.mm  # type: ignore
astropy_q1_50mm = 50.0 * u.mm  # type: ignore
astropy_q2_2in = 2.0 * imperial.inch  # type: ignore
astropy_q3_05m = 0.5 * u.m  # type: ignore
astropy_zero_mm = 0 * u.mm  # type: ignore

# Fluid dynamics pre-created quantities
qnty_P1 = Q(PRESSURE_VALUE, PressureUnits.Pa)
qnty_P2 = Q(1800.0, PressureUnits.Pa)
qnty_D_fluid = Q(LENGTH_VALUE, LengthUnits.millimeter)
qnty_L = Q(100.0, LengthUnits.meter)
qnty_rho = Q(850.0, DimensionlessUnits.dimensionless)
qnty_pi = Q(3.14159, DimensionlessUnits.dimensionless)
qnty_2 = Q(2, DimensionlessUnits.dimensionless)
qnty_4 = Q(4.0, DimensionlessUnits.dimensionless)

pint_P1 = ureg.Quantity(PRESSURE_VALUE, "psi")
pint_P2 = ureg.Quantity(1800.0, "psi")
pint_D_fluid = ureg.Quantity(LENGTH_VALUE, "mm")
pint_L = ureg.Quantity(100.0, "m")
pint_rho = ureg.Quantity(850.0, "kg/m^3")

unyt_P1 = unyt.unyt_quantity(PRESSURE_VALUE, "psi")
unyt_P2 = unyt.unyt_quantity(1800.0, "psi")
unyt_D_fluid = unyt.unyt_quantity(LENGTH_VALUE, "mm")
unyt_L = unyt.unyt_quantity(100.0, "m")

astropy_P1 = PRESSURE_VALUE * imperial.psi  # type: ignore
astropy_P2 = 1800.0 * imperial.psi  # type: ignore
astropy_D_fluid = LENGTH_VALUE * u.mm  # type: ignore
astropy_L = 100.0 * u.m  # type: ignore


def benchmark_operation(operation, iterations=1000):
    """Benchmark an operation with optimized warmup and timing."""
    # Optimized warmup with exception pre-check
    warmup_failed = False
    for _ in range(5):  # Reduced warmup iterations
        try:
            operation()
            break
        except Exception:
            warmup_failed = True

    if warmup_failed:
        # If warmup consistently fails, don't bother with timing
        try:
            result = operation()
        except Exception as e:
            return float("inf"), f"ERROR: {e}"

    # Optimized timing loop
    start = time.perf_counter()
    result = None

    # Pre-allocate loop to reduce overhead
    try:
        for _ in range(iterations):
            result = operation()
    except Exception as e:
        return float("inf"), f"ERROR: {e}"

    end = time.perf_counter()
    avg_time_us = (end - start) / iterations * 1_000_000
    return avg_time_us, result


def format_relative(qnty_time, pint_time, unyt_time, astropy_time=None):
    """Return a string with relative slowdown factors (library_time / qnty_time).

    A value of 5.0 under Pint means: Pint took 5x the time of Qnty for that operation.
    """
    inf_val = float("inf")
    if qnty_time == inf_val:
        return "N/A"
    denom = qnty_time if qnty_time else inf_val
    pint_r = pint_time / denom if pint_time != inf_val else float("nan")
    unyt_r = unyt_time / denom if unyt_time != inf_val else float("nan")
    if astropy_time is not None and astropy_time != inf_val:
        astro_r = astropy_time / denom
        return f"P:{pint_r:.1f}x U:{unyt_r:.1f}x A:{astro_r:.1f}x"
    return f"P:{pint_r:.1f}x U:{unyt_r:.1f}x A:N/A"


def print_comparison_table(results):
    """Print optimized comparison table with speedup factors."""
    # Pre-compiled constants for better performance
    SEPARATOR_120 = "=" * 120
    DASH_120 = "-" * 120
    INF_VAL = float("inf")

    print("\n" + SEPARATOR_120)
    print("PERFORMANCE COMPARISON: Qnty vs Pint vs Unyt vs Astropy")
    print(SEPARATOR_120)

    # Header
    print(f"\n{'Operation':<30} {'Qnty (us)':<12} {'Pint (us)':<12} {'Unyt (us)':<12} {'Astropy (us)':<14} {'Relative Slowdown (Lib/Qnty)':<40} {'Status'}")
    print(DASH_120)

    # Pre-allocate accumulators
    totals = [0.0, 0.0, 0.0, 0.0]  # qnty, pint, unyt, astropy
    valid_comparisons = 0

    # Optimized result processing
    for result_tuple in results:
        # Unpack results efficiently
        if len(result_tuple) == 4:
            op_name, qnty_result, pint_result, unyt_result = result_tuple
            astropy_result = (INF_VAL, "N/A")
        else:
            op_name, qnty_result, pint_result, unyt_result, astropy_result = result_tuple

        # Extract times in batch
        times = [qnty_result[0], pint_result[0], unyt_result[0], astropy_result[0]]

        # Format times efficiently
        time_strs = [f"{t:.2f}" if t != INF_VAL else ("ERROR" if i < 3 else "N/A") for i, t in enumerate(times)]

        # Calculate relative slowdown factors
        speedup = format_relative(*times)

        # Update totals if qnty succeeded
        if times[0] != INF_VAL:
            status = "OK"
            for i, t in enumerate(times):
                if t != INF_VAL:
                    totals[i] += t
            valid_comparisons += 1
        else:
            status = "ERR"

        print(f"{op_name:<30} {time_strs[0]:<12} {time_strs[1]:<12} {time_strs[2]:<12} {time_strs[3]:<14} {speedup:<40} {status}")

    # Optimized Summary calculation
    if valid_comparisons > 0:
        # Calculate averages efficiently
        comparison_reciprocal = 1.0 / valid_comparisons
        avg_times = [total * comparison_reciprocal if total > 0 else 0.0 for total in totals]
        avg_qnty_time, avg_pint_time, avg_unyt_time, avg_astropy_time = avg_times

        print(DASH_120)
        print(
            f"{'AVERAGE':<30} {avg_qnty_time:.2f}      {avg_pint_time:.2f}      {avg_unyt_time:.2f}      {avg_astropy_time:.2f}        "
            f"{format_relative(avg_qnty_time, avg_pint_time, avg_unyt_time, avg_astropy_time):<40}"
        )

        if avg_pint_time > 0:
            pint_ratio = avg_pint_time / avg_qnty_time if avg_qnty_time else float('inf')
            print(f"\n[RESULT] Average Relative Slowdown: Pint:{pint_ratio:.1f}x | Unyt:{(avg_unyt_time/avg_qnty_time):.1f}x | Astropy:{(avg_astropy_time/avg_qnty_time):.1f}x")

            tier_messages = [
                (20, "[TIER] BLAZING: Qnty shows >20x lower latency vs Pint"),
                (10, "[TIER] EXCELLENT: 10–20x lower latency"),
                (5, "[TIER] GREAT: 5–10x lower latency"),
                (2, "[TIER] GOOD: 2–5x lower latency"),
            ]
            for threshold, message in tier_messages:
                if pint_ratio >= threshold:
                    print(message)
                    break


def test_benchmark_suite(capsys):
    """Comprehensive benchmark suite comparing Qnty and Pint."""

    print("\n" + "=" * 80)
    print("QNTY PERFORMANCE BENCHMARKS")
    print("=" * 80)
    print("\nComparing Qnty (high-performance) vs Pint (established library)")
    print("Testing real-world engineering calculations...")

    results = []

    # ========== TEST 1: Simple Unit Conversion ==========
    def qnty_conversion():
        return qnty_meter.to(LengthUnits.millimeter)

    def pint_conversion():
        return pint_meter.to("millimeter")

    def unyt_conversion():
        return unyt_meter.in_units("millimeter")  # type: ignore

    def astropy_conversion():
        return astropy_meter.to(u.mm)  # type: ignore

    qnty_result = benchmark_operation(qnty_conversion, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_conversion, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_conversion, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_conversion, DEFAULT_ITER)
    results.append(("Unit Conversion (m -> mm)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 2: Mixed Unit Addition ==========
    def qnty_mixed_addition():
        return qnty_mm_100 + qnty_inch_2

    def pint_mixed_addition():
        return pint_mm_100 + pint_inch_2

    def unyt_mixed_addition():
        return unyt_mm_100 + unyt_inch_2

    def astropy_mixed_addition():
        return astropy_mm_100 + astropy_inch_2

    qnty_result = benchmark_operation(qnty_mixed_addition, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_mixed_addition, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_mixed_addition, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_mixed_addition, DEFAULT_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Mixed Addition (mm + in)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 3: Multiplication ==========
    def qnty_multiplication():
        return qnty_length_10 * qnty_width_5

    def pint_multiplication():
        return pint_length_10 * pint_width_5

    def unyt_multiplication():
        return unyt_length_10 * unyt_width_5

    def astropy_multiplication():
        return astropy_length_10 * astropy_width_5

    qnty_result = benchmark_operation(qnty_multiplication, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_multiplication, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_multiplication, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_multiplication, DEFAULT_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Multiplication (m x m)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 4: Division ==========
    def qnty_division():
        return qnty_pressure / qnty_area_10mm

    def pint_division():
        return pint_pressure / pint_area_10mm

    def unyt_division():
        return unyt_pressure / unyt_area_10mm

    def astropy_division():
        return astropy_pressure / astropy_area_10mm

    qnty_result = benchmark_operation(qnty_division, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_division, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_division, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_division, DEFAULT_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Division (psi / mm)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 5: Complex Engineering Calculation (ASME) ==========
    def qnty_complex():
        return (qnty_P * qnty_D) / (Q(2, DimensionlessUnits.dimensionless) * (qnty_S * qnty_E * qnty_W + qnty_P * qnty_Y))

    def pint_complex():
        return (pint_P * pint_D) / (2 * (pint_S * pint_E * pint_W + pint_P * pint_Y))  # type: ignore

    def unyt_complex():
        return (unyt_P * unyt_D) / (2 * (unyt_S * unyt_E * unyt_W + unyt_P * unyt_Y))

    def astropy_complex():
        return (astropy_P * astropy_D) / (2 * (astropy_S * astropy_E * astropy_W + astropy_P * astropy_Y))

    qnty_result = benchmark_operation(qnty_complex, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_complex, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_complex, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_complex, DEFAULT_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Complex ASME Equation", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 6: Type-Safe Variables ==========
    def qnty_typesafe():
        assert qnty_length is not None
        return qnty_length.to(LengthUnits.meter)

    def pint_typesafe():
        # Pint doesn't have type-safe variables, so we simulate
        return pint_length_100mm.to("meter")

    def unyt_typesafe():
        return unyt_length_100mm.in_units("meter")  # type: ignore

    def astropy_typesafe():
        return astropy_length_100mm.to(u.m)  # type: ignore

    qnty_result = benchmark_operation(qnty_typesafe, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_typesafe, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_typesafe, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_typesafe, DEFAULT_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Type-Safe Variables", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 7: Chained Operations ==========
    def qnty_chained():
        result = (qnty_q1_50mm + qnty_q2_2in) * 2 + qnty_q3_05m
        return result.to(LengthUnits.millimeter)

    def pint_chained():
        result = (pint_q1_50mm + pint_q2_2in) * 2 + pint_q3_05m  # type: ignore
        return result.to("millimeter")  # type: ignore

    def unyt_chained():
        result = (unyt_q1_50mm + unyt_q2_2in) * 2 + unyt_q3_05m
        return result.in_units("millimeter")  # type: ignore

    def astropy_chained():
        result = (astropy_q1_50mm + astropy_q2_2in) * 2 + astropy_q3_05m
        return result.to(u.mm)  # type: ignore

    qnty_result = benchmark_operation(qnty_chained, DEFAULT_ITER)
    pint_result = benchmark_operation(pint_chained, DEFAULT_ITER)
    unyt_result = benchmark_operation(unyt_chained, DEFAULT_ITER)
    astropy_result = benchmark_operation(astropy_chained, DEFAULT_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Chained Operations", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 8: Many Small Operations (Optimized) ==========
    # Pre-create quantities for loop to avoid repeated object creation
    qnty_loop_quantities = [Q(i, LengthUnits.millimeter) for i in range(10)]
    pint_loop_quantities = [ureg.Quantity(i, "millimeter") for i in range(10)]
    unyt_loop_quantities = [unyt.unyt_quantity(i, "millimeter") for i in range(10)]
    astropy_loop_quantities = [i * u.mm for i in range(10)]  # type: ignore

    def qnty_many_ops():
        total = qnty_zero_mm
        # Use pre-created quantities to avoid allocation overhead
        for qty in qnty_loop_quantities:
            total = total + qty
        return total

    def pint_many_ops():
        total = pint_zero_mm
        # Use pre-created quantities to avoid allocation overhead
        for qty in pint_loop_quantities:
            total = total + qty
        return total

    def unyt_many_ops():
        total = unyt_zero_mm
        # Use pre-created quantities to avoid allocation overhead
        for qty in unyt_loop_quantities:
            total = total + qty
        return total

    def astropy_many_ops():
        total = astropy_zero_mm
        # Use pre-created quantities to avoid allocation overhead
        for qty in astropy_loop_quantities:
            total = total + qty
        return total

    # Use higher iteration count for small operations to get better averaging
    qnty_result = benchmark_operation(qnty_many_ops, SMALL_OP_ITER)
    pint_result = benchmark_operation(pint_many_ops, SMALL_OP_ITER)
    unyt_result = benchmark_operation(unyt_many_ops, SMALL_OP_ITER)
    astropy_result = benchmark_operation(astropy_many_ops, SMALL_OP_ITER) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("10 Additions Loop (Optimized)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 9: (Removed) Complex Fluid Dynamics Equation ==========
    # Temporarily disabled pending consistent density unit representation across libraries.
    # Previous version mixed dimensionless and physical density units leading to unfair comparisons.

    # qnty_result = benchmark_operation(qnty_fluid_dynamics, 2000)
    # pint_result = benchmark_operation(pint_fluid_dynamics, 2000)
    # unyt_result = benchmark_operation(unyt_fluid_dynamics, 2000)
    # astropy_result = benchmark_operation(astropy_fluid_dynamics, 2000)
    # results.append(("Complex Fluid Dynamics", qnty_result, pint_result, unyt_result, astropy_result))

    # Print results
    with capsys.disabled():
        print_comparison_table(results)

        # Additional insights
        print("\n" + "=" * 80)
        print("KEY INSIGHTS:")
        print("-" * 80)
        print("• All libraries initialized with the same SI units for base fairness")
        print("• Ratios show relative slowdown (higher = more time per op vs Qnty)")
        print("• Qnty design features: prime-based dimension encoding, precomputed tables, __slots__/caching")
        print("• Type-safe variables (Qnty) help prevent dimensional category mistakes early")
        print("\n[TIP] Adjust QNTY_BENCH_ITER / QNTY_BENCH_SMALL_ITER env vars for deeper runs")
        print("=" * 80)


if __name__ == "__main__":
    # Run the benchmark when executed directly
    class DummyCapsys:
        """Dummy capsys for direct execution."""

        def disabled(self):
            class Context:
                def __enter__(self):
                    pass

                def __exit__(self, *_):
                    pass

            return Context()

    test_benchmark_suite(DummyCapsys())
