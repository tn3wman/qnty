import pytest

from qnty import Dimensionless, Length, Pressure, Problem
from qnty.algebra import equation
from qnty.problems.rules import add_rule


def assert_qty_close(actual_var, expected_value, expected_unit, rel_tol=1e-9):
    """Helper function to assert variable quantity is close to expected value with relative tolerance."""
    from qnty.core.unit import ureg

    # Get the expected unit
    expected_unit_obj = ureg.resolve(expected_unit)
    if expected_unit_obj is None:
        raise ValueError(f"Unknown unit: {expected_unit}")

    # Convert the actual value to the expected unit for comparison
    if actual_var.value is None:
        actual_value_in_expected_unit = None
    else:
        # Convert from SI (actual_var.value) to expected unit
        actual_value_in_expected_unit = actual_var.value / expected_unit_obj.si_factor

    assert pytest.approx(expected_value, rel=rel_tol) == actual_value_in_expected_unit


def assert_problem_results(problem, expected_results):
    for var_name, expected_value, expected_unit, tolerance in expected_results:
        actual_var = getattr(problem, var_name)
        assert_qty_close(actual_var, expected_value, expected_unit, tolerance)


class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    P = Pressure("Design Pressure").set(90).psi
    D = Length("Outside Diameter").set(0.84).inch
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    c = Length("Mechanical Allowances").set(0.0).inch
    S = Pressure("Allowable Stress").set(20000).psi
    E = Dimensionless("Quality Factor").set(0.8).dimensionless
    W = Dimensionless("Weld Joint Strength Reduction Factor").set(1).dimensionless

    Y = Dimensionless("Y Coefficient").set(0.4).dimensionless

    T = Length("Wall Thickness")
    d = Length("Inside Diameter")
    t = Length("Pressure Design Thickness")
    t_m = Length("Minimum Required Thickness")
    P_max = Pressure("Pressure, Maximum")

    # Equations
    T_eqn = equation(T, T_bar * (1 - U_m))
    d_eqn = equation(d, D - 2 * T)
    t_eqn = equation(t, (P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = equation(t_m, t + c)
    P_max_eqn = equation(P_max, (2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))


    # # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    # TODO: Work on the validation system later
    # thick_wall_check = add_rule(
    #     t.geq(D / 6),
    #     "Thick wall condition detected (t >= D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
    #     warning_type="CODE_COMPLIANCE",
    #     severity="WARNING",
    # )

    # pressure_ratio_check = add_rule(
    #     P.gt((S * E) * 0.385),
    #     "High pressure ratio detected (P/(S*E) > 0.385). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
    #     warning_type="CODE_COMPLIANCE",
    #     severity="WARNING",
    # )

def create_straight_pipe_internal():
    return StraightPipeInternal()


def test_simple_problem():
    problem = create_straight_pipe_internal()

    problem.solve()

    expected_results = [
        # Known variables (exact)
        ("P", 90, "psi", None),
        ("D", 0.84, "in", None),
        ("T_bar", 0.147, "in", None),
        ("U_m", 0.125, "dimensionless", None),
        ("c", 0.0, "in", None),
        ("S", 20000, "psi", None),
        ("E", 0.8, "dimensionless", None),
        ("W", 1, "dimensionless", None),
        ("Y", 0.4, "dimensionless", None),
        # Calculated variables (with tolerance)
        ("T", 0.128625, "in", 1e-9),
        ("d", 0.58275, "in", 1e-9),
        ("t", 0.002357196308306311, "in", 1e-9),
        ("t_m", 0.002357196308306311, "in", 1e-9),
        ("P_max", 5584.045584045583, "psi", 1e-9),
    ]

    assert_problem_results(problem, expected_results)
