import pytest

from qnty import AnglePlane, Area, Dimensionless, Length, Pressure, Problem, cond_expr, max_expr, min_expr, sin
from qnty.algebra import equation, geq, gt, leq
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
    """
    Table-driven test helper for asserting problem results.

    Args:
        problem: Solved engineering problem instance
        expected_results: List of tuples (variable_name, expected_value, expected_unit, tolerance)
                         If tolerance is None, exact comparison is used
                         If tolerance is provided, approximate comparison is used

    Example:
        expected_results = [
            ("P", 90, "psi", None),          # Exact comparison
            ("t", 0.002357, "inch", 1e-9),     # Approximate comparison
        ]
        assert_problem_results(problem, expected_results)
    """
    for var_name, expected_value, expected_unit, tolerance in expected_results:
        actual_var = getattr(problem, var_name)
        assert_qty_close(actual_var, expected_value, expected_unit, tolerance)


class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    P = Pressure("Design Pressure").set(90).pound_force_per_square_inch
    D = Length("Outside Diameter").set(0.84).inch
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    c = Length("Mechanical Allowances").set(0.0).inch
    S = Pressure("Allowable Stress").set(20000).pound_force_per_square_inch
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


    # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    thick_wall_check = add_rule(
        geq(t, D / 6),
        "Thick wall condition detected (t >= D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )

    pressure_ratio_check = add_rule(
        gt(P, (S * E) * 0.385),
        "High pressure ratio detected (P/(S*E) > 0.385). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )

def create_straight_pipe_internal():
    return StraightPipeInternal()


class WeldedBranchConnection(Problem):
    """
    Composed Branch Reinforcement using sub-problems.
    Demonstrates the new composition pattern with clean syntax.
    """

    name = "Composed Branch Connection Analysis (ASME B31.3)"
    description = "Reinforcement area calculations using composed sub-problems per ASME B31.3."

    # System-level variables
    P = Pressure("Design Pressure").set(90).pound_force_per_square_inch
    beta = AnglePlane("Branch Angle").set(90).degree

    # Sub-problems - automatically integrated with namespace prefixes
    header = create_straight_pipe_internal()
    branch = create_straight_pipe_internal()

    # Share system pressure with sub-problems
    header.P.value = None
    branch.P.value = None
    header_P_eqn = equation(header.P, P)
    branch_P_eqn = equation(branch.P, P)

    # # Known variables for reinforcement pad
    D_r = Length("Outside Diameter, Reinforcement").set(0).inch
    T_bar_r = Length("Thickness, Reinforcement").set(0).inch
    U_m_r = Dimensionless("Mill Undertolerance, Reinforcement").set(0).dimensionless
    S_r = Pressure("Allowable Stress, Reinforcement").set(0).pound_force_per_square_inch

    # # Unknown variables for reinforcement pad
    A_r = Area("Reinforcement Ring Area")
    T_r = Length("Nominal Thickness, Reinforcement")

    # # # Known variables for welds
    z_b = Length("Weld Leg, Branch").set(0).inch
    z_r = Length("Weld Leg, Reinforcement").set(0).inch
    t_c_max = Length("Weld Throat, Max").set(6).millimeter

    # # Unknown variables for welds
    t_c_b = Length("Weld Throat, Branch")
    t_c_r = Length("Weld Throat, Reinforcement")
    A_w_b = Area("Weld Area, Branch")
    A_w_r = Area("Weld Area, Reinforcement")
    A_w = Area("Weld Area")

    # # Unknown variables for branch reinforcement zone
    d_1 = Length("Effective Length Removed")
    d_2 = Length("Reinforcement Zone Radius")
    L_4 = Length("Reinforcement Zone Height")


    # # Unknown variables for required and available area
    A_1 = Area("Reinforcement Area Required")
    A_2 = Area("Reinforcement Area Run")
    A_3 = Area("Reinforcement Area Branch")
    A_4 = Area("Reinforcement Area Total")


    d_1_eqn = equation(d_1, (branch.D - 2 * (branch.T - branch.c)) / sin(beta))
    d_2_eqn = equation(d_2, max_expr(d_1, (branch.T - branch.c) + (header.T - header.c) + d_1 / 2))
    L_4_eqn = equation(L_4, min_expr(2.5 * (header.T - header.c), 2.5 * (branch.T - branch.c) + T_bar_r))



    # Calculations for reinforcement pad
    A_r_eqn = equation(A_r, min_expr(T_r, L_4) * (min_expr(D_r, 2 * d_2) - branch.D / sin(beta)) * min_expr(1, S_r / header.S))
    T_r_eqn = equation(T_r, T_bar_r * (1 - U_m_r))

    # Calculation for weld area
    t_c_b_eqn = equation(t_c_b, min_expr(0.7 * branch.T_bar, t_c_max))
    t_c_r_eqn = equation(t_c_r, 0.5 * T_bar_r)

    A_w_b_eqn = equation(
        A_w_b,
        cond_expr(
            leq(T_r, 0),
            2 * 0.5 * max_expr((t_c_b / 0.707), z_b) ** 2,
            cond_expr(
                leq(T_r,L_4),
                2 * 0.5 * max_expr((t_c_b / 0.707), z_b) ** 2,
                0
            )
        )
    )

    A_w_r_eqn = equation(
        A_w_r,
        cond_expr(
            leq(D_r, 2 * d_2 - max_expr((t_c_r / 0.707), z_r)),
            2 * 0.5 * max_expr((t_c_r / 0.707), z_r) ** 2,
            0
        )
    )

    A_w_eqn = equation(A_w, A_w_b + A_w_r)

    # Calculation for total area
    A_1_eqn = equation(A_1, header.t * d_1 * (2 - sin(beta)))
    A_2_eqn = equation(A_2, (2 * d_2 - d_1) * (header.T - header.t - header.c))
    A_3_eqn = equation(A_3, (2 * L_4 * (branch.T - branch.t - branch.c) / sin(beta)) * min_expr(1, branch.S / header.S))
    A_4_eqn = equation(A_4, A_r + A_w)


def create_welded_branch_connection():
    """Factory function to create a BranchReinforcement engineering problem instance."""
    return WeldedBranchConnection()


def test_branch_reinforcement_h301(capsys):
    problem = create_welded_branch_connection()

    # For system
    problem.P.set(2068000).pascal

    # For header
    problem.header.D.set(219.1).millimeter
    problem.header.T_bar.set(8.18).millimeter
    problem.header.U_m.set(0.125).dimensionless
    problem.header.c.set(2.5).millimeter
    problem.header.S.set(110000000).pascal # 110 MPa
    problem.header.E.set(1).dimensionless
    problem.header.W.set(1).dimensionless
    problem.header.Y.set(0.4).dimensionless

    # For run
    problem.branch.D.set(114.3).millimeter
    problem.branch.T_bar.set(6.02).millimeter
    problem.branch.U_m.set(0.125).dimensionless
    problem.branch.c.set(2.5).millimeter
    problem.branch.S.set(110000000).pascal
    problem.branch.E.set(1).dimensionless
    problem.branch.W.set(1).dimensionless
    problem.branch.Y.set(0.4).dimensionless

    problem.solve()

    expected_results = [
        ("d_1", 108.765, "millimeter", 1e-9),
        ("d_2", 108.765, "millimeter", 1e-9),
        ("L_4", 6.91875, "millimeter", 1e-9),
        ("A_1", 222.33391704383038, "mm2", 1e-9),
        ("A_2", 284.23907045616954, "mm2", 1e-9),
        ("A_3", 23.53896202060505, "mm2", 1e-9),
        ("A_4", 35.52632094892658, "mm2", 1e-9),
    ]

    with capsys.disabled():
        print("")
        print(problem.d_1)
        print(problem.d_2)
        print(problem.L_4)
        print(problem.A_1)
        print(problem.A_2)
        print(problem.A_3)
        print(problem.A_w_b)
        print(problem.A_w_r)
        print(problem.A_w)
        print(problem.A_4)

    assert problem.is_solved

    assert_problem_results(problem, expected_results)



def test_branch_reinforcement_h303(capsys):
    problem = create_welded_branch_connection()

    # For system
    problem.P.set(3450000).pascal

    # For header
    problem.header.D.set(406.4).mm
    problem.header.T_bar.set(12.70).mm
    problem.header.U_m.set(0.125).dimensionless
    problem.header.c.set(2.5).mm
    problem.header.S.set(99300000).pascal
    problem.header.E.set(1).dimensionless
    problem.header.W.set(1).dimensionless
    problem.header.Y.set(0.4).dimensionless

    # For run
    problem.branch.D.set(168.3).mm
    problem.branch.T_bar.set(7.11).mm
    problem.branch.U_m.set(0.125).dimensionless
    problem.branch.c.set(2.5).mm
    problem.branch.S.set(99300000).pascal
    problem.branch.E.set(1).dimensionless
    problem.branch.W.set(1).dimensionless
    problem.branch.Y.set(0.4).dimensionless

    # For reinforcement
    problem.beta.set(60).degree
    problem.D_r.set(305).mm
    problem.T_bar_r.set(12.7).mm
    problem.S_r.set(99300000).pascal

    problem.z_b.set(10).mm
    problem.z_r.set(10).mm

    problem.solve()

    assert problem.is_solved

    expected_results = [
        ("d_1", 185.74224185234047, "mm", 1e-9),
        ("d_2", 185.74224185234047, "mm", 1e-9),
        ("L_4", 21.531249999999996, "mm", 1e-9),
        ("A_1", 1466.6064824824148, "square_millimeter", 1e-9),
        ("A_2", 306.3723083688089, "square_millimeter", 1e-9),
        ("A_3", 41.65320666380044, "square_millimeter", 1e-9),
        ("A_4", 1605.4315222628036, "square_millimeter", 1e-9),
        ("A_r", 1405.4315222628036, "square_millimeter", 1e-9),
        ("A_w", 200.0, "square_millimeter", 1e-9),
        # ("P_max", 4037.931455359164, "kPa", 1e-9),
    ]

    assert_problem_results(problem, expected_results)

    with capsys.disabled():
        print("")
        print(problem.beta)
        print(problem.d_1)
        print(problem.d_2)
        print(problem.L_4)
        print(problem.A_1)
        print(problem.A_2)
        print(problem.A_3)
        print(problem.A_w_b)
        print(problem.A_w_r)
        print(problem.A_w)
        print(problem.A_4)
        print(problem.A_r)
