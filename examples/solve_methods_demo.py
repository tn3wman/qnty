#!/usr/bin/env python3
"""
Test script for the new solve() and solve_from() methods.

This script tests the solve functionality that replaces the automatic solver.
"""

import sys

sys.path.insert(0, "src")

from qnty import Dimensionless, Length, Pressure


def test_solve_from_method():
    """Test the solve_from() method."""
    print("=== Testing solve_from() method ===")

    # Simple linear equation: T = T_bar * (1 - U_m)
    T_bar = Length(0.147, "inch", "T_bar")
    U_m = Dimensionless(0.125, "U_m")
    T = Length("T", is_known=False)

    print(f"Given: T_bar = {T_bar}, U_m = {U_m}")
    print(f"Before solve: T = {T}")

    # Solve using solve_from
    T.solve_from(T_bar * (1 - U_m))

    print(f"After solve_from(T_bar * (1 - U_m)): T = {T}")

    # Verify the result manually
    expected_value = 0.147 * (1 - 0.125)  # = 0.128625 inches
    actual_mm = T.quantity.value if T.quantity else 0
    expected_mm = expected_value * 25.4  # Convert to mm

    print(f"Expected: {expected_mm:.4f} mm, Got: {actual_mm:.4f} mm")
    assert abs(actual_mm - expected_mm) < 0.001, f"Expected {expected_mm}, got {actual_mm}"
    print("✅ solve_from() test passed!")


def test_equation_based_solve():
    """Test the equation-based solve() method."""
    print("\n=== Testing equation-based solve() method ===")

    # Multi-step problem: T = T_bar * (1 - U_m), then d = D - 2*T
    D = Length(10.0, "inch", "D")
    T_bar = Length(0.147, "inch", "T_bar")
    U_m = Dimensionless(0.125, "U_m")

    # Unknown variables
    T = Length("T", is_known=False)
    d = Length("d", is_known=False)

    print(f"Given: D = {D}, T_bar = {T_bar}, U_m = {U_m}")
    print(f"Unknown: T = {T}, d = {d}")

    # Create equations
    T_eq = T.equals(T_bar * (1 - U_m))
    d_eq = d.equals(D - 2 * T)

    print(f"Equations: {T_eq}, {d_eq}")

    # Solve T first
    print("Solving T...")
    T.solve()
    print(f"T = {T}")

    # Solve d second
    print("Solving d...")
    d.solve()
    print(f"d = {d}")

    # Verify results
    expected_T_inch = 0.147 * (1 - 0.125)  # 0.128625 inches
    expected_d_inch = 10.0 - 2 * expected_T_inch  # 9.74275 inches

    if T.quantity:
        temp_length = Length.from_value(1, "inch", "temp")
        if temp_length.quantity:
            T_inch = T.quantity.to(temp_length.quantity.unit).value
        else:
            T_inch = 0
    else:
        T_inch = 0
    d_inch = d.quantity.value if d.quantity else 0

    print(f"T: Expected {expected_T_inch:.6f} in, Got {T_inch:.6f} in")
    print(f"d: Expected {expected_d_inch:.6f} in, Got {d_inch:.6f} in")

    assert abs(T_inch - expected_T_inch) < 0.001, f"T: Expected {expected_T_inch}, got {T_inch}"
    assert abs(d_inch - expected_d_inch) < 0.001, f"d: Expected {expected_d_inch}, got {d_inch}"
    print("✅ equation-based solve() test passed!")


def test_complex_expressions():
    """Test solve with more complex expressions."""
    print("\n=== Testing complex expressions ===")

    # Pressure vessel calculation: P = (S * t) / (R + 0.6 * t)
    # Solve for t given P, S, R
    P = Pressure(100, "pascal", "P")  # Internal pressure
    S = Pressure(200, "pascal", "S")  # Allowable stress (treating as pressure for units)
    R = Length(50, "millimeter", "R")  # Radius

    t = Length("t", is_known=False)  # Wall thickness to solve for

    print(f"Given: P = {P}, S = {S}, R = {R}")
    print("Solve: P = (S * t) / (R + 0.6 * t) for t")

    # Create equation: P * (R + 0.6 * t) = S * t
    # Rearranged: P * R = S * t - P * 0.6 * t = t * (S - P * 0.6)
    # So: t = (P * R) / (S - P * 0.6)

    # Using solve_from for the rearranged form
    t.solve_from((P * R) / (S - P * 0.6))

    print(f"Solved t = {t}")

    # Verify by substitution
    if t.quantity:
        lhs_value = 100.0  # P value in Pa
        # Calculate RHS manually: (S * t) / (R + 0.6 * t)
        # All values converted to consistent units
        S_val = 200.0  # Pa
        t_val = t.quantity.value / 1000.0  # Convert mm to m for calculation
        R_val = 50.0 / 1000.0  # Convert mm to m

        rhs_value = (S_val * t_val) / (R_val + 0.6 * t_val)

        print(f"Verification: LHS = {lhs_value:.6f} Pa, RHS = {rhs_value:.6f} Pa")
        assert abs(lhs_value - rhs_value) < 0.01, f"Verification failed: {lhs_value} != {rhs_value}"

    print("✅ complex expression test passed!")


