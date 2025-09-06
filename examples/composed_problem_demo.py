from qnty import Dimensionless, Length, Pressure
from qnty import cond_expr, min_expr
from qnty import Problem
from qnty.problems.rules import add_rule


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
    T = Length(0.0, "inch", "Wall Thickness", is_known=False)
    d = Length(0.0, "inch", "Inside Diameter", is_known=False)
    t = Length(0.0, "inch", "Pressure Design Thickness", is_known=False)
    t_m = Length(0.0, "inch", "Minimum Required Thickness", is_known=False)
    P_max = Pressure(0.0, "psi", "Pressure, Maximum", is_known=False)

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
    I_i = Dimensionless(1.0, "Intrados Correction Factor", is_known=False)
    I_e = Dimensionless(1.0, "Extrados Correction Factor", is_known=False)
    t_i = Length(1.0, "inch", "Design Thickness, Inside Bend", is_known=False)
    t_e = Length(1.0, "inch", "Design Thickness, Outside Bend", is_known=False)
    t_m_i = Length(1.0, "inch", "Minimum Required Thickness, Inside Bend", is_known=False)
    t_m_e = Length(1.0, "inch", "Minimum Required Thickness, Outside Bend", is_known=False)
    P_max_i = Pressure(1.0, "psi", "Maximum Pressure, Inside Bend", is_known=False)
    P_max_e = Pressure(1.0, "psi", "Maximum Pressure, Outside Bend", is_known=False)
    P_max = Pressure(1.0, "psi", "Maximum Allowable Pressure", is_known=False)

    # Equations
    I_i_eqn = I_i.equals((4*(R_1/s.D) - 1)/(4*(R_1/s.D) - 2))
    I_e_eqn = I_e.equals((4*(R_1/s.D) + 1)/(4*(R_1/s.D) + 2))

    t_i_eqn = t_i.equals(
        (s.P * s.D) / (2 * ((s.S * s.E * s.W/I_i) + s.P * s.Y))
    )
    t_e_eqn = t_e.equals(
        (s.P * s.D) / (2 * ((s.S * s.E * s.W/I_e) + s.P * s.Y))
    )

    t_m_i_eqn = t_m_i.equals(t_i + s.c)
    t_m_e_eqn = t_m_e.equals(t_e + s.c)

    P_max_i_eqn = P_max_i.equals(
        2*s.E*s.S*s.W*s.T/(I_i*(s.D - 2*s.Y*s.T))
    )

    P_max_e_eqn = P_max_e.equals(
        2*s.E*s.S*s.W*s.T/(I_e*(s.D - 2*s.Y*s.T))
    )

    P_max_eqn = P_max.equals(min_expr(P_max_i, P_max_e, s.P_max))

def create_pipe_bends():
    return PipeBends()


def test_composed_problem():
    problem = create_pipe_bends()

    problem.solve()

    print(problem.P_max)


if __name__ == "__main__":
    test_composed_problem()
