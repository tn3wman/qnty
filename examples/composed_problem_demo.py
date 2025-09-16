from qnty import Dimensionless, Length, Pressure, Problem, cond_expr, min_expr
from qnty.algebra import equation, geq, gt, lt
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


def test_composed_problem():
    problem = create_pipe_bends()

    problem.solve()

    print(problem.P_max)

    problem.s.D.set(1).inch

    problem.solve()

    print(problem.P_max)

    problem.s.D.set(2).inch

    problem.solve()

    print(problem.P_max)

    # Using new direct access properties instead of problem.s.P.quantity.value
    print(problem.s.P.symbol)
    print(problem.s.P.value)
    print(problem.s.P.name)

    print(problem.s.D)
    print(problem.s.T_bar)
    print(problem.s.U_m)
    print(problem.s.c)
    print(problem.s.S)
    print(problem.s.E)
    print(problem.s.W)
    print(problem.s.Y)
    print(problem.s.T)
    print(problem.s.d)
    print(problem.s.t)
    print(problem.s.t_m)
    print(problem.s.P_max)

    print(problem.I_i)
    print(problem.I_i.value)
    print(problem.I_e)
    print(problem.t_i)
    print(problem.t_e)
    print(problem.t_m_i)
    print(problem.t_m_e)
    print(problem.P_max_i)
    print(problem.P_max_e)


if __name__ == "__main__":
    test_composed_problem()
