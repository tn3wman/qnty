from qnty import Dimensionless, Length, Pressure, Problem, cond_expr, min_expr
from qnty.problems.rules import add_rule


# Define a composed problem that includes another problem as a sub-component
class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    # Known variables - using new simplified syntax
    P = Pressure(90, "psi", "Design Pressure")
    D = Length(0.84, "inch", "Outside Diameter")
    T_bar = Length(0.147, "inch", "Nominal Wall Thickness")
    U_m = Dimensionless(0.125, "Mill Undertolerance")
    c = Length(0.0, "inch", "Mechanical Allowances")
    S = Pressure(20000, "psi", "Allowable Stress")
    E = Dimensionless(0.8, "Quality Factor")
    W = Dimensionless(1, "Weld Joint Strength Reduction Factor")

    # Unknown variables - using new simplified syntax
    Y = Dimensionless(0.4, "Y Coefficient")
    T = Length("Wall Thickness", "inch")
    d = Length("Inside Diameter", "inch")
    t = Length("Pressure Design Thickness", "inch")
    t_m = Length("Minimum Required Thickness", "inch")
    P_max = Pressure("Pressure, Maximum", "psi")

    # Equations
    T_eqn = T.equals(T_bar * (1 - U_m))
    d_eqn = d.equals(D - 2 * T)
    t_eqn = t.equals((P * D) / (2 * (S * E * W + P * Y)))
    t_m_eqn = t_m.equals(t + c)
    P_max_eqn = P_max.equals((2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))

    # ASME B31.3 Section 304.1.1 Y coefficient logic
    # Explicit handling of both conditions per ASME B31.3
    Y_eqn = Y.equals(
        cond_expr(
            t.lt(D / 6),
            Y,  # Table value for t < D/6
            cond_expr(
                t.geq(D / 6),
                (d + 2 * c) / (D + d + 2 * c),  # Calculated for t >= D/6
                Y,  # Fallback (should not be reached)
            ),
        )
    )

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


class PipeBends(Problem):
    s = create_straight_pipe_internal()

    s.Y.set(0.4).dimensionless

    R_1 = Length(5, "inch", "Bend Radius")
    I_i = Dimensionless("Intrados Correction Factor")
    I_e = Dimensionless("Extrados Correction Factor")
    t_i = Length("Design Thickness, Inside Bend", "inch")
    t_e = Length("Design Thickness, Outside Bend", "inch")
    t_m_i = Length("Minimum Required Thickness, Inside Bend", "inch")
    t_m_e = Length("Minimum Required Thickness, Outside Bend", "inch")
    P_max_i = Pressure("Maximum Pressure, Inside Bend", "psi")
    P_max_e = Pressure("Maximum Pressure, Outside Bend", "psi")
    P_max = Pressure("Maximum Allowable Pressure", "psi")

    # Equations
    I_i_eqn = I_i.equals((4 * (R_1 / s.D) - 1) / (4 * (R_1 / s.D) - 2))
    I_e_eqn = I_e.equals((4 * (R_1 / s.D) + 1) / (4 * (R_1 / s.D) + 2))

    t_i_eqn = t_i.equals((s.P * s.D) / (2 * ((s.S * s.E * s.W / I_i) + s.P * s.Y)))
    t_e_eqn = t_e.equals((s.P * s.D) / (2 * ((s.S * s.E * s.W / I_e) + s.P * s.Y)))

    t_m_i_eqn = t_m_i.equals(t_i + s.c)
    t_m_e_eqn = t_m_e.equals(t_e + s.c)

    P_max_i_eqn = P_max_i.equals(2 * s.E * s.S * s.W * s.T / (I_i * (s.D - 2 * s.Y * s.T)))

    P_max_e_eqn = P_max_e.equals(2 * s.E * s.S * s.W * s.T / (I_e * (s.D - 2 * s.Y * s.T)))

    P_max_eqn = P_max.equals(min_expr(P_max_i, P_max_e, s.P_max))


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
    print(problem.s.P.unit)
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
