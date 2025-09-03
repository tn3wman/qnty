"""
Demonstration of fluent typing with consolidated variables.

This file shows how the .pyi stub file provides rich IDE autocomplete
and type checking for the dynamically generated setter properties.
"""

from qnty.variables import Length, Pressure, Dimensionless
from qnty.expression import cond_expr


def asme_demo_option_1():
    # Known variables - using new simplified syntax
    P = Pressure(90, "psi", "Design Pressure")
    P.symbol = "P"
    D = Length(0.84, "inch", "Outside Diameter")
    D.symbol = "D"
    T_bar = Length(0.147, "inch", "Nominal Wall Thickness")
    T_bar.symbol = "T_bar"
    U_m = Dimensionless(0.125, "Mill Undertolerance")
    U_m.symbol = "U_m"
    c = Length(0.0, "inch", "Mechanical Allowances")
    c.symbol = "c"
    S = Pressure(20000, "psi", "Allowable Stress")
    S.symbol = "S"
    E = Dimensionless(0.8, "Quality Factor")
    E.symbol = "E"
    W = Dimensionless(1, "Weld Joint Strength Reduction Factor")
    W.symbol = "W"

    # Unknown variables - using new simplified syntax
    # Y = Dimensionless(0.4, "Y Coefficient", is_known=False)
    # Y.symbol = "Y"
    # T = Length(0.0, "inch", "Wall Thickness", is_known=False)
    # T.symbol = "T"
    # d = Length(0.0, "inch", "Inside Diameter", is_known=False)
    # d.symbol = "d"
    # t = Length(0.0, "inch", "Pressure Design Thickness", is_known=False)
    # t.symbol = "t"
    # t_m = Length(0.0, "inch", "Minimum Required Thickness", is_known=False)
    # t_m.symbol = "t_m"
    # P_max = Pressure(0.0, "psi", "Pressure, Maximum", is_known=False)

    # Equations
    T = T_bar * (1 - U_m)  # Wall Thickness
    d = D - 2 * T  # Inside Diameter
    # T_eqn = T.equals(T_bar * (1 - U_m))
    # d_eqn = d.equals(D - 2 * T)
    # t_eqn = t.equals((P * D) / (2 * (S * E * W + P * Y)))
    # t_m_eqn = t_m.equals(t + c)
    # P_max_eqn = P_max.equals((2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))

    print(T)
    print(d)

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


if __name__ == "__main__":
    print("=== ASME Demo ===")
    asme_demo_option_1()
    
