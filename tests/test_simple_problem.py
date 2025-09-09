import pytest

from qnty import Dimensionless, Length, Pressure, Problem, cond_expr
from qnty.problems.rules import add_rule


def assert_qty_close(actual_var, expected_value, expected_unit, rel_tol=1e-9):
    """Helper function to assert variable quantity is close to expected value with relative tolerance."""
    # expected_qty = Qty(expected_value, expected_unit)
    assert pytest.approx(expected_value, rel=rel_tol) == actual_var.value
    assert expected_unit == actual_var.unit



def assert_problem_results(problem, expected_results):
    for var_name, expected_value, expected_unit, tolerance in expected_results:
        actual_var = getattr(problem, var_name)
        assert_qty_close(
            actual_var,
            expected_value,
            expected_unit,
            tolerance
        )

class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    # Known variables - using new simplified syntax
    P = Pressure(90, "psi", "Design Pressure")
    D = Length(0.5, "inch", "Outside Diameter")
    T_bar = Length(0.035, "inch", "Nominal Wall Thickness")
    U_m = Dimensionless(0.125, "Mill Undertolerance")
    c = Length(0.0, "inch", "Mechanical Allowances")
    S = Pressure(20000, "psi", "Allowable Stress")
    E = Dimensionless(1, "Quality Factor")
    W = Dimensionless(1, "Weld Joint Strength Reduction Factor")

    # Unknown variables - using new simplified syntax
    Y = Dimensionless(0.4, "Y Coefficient")
    T = Length("Wall Thickness", is_known=False)
    d = Length("Inside Diameter", is_known=False)
    t = Length("Pressure Design Thickness", is_known=False)
    t_m = Length("Minimum Required Thickness", is_known=False)
    P_max = Pressure("Pressure, Maximum", is_known=False)

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
        ("P", 90, "psi", 1e-9),
        ("D", 0.5, "in", 1e-9),
        ("T_bar", 0.035, "in", 1e-9),
        ("U_m", 0.125, "", 1e-9),
        ("c", 0.0, "in", 1e-9),
        ("S", 20000, "psi", 1e-9),
        ("E", 1.0, "", 1e-9),
        ("W", 1, "", 1e-9),
        ("Y", 0.4, "", 1e-9),
        # Calculated variables (with tolerance)
        ("T", 0.030625000000000003, "in", 1e-9),
        ("d", 0.43875, "in", 1e-9),
        ("t", 0.028523657416650028, "mm", 1e-9),
        ("t_m", 0.028523657416650028, "mm", 1e-9),
        ("P_max", 17762518.033648793, "Pa", 1e-9),
    ]



    assert_problem_results(problem, expected_results)
