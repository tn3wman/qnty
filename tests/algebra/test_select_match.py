"""
Tests for SelectVariable and match_expr functionality
"""

import pytest
from dataclasses import dataclass

from qnty import Dimensionless, Length, Pressure, Problem
from qnty.algebra import SelectOption, SelectVariable, equation, match_expr


@dataclass(frozen=True)
class GasketType(SelectOption):
    """Example select options for gasket types."""
    non_self_energized: str = "non_self_energized"
    self_energized: str = "self_energized"


@dataclass(frozen=True)
class MaterialGrade(SelectOption):
    """Example select options for material grades."""
    grade_a: str = "A"
    grade_b: str = "B"
    grade_c: str = "C"


def test_select_variable_creation():
    """Test creating a SelectVariable with options."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    assert gasket_type.name == "Gasket Type"
    assert gasket_type.selected == GasketType.non_self_energized
    assert gasket_type.value == GasketType.non_self_energized


def test_select_variable_get_options():
    """Test getting all valid options from a SelectVariable."""
    gasket_type = SelectVariable("Gasket Type", GasketType)

    options = gasket_type.get_options()
    option_values = gasket_type.get_option_values()
    option_names = gasket_type.get_option_names()

    # Should have exactly 2 options
    assert len(options) == 2
    assert len(option_values) == 2
    assert len(option_names) == 2

    # Check that the options are correct
    assert "non_self_energized" in option_names
    assert "self_energized" in option_names
    assert GasketType.non_self_energized in option_values
    assert GasketType.self_energized in option_values


def test_select_variable_select():
    """Test selecting different options."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    assert gasket_type.value == GasketType.non_self_energized

    # Change selection
    gasket_type.select(GasketType.self_energized)
    assert gasket_type.value == GasketType.self_energized


def test_select_variable_invalid_option():
    """Test that invalid options raise an error."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    with pytest.raises(ValueError, match="Invalid option"):
        gasket_type.select("invalid_option")


def test_match_expr_basic():
    """Test basic match expression functionality."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    # Create a simple match expression with constants
    result = match_expr(
        gasket_type,
        GasketType.non_self_energized, 25,
        GasketType.self_energized, 15
    )

    # Evaluate with non_self_energized selected
    evaluated = result.evaluate({})
    assert evaluated.value == 25

    # Change selection and evaluate again
    gasket_type.select(GasketType.self_energized)
    evaluated = result.evaluate({})
    assert evaluated.value == 15


def test_match_expr_with_quantities():
    """Test match expression with Quantity objects."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    pressure_a = Pressure("P_a").set(100).psi
    pressure_b = Pressure("P_b").set(200).psi

    result = match_expr(
        gasket_type,
        GasketType.non_self_energized, pressure_a,
        GasketType.self_energized, pressure_b
    )

    # Evaluate with non_self_energized selected
    evaluated = result.evaluate({})
    assert pytest.approx(evaluated.value, rel=1e-9) == pressure_a.value

    # Change selection
    gasket_type.select(GasketType.self_energized)
    evaluated = result.evaluate({})
    assert pytest.approx(evaluated.value, rel=1e-9) == pressure_b.value


def test_match_expr_with_expressions():
    """Test match expression with arithmetic expressions."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    G = Length("G").set(3).inch
    P = Pressure("P").set(100).psi
    b = Length("b").set(0.5).inch
    m = Dimensionless("m").set(2.0).dimensionless

    # Formula from ASME code:
    # Non-self-energized: 0.785*G^2*P + 2*b*pi*G*m*P  (equation 4.16.4)
    # Self-energized: 0.785*G^2*P  (equation 4.16.5)
    import math
    pi = math.pi

    result = match_expr(
        gasket_type,
        GasketType.non_self_energized, 0.785 * G**2 * P + 2 * b * pi * G * m * P,
        GasketType.self_energized, 0.785 * G**2 * P
    )

    # Evaluate with non_self_energized selected
    evaluated_non_self = result.evaluate({})

    # Change to self_energized
    gasket_type.select(GasketType.self_energized)
    evaluated_self = result.evaluate({})

    # Self-energized should be less (no second term)
    assert evaluated_self.value < evaluated_non_self.value


