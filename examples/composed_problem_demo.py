from qnty import Dimensionless, Length, Pressure, Problem, cond_expr, min_expr, sin, Area, AnglePlane, max_expr
from qnty.algebra import equation, geq, gt, lt, leq
from qnty.problems.rules import add_rule


# Define a composed problem that includes another problem as a sub-component
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

    # ASME B31.3 Section 304.1.1 Y coefficient logic
    # Explicit handling of both conditions per ASME B31.3
    Y_eqn = equation(Y,
        cond_expr(
            lt(t, D / 6),
            Y,  # Table value for t < D/6
            cond_expr(
                geq(t, D / 6),
                (d + 2 * c) / (D + d + 2 * c),  # Calculated for t >= D/6
                Y,  # Fallback (should not be reached)
            ),
        )
    )

    # # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
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


class PipeBends(Problem):
    s = create_straight_pipe_internal()

    s.Y.set(0.4).dimensionless

    R_1 = Length("Bend Radius").set(5).inch
    I_i = Dimensionless("Intrados Correction Factor")
    I_e = Dimensionless("Extrados Correction Factor")
    t_i = Length("Design Thickness, Inside Bend")
    t_e = Length("Design Thickness, Outside Bend")
    t_m_i = Length("Minimum Required Thickness, Inside Bend")
    t_m_e = Length("Minimum Required Thickness, Outside Bend")
    P_max_i = Pressure("Maximum Pressure, Inside Bend")
    P_max_e = Pressure("Maximum Pressure, Outside Bend")
    P_max = Pressure("Maximum Allowable Pressure")

    # Equations
    I_i_eqn = equation(I_i, (4 * (R_1 / s.D) - 1) / (4 * (R_1 / s.D) - 2))
    I_e_eqn = equation(I_e, (4 * (R_1 / s.D) + 1) / (4 * (R_1 / s.D) + 2))

    t_i_eqn = equation(t_i, (s.P * s.D) / (2 * ((s.S * s.E * s.W / I_i) + s.P * s.Y)))
    t_e_eqn = equation(t_e, (s.P * s.D) / (2 * ((s.S * s.E * s.W / I_e) + s.P * s.Y)))

    t_m_i_eqn = equation(t_m_i, t_i + s.c)
    t_m_e_eqn = equation(t_m_e, t_e + s.c)

    P_max_i_eqn = equation(P_max_i, 2 * s.E * s.S * s.W * s.T / (I_i * (s.D - 2 * s.Y * s.T)))

    P_max_e_eqn = equation(P_max_e, 2 * s.E * s.S * s.W * s.T / (I_e * (s.D - 2 * s.Y * s.T)))

    P_max_eqn = equation(P_max, min_expr(P_max_i, P_max_e, s.P_max))


def create_pipe_bends():
    return PipeBends()

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

    A_w_b_eqn = equation(A_w_b, cond_expr(leq(T_r, 0), 2 * 0.5 * max_expr((t_c_b / 0.707), z_b) ** 2, cond_expr(leq(T_r, L_4), 2 * 0.5 * max_expr((t_c_b / 0.707), z_b) ** 2, 0)))

    A_w_r_eqn = equation(A_w_r, cond_expr(leq(D_r, 2 * d_2 - max_expr((t_c_r / 0.707), z_r)), 2 * 0.5 * max_expr((t_c_r / 0.707), z_r) ** 2, 0))

    A_w_eqn = equation(A_w, A_w_b + A_w_r)

    # Calculation for total area
    A_1_eqn = equation(A_1, header.t * d_1 * (2 - sin(beta)))
    A_2_eqn = equation(A_2, (2 * d_2 - d_1) * (header.T - header.t - header.c))
    A_3_eqn = equation(A_3, (2 * L_4 * (branch.T - branch.t - branch.c) / sin(beta)) * min_expr(1, branch.S / header.S))
    A_4_eqn = equation(A_4, A_r + A_w)


def create_welded_branch_connection():
    """Factory function to create a BranchReinforcement engineering problem instance."""
    return WeldedBranchConnection()


def test_composed_problem():
    # problem = create_pipe_bends()
    p = create_welded_branch_connection()

    p.header.D.set(4.5).inch
    p.header.T_bar.set(0.120).inch
    p.branch.D.set(1.5).inch
    p.branch.T_bar.set(0.147).inch

    p.solve()

    print(p.header.P_max)



if __name__ == "__main__":
    test_composed_problem()
