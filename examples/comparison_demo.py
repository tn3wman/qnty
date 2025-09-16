#!/usr/bin/env python3
"""
Demonstration of comparison methods in qnty.

This example shows how to use the comparison methods (lt, gt, leq, geq)
and operators (<, >, <=, >=) with dimensional quantities.
"""

import sys

sys.path.insert(0, "src")

from qnty.core import Q


def basic_comparisons():
    """Demonstrate basic comparison operations."""
    print("=== Basic Comparisons ===\n")

    # Create some pressure values
    P1 = Q(100000, "pascal")  # 100 kPa
    P2 = Q(150000, "pascal")  # 150 kPa

    print(f"P1 = {P1}")
    print(f"P2 = {P2}")
    print()

    # Using operators
    print("Using Python operators:")
    print(f"  P1 < P2 = {P1 < P2}")
    print(f"  P1 > P2 = {P1 > P2}")
    print(f"  P1 <= P2 = {P1 <= P2}")
    print(f"  P1 >= P2 = {P1 >= P2}")
    print()


def mixed_unit_comparisons():
    """Demonstrate comparisons with automatic unit conversion."""
    print("=== Mixed Unit Comparisons ===\n")

    # Compare lengths in different units
    L1 = Q(1, "meter")
    L2 = Q(100, "centimeter")
    L3 = Q(39.37, "inch")

    print(f"L1 = {L1}")
    print(f"L2 = {L2}")
    print(f"L3 = {L3}")
    print()

    print("Are they equal? (automatic unit conversion)")
    print(f"  1m == 100cm? {L1 == L2}")

    # Check approximate equality by comparing to known conversion
    print(f"  1m ≈ 39.37in? {L1.to_unit('inch').value} ≈ {L3.value}")
    print()

    # Compare pressures in different units
    P_psi = Q(14.7, "pound_force_per_square_inch")
    P_Pa = Q(101352.9, "pascal")  # 101.325 kPa

    print(f"P_psi = {P_psi}")
    print(f"P_Pa = {P_Pa}")
    print()

    print("Comparing atmospheric pressure in different units:")
    print(f"  14.7 psi == 101325 Pa? {P_psi == P_Pa}")
    print("  They are approximately equal (within tolerance)")
    print()


def range_validation():
    """Demonstrate using comparisons for range validation."""
    print("=== Range Validation ===\n")

    # Define a pressure and acceptable range
    P_operating = Q(120000, "pascal")  # 120 kPa
    P_min = Q(80000, "pascal")         # 80 kPa
    P_max = Q(150000, "pascal")        # 150 kPa

    print(f"Operating: {P_operating}")
    print(f"Min Safe:  {P_min}")
    print(f"Max Safe:  {P_max}")
    print()

    # Check if within range using comparisons
    above_min = P_operating >= P_min
    below_max = P_operating <= P_max

    print("Safety checks:")
    print(f"  Above minimum? {above_min}")
    print(f"  Below maximum? {below_max}")
    print()

    # Combined check (both conditions must be true)
    # In a real expression system, this would evaluate to True/False
    print(f"  Within safe range? {P_operating >= P_min and P_operating <= P_max}")
    print()


def design_decisions():
    """Demonstrate comparisons for engineering design decisions."""
    print("=== Design Decision Example ===\n")

    # Wall thickness calculation based on pressure
    P = Q(100000, "pascal")          # 100 kPa
    P_threshold = Q(80000, "pascal") # 80 kPa

    print(f"Design pressure: {P}")
    print(f"High pressure threshold: {P_threshold}")
    print()

    # Determine wall thickness requirement
    is_high_pressure = P > P_threshold
    print(f"Is high pressure design required? {is_high_pressure}")
    print()

    # Select appropriate thickness
    T_standard = Q(5, "millimeter")
    T_reinforced = Q(8, "millimeter")

    print(f"Standard thickness: {T_standard}")
    print(f"Reinforced thickness: {T_reinforced}")

    # In practice, you might use this in conditional logic
    if P > P_threshold:
        selected = T_reinforced
        print(f"Selected: {selected} (high pressure design)")
    else:
        selected = T_standard
        print(f"Selected: {selected} (standard design)")
    print()


def safety_factor_check():
    """Demonstrate using comparisons for safety factor validation."""
    print("=== Safety Factor Validation ===\n")

    # Material and loading conditions
    S_yield = Q(250000000, "pascal")   # 250 MPa
    S_applied = Q(100000000, "pascal") # 100 MPa

    print(f"Yield strength: {S_yield}")
    print(f"Applied stress: {S_applied}")
    print()

    # Calculate safety factor
    SF = S_yield / S_applied
    print(f"Calculated safety factor: {SF}")
    print()

    # Check against minimum requirements
    SF_min = 2.0  # Minimum required safety factor

    # Create a dimensionless variable for comparison
    SF_min_var = Q(SF_min, "dimensionless")

    is_safe = SF >= SF_min_var
    print(f"Minimum required SF: {SF_min}")
    print(f"Is design safe (SF >= {SF_min})? {is_safe}")
    print()


def main():
    """Run all demonstrations."""
    print("=" * 60)
    print("QNTY Comparison Methods Demonstration")
    print("=" * 60)
    print()

    basic_comparisons()
    mixed_unit_comparisons()
    range_validation()
    design_decisions()
    safety_factor_check()

    print("=" * 60)
    print("Key Features Demonstrated:")
    print("  • Comparison methods: lt(), gt(), leq(), geq()")
    print("  • Python operators: <, >, <=, >=")
    print("  • Automatic unit conversion in comparisons")
    print("  • Range validation and safety checks")
    print("  • Design decision logic with comparisons")
    print("=" * 60)


if __name__ == "__main__":
    main()
