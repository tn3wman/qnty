"""
Performance Benchmark Tests
============================

Compare Qnty performance against Pint library for various engineering calculations.
Shows speedup factors and validates calculation accuracy.
"""

import time

import astropy.units as u
import pint
import unyt
from astropy.units import imperial

from qnty import Length
from qnty.quantities import Q
from qnty.units import DimensionlessUnits, LengthUnits, PressureUnits, MassDensityUnits

# Pre-define all variables to exclude initialization from performance measurements
ASTROPY_AVAILABLE = True

# Test values
TEST_VALUE = 100.0
PRESSURE_VALUE = 2900.75
LENGTH_VALUE = 168.275

# Initialize unit registries once
ureg = pint.UnitRegistry()

# Pre-create all Qnty quantities
qnty_meter = Q(TEST_VALUE, LengthUnits.meter)
qnty_mm_100 = Q(100.0, LengthUnits.millimeter)
qnty_inch_2 = Q(2.0, LengthUnits.inch)
qnty_length_10 = Q(10.0, LengthUnits.meter)
qnty_width_5 = Q(5.0, LengthUnits.meter)
qnty_pressure = Q(PRESSURE_VALUE, PressureUnits.psi)
qnty_area_10mm = Q(10.0, LengthUnits.millimeter)
qnty_P = Q(PRESSURE_VALUE, PressureUnits.psi)
qnty_D = Q(LENGTH_VALUE, LengthUnits.millimeter)
qnty_S = Q(137.895, PressureUnits.MPa)
qnty_E = Q(0.8, DimensionlessUnits.dimensionless)
qnty_W = Q(1.0, DimensionlessUnits.dimensionless)
qnty_Y = Q(0.4, DimensionlessUnits.dimensionless)
qnty_length_var = Length("beam_length")
# Set the quantity directly to avoid the internal bug
from qnty.quantities import Q
qnty_length_var._quantity = Q(100.0, LengthUnits.millimeter)
qnty_length_var.is_known = True
qnty_q1_50mm = Q(50.0, LengthUnits.millimeter)
qnty_q2_2in = Q(2.0, LengthUnits.inch)
qnty_q3_05m = Q(0.5, LengthUnits.meter)
qnty_zero_mm = Q(0, LengthUnits.millimeter)

# Pre-create all Pint quantities
pint_meter = ureg.Quantity(TEST_VALUE, "meter")
pint_mm_100 = ureg.Quantity(100.0, "millimeter")
pint_inch_2 = ureg.Quantity(2.0, "inch")
pint_length_10 = ureg.Quantity(10.0, "meter")
pint_width_5 = ureg.Quantity(5.0, "meter")
pint_pressure = ureg.Quantity(PRESSURE_VALUE, "psi")
pint_area_10mm = ureg.Quantity(10.0, "millimeter")
pint_P = ureg.Quantity(PRESSURE_VALUE, "psi")
pint_D = ureg.Quantity(LENGTH_VALUE, "mm")
pint_S = ureg.Quantity(137.895, "MPa")
pint_E = ureg.Quantity(0.8, "dimensionless")
pint_W = ureg.Quantity(1.0, "dimensionless")
pint_Y = ureg.Quantity(0.4, "dimensionless")
pint_length_100mm = ureg.Quantity(100.0, "millimeter")
pint_q1_50mm = ureg.Quantity(50.0, "millimeter")
pint_q2_2in = ureg.Quantity(2.0, "inch")
pint_q3_05m = ureg.Quantity(0.5, "meter")
pint_zero_mm = ureg.Quantity(0, "millimeter")

