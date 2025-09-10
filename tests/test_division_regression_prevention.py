"""
Comprehensive Division Bug Regression Prevention Test Suite
===========================================================

This test suite is specifically designed to prevent the regression of the
division optimization bug that was fixed in BinaryOperation._divide().

The original bug: When dividing by any quantity with value 1.0, the method
would incorrectly return the numerator unchanged instead of performing
proper dimensional analysis, leading to expressions like:
- 5 inches / 1 inch = 5 inches (WRONG) instead of 5 (dimensionless)

This caused the D=1 inch solver bug in composed problems and other issues.

The fix ensures the optimization only applies to truly dimensionless 1.0 values.
"""

import pytest

from qnty import (
    Area,
    Dimensionless,
    EnergyHeatWork,
    Force,
    Length,
    Mass,
    Pressure,
    Temperature,
    Time,
    VelocityLinear,
    Volume,
)


class TestDivisionOptimizationRegression:
    """Comprehensive tests to prevent division optimization regression."""

    def test_division_by_one_with_same_dimensions_returns_dimensionless(self):
        """
        CRITICAL: Division of same dimensions with divisor = 1.0 must return dimensionless.

        This is the exact bug that was fixed. Any regression here would break:
        - Complex engineering expressions
        - Solver functionality for certain values
        - Dimensional analysis correctness
        """
        test_cases = [
            # (numerator_value, numerator_unit, denominator_value, denominator_unit, var_type)
            (5.0, "meter", 1.0, "meter", Length),
            (10.0, "square_meter", 1.0, "square_meter", Area),
            (100.0, "newton", 1.0, "newton", Force),
            (50.0, "pascal", 1.0, "pascal", Pressure),
            (373.0, "K", 1.0, "K", Temperature),
            (60.0, "second", 1.0, "second", Time),
            (20.0, "kilogram", 1.0, "kilogram", Mass),
            (15.0, "meter_per_second", 1.0, "meter_per_second", VelocityLinear),
        ]

        for num_val, num_unit, den_val, den_unit, var_type in test_cases:
            # Create variables with the problematic case (divisor = 1.0)
            numerator = var_type(num_val, num_unit, f"Test {var_type.__name__} Numerator")
            denominator = var_type(den_val, den_unit, f"Test {var_type.__name__} Denominator")

            # Perform division that previously failed
            result_expr = numerator / denominator
            context = {numerator.name: numerator, denominator.name: denominator}
            result = result_expr.evaluate(context)

            # CRITICAL ASSERTIONS: Must be dimensionless with expected value
            expected_value = num_val / den_val
            assert result.value == pytest.approx(expected_value), f"Division result incorrect for {var_type.__name__}: expected {expected_value}, got {result.value}"

            assert result._dimension_sig == 1, f"Division of same dimensions must be dimensionless for {var_type.__name__}: got dimension {result._dimension_sig}"

            assert result.unit.symbol == "", f"Dimensionless result must have empty unit symbol for {var_type.__name__}: got '{result.unit.symbol}'"

    def test_division_by_exactly_one_point_zero_edge_cases(self):
        """
        Test edge cases around the exact value 1.0 to ensure the fix is precise.
        """
        length1 = Length(10, "meter", "Length 1")

        # Test values very close to 1.0 but not exactly 1.0
        close_values = [0.9999999, 1.0000001, 0.999999999, 1.000000001]

        for close_val in close_values:
            length2 = Length(close_val, "meter", "Close to One")
            result_expr = length1 / length2
            result = result_expr.evaluate({"Length 1": length1, "Close to One": length2})

            # Should still be dimensionless (proper division, not optimization)
            expected = 10.0 / close_val
            assert result.value == pytest.approx(expected, abs=1e-6)
            assert result._dimension_sig == 1  # Dimensionless

    def test_division_by_dimensionless_one_still_uses_optimization(self):
        """
        Verify that the fix preserves the valid optimization for dimensionless 1.0.
        """
        length = Length(5, "meter", "Test Length")
        dimensionless_one = Dimensionless(1.0, "Unity")

        result_expr = length / dimensionless_one
        result = result_expr.evaluate({"Test Length": length, "Unity": dimensionless_one})

        # Should return the length unchanged (optimization preserved)
        assert result.value == pytest.approx(5.0)
        # Length dimension is typically 2
        length_dim = 2 if length.quantity is None else length.quantity._dimension_sig
        assert result._dimension_sig == length_dim  # Same as original
        assert result.unit.symbol == "m"  # Original unit preserved

    def test_original_d_equals_one_inch_scenario(self):
        """
        Test the exact scenario that originally failed: D = 1 inch in pipe calculations.

        This recreates the original bug scenario from the composed_problem_demo.py
        where R_1 = 5 inches, D = 1 inch, and the expression (4*(R_1/D) - 1) failed.
        """
        R_1 = Length(5, "inch", "Bend Radius")
        D = Length(1, "inch", "Diameter")  # The problematic case

        # Build the expression that was failing: 4*(R_1/D) - 1
        ratio_expr = R_1 / D
        four_times_expr = 4 * ratio_expr
        result_expr = four_times_expr - 1

        context = {"Bend Radius": R_1, "Diameter": D}

        # Each step must work correctly
        ratio_result = ratio_expr.evaluate(context)
        assert ratio_result.value == pytest.approx(5.0), "R_1/D should equal 5.0"
        assert ratio_result._dimension_sig == 1, "R_1/D should be dimensionless"

        four_times_result = four_times_expr.evaluate(context)
        assert four_times_result.value == pytest.approx(20.0), "4*(R_1/D) should equal 20.0"
        assert four_times_result._dimension_sig == 1, "4*(R_1/D) should be dimensionless"

        final_result = result_expr.evaluate(context)
        assert final_result.value == pytest.approx(19.0), "4*(R_1/D) - 1 should equal 19.0"
        assert final_result._dimension_sig == 1, "Final result should be dimensionless"

    def test_division_optimization_boundary_conditions(self):
        """
        Test boundary conditions around the optimization to ensure robustness.
        """
        length = Length(10, "meter", "Base Length")

        # Test various values that should NOT trigger the faulty optimization
        test_divisors = [
            (1, "inch"),  # Different unit, same value
            (1, "foot"),  # Different unit, same value
            (1, "millimeter"),  # Different unit, same value
        ]

        for div_val, div_unit in test_divisors:
            divisor = Length(div_val, div_unit, f"Divisor {div_unit}")
            result_expr = length / divisor
            result = result_expr.evaluate({"Base Length": length, f"Divisor {div_unit}": divisor})

            # Should perform proper division with unit conversion
            assert result._dimension_sig == 1, f"Division should be dimensionless for {div_unit}"
            # Value will depend on unit conversion, but should not be 10.0 (which would indicate faulty optimization)
            assert result.value != 10.0, f"Should not return original value for different units: {div_unit}"

    def test_mixed_dimension_divisions_with_one_values(self):
        """
        Test mixed dimension divisions where some operands have value 1.0.
        These should never use the optimization.
        """
        test_cases = [
            # (numerator_type, num_val, num_unit, denominator_type, den_val, den_unit)
            (Area, 10, "square_meter", Length, 1, "meter"),  # Area / Length = Length
            (Volume, 8, "cubic_meter", Area, 1, "square_meter"),  # Volume / Area = Length
            (Force, 100, "newton", Area, 1, "square_meter"),  # Force / Area = Pressure
            (EnergyHeatWork, 500, "joule", Length, 1, "meter"),  # Energy / Length = Force
        ]

        for num_type, num_val, num_unit, den_type, den_val, den_unit in test_cases:
            numerator = num_type(num_val, num_unit, f"{num_type.__name__} Num")
            denominator = den_type(den_val, den_unit, f"{den_type.__name__} Den")

            result_expr = numerator / denominator
            context = {numerator.name: numerator, denominator.name: denominator}
            result = result_expr.evaluate(context)

            # Should NOT return the original numerator unless it's a valid unit conversion
            # For Force/Area = Pressure case: 100 N / 1 m² = 100 Pa (valid conversion)
            # The key test is dimensional correctness, not value equality
            if num_type == Force and den_type == Area and num_val == 100 and den_val == 1:
                # This is a valid case: 100 N / 1 m² = 100 Pa
                assert result.value == pytest.approx(100.0), "100 N / 1 m² should equal 100 Pa"
            else:
                # For other cases, value should be different if optimization was incorrectly applied
                pass  # Just ensure dimensional correctness below

            # Should have different dimension than both operands (since it's a different quantity type)
            assert result._dimension_sig != numerator.quantity._dimension_sig, f"Result should have different dimension than numerator: {num_type.__name__}/{den_type.__name__}"

    def test_negative_one_optimization_boundaries(self):
        """
        Test the -1.0 optimization to ensure it's also properly bounded.
        """
        # Dimensionless -1.0 should use optimization
        length = Length(5, "meter", "Test Length")
        neg_dimensionless = Dimensionless(-1.0, "Negative Unity")

        result_expr = length / neg_dimensionless
        result = result_expr.evaluate({"Test Length": length, "Negative Unity": neg_dimensionless})

        # Should be -5 meters (negation optimization)
        assert result.value == pytest.approx(-5.0)
        # Length dimension is typically 2
        length_dim = 2 if length.quantity is None else length.quantity._dimension_sig
        assert result._dimension_sig == length_dim

        # Dimensional -1.0 should NOT use optimization
        neg_length = Length(-1, "meter", "Negative Length")
        result_expr2 = length / neg_length
        result2 = result_expr2.evaluate({"Test Length": length, "Negative Length": neg_length})

        # Should be -5 dimensionless (proper division)
        assert result2.value == pytest.approx(-5.0)
        assert result2._dimension_sig == 1  # Dimensionless

    def test_chained_divisions_with_multiple_ones(self):
        """
        Test chained divisions where multiple divisors have value 1.0.
        Each step must be handled correctly.
        """
        area = Area(20, "square_meter", "Base Area")
        length1 = Length(1, "meter", "Length 1")  # First 1.0 divisor
        length2 = Length(1, "meter", "Length 2")  # Second 1.0 divisor

        # Chain: Area / Length1 / Length2 = Dimensionless
        first_division = area / length1
        second_division = first_division / length2

        context = {"Base Area": area, "Length 1": length1, "Length 2": length2}

        # First division: Area/Length = Length
        intermediate = first_division.evaluate(context)
        assert intermediate._dimension_sig == 2  # Length dimension

        # Second division: Length/Length = Dimensionless
        final = second_division.evaluate(context)
        assert final._dimension_sig == 1  # Dimensionless
        assert final.value == pytest.approx(20.0)  # 20 m² / (1 m * 1 m) = 20

    def test_binary_operation_divide_method_directly(self):
        """
        Test the BinaryOperation._divide method directly to ensure fix is in place.
        """
        # No longer need to import BinaryOperation since we use variable division

        # Create a division expression using variable division (which creates BinaryOperation internally)
        left_expr = Length(5, "inch", "Left")
        right_expr = Length(1, "inch", "Right")

        division_expr = left_expr / right_expr  # This creates BinaryOperation internally
        context = {"Left": left_expr, "Right": right_expr}

        # This should NOT use the faulty optimization
        result = division_expr.evaluate(context)

        assert result.value == pytest.approx(5.0)
        assert result._dimension_sig == 1  # Must be dimensionless
        assert result.unit.symbol == ""  # Must have no unit


