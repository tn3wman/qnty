"""Profile multiplication step-by-step."""
import time
from qnty.quantities import Quantity
from qnty.units import LengthUnits
from qnty.quantities.base_qnty import _cache_manager

def profile_step(name, operation, iterations=10000):
    """Profile a single operation step."""
    # Warmup
    for _ in range(100):
        try:
            operation()
        except:
            pass
    
    # Time it
    start = time.perf_counter()
    for _ in range(iterations):
        operation()
    end = time.perf_counter()
    
    avg_time_us = (end - start) / iterations * 1_000_000
    print(f"{name:<30}: {avg_time_us:.3f} μs")
    return avg_time_us

# Setup
length_10 = Quantity(10.0, LengthUnits.meter)
width_5 = Quantity(5.0, LengthUnits.meter)

print("=== MULTIPLICATION STEP-BY-STEP PROFILING ===")
print()

# Profile individual steps in multiplication
def step_1_type_check():
    return isinstance(width_5, int | float)

def step_2_attr_extraction():
    return (length_10.value, length_10._si_factor, length_10._dimension_sig,
            width_5.value, width_5._si_factor, width_5._dimension_sig)

def step_3_cache_lookup():
    cache_key = (length_10._dimension_sig, width_5._dimension_sig)
    return cache_key in _cache_manager.multiplication_cache

def step_4_cache_retrieval():
    cache_key = (length_10._dimension_sig, width_5._dimension_sig)
    return _cache_manager.multiplication_cache[cache_key]

def step_5_si_calculation():
    return (length_10.value * length_10._si_factor) * (width_5.value * width_5._si_factor)

def step_6_full_multiplication():
    return length_10 * width_5

def step_7_quantity_creation():
    # Simulate the final Quantity creation
    cached_unit = _cache_manager.multiplication_cache[(length_10._dimension_sig, width_5._dimension_sig)]
    result_si_value = (length_10.value * length_10._si_factor) * (width_5.value * width_5._si_factor)
    return Quantity(result_si_value / cached_unit.si_factor, cached_unit)

# Profile each step
total = 0
total += profile_step("1. Type check", step_1_type_check)
total += profile_step("2. Attribute extraction", step_2_attr_extraction)  
total += profile_step("3. Cache lookup", step_3_cache_lookup)
total += profile_step("4. Cache retrieval", step_4_cache_retrieval)
total += profile_step("5. SI calculation", step_5_si_calculation)
step_6_time = profile_step("6. Full multiplication", step_6_full_multiplication)
total += profile_step("7. Quantity creation", step_7_quantity_creation)

print()
print(f"Sum of individual steps: {total:.3f} μs")
print(f"Full multiplication:     {step_6_time:.3f} μs")
print(f"Overhead:                {step_6_time - total:.3f} μs")

# Test comparison with addition
length_10_mm = Quantity(10000.0, LengthUnits.millimeter)
width_5_mm = Quantity(5000.0, LengthUnits.millimeter)

def addition_test():
    return length_10_mm + width_5_mm

print()
add_time = profile_step("Addition (same unit)", addition_test)
print(f"Multiplication vs Addition: {step_6_time / add_time:.1f}x slower")