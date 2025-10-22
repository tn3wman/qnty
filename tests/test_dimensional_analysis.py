"""
Comprehensive tests for dimensional analysis enforcement in Qnty.

This test suite ensures that:
1. Direct arithmetic operations catch dimensional mismatches
2. Expression system catches dimensional mismatches
3. Problem solving system catches dimensional mismatches
4. All dimensional errors are properly surfaced to the user
"""

import pytest

from qnty import Area, Dimensionless, Force, Length, Pressure, Problem, Torque
from qnty.algebra import equation


class TestDirectArithmetic:
    """Test dimensional checking in direct Quantity arithmetic operations."""

    def test_add_incompatible_dimensions_raises_error(self):
        """Adding quantities with incompatible dimensions should raise TypeError."""
        length = Length("length").set(5, "meter")
        area = Area("area").set(10, "meter2")

        with pytest.raises(TypeError, match="Dimension mismatch"):
            _ = length + area

    def test_subtract_incompatible_dimensions_raises_error(self):
        """Subtracting quantities with incompatible dimensions should raise TypeError."""
        force = Force("force").set(100, "newton")
        pressure = Pressure("pressure").set(50, "pascal")

        with pytest.raises(TypeError, match="Dimension mismatch"):
            _ = force - pressure

    def test_add_compatible_dimensions_succeeds(self):
        """Adding quantities with same dimensions should succeed."""
        l1 = Length("l1").set(5, "meter")
        l2 = Length("l2").set(3, "meter")

        result = l1 + l2
        assert result.value is not None
        # Both are stored in SI (meters), so should be 8.0
        assert abs(result.value - 8.0) < 1e-10

    def test_multiply_different_dimensions_creates_new_dimension(self):
        """Multiplying different dimensions should create compound dimension."""
        length = Length("length").set(5, "meter")
        force = Force("force").set(10, "newton")

        result = length * force
        # Should create Torque dimension (Force * Length)
        assert result.value is not None
        # 5 m * 10 N = 50 N⋅m in SI
        assert abs(result.value - 50.0) < 1e-10

    def test_divide_creates_inverse_dimension(self):
        """Division should create proper inverse dimensions."""
        force = Force("force").set(100, "newton")
        area = Area("area").set(2, "meter2")

        result = force / area
        # Should create Pressure dimension (Force / Area)
        assert result.value is not None
        # 100 N / 2 m² = 50 Pa in SI
        assert abs(result.value - 50.0) < 1e-10


class TestExpressionSystem:
    """Test dimensional checking in algebraic expression system."""

    def test_expression_add_incompatible_raises_error(self):
        """Expression addition with incompatible dimensions should raise error."""
        length = Length("length_var")
        area = Area("area_var")

        length.set(5, "meter")
        area.set(10, "meter2")

        # Create expression: length + area
        expr = length + area

        with pytest.raises(TypeError, match="Dimension mismatch"):
            result = expr.evaluate({"length_var": length, "area_var": area})

    def test_expression_subtract_incompatible_raises_error(self):
        """Expression subtraction with incompatible dimensions should raise error."""
        force = Force("force_var")
        pressure = Pressure("pressure_var")

        force.set(100, "newton")
        pressure.set(50, "pascal")

        # Create expression: force - pressure
        expr = force - pressure

        with pytest.raises(TypeError, match="Dimension mismatch"):
            result = expr.evaluate({"force_var": force, "pressure_var": pressure})

    def test_expression_compatible_operations_succeed(self):
        """Expression operations with compatible dimensions should succeed."""
        l1 = Length("l1")
        l2 = Length("l2")

        l1.set(5, "meter")
        l2.set(3, "meter")

        # Create expression: l1 + l2
        expr = l1 + l2

        result = expr.evaluate({"l1": l1, "l2": l2})
        assert result.value is not None
        assert abs(result.value - 8.0) < 1e-10


class TestProblemSolving:
    """Test dimensional checking in Problem solving system."""

    def test_problem_equation_with_dimensional_mismatch_raises_error(self):
        """
        Problem with dimensionally inconsistent equation should raise error.

        This tests the exact scenario from the flange design issue where
        A_m and A_b were incorrectly defined as Length instead of Area.
        """

        class InconsistentProblem(Problem):
            name = "Test Problem with Dimensional Error"

            # Intentionally create dimensional inconsistency
            force_var = Force("Force Variable").set(100).newton
            area_var = Area("Area Variable", is_known=False)

            # This equation is dimensionally inconsistent:
            # area_var = force_var (Force ≠ Area)
            bad_equation = equation(area_var, force_var)

        problem = InconsistentProblem()

        # When solving, should detect the dimensional inconsistency
        with pytest.raises(TypeError, match="Dimension mismatch"):
            problem.solve()

    def test_problem_with_wrong_unit_in_complex_expression(self):
        """
        Test detecting dimensional errors in complex expressions similar to flange design.

        Simulates: A_m = (W_o + F_A) / S_bo
        where A_m should be Area but wrong dimensions on RHS would cause error.
        """

        class ComplexDimensionalProblem(Problem):
            name = "Complex Dimensional Check"

            # Correct dimensions
            W_o = Force("Bolt Load").set(1000).newton
            F_A = Force("Axial Force").set(500).newton
            S_bo = Pressure("Allowable Stress").set(200e6).pascal

            # A_m should be Area (Force / Pressure = Area)
            A_m = Area("Required Area", is_known=False)

            # Correct equation: A_m = (W_o + F_A) / S_bo
            area_equation = equation(A_m, (W_o + F_A) / S_bo)

        problem = ComplexDimensionalProblem()
        problem.solve()

        # Should solve correctly without errors
        assert problem.A_m.value is not None

        # Verify the dimension is actually Area
        from qnty.core.dimension_catalog import Area as AreaDim

        assert problem.A_m.dim == AreaDim

    def test_problem_catches_error_when_length_assigned_to_area(self):
        """
        Explicitly test the A_m/A_b scenario: assigning Length to Area variable.

        This is the core issue reported by the user.
        """

        class FlangeSimplified(Problem):
            name = "Simplified Flange Problem"

            # Variables with correct dimensions
            force = Force("Force").set(1000).newton
            stress = Pressure("Stress").set(200e6).pascal

            # Intentionally define wrong: should be Area but we'll try to assign wrong dimension
            wrong_area = Length("Wrong Area", is_known=False)  # Should be Area!

            # This equation tries to assign an Area result to a Length variable
            # force / stress = Area, but wrong_area is Length
            bad_eqn = equation(wrong_area, force / stress)

        problem = FlangeSimplified()

        # Should detect dimensional mismatch during solving
        with pytest.raises(TypeError, match="Dimension mismatch"):
            problem.solve()

    def test_problem_with_torque_instead_of_force(self):
        """Test catching dimensional errors with similar but incompatible dimensions."""

        class TorqueVsForce(Problem):
            name = "Torque vs Force Error"

            length = Length("Length").set(2).meter
            force = Force("Force").set(100).newton

            # torque_wrong is defined as Force but equation gives Torque
            torque_wrong = Force("Wrong Torque", is_known=False)

            # length * force = Torque, not Force
            wrong_eqn = equation(torque_wrong, length * force)

        problem = TorqueVsForce()

        with pytest.raises(TypeError, match="Dimension mismatch"):
            problem.solve()


class TestDimensionalConsistency:
    """Test that dimensional analysis is enforced consistently across all operations."""

    def test_nested_expressions_maintain_dimensional_checking(self):
        """Nested expression operations should still enforce dimensional checks."""
        l1 = Length("l1").set(5, "meter")
        l2 = Length("l2").set(3, "meter")
        area = Area("area").set(10, "meter2")

        # (l1 + l2) is Length, adding Area should fail
        expr = (l1 + l2) + area

        with pytest.raises(TypeError, match="Dimension mismatch"):
            result = expr.evaluate({"l1": l1, "l2": l2, "area": area})

    def test_division_by_same_dimension_creates_dimensionless(self):
        """Dividing same dimensions should create dimensionless quantity."""
        l1 = Length(10, "meter")
        l2 = Length(2, "meter")

        result = l1 / l2

        # Should be dimensionless
        assert result.dim.is_dimensionless()
        # Value should be 10/2 = 5.0
        assert abs(result.value - 5.0) < 1e-10

    def test_power_maintains_dimensional_consistency(self):
        """Power operations should properly scale dimensions."""
        length = Length(3, "meter")

        # length^2 should give Area
        squared = length**2

        from qnty.core.dimension_catalog import Area as AreaDim

        assert squared.dim == AreaDim
        # 3^2 = 9
        assert abs(squared.value - 9.0) < 1e-10

    def test_dimensionless_operations_with_dimensional_quantities(self):
        """Test that dimensionless numbers only add/subtract to dimensionless quantities."""
        length = Length(5, "meter")
        dimensionless = Dimensionless(2, "dimensionless")

        # Adding dimensionless number (not quantity) to dimensional should fail
        with pytest.raises(TypeError, match="Cannot add dimensionless number"):
            _ = length + 2.0

        # But multiplying should work (scaling)
        result = length * 2.0
        assert abs(result.value - 10.0) < 1e-10


class TestEdgeCases:
    """Test edge cases and corner scenarios for dimensional analysis."""

    def test_zero_values_still_enforce_dimensions(self):
        """Zero values should still enforce dimensional compatibility."""
        zero_force = Force("zero_force").set(0, "newton")
        area = Area("area").set(5, "meter2")

        with pytest.raises(TypeError, match="Dimension mismatch"):
            _ = zero_force + area

    def test_negative_values_enforce_dimensions(self):
        """Negative values should still enforce dimensional compatibility."""
        neg_force = Force("neg_force").set(-100, "newton")
        pressure = Pressure("pressure").set(50, "pascal")

        with pytest.raises(TypeError, match="Dimension mismatch"):
            _ = neg_force - pressure

    def test_very_small_values_enforce_dimensions(self):
        """Very small values should still enforce dimensional compatibility."""
        tiny_length = Length("tiny_length").set(1e-15, "meter")
        tiny_area = Area("tiny_area").set(1e-15, "meter2")

        with pytest.raises(TypeError, match="Dimension mismatch"):
            _ = tiny_length + tiny_area


class TestComparisonWithZero:
    """Test that comparisons with dimensionless zero are allowed."""

    def test_compare_length_to_zero(self):
        """Comparing dimensional quantity to zero should work."""
        length = Length("test").set(5).meter
        zero = Dimensionless("zero").set(0).dimensionless

        # All comparison operators should work with zero
        assert length > zero
        assert length >= zero
        assert not (length < zero)
        assert not (length <= zero)

    def test_compare_negative_length_to_zero(self):
        """Comparing negative dimensional quantity to zero should work."""
        length = Length("test").set(-5).meter
        zero = Dimensionless("zero").set(0).dimensionless

        assert length < zero
        assert length <= zero
        assert not (length > zero)
        assert not (length >= zero)

    def test_compare_exactly_zero_to_zero(self):
        """Comparing zero dimensional quantity to zero should work."""
        length = Length("test").set(0).meter
        zero = Dimensionless("zero").set(0).dimensionless

        assert length <= zero
        assert length >= zero
        assert not (length < zero)
        assert not (length > zero)

    def test_compare_to_non_zero_dimensionless_fails(self):
        """Comparing dimensional quantity to non-zero dimensionless should fail."""
        length = Length("test").set(5).meter
        one = Dimensionless("one").set(1).dimensionless

        with pytest.raises(TypeError, match="Cannot compare quantities with different dimensions"):
            _ = length > one

    def test_compare_different_dimensions_fails(self):
        """Comparing different dimensional quantities should fail."""
        length = Length("test").set(5).meter
        pressure = Pressure("test").set(100).pascal

        with pytest.raises(TypeError, match="Cannot compare quantities with different dimensions"):
            _ = length > pressure

    def test_leq_with_zero_in_expression(self):
        """Test leq(T_r, 0) pattern common in engineering."""
        from qnty.algebra import leq

        T_r = Length("T_r").set(5).inch

        # Create comparison expression: T_r <= 0
        zero = Dimensionless("zero").set(0).dimensionless
        comparison = leq(T_r, zero)

        # Should evaluate to False (5 inch is not <= 0)
        result = comparison.evaluate({"T_r": T_r})
        assert result.value == 0.0  # False as float

    def test_leq_with_negative_value(self):
        """Test leq(T_r, 0) when T_r is negative."""
        from qnty.algebra import leq

        T_r = Length("T_r").set(-5).inch

        # Create comparison expression: T_r <= 0
        zero = Dimensionless("zero").set(0).dimensionless
        comparison = leq(T_r, zero)

        # Should evaluate to True (negative is <= 0)
        result = comparison.evaluate({"T_r": T_r})
        assert result.value == 1.0  # True as float


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