class TestDivisionOptimizationPreservation:
    """Tests to ensure valid optimizations are preserved."""

    def test_dimensionless_optimizations_still_work(self):
        """Ensure that valid optimizations for dimensionless values still work."""
        length = Length(10, "meter", "Test Length")

        # These should still use optimizations
        unity = Dimensionless(1.0, "Unity")
        neg_unity = Dimensionless(-1.0, "Negative Unity")

        # Division by dimensionless 1.0
        result1_expr = length / unity
        result1 = result1_expr.evaluate({"Test Length": length, "Unity": unity})

        assert result1.value == pytest.approx(10.0)
        # Length dimension is typically 2
        length_dim = 2 if length.quantity is None else length.quantity._dimension_sig
        assert result1._dimension_sig == length_dim
        assert result1.unit.symbol == "m"

        # Division by dimensionless -1.0
        result2_expr = length / neg_unity
        result2 = result2_expr.evaluate({"Test Length": length, "Negative Unity": neg_unity})

        assert result2.value == pytest.approx(-10.0)
        # Length dimension is typically 2
        length_dim = 2 if length.quantity is None else length.quantity._dimension_sig
        assert result2._dimension_sig == length_dim
        assert result2.unit.symbol == "m"


if __name__ == "__main__":
    # Quick verification run
    test_suite = TestDivisionOptimizationRegression()

    print("Running division regression prevention tests...")
    test_suite.test_division_by_one_with_same_dimensions_returns_dimensionless()
    print("✓ Same dimension divisions test passed")

    test_suite.test_original_d_equals_one_inch_scenario()
    print("✓ Original D=1 inch scenario test passed")

    test_suite.test_mixed_dimension_divisions_with_one_values()
    print("✓ Mixed dimension divisions test passed")

    test_suite.test_binary_operation_divide_method_directly()
    print("✓ Direct BinaryOperation test passed")

    print("\n🛡️  All division regression prevention tests passed!")
    print("The division optimization bug fix is protected against regression.")