def test_match_expr_in_problem():
    """Test using match_expr in a Problem class."""

    class SimpleMatchProblem(Problem):
        name = "Simple Match Problem"

        # Select variable for material grade
        material = SelectVariable("Material Grade", MaterialGrade, MaterialGrade.grade_a)

        # Different allowable stresses for different grades
        allowable_stress = Pressure("Allowable Stress")

        # Use match to set allowable stress based on material
        allowable_stress_eqn = equation(
            allowable_stress,
            match_expr(
                material,
                MaterialGrade.grade_a, 20000,
                MaterialGrade.grade_b, 25000,
                MaterialGrade.grade_c, 30000
            )
        )

    problem = SimpleMatchProblem()
    problem.solve()

    # Check grade A (values are dimensionless in this test, stored in SI which is Pa for Pressure)
    # Since we're providing dimensionless numbers, they're treated as SI units (Pa)
    # 20000 psi = 137895145 Pa, but since we're giving dimensionless 20000, it's stored as 20000 Pa
    assert pytest.approx(problem.allowable_stress.value, rel=1e-3) == 20000  # Value in Pa

    # Change to grade B
    problem.material.select(MaterialGrade.grade_b)
    problem.solve()
    assert pytest.approx(problem.allowable_stress.value, rel=1e-3) == 25000

    # Change to grade C
    problem.material.select(MaterialGrade.grade_c)
    problem.solve()
    assert pytest.approx(problem.allowable_stress.value, rel=1e-3) == 30000


def test_match_expr_three_way():
    """Test match expression with more than two options."""
    material = SelectVariable("Material Grade", MaterialGrade, MaterialGrade.grade_a)

    result = match_expr(
        material,
        MaterialGrade.grade_a, 100,
        MaterialGrade.grade_b, 200,
        MaterialGrade.grade_c, 300
    )

    # Test each option
    evaluated = result.evaluate({})
    assert evaluated.value == 100

    material.select(MaterialGrade.grade_b)
    evaluated = result.evaluate({})
    assert evaluated.value == 200

    material.select(MaterialGrade.grade_c)
    evaluated = result.evaluate({})
    assert evaluated.value == 300


def test_match_expr_no_selection():
    """Test that match_expr raises error when no option is selected."""
    gasket_type = SelectVariable("Gasket Type", GasketType)  # No initial selection

    result = match_expr(
        gasket_type,
        GasketType.non_self_energized, 25,
        GasketType.self_energized, 15
    )

    with pytest.raises(ValueError, match="has no value selected"):
        result.evaluate({})


def test_match_expr_missing_case():
    """Test that match_expr raises error when selected value has no case."""
    # This shouldn't happen in practice due to validation, but test the error handling
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    # Create match with only one case
    result = match_expr(
        gasket_type,
        GasketType.self_energized, 15  # Only has self_energized case
    )

    # Should raise error because non_self_energized is selected but not in cases
    with pytest.raises(ValueError, match="No case for value"):
        result.evaluate({})


def test_match_expr_invalid_args():
    """Test that match_expr validates argument count."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    # Odd number of cases (missing expression for last option)
    with pytest.raises(ValueError, match="even number of arguments"):
        match_expr(
            gasket_type,
            GasketType.non_self_energized, 25,
            GasketType.self_energized  # Missing expression
        )


def test_select_variable_str_repr():
    """Test string representation of SelectVariable."""
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

    str_repr = str(gasket_type)
    assert "Gasket Type" in str_repr
    assert "non_self_energized" in str_repr

    repr_str = repr(gasket_type)
    assert "SelectVariable" in repr_str