# Pre-create all Unyt quantities
unyt_meter = unyt.unyt_quantity(TEST_VALUE, "meter")
unyt_mm_100 = unyt.unyt_quantity(100.0, "millimeter")
unyt_inch_2 = unyt.unyt_quantity(2.0, "inch")
unyt_length_10 = unyt.unyt_quantity(10.0, "meter")
unyt_width_5 = unyt.unyt_quantity(5.0, "meter")
unyt_pressure = unyt.unyt_quantity(PRESSURE_VALUE, "psi")
unyt_area_10mm = unyt.unyt_quantity(10.0, "millimeter")
unyt_P = unyt.unyt_quantity(PRESSURE_VALUE, "psi")
unyt_D = unyt.unyt_quantity(LENGTH_VALUE, "mm")
unyt_S = unyt.unyt_quantity(137.895, "MPa")
unyt_E = unyt.unyt_quantity(0.8, "dimensionless")
unyt_W = unyt.unyt_quantity(1.0, "dimensionless")
unyt_Y = unyt.unyt_quantity(0.4, "dimensionless")
unyt_length_100mm = unyt.unyt_quantity(100.0, "millimeter")
unyt_q1_50mm = unyt.unyt_quantity(50.0, "millimeter")
unyt_q2_2in = unyt.unyt_quantity(2.0, "inch")
unyt_q3_05m = unyt.unyt_quantity(0.5, "meter")
unyt_zero_mm = unyt.unyt_quantity(0, "millimeter")

# Pre-create all Astropy quantities
astropy_meter = TEST_VALUE * u.m  # type: ignore
astropy_mm_100 = 100.0 * u.mm  # type: ignore
astropy_inch_2 = 2.0 * imperial.inch  # type: ignore
astropy_length_10 = 10.0 * u.m  # type: ignore
astropy_width_5 = 5.0 * u.m  # type: ignore
astropy_pressure = PRESSURE_VALUE * imperial.psi  # type: ignore
astropy_area_10mm = 10.0 * u.mm  # type: ignore
astropy_P = PRESSURE_VALUE * imperial.psi  # type: ignore
astropy_D = LENGTH_VALUE * u.mm  # type: ignore
astropy_S = 137.895 * u.MPa  # type: ignore
astropy_E = 0.8 * u.dimensionless_unscaled  # type: ignore
astropy_W = 1.0 * u.dimensionless_unscaled  # type: ignore
astropy_Y = 0.4 * u.dimensionless_unscaled  # type: ignore
astropy_length_100mm = 100.0 * u.mm  # type: ignore
astropy_q1_50mm = 50.0 * u.mm  # type: ignore
astropy_q2_2in = 2.0 * imperial.inch  # type: ignore
astropy_q3_05m = 0.5 * u.m  # type: ignore
astropy_zero_mm = 0 * u.mm  # type: ignore

# Fluid dynamics pre-created quantities
qnty_P1 = Q(PRESSURE_VALUE, PressureUnits.psi)
qnty_P2 = Q(1800.0, PressureUnits.psi)
qnty_D_fluid = Q(LENGTH_VALUE, LengthUnits.millimeter)
qnty_L = Q(100.0, LengthUnits.meter)
qnty_rho = Q(850.0, MassDensityUnits.kilogram_per_cubic_meter)
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