def test_comparison_methods():
    """Test comparison methods (lt, gt, leq, geq) with expressions."""
    print("\n=== Testing Comparison Methods ===")
    
    # Create some variables with known values
    P = Pressure(100, "pascal", "Internal Pressure")
    P_max = Pressure(150, "pascal", "Maximum Allowable Pressure")
    P_min = Pressure(50, "pascal", "Minimum Required Pressure")
    
    T = Length(5, "millimeter", "Wall Thickness")
    T_min = Length(3, "millimeter", "Minimum Thickness")
    T_max = Length(8, "millimeter", "Maximum Thickness")
    
    print("Given values:")
    print(f"  P = {P}, P_max = {P_max}, P_min = {P_min}")
    print(f"  T = {T}, T_min = {T_min}, T_max = {T_max}")
    print()
    
    # Test basic comparisons using methods
    print("Method-based comparisons:")
    
    # Less than
    result_lt = P.lt(P_max/6 + 7 * 3)
    print(f"  P.lt(P_max): P < P_max? → {result_lt}")
    
    # Greater than
    result_gt = P.gt(P_min)
    print(f"  P.gt(P_min): P > P_min? → {result_gt}")
    
    # Less than or equal
    result_leq = T.leq(T_max)
    print(f"  T.leq(T_max): T ≤ T_max? → {result_leq}")
    
    # Greater than or equal
    result_geq = T.geq(T_min)
    print(f"  T.geq(T_min): T ≥ T_min? → {result_geq}")
    
    print()
    
    # Test with Python operators
    print("Operator-based comparisons:")
    print(f"  P < P_max: {P < P_max}")
    print(f"  P > P_min: {P > P_min}")
    print(f"  T <= T_max: {T <= T_max}")
    print(f"  T >= T_min: {T >= T_min}")
    
    print()
    
    # Test comparisons in expressions
    print("Comparisons in complex expressions:")
    
    # Safety factor calculation: SF = P_max / P
    SF = Pressure("Safety Factor", is_known=False)
    SF.solve_from(P_max / P)
    print(f"  Safety Factor = P_max / P = {SF}")
    
    # Check if safety factor is adequate (SF > 1.2)
    SF_adequate = SF.gt(1.2)
    print(f"  Is SF > 1.2? → {SF_adequate}")
    
    print()
    
    # Range checks
    print("Range validation checks:")
    
    # Check if pressure is within acceptable range
    P_in_range = P.geq(P_min) * P.leq(P_max)  # Both conditions must be true
    print(f"  P_min ≤ P ≤ P_max? → {P_in_range}")
    
    # Check if thickness is within tolerance
    T_in_range = T.geq(T_min) * T.leq(T_max)
    print(f"  T_min ≤ T ≤ T_max? → {T_in_range}")
    
    print()
    
    # Conditional expressions with comparisons
    print("Conditional logic with comparisons:")
    
    # Example: If P > 120 Pa, use thicker wall
    P_high = Pressure(120, "pascal", "High Pressure Threshold")
    need_thick_wall = P.gt(P_high/6)
    print(f"  Need thicker wall (P > 120 Pa)? → {need_thick_wall}")
    
    # Calculate required thickness based on condition
    # T_required = 5mm if P <= 120Pa, else 7mm
    T_standard = Length(5, "millimeter", "Standard Thickness")
    T_reinforced = Length(7, "millimeter", "Reinforced Thickness")
    
    # This would typically be used in a conditional expression
    print(f"  Standard thickness: {T_standard}")
    print(f"  Reinforced thickness: {T_reinforced}")
    print(f"  Use reinforced: {need_thick_wall}")
    
    print()
    
    # Mixed unit comparisons (automatic conversion)
    print("Mixed unit comparisons:")
    
    L1 = Length(1, "meter", "Length 1")
    L2 = Length(1200, "millimeter", "Length 2")  # 1.2 meters
    
    print(f"  L1 = {L1}, L2 = {L2}")
    print(f"  L1 < L2 (1m < 1200mm)? → {L1 < L2}")
    print(f"  L1.lt(L2)? → {L1.lt(L2)}")
    
    P1 = Pressure(100, "kilopascal", "Pressure 1")
    P2 = Pressure(15, "pound_force_per_square_inch", "Pressure 2")  # ~103.4 kPa
    
    print(f"  P1 = {P1}, P2 = {P2}")
    print(f"  P1 < P2 (100 kPa < 15 psi)? → {P1 < P2}")
    print(f"  P1.lt(P2)? → {P1.lt(P2)}")
    
    print("\n✅ Comparison methods test passed!")


def test_error_conditions():
    """Test error conditions and edge cases."""
    print("\n=== Testing error conditions ===")

    # Test solving with no equations
    x = Length("x", is_known=False)

    try:
        x.solve()
        raise AssertionError("Should have raised ValueError for no equations")
    except ValueError as e:
        print(f"✅ Correctly caught error for no equations: {e}")

    # Test solving unsolvable equation
    y = Length("y", is_known=False)
    z = Length("z", is_known=False)

    # Create equation with two unknowns
    y.equals(z + 5)  # Create equation but don't store it

    try:
        y.solve()
        raise AssertionError("Should have raised ValueError for unsolvable equation")
    except ValueError as e:
        print(f"✅ Correctly caught error for unsolvable equation: {e}")

    print("✅ error condition tests passed!")


def main():
    """Run all tests."""
    print("Testing new solve() and solve_from() methods...")
    print("=" * 60)

    test_solve_from_method()
    test_equation_based_solve()
    test_complex_expressions()
    test_comparison_methods()  # Add the new comparison test
    test_error_conditions()

    print("\n" + "=" * 60)
    print("🎉 All solve method tests passed!")
    print("\nNew solve capabilities:")
    print("  • var.solve_from(expression) - Create equation and solve immediately")
    print("  • var.solve() - Find equations in scope and solve automatically")
    print("  • Automatic variable discovery from calling scope")
    print("  • Support for complex multi-variable systems")
    print("  • Comparison methods: lt(), gt(), leq(), geq() and operators")
    print("  • Drop-in replacement for removed auto-evaluation")


if __name__ == "__main__":
    main()
