"""
Test re-solving functionality to ensure problems can be solved multiple times
with different input values, maintaining correct units and producing accurate results.

This test was created to address an issue where changing variable values and
re-solving would not update the results, and where unit preservation was lost.
"""

import pytest

from qnty import Dimensionless, Length, Pressure, Problem


class SimpleProblemForReSolving(Problem):
    """A simple problem for testing re-solving functionality."""

    # Known variables
    P = Pressure(100, "psi", "Design Pressure")
    D = Length(1.0, "inch", "Diameter")
    factor = Dimensionless(2.0, "Multiplication Factor")

    # Unknown variables
    result = Pressure("Result Pressure", "psi")

    # Simple equation: result = P * factor
    result_eqn = result.equals(P * factor)


def test_basic_re_solving():
    """Test that re-solving works with changed known variables."""
    problem = SimpleProblemForReSolving()

    # First solve
    problem.solve()

    # Verify first result
    # result = P * factor = 100 * 2.0 = 200 psi
    assert problem.result.quantity is not None
    assert problem.result.quantity.value == pytest.approx(200.0)
    assert problem.result.quantity.unit.symbol == "psi"

    # Change P and re-solve
    problem.P.set(150, "psi")  # Using the fixed set method
    problem.solve()

    # Verify second result
    # result = P * factor = 150 * 2.0 = 300 psi
    assert problem.result.quantity is not None
    assert problem.result.quantity.value == pytest.approx(300.0)
    assert problem.result.quantity.unit.symbol == "psi"


def test_unit_preservation_in_re_solving():
    """Test that original units are preserved after re-solving."""
    problem = SimpleProblemForReSolving()

    # First solve - should give result in psi
    problem.solve()
    assert problem.result.quantity is not None
    assert problem.result.quantity.unit.symbol == "psi"

    # Change input and re-solve
    problem.P.set(200, "psi")
    problem.solve()

    # Unit should still be psi
    assert problem.result.quantity is not None
    assert problem.result.quantity.unit.symbol == "psi"
    assert problem.result.quantity.value == pytest.approx(400.0)  # 200 * 2.0


def test_multiple_variable_changes():
    """Test re-solving with multiple variable changes."""
    problem = SimpleProblemForReSolving()

    # Initial solve
    problem.solve()

    # Change both P and factor
    problem.P.set(50, "psi")
    problem.factor.set(3.0, "dimensionless")
    problem.solve()

    # result = 50 * 3.0 = 150 psi
    assert problem.result.quantity is not None
    assert problem.result.quantity.value == pytest.approx(150.0)
    assert problem.result.quantity.unit.symbol == "psi"


def test_fluent_api_re_solving():
    """Test re-solving using the fluent API (.set().unit)."""
    problem = SimpleProblemForReSolving()

    # First solve
    problem.solve()

    # Change using fluent API
    problem.P.set(120).psi
    problem.solve()

    # result = 120 * 2.0 = 240 psi
    assert problem.result.quantity is not None
    assert problem.result.quantity.value == pytest.approx(240.0)


def test_unit_conversion_in_re_solving():
    """Test that unit conversion works properly during re-solving."""
    problem = SimpleProblemForReSolving()

    # First solve with original units
    problem.solve()
    assert problem.result.quantity is not None
    assert problem.result.quantity.unit.symbol == "psi"

    # Change D using different units
    problem.D.set(2.54, "centimeter")  # 2.54 cm = 1 inch
    problem.solve()

    # Result should be the same since D doesn't affect the equation
    # and the result should still be in psi
    assert problem.result.quantity is not None
    assert problem.result.quantity.unit.symbol == "psi"


def test_original_variable_states_preserved():
    """Test that original variable known/unknown states are preserved."""
    problem = SimpleProblemForReSolving()

    # Check initial states
    assert problem.P.is_known
    assert problem.D.is_known
    assert problem.factor.is_known
    assert not problem.result.is_known

    # Solve
    problem.solve()

    # After solving, result should become known
    assert problem.result.is_known

    # Change a variable and re-solve
    problem.P.set(75, "psi")
    problem.solve()

    # States should be preserved correctly
    assert problem.P.is_known
    assert problem.D.is_known
    assert problem.factor.is_known
    assert problem.result.is_known


class ComposedProblemForReSolving(Problem):
    """Test composed problem re-solving."""

    # Compose the simple problem
    sub = SimpleProblemForReSolving()

    # Additional variables
    multiplier = Dimensionless(1.5, "Multiplier")
    final_result = Pressure("Final Result", "psi")

    # Equation: final_result = sub.result * multiplier
    final_eqn = final_result.equals(sub.result * multiplier)


def test_composed_problem_re_solving():
    """Test that composed problems also support re-solving correctly."""
    problem = ComposedProblemForReSolving()

    # Initial solve
    problem.solve()

    # Check initial calculation:
    # sub.result = sub.P * sub.factor = 100 * 2.0 = 200 psi
    # final_result = sub.result * multiplier = 200 * 1.5 = 300 psi
    assert problem.final_result.quantity is not None
    assert problem.final_result.quantity.value == pytest.approx(300.0)
    assert problem.final_result.quantity.unit.symbol == "psi"

    # Change sub-problem variable and re-solve
    problem.sub_P.set(200, "psi")  # Change composed variable
    problem.solve()

    # New calculation:
    # sub.result = 200 * 2.0 = 400 psi
    # final_result = 400 * 1.5 = 600 psi
    assert problem.final_result.quantity is not None
    assert problem.final_result.quantity.value == pytest.approx(600.0)
    assert problem.final_result.quantity.unit.symbol == "psi"


def test_set_method_with_unit_parameter():
    """Test the set method with unit parameter works correctly."""
    problem = SimpleProblemForReSolving()

    # Test set with unit parameter
    problem.P.set(150, "psi")

    # Verify the new value was set correctly
    assert problem.P.quantity is not None
    assert problem.P.quantity.value == pytest.approx(150.0)
    assert problem.P.quantity.unit.symbol == "psi"


def test_error_handling_in_re_solving():
    """Test error handling when using invalid units."""
    problem = SimpleProblemForReSolving()

    # Test invalid unit
    with pytest.raises(ValueError):
        problem.P.set(100, "invalid_unit")


if __name__ == "__main__":
    # Run individual tests for debugging
    test_basic_re_solving()
    print("✓ Basic re-solving test passed")

    test_unit_preservation_in_re_solving()
    print("✓ Unit preservation test passed")

    test_multiple_variable_changes()
    print("✓ Multiple variable changes test passed")

    test_fluent_api_re_solving()
    print("✓ Fluent API re-solving test passed")

    test_unit_conversion_in_re_solving()
    print("✓ Unit conversion re-solving test passed")

    test_original_variable_states_preserved()
    print("✓ Variable states preservation test passed")

    test_composed_problem_re_solving()
    print("✓ Composed problem re-solving test passed")

    test_set_method_with_unit_parameter()
    print("✓ Set method with unit parameter test passed")

    test_error_handling_in_re_solving()
    print("✓ Error handling test passed")

    print("\nAll re-solving tests passed! 🎉")