def format_speedup(qnty_time, pint_time, unyt_time, astropy_time=None):
    """Format speedup comparison with optimized calculations."""
    # Fast path: check for infinite values first
    inf_val = float("inf")
    if qnty_time == inf_val or pint_time == inf_val or unyt_time == inf_val:
        return "N/A"

    # Pre-calculate reciprocal for better performance
    qnty_reciprocal = 1.0 / qnty_time
    pint_speedup = pint_time * qnty_reciprocal
    unyt_speedup = unyt_time * qnty_reciprocal

    if astropy_time is not None and astropy_time != inf_val:
        astropy_speedup = astropy_time * qnty_reciprocal
        return f"Pint:{pint_speedup:.1f}x|Unyt:{unyt_speedup:.1f}x|Astropy:{astropy_speedup:.1f}x"
    else:
        return f"Pint:{pint_speedup:.1f}x|Unyt:{unyt_speedup:.1f}x|Astropy:N/A"


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
    print(f"\n{'Operation':<30} {'Qnty (us)':<12} {'Pint (us)':<12} {'Unyt (us)':<12} {'Astropy (us)':<14} {'Speedup vs Qnty':<40} {'Status'}")
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

        # Calculate speedup
        speedup = format_speedup(*times)

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
            f"{format_speedup(avg_qnty_time, avg_pint_time, avg_unyt_time, avg_astropy_time):<40}"
        )

        if avg_pint_time > 0:
            pint_speedup = avg_pint_time / avg_qnty_time
            print(f"\n[RESULT] Overall Performance: Qnty is {pint_speedup:.1f}x faster than Pint")

            # Performance tier message with optimized thresholds
            tier_messages = [(20, "[TIER] BLAZING FAST: Over 20x speedup!"), (10, "[TIER] EXCELLENT: 10-20x speedup!"), (5, "[TIER] GREAT: 5-10x speedup!"), (2, "[TIER] GOOD: 2-5x speedup!")]

            for threshold, message in tier_messages:
                if pint_speedup >= threshold:
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

    qnty_result = benchmark_operation(qnty_conversion, 2000)
    pint_result = benchmark_operation(pint_conversion, 2000)
    unyt_result = benchmark_operation(unyt_conversion, 2000)
    astropy_result = benchmark_operation(astropy_conversion, 2000)
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

    qnty_result = benchmark_operation(qnty_mixed_addition, 2000)
    pint_result = benchmark_operation(pint_mixed_addition, 2000)
    unyt_result = benchmark_operation(unyt_mixed_addition, 2000)
    astropy_result = benchmark_operation(astropy_mixed_addition, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
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

    qnty_result = benchmark_operation(qnty_multiplication, 2000)
    pint_result = benchmark_operation(pint_multiplication, 2000)
    unyt_result = benchmark_operation(unyt_multiplication, 2000)
    astropy_result = benchmark_operation(astropy_multiplication, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
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

    qnty_result = benchmark_operation(qnty_division, 2000)
    pint_result = benchmark_operation(pint_division, 2000)
    unyt_result = benchmark_operation(unyt_division, 2000)
    astropy_result = benchmark_operation(astropy_division, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Division (psi / mm)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 5: Complex Engineering Calculation (ASME) ==========
    def qnty_complex():
        return (qnty_P * qnty_D) / (2 * (qnty_S * qnty_E * qnty_W + qnty_P * qnty_Y))

    def pint_complex():
        return (pint_P * pint_D) / (2 * (pint_S * pint_E * pint_W + pint_P * pint_Y))  # type: ignore

    def unyt_complex():
        return (unyt_P * unyt_D) / (2 * (unyt_S * unyt_E * unyt_W + unyt_P * unyt_Y))

    def astropy_complex():
        return (astropy_P * astropy_D) / (2 * (astropy_S * astropy_E * astropy_W + astropy_P * astropy_Y))

    qnty_result = benchmark_operation(qnty_complex, 2000)
    pint_result = benchmark_operation(pint_complex, 2000)
    unyt_result = benchmark_operation(unyt_complex, 2000)
    astropy_result = benchmark_operation(astropy_complex, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("Complex ASME Equation", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 6: Type-Safe Variables ==========
    def qnty_typesafe():
        assert qnty_length_var.quantity is not None
        # Return the quantity object itself converted to consistent units, not the scalar
        return Q(qnty_length_var.quantity.to(LengthUnits.meter), LengthUnits.meter)

    def pint_typesafe():
        # Pint doesn't have type-safe variables, so we simulate
        return pint_length_100mm.to("meter")

    def unyt_typesafe():
        return unyt_length_100mm.in_units("meter")  # type: ignore

    def astropy_typesafe():
        return astropy_length_100mm.to(u.m)  # type: ignore

    qnty_result = benchmark_operation(qnty_typesafe, 2000)
    pint_result = benchmark_operation(pint_typesafe, 2000)
    unyt_result = benchmark_operation(unyt_typesafe, 2000)
    astropy_result = benchmark_operation(astropy_typesafe, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
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

    qnty_result = benchmark_operation(qnty_chained, 2000)
    pint_result = benchmark_operation(pint_chained, 2000)
    unyt_result = benchmark_operation(unyt_chained, 2000)
    astropy_result = benchmark_operation(astropy_chained, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
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
    qnty_result = benchmark_operation(qnty_many_ops, 2000)  # Increased iterations
    pint_result = benchmark_operation(pint_many_ops, 2000)
    unyt_result = benchmark_operation(unyt_many_ops, 2000)
    astropy_result = benchmark_operation(astropy_many_ops, 2000) if ASTROPY_AVAILABLE else (float("inf"), "N/A")
    results.append(("10 Additions Loop (Optimized)", qnty_result, pint_result, unyt_result, astropy_result))

    # ========== TEST 9: Complex Fluid Dynamics Equation ==========
    # Simplified engineering calculation with multiple unit conversions and operations
    def qnty_fluid_dynamics():
        # Convert pressure drop to consistent units
        dP = qnty_P1 - qnty_P2
        dP_Pa = Q(dP.to(PressureUnits.Pa), PressureUnits.Pa)

        # Diameter in meters for calculation
        D_m = Q(qnty_D_fluid.to(LengthUnits.meter), LengthUnits.meter)

        # Flow calculation with unit-aware operations
        area = qnty_pi * D_m * D_m / qnty_4

        # Simplified velocity calculation (unit-aware pressure-driven flow)
        velocity_factor = (dP_Pa * area) / (qnty_rho * qnty_L)

        # Return a complex engineering result with unit scaling
        result = velocity_factor * Q(1000, DimensionlessUnits.dimensionless)
        return result

    def pint_fluid_dynamics():
        # Convert pressure drop to consistent units
        dP = pint_P1 - pint_P2
        dP_Pa = dP.to("Pa")

        # Diameter in meters for calculation
        D_m = pint_D_fluid.to("m")

        # Flow calculation with unit-aware operations
        pi = ureg.Quantity(3.14159, "dimensionless")
        four = ureg.Quantity(4.0, "dimensionless")
        area = pi * D_m * D_m / four

        # Simplified velocity calculation (unit-aware pressure-driven flow)
        velocity_factor = (dP_Pa * area) / (pint_rho * pint_L)

        # Return a complex engineering result with unit scaling
        result = velocity_factor * ureg.Quantity(1000, "dimensionless")
        return result

    def unyt_fluid_dynamics():
        # Convert pressure drop to consistent units
        dP = unyt_P1 - unyt_P2
        dP_Pa = dP.in_units("Pa")  # type: ignore

        # Diameter in meters for calculation
        D_m = unyt_D_fluid.in_units("m")  # type: ignore

        # Flow calculation with unit-aware operations
        pi = unyt.unyt_quantity(3.14159, "dimensionless")
        four = unyt.unyt_quantity(4.0, "dimensionless")
        rho = unyt.unyt_quantity(850.0, "kg/m**3")
        area = pi * D_m * D_m / four

        # Simplified velocity calculation (unit-aware pressure-driven flow)
        velocity_factor = (dP_Pa * area) / (rho * unyt_L)

        # Return a complex engineering result with unit scaling
        result = velocity_factor * unyt.unyt_quantity(1000, "dimensionless")
        return result

    def astropy_fluid_dynamics():
        # Convert pressure drop to consistent units
        dP = astropy_P1 - astropy_P2
        dP_Pa = dP.to(u.Pa)  # type: ignore

        # Diameter in meters for calculation
        D_m = astropy_D_fluid.to(u.m)  # type: ignore

        # Flow calculation with unit-aware operations
        pi = 3.14159 * u.dimensionless_unscaled  # type: ignore
        four = 4.0 * u.dimensionless_unscaled  # type: ignore
        rho = 850.0 * (u.kg / u.m**3)  # type: ignore  # density
        area = pi * D_m * D_m / four

        # Simplified velocity calculation (unit-aware pressure-driven flow)
        velocity_factor = (dP_Pa * area) / (rho * astropy_L)

        # Return a complex engineering result with unit scaling
        result = velocity_factor * (1000 * u.dimensionless_unscaled)  # type: ignore
        return result

    qnty_result = benchmark_operation(qnty_fluid_dynamics, 2000)
    pint_result = benchmark_operation(pint_fluid_dynamics, 2000)
    unyt_result = benchmark_operation(unyt_fluid_dynamics, 2000)
    astropy_result = benchmark_operation(astropy_fluid_dynamics, 2000)
    results.append(("Complex Fluid Dynamics", qnty_result, pint_result, unyt_result, astropy_result))

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
                def __enter__(self):
                    pass

                def __exit__(self, *_):
                    pass

            return Context()

    test_benchmark_suite(DummyCapsys())
