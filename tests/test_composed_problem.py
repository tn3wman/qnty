import pytest

import qnty as qt
from qnty.problems.rules import add_rule


def assert_qty_close(actual_var, expected_value, expected_unit, rel_tol=1e-9):
    """Helper function to assert variable quantity is close to expected value with relative tolerance."""
    # expected_qty = Qty(expected_value, expected_unit)
    if expected_unit == 'inch':
        expected_unit = 'in'
    if expected_unit == 'square_millimeter':
        expected_unit = '$\\mathrm{mm}^{2}$'
    assert pytest.approx(expected_value, rel=rel_tol) == actual_var.value
    assert expected_unit == actual_var.unit



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
        if expected_unit != '':
            actual_var = actual_var.to_unit(expected_unit)
        
        assert_qty_close(actual_var, expected_value, expected_unit, tolerance)


class StraightPipeInternal(qt.Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    # Known variables - using new simplified syntax
    P = qt.Pressure(90, "psi", "Design Pressure")
    D = qt.Length(0.84, "inch", "Outside Diameter")
    T_bar = qt.Length(0.147, "inch", "Nominal Wall Thickness")
    U_m = qt.Dimensionless(0.125, "Mill Undertolerance")
    c = qt.Length(0.0, "inch", "Mechanical Allowances")
    S = qt.Pressure(20000, "psi", "Allowable Stress")
    E = qt.Dimensionless(0.8, "Quality Factor")
    W = qt.Dimensionless(1, "Weld Joint Strength Reduction Factor")

    # Unknown variables - using new simplified syntax
    Y = qt.Dimensionless(0.4, "Y Coefficient")
    # T = qt.Length(0.0, "inch", "Wall Thickness")
    # d = qt.Length(0.0, "inch", "Inside Diameter")
    # t = qt.Length(0.0, "inch", "Pressure Design Thickness")
    # t_m = qt.Length(0.0, "inch", "Minimum Required Thickness")
    # P_max = qt.Pressure(0.0, "psi", "Pressure, Maximum")
    T = qt.Length("Wall Thickness", "inch")
    d = qt.Length("Inside Diameter", "inch")
    t = qt.Length("Pressure Design Thickness", "inch")
    t_m = qt.Length("Minimum Required Thickness", "inch")
    P_max = qt.Pressure("Pressure, Maximum", "psi")

    # Equations
    T_eqn = T.equals(T_bar * (1 - U_m))
    d_eqn = d.equals(D - 2 * T)
    t_eqn = t.equals((P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = t_m.equals(t + c)
    P_max_eqn = P_max.equals((2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))

    # ASME B31.3 Section 304.1.1 Y coefficient logic
    # Explicit handling of both conditions per ASME B31.3
    Y_eqn = Y.equals(
        qt.cond_expr(
            t.lt(D / 6),
            Y,  # Table value for t < D/6
            qt.cond_expr(
                t.geq(D / 6),
                (d + 2 * c) / (D + d + 2 * c),  # Calculated for t >= D/6
                Y,  # Fallback (should not be reached)
            ),
        )
    )

    # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    thick_wall_check = add_rule(
        t.geq(D / 6),
        "Thick wall condition detected (t ≥ D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
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


class WeldedBranchConnection(qt.Problem):
    """
    Composed Branch Reinforcement using sub-problems.
    Demonstrates the new composition pattern with clean syntax.
    """

    name = "Composed Branch Connection Analysis (ASME B31.3)"
    description = "Reinforcement area calculations using composed sub-problems per ASME B31.3."

    # System-level variables
    P = qt.Pressure(90, "psi", "Design Pressure")
    # TODO: Fix how angle calculations are handled
    beta = qt.AnglePlane(1.5708, "degree", "Branch Angle")

    # Sub-problems - automatically integrated with namespace prefixes
    header = create_straight_pipe_internal()
    branch = create_straight_pipe_internal()

    # Share system pressure with sub-problems
    header.P.mark_unknown()
    branch.P.mark_unknown()
    header_P_eqn = header.P.equals(P)
    branch_P_eqn = branch.P.equals(P)

    # Set default values for header
    header.D.set(2.375).inch
    header.T_bar.set(0.218).inch
    header.U_m.set(0.125).dimensionless
    header.c.set(0.0).inch
    header.S.set(20000).psi
    header.E.set(1).dimensionless
    header.W.set(1).dimensionless
    header.Y.set(0.4).dimensionless

    # Set default values for branch
    branch.D.set(1.315).inch
    branch.T_bar.set(0.179).inch
    branch.U_m.set(0.125).dimensionless
    branch.c.set(0.0).inch
    branch.S.set(20000).psi
    branch.E.set(1).dimensionless
    branch.W.set(1).dimensionless
    branch.Y.set(0.4).dimensionless

    # # Known variables for reinforcement pad
    D_r = qt.Length("Outside Diameter, Reinforcement", "inch", 0)
    T_bar_r = qt.Length("Thickness, Reinforcement", "inch", 0)
    U_m_r = qt.Dimensionless("Mill Undertolerance, Reinforcement", 0)
    S_r = qt.Pressure("Allowable Stress, Reinforcement", "psi", 0)

    # # Unknown variables for reinforcement pad
    A_r = qt.Area("Reinforcement Ring Area", "square_inch")
    T_r = qt.Length("Nominal Thickness, Reinforcement", "inch")
    # # Known variables for welds
    z_b = qt.Length("Weld Leg, Branch", "inch", 0)
    z_r = qt.Length("Weld Leg, Reinforcement", "inch", 0    )
    t_c_max = qt.Length("Weld Throat, Max", "mm", 6)

    # # Unknown variables for welds
    t_c_b = qt.Length("Weld Throat, Branch", "inch")
    t_c_r = qt.Length("Weld Throat, Reinforcement", "inch")
    A_w_b = qt.Area("Weld Area, Branch", "square_inch")
    A_w_r = qt.Area("Weld Area, Reinforcement", "square_inch")
    A_w = qt.Area("Weld Area", "square_inch")

    # # Unknown variables for branch reinforcement zone
    d_1 = qt.Length("Effective Length Removed", "inch")
    d_2 = qt.Length("Reinforcement Zone Radius", "inch")
    L_4 = qt.Length("Reinforcement Zone Height", "inch")

    # # Unknown variables for required and available area
    A_1 = qt.Area("Reinforcement Area Required", "square_inch")
    A_2 = qt.Area("Reinforcement Area Run", "square_inch")
    A_3 = qt.Area("Reinforcement Area Branch", "square_inch")
    A_4 = qt.Area("Reinforcement Area Total", "square_inch")

    # Calculations for branch reinforcement zone
    d_1_eqn = d_1.equals((branch.D - 2 * (branch.T - branch.c)) / qt.sin(beta))
    d_2_eqn = d_2.equals(qt.max_expr(d_1, (branch.T - branch.c) + (header.T - header.c) + d_1 / 2))
    L_4_eqn = L_4.equals(qt.min_expr(2.5 * (header.T - header.c), 2.5 * (branch.T - branch.c) + T_bar_r))

    # Calculations for reinforcement pad
    A_r_eqn = A_r.equals(qt.min_expr(T_r, L_4) * (qt.min_expr(D_r, 2 * d_2) - branch.D / qt.sin(beta)) * qt.min_expr(1, S_r / header.S))

    T_r_eqn = T_r.equals(T_bar_r * (1 - U_m_r))

    # Calculation for weld area
    t_c_b_eqn = t_c_b.equals(qt.min_expr(0.7 * branch.T_bar, t_c_max))
    t_c_r_eqn = t_c_r.equals(0.5 * T_bar_r)

    A_w_b_eqn = A_w_b.equals(
        qt.cond_expr(
            T_r.leq(0), # T_r doesn't exist, no reinforcement interference
            2 * 0.5 * qt.max_expr((t_c_b / 0.707), z_b) ** 2, # Calculate weld area
            qt.cond_expr(
                T_r.leq(L_4), # T_r + weld leg fits within L_4
                2 * 0.5 * qt.max_expr((t_c_b / 0.707), z_b) ** 2, # Calculate weld area
                0, # T_r + weld leg exceeds L_4, no weld area
            ),
        )
    )

    A_w_r_eqn = A_w_r.equals(
        qt.cond_expr(
            D_r.leq(2 * d_2 - qt.max_expr((t_c_r / 0.707), z_r)),
            2 * 0.5 * qt.max_expr((t_c_r / 0.707), z_r) ** 2,
            0
        )
    )

    A_w_eqn = A_w.equals(A_w_b + A_w_r)

    # Calculation for total area
    A_1_eqn = A_1.equals(header.t * d_1 * (2 - qt.sin(beta)))
    A_2_eqn = A_2.equals((2 * d_2 - d_1) * (header.T - header.t - header.c))
    A_3_eqn = A_3.equals((2 * L_4 * (branch.T - branch.t - branch.c) / qt.sin(beta)) * qt.min_expr(1, branch.S / header.S))
    A_4_eqn = A_4.equals(A_r + A_w)


def create_welded_branch_connection():
    """Factory function to create a BranchReinforcement engineering problem instance."""
    return WeldedBranchConnection()


def test_branch_reinforcement_h301(capsys):
    problem = create_welded_branch_connection()

    # For system
    problem.P.set(2068).kPa

    # For header
    problem.header.D.set(219.1).mm
    problem.header.T_bar.set(8.18).mm
    problem.header.U_m.set(0.125).dimensionless
    problem.header.c.set(2.5).mm
    problem.header.S.set(110).MPa
    problem.header.E.set(1).dimensionless
    problem.header.W.set(1).dimensionless
    problem.header.Y.set(0.4).dimensionless

    # For run
    problem.branch.D.set(114.3).mm
    problem.branch.T_bar.set(6.02).mm
    problem.branch.U_m.set(0.125).dimensionless
    problem.branch.c.set(2.5).mm
    problem.branch.S.set(110).MPa
    problem.branch.E.set(1).dimensionless
    problem.branch.W.set(1).dimensionless
    problem.branch.Y.set(0.4).dimensionless

    problem.solve()

    # problem.A_4.to_unit.square_millimeter

    assert problem.is_solved

    expected_results = [
        ("d_1", 108.765, "mm", 1e-9),
        ("d_2", 108.765, "mm", 1e-9),
        ("L_4", 6.91875, "mm", 1e-9),
        ("A_1", 222.33391704383038, "square_millimeter", 1e-9),
        ("A_2", 284.23907045616954, "square_millimeter", 1e-9),
        ("A_3", 23.53896202060505, "square_millimeter", 1e-9),
        ("A_4", 35.52632094892658, "square_millimeter", 1e-9),
    ]

    assert_problem_results(problem, expected_results)

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
