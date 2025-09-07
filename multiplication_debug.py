"""
Debug multiplication performance to understand the bottleneck.
"""
import time
import pint
from qnty.quantities import Length, Quantity
from qnty.units import LengthUnits

def benchmark_operation(operation, iterations=2000):
    """Simple benchmark function."""
    # Warmup
    for _ in range(5):
        try:
            operation()
        except Exception:
            pass
    
    # Timing
    start = time.perf_counter()
    for _ in range(iterations):
        result = operation()
    end = time.perf_counter()
    
    return (end - start) / iterations * 1_000_000, result

# Setup test quantities
qnty_length_10 = Quantity(10.0, LengthUnits.meter)
qnty_width_5 = Quantity(5.0, LengthUnits.meter)

ureg = pint.UnitRegistry()
pint_length_10 = ureg.Quantity(10.0, "meter")
pint_width_5 = ureg.Quantity(5.0, "meter")

# Test different multiplication scenarios
def test_qnty_same_unit():
    return qnty_length_10 * qnty_width_5

def test_pint_same_unit():
    return pint_length_10 * pint_width_5

def test_qnty_scalar():
    return qnty_length_10 * 5.0

def test_pint_scalar():
    return pint_length_10 * 5.0

print("=== MULTIPLICATION PERFORMANCE DEBUG ===")
print()

# Test 1: Same unit multiplication
qnty_time, qnty_result = benchmark_operation(test_qnty_same_unit, 2000)
pint_time, pint_result = benchmark_operation(test_pint_same_unit, 2000)
speedup = pint_time / qnty_time
print(f"Same Unit Multiplication:")
print(f"  Qnty: {qnty_time:.3f} μs -> {qnty_result}")
print(f"  Pint: {pint_time:.3f} μs -> {pint_result}")
print(f"  Speedup: {speedup:.1f}x")
print()

# Test 2: Scalar multiplication
qnty_time, qnty_result = benchmark_operation(test_qnty_scalar, 2000)
pint_time, pint_result = benchmark_operation(test_pint_scalar, 2000)
speedup = pint_time / qnty_time
print(f"Scalar Multiplication:")
print(f"  Qnty: {qnty_time:.3f} μs -> {qnty_result}")
print(f"  Pint: {pint_time:.3f} μs -> {pint_result}")
print(f"  Speedup: {speedup:.1f}x")
print()

# Profile the qnty multiplication step by step
print("=== QNTY MULTIPLICATION PROFILING ===")

def profile_qnty_multiply():
    """Profile individual steps in qnty multiplication."""
    q1 = qnty_length_10
    q2 = qnty_width_5
    
    # Test attribute access
    start = time.perf_counter()
    for _ in range(1000):
        _ = q1.quantity, q2.quantity
    attr_time = (time.perf_counter() - start) / 1000 * 1_000_000
    
    # Test actual multiplication
    start = time.perf_counter()
    for _ in range(1000):
        result = q1.quantity * q2.quantity
    mult_time = (time.perf_counter() - start) / 1000 * 1_000_000
    
    print(f"Attribute access: {attr_time:.3f} μs")
    print(f"Multiplication: {mult_time:.3f} μs")
    
profile_qnty_multiply()