"""
Test that composed problems preserve variable types correctly.

This test file ensures that when problems are composed together,
the type of variables (Length, Pressure, etc.) is preserved and
not inadvertently converted to Dimensionless.
"""

import pytest

from qnty import Dimensionless, Length, Pressure, Problem


class SimpleProblem(Problem):
    """A simple problem with different variable types."""

    P = Pressure(100, "psi", "Pressure")
    D = Length(1.0, "inch", "Diameter")
    E = Dimensionless(0.8, "Efficiency")

    # Unknown variables
    P_out = Pressure("Output Pressure", "psi")

    # Simple equation
    P_out_eqn = P_out.equals(P * E)


def create_simple_problem():
    """Factory function to create a simple problem instance."""
    return SimpleProblem()


class ComposedProblem(Problem):
    """A problem that composes another problem."""

    # Compose the simple problem
    sub = create_simple_problem()

    # Type hints for composed variables (for IDE support)
    sub_P: Pressure
    sub_D: Length
    sub_E: Dimensionless
    sub_P_out: Pressure

    # Try to modify composed variables - this should preserve types
    sub.P.set(150).psi  # Should work with Pressure type
    sub.D.set(2.0).inch  # Should work with Length type
    sub.E.set(0.9).dimensionless  # Should work with Dimensionless type

    # Add our own variables
    factor = Dimensionless(1.5, "Factor")
    P_final = Pressure("Final Pressure", "psi")

    # Equation using composed variables
    P_final_eqn = P_final.equals(sub.P_out * factor)


def test_composed_problem_preserves_variable_types():
    """Test that variable types are preserved in composed problems."""
    problem = ComposedProblem()

    # Check that sub-problem variables maintain their types
    assert hasattr(problem.sub_P, "quantity"), "Composed variable should have quantity attribute"
    assert hasattr(problem.sub_D, "quantity"), "Composed variable should have quantity attribute"
    assert hasattr(problem.sub_E, "quantity"), "Composed variable should have quantity attribute"

    # The crucial test: Check that we can use type-specific setters
    # This will fail if the variable was converted to Dimensionless

    # Test Pressure variable - the setter should have the correct type
    result_P = problem.sub_P.set(200).psi  # Should not raise AttributeError
    assert result_P is not None
    assert result_P == problem.sub_P  # The setter returns the variable

    # Test Length variable - the setter should have the correct type
    result_D = problem.sub_D.set(3.0).inch  # Should not raise AttributeError
    assert result_D is not None
    assert result_D == problem.sub_D  # The setter returns the variable

    # Test Dimensionless variable - the setter should have the correct type
    result_E = problem.sub_E.set(0.95).dimensionless  # Should not raise AttributeError
    assert result_E is not None
    assert result_E == problem.sub_E  # The setter returns the variable


def test_composed_problem_type_specific_units():
    """Test that type-specific unit conversions work in composed problems."""
    problem = ComposedProblem()

    # Test Pressure-specific units
    problem.sub_P.set(100).bar  # Should work
    assert problem.sub_P.quantity is not None

    problem.sub_P.set(14.5).psi  # Should work
    assert problem.sub_P.quantity is not None

    problem.sub_P.set(101325).pascal  # Should work
    assert problem.sub_P.quantity is not None

    # Test Length-specific units
    problem.sub_D.set(25.4).millimeter  # Should work
    assert problem.sub_D.quantity is not None

    problem.sub_D.set(1.0).meter  # Should work
    assert problem.sub_D.quantity is not None

    problem.sub_D.set(3.28).foot  # Should work
    assert problem.sub_D.quantity is not None


def test_nested_composition_preserves_types():
    """Test that types are preserved even in nested compositions."""

    class DoubleComposedProblem(Problem):
        """A problem that composes a composed problem."""

        # Compose the already-composed problem
        composed = ComposedProblem()

        # Type hints for doubly-composed variables (for IDE support)
        composed_sub_P: Pressure
        composed_sub_D: Length
        composed_sub_E: Dimensionless
        composed_sub_P_out: Pressure
        composed_factor: Dimensionless
        composed_P_final: Pressure

        # Access deeply nested variables
        composed.sub.P.set(250).psi  # Should still work
        composed.sub.D.set(4.0).inch  # Should still work

    problem = DoubleComposedProblem()

    # The deeply nested variables should still have the right types
    # These are now doubly-namespaced: composed_sub_P, composed_sub_D, etc.

    # Test that we can still use type-specific setters
    result_P = problem.composed_sub_P.set(300).psi  # Should not raise AttributeError
    assert result_P is not None
    assert result_P == problem.composed_sub_P

    result_D = problem.composed_sub_D.set(5.0).inch  # Should not raise AttributeError
    assert result_D is not None
    assert result_D == problem.composed_sub_D


def test_original_setter_methods_work():
    """Test that the original setter methods still function correctly."""
    problem = ComposedProblem()

    # Test using the full setter chain
    result = problem.sub_P.set(100).psi
    assert result == problem.sub_P
    assert problem.sub_P.quantity is not None
    assert problem.sub_P.quantity.value == pytest.approx(100.0)

    result = problem.sub_D.set(2.5).centimeter
    assert result == problem.sub_D
    assert problem.sub_D.quantity is not None
    # The value stored depends on the default unit for Length
    # We just need to verify it was set and has a value
    assert problem.sub_D.quantity.value > 0


def test_variable_type_in_expressions():
    """Test that composed variables maintain their types when used in expressions."""
    problem = ComposedProblem()

    # Create expressions using composed variables
    expr1 = problem.sub_P * 2  # Should create a valid expression
    expr2 = problem.sub_D + problem.sub_D  # Should create a valid expression
    expr3 = problem.sub_E * 0.5  # Should create a valid expression

    # These expressions should be valid
    assert expr1 is not None
    assert expr2 is not None
    assert expr3 is not None

    # The variables in the expressions should maintain their types
    # (This is implicitly tested by the fact that the expressions can be created)


def test_solving_with_preserved_types():
    """Test that problem solving works correctly with preserved variable types."""
    problem = ComposedProblem()

    # Set known values
    problem.sub_P.set(100).psi
    problem.sub_E.set(0.8).dimensionless
    problem.factor.set(1.2).dimensionless

    # Solve the problem
    problem.solve()

    # Check that the solution maintains proper types
    assert problem.sub_P_out.quantity is not None
    assert problem.P_final.quantity is not None

    # Check the calculated values
    # P_out = P * E = 100 * 0.8 = 80 psi
    # P_final = P_out * factor = 80 * 1.2 = 96 psi
    assert problem.sub_P_out.quantity.value == pytest.approx(80.0)
    assert problem.P_final.quantity.value == pytest.approx(96.0)


def test_error_on_wrong_unit_type():
    """Test that using wrong unit types raises appropriate errors."""
    problem = ComposedProblem()

    # These should raise AttributeError because the units don't match the variable type
    # Test on the setters (where unit properties are accessible)
    with pytest.raises(AttributeError):
        problem.sub_P.set(100).meter  # type: ignore[attr-defined] # Pressure setter doesn't have meter

    with pytest.raises(AttributeError):
        problem.sub_D.set(1.0).psi  # type: ignore[attr-defined] # Length setter doesn't have psi

    with pytest.raises(AttributeError):
        problem.sub_E.set(0.5).inch  # type: ignore[attr-defined] # Dimensionless setter doesn't have inch


if __name__ == "__main__":
    # Run a quick test to verify the fix works
    test_composed_problem_preserves_variable_types()
    print("✓ Basic type preservation test passed")

    test_composed_problem_type_specific_units()
    print("✓ Type-specific units test passed")

    test_nested_composition_preserves_types()
    print("✓ Nested composition test passed")

    test_original_setter_methods_work()
    print("✓ Setter methods test passed")

    test_variable_type_in_expressions()
    print("✓ Variable expressions test passed")

    test_solving_with_preserved_types()
    print("✓ Problem solving test passed")

    test_error_on_wrong_unit_type()
    print("✓ Wrong unit type error test passed")

    print("\nAll tests passed! Variable types are correctly preserved in composed problems.")
