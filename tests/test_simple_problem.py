import pytest

from qnty import Dimensionless, Length, Pressure, Problem
from qnty.problems.rules import add_rule


def assert_qty_close(actual_var, expected_value, expected_unit, rel_tol=1e-9):
    """Helper function to assert variable quantity is close to expected value with relative tolerance."""
    # expected_qty = Qty(expected_value, expected_unit)
    assert pytest.approx(expected_value, rel=rel_tol) == actual_var.value
    assert expected_unit == actual_var.unit


def assert_problem_results(problem, expected_results):
    for var_name, expected_value, expected_unit, tolerance in expected_results:
        actual_var = getattr(problem, var_name)
        assert_qty_close(actual_var, expected_value, expected_unit, tolerance)


class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    # Known variables - using new clean syntax
    P = Pressure("Design_Pressure", "psi", 90)
    D = Length("Outside_Diameter", "inch", 0.5)
    T_bar = Length("Nominal_Wall_Thickness", "inch", 0.035)
    U_m = Dimensionless("Mill_Undertolerance", 0.125)
    c = Length("Mechanical_Allowances", "inch", 0.0)
    S = Pressure("Allowable_Stress", "psi", 20000)
    E = Dimensionless("Quality_Factor", 1)
    W = Dimensionless("Weld_Joint_Strength_Reduction_Factor", 1)

    # Unknown variables - using new clean syntax
    Y = Dimensionless("Y_Coefficient", 0.4)
    T = Length("Wall_Thickness", "inch")
    d = Length("Inside_Diameter", "inch")
    t = Length("Pressure_Design_Thickness", "inch")
    t_m = Length("Minimum_Required_Thickness", "inch")
    P_max = Pressure("Pressure_Maximum", "psi")

    # Equations
    T_eqn = T.equals(T_bar * (1 - U_m))
    d_eqn = d.equals(D - 2 * T)
    t_eqn = t.equals((P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = t_m.equals(t + c)
    P_max_eqn = P_max.equals((2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))

    # ASME B31.3 Section 304.1.1 Y coefficient logic
    # Explicit handling of both conditions per ASME B31.3
    # Y_eqn = Y.equals(
    #     cond_expr(
    #         t.lt(D / 6),
    #         Y,  # Table value for t < D/6
    #         cond_expr(
    #             t.geq(D / 6),
    #             (d + 2 * c) / (D + d + 2 * c),  # Calculated for t >= D/6
    #             Y,  # Fallback (should not be reached)
    #         ),
    #     )
    # )

    # # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    thick_wall_check = add_rule(
        t.geq(D / 6),
        "Thick wall condition detected (t >= D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )

    pressure_ratio_check = add_rule(
        P.gt((S * E) * 0.385),
        "High pressure ratio detected (P/(S*E) > 0.385). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )


def create_straight_pipe_internal():
    return StraightPipeInternal()


def test_simple_problem():
    problem = create_straight_pipe_internal()

    problem.solve()

    expected_results = [
        # Known variables (exact)
        ("P", 90, "psi", None),
        ("D", 0.5, "in", None),
        ("T_bar", 0.035, "in", None),
        ("U_m", 0.125, "", None),
        ("c", 0.0, "in", None),
        ("S", 20000, "psi", None),
        ("E", 1.0, "", None),
        ("W", 1, "", None),
        ("Y", 0.4, "", None),
        # Calculated variables (with tolerance)
        ("T", 0.030625000000000003, "in", 1e-9),
        ("d", 0.43875, "in", 1e-9),
        ("t", 0.0011229786384507885, "in", 1e-9),
        ("t_m", 0.0011229786384507885, "in", 1e-9),
        ("P_max", 2576.2355415352267, "psi", 1e-9),
    ]

    assert_problem_results(problem, expected_results)
