import math
from dataclasses import dataclass

import pytest

from qnty import Area, Dimensionless, Force, Length, Pressure, Problem, SecondMomentOfArea, Torque
from qnty.algebra import SelectOption, SelectVariable, abs_expr, cond_expr, equation, geq, gt, leq, ln, log10, match_expr, max_expr, sqrt
from qnty.core.dimension import Dimension
from qnty.core.quantity import Quantity
from qnty.problems.rules import add_rule


@dataclass(frozen=True)
class PressureType(SelectOption):
    """ASME flange types for bolt load calculations."""
    internal: str = "internal"
    external: str = "external"

@dataclass(frozen=True)
class GasketType(SelectOption):
    """ASME gasket types for bolt load calculations."""
    non_self_energized: str = "non_self_energized"
    self_energized: str = "self_energized"

@dataclass(frozen=True)
class FlangeType(SelectOption):
    """ASME flange types for bolt load calculations."""
    integral_welded_slip: str = "integral_welded_slip"
    loose_type_lap_with_hub: str = "loose_type_lap_with_hub"
    loose_type_lap_without_hub: str = "loose_type_lap_without_hub"
    reverse_integral_type: str = "reverse_integral_type"
    reverse_loose_type: str = "reverse_loose_type"


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


class FlangeDesign(Problem):
    name = "Flange Design Procedure per ASME BPVC Section VIII Division 2"
    description = "Calculate the minimum wall thickness of a flange under internal pressure."

    # Step 1. Determine the design pressure and temperature of the flange joint, and the external net-section axial force, F_A , and bending moment, M_E. If the pressure is negative, the absolute value of the pressure should be used in this procedure.
    P = Pressure("Design Pressure").set(100).pound_force_per_square_inch
    pressure_type = SelectVariable("Pressure Type", PressureType, PressureType.internal)
    F_A = Force("External Net-Section Axial Force F_A").set(0).pound_force
    M_E = Torque("External Net-Section Bending Moment M_E").set(0).foot_pound_force

    # Step 2. Determine the design bolt loads for operating condition, W_o , and the gasket seating condition, W_g , and corresponding actual bolt area, A_b , from 4.16.6.
    # Step 2.1. Determine the design pressure and temperature of the flange joint.
        # Pressure is already defined above as P
        # TODO: Add temperature handling
    # Step 2.2. Select a gasket and determine the gasket factors m and y from Table 4.16.1, or other sources. The selected gasket width should comply with the guidelines detailed in Table 4.16.2.
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)
    m = Dimensionless("Gasket Factor m").set(2).dimensionless
    y = Pressure("Gasket Factor y").set(2000).pound_force_per_square_inch

    # Step 2.3. Determine the width of the gasket, N, basic gasket seating width, b_0, the effective gasket seating width, b, and the location of the gasket reaction, G, based on the flange and gasket geometry, the information in Table 4.16.3 and Figure 4.16.8, and the equations shown below. Note that for lap joint flanges, G is equal to the midpoint of contact between the flange and the lap, see Figures 4.16.5 and 4.16.8.
    N = Length("Gasket Width N").set(0.25).inch

    b_0 = Length("Basic Gasket Seating Width b_0")
    b_0_cond = Length("Condition for b_0").set(6).millimeter

    b = Length("Effective Gasket Seating Width b")
    C_ul = Length("Conversion factor for length").set(1).inch

    G = Length("Location of Gasket Reaction G")
    G_c = Length("Outside Diameter of Gasket Contact Area").set(2.875).inch

    b_0_eqn = equation(b_0, N / 2)
    b_eqn = equation(
        b,
        cond_expr(
            leq(b_0, b_0_cond),
            b_0,
            0.5*C_ul*sqrt(b_0/C_ul)
        )
    )
    G_eqn = equation(
        G,
        cond_expr(
            leq(b_0, b_0_cond),
            G_c - N,
            G_c - 2*b
        )
    )

    # Step 2.4. Determine the design bolt load for the operating condition.
    W_o = Force("Design Bolt Load for Operating Condition W_o")
    pi = math.pi  # For use in equations
    W_o_eqn = equation(
        W_o,
        match_expr(
            gasket_type,
            GasketType.non_self_energized, 0.785 * G**2 * P + 2 * b * pi * G * m * P,  # Equation 4.16.4
            GasketType.self_energized, 0.785 * G**2 * P  # Equation 4.16.5
        )
    )

    # Step 2.5. Determine the design bolt load for the gasket seating condition.
    A_b = Area("Total cross-sectional area of all bolts")
    n_b = Dimensionless("Number of Bolts").set(6).dimensionless
    d_b = Length("Specified Bolt Diameter").set(0.4041).inch

    A_b_eqn = equation(A_b, n_b * pi * (d_b / 2)**2)

    S_bo = Pressure("Allowable stress from Annex 3-A for the bolt evaluated at the design temperature.").set(20000).pound_force_per_square_inch
    S_bg = Pressure("Allowable stress from Annex 3-A for the bolt evaluated at the gasket seating temperature").set(20000).pound_force_per_square_inch

    A_m = Area("Total minimum required cross-sectional area of bolts")

    W_gs = Force("design bolt load for the gasket seating condition")

    W_gs_eqn = equation(
        W_gs,
        match_expr(
            gasket_type,
            GasketType.non_self_energized, pi*b*G*y,
            GasketType.self_energized, 0
        )
    )

    A_m_eqn = equation(
        A_m,
        max_expr(
            (W_o + F_A + (4*M_E) / G) / S_bo,
            W_gs/S_bg
        )
    )

    W_g = Force("Design Bolt Load for Gasket Seating Condition W_g")
    W_g_eqn = equation(
        W_g,
        ((A_m + A_b) / 2) * S_bg
    )

    # A_b must be greater than or equal to A_m
    bolt_area_check = add_rule(
        geq(A_b, A_m),
        "Bolt area A_b is less than minimum required bolt area A_m.",
        warning_type="DESIGN_CHECK",
        severity="ERROR",
    )

    # Step 3. Determine an initial flange geometry, in addition to the information required to determine the bolt load, the following geometric parameters are required
    # (a) The flange bore, B (b) The bolt circle diameter, C (c) The outside diameter of the flange, A (d) The flange thickness, t (e) The thickness of the hub at the large end, g1 (f) The thickness of the hub at the small end, g0 (g) The hub length, h
    B = Length("Flange Bore").set(2.375).inch
    C = Length("Bolt Circle Diameter").set(4.5).inch
    A = Length("Outside Diameter of the Flange").set(5.5).inch
    t = Length("Flange Thickness").set(0.75).inch
    g_1 = Length("Thickness of the Hub at the Large End").set(0).inch
    g_0 = Length("Thickness of the Hub at the Small End").set(0).inch
    h = Length("Hub Length").set(0).inch

    # TODO: radius to be at least 0.25g1 but not less than 5 mm (0.1875 in.) if hubbed flange
    r_1 = Length("Fillet Radius at the Junction of the Hub and Flange").set(0).inch

    # Step 4. Determine the flange stress factors using the equations in Tables 4.16.4 and 4.16.5.
    K = Dimensionless("ratio of the flange outside diameter to the flange inside diameter")
    K_eq = equation(
        K,
        A / B
    )

    # expr_Y = (1/(K-1)) * (0.66845 + 5.71690 * ((K**2 * log10(K)) / (K**2 - 1)))
    # expr_Y_r = alpha_r * Y

    # expr_T = (K**2 * (1+8.55246*log10(K)) - 1) / ((1.04720 + 1.9448*K**2) * (K - 1))
    # expr_T_r = (Z+0.3)/(Z-0.3) * alpha_r * T

    # expr_U = (K**2 * (1 + 8.55246*log10(K)) - 1) / (1.36136 * (K**2 - 1) * (K - 1))
    # expr_U_r = alpha_r * U

    # expr_Z = (K**2 + 1) / (K**2 - 1)

    # expr_L = (t*e + 1)/T + (t**3/d)
    # expr_L_r = (t*e_r + 1)/T_r + (t**3/d_r)

    # expr_e_integral = F/h_o
    # expr_e_r_integral = F/h_or

    # expr_e_loose = F_L/h_o
    # expr_e_r_loose = F_L/h_or

    # expr_e_slip = F_S/h_o

    # expr_d_integral = (U * g_0**2 * h_o) / V
    # expr_d_r_integral = (U_r * g_0**2 * h_or) / V

    # expr_d_loose = (U * g_0**2 * h_o) / V_L
    # expr_d_r_loose = (U_r * g_0**2 * h_or) / V_L

    # expr_d_slip = (U * g_0**2 * h_o) / V_S

    # expr_h_o = sqrt(B*g_0)
    # expr_h_or = sqrt(A*g_0)

    # expr_X_g = g_1/g_0
    # expr_X_g2 = (g_2/g_0)
    # # TODO: If it is an intergral flange and g_1 = g_0, X_h = 2.0 otherwise X_h = h/h_o
    # expr_X_h = h/h_o
    # # TODO: If it is an intergral flange and g_1 = g_0, X_h = 2.0 otherwise X_h = h/h_or
    # expr_X_h_r = h/h_or


    # Step 5. Determine the flange forces.
    H_D = Force("total hydrostatic end force on the area inside of the flange")
    H = Force("total hydrostatic end force")
    H_T = Force("difference between the total hydrostatic end force and hydrostatic end force on the area inside the flange")
    H_G = Force("gasket load for the operating condition")

    H_D_eqn = equation(H_D, 0.785 * B**2 * P)
    H_eqn = equation(H, 0.785 * G**2 * P)
    H_T_eqn = equation(H_T, H - H_D)
    H_G_eqn = equation(H_G, W_o - H)


    # Step 6. Determine the flange moment for the operating condition using eq. (4.16.14) or eq. (4.16.15), as applicable. When specified by the user or the user's designated agent, the maximum bolt spacing (Bs ma x) and the bolt spacing correction factor (B sc) shall be applied in calculating the flange moment for internal pressure using the equations in Table 4.16.11. The flange moment Mo for the operating condition and flange moment M g for the gasket seating condition without correction for bolt spacing B s c = 1 is used for the calculation of the rigidity index in Step 10. In these equations, h D , hT , and hG are determined from Table 4.16.6. For integral and loose type flanges, the moment M oe is calculated using eq. (4.16.16) where I and Ip in this equation are determined from Table 4.16.7. For reverse type flanges, the procedure to determine M oe shall be agreed upon between the Designer and the Owner.
    M_o = Torque("flange design moment for the operating condition")
    M_oe = Torque("component of the flange design moment resulting from a net section bending moment and/or axial force")

    h_D = Length("moment arm for load H_D")
    h_T = Length("moment arm for load H_T")
    h_G = Length("moment arm for load H_G")

    flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

    h_D_eqn = equation(
        h_D,
        match_expr(
            flange_type,
            FlangeType.integral_welded_slip, (C-B-g_1) / 2,
            FlangeType.loose_type_lap_with_hub, (C-B) / 2,
            FlangeType.loose_type_lap_without_hub, (C-B) / 2,
            FlangeType.reverse_integral_type, (C+g_1-2*g_0-B) / 2,
            FlangeType.reverse_loose_type, (C-B) / 2,
        )
    )

    h_T_eqn = equation(
        h_T,
        match_expr(
            flange_type,
            FlangeType.integral_welded_slip, (1/2)*((C-B)/2 + h_G),
            FlangeType.loose_type_lap_with_hub, (C-G)/2,
            FlangeType.loose_type_lap_without_hub, (C-G)/2,
            FlangeType.reverse_integral_type, (1/2)*(C - (B+G)/2),
            FlangeType.reverse_loose_type, (1/2)*(C - (B+G)/2),
        )
    )

    h_G_eqn = equation(
        h_G,
        match_expr(
            flange_type,
            FlangeType.integral_welded_slip, (C-G)/2,
            FlangeType.loose_type_lap_with_hub, (C-G)/2,
            FlangeType.loose_type_lap_without_hub, (C-G)/2,
            FlangeType.reverse_integral_type, (C-G)/2,
            FlangeType.reverse_loose_type, (C-G)/2,
        )
    )

    a = Length("nominal bolt diameter").set(0.5).inch

    B_s = Length("bolt spacing")
    B_s_eqn = equation(
        B_s,
        2 * pi * (C / 2) / n_b
    )

    B_sc = Dimensionless("bolt spacing correction factor")
    B_sc_eqn = equation(
        B_sc,
        max_expr(1, sqrt(B_s/(2*a + t)))
    )

    F_sr = Dimensionless("moment factor used to design split rings").set(1.0).dimensionless # 1.0 for non-split rings

    M_o_eqn = equation(
        M_o,
        match_expr(
            pressure_type,
            PressureType.internal, abs_expr(((H_D*h_D + H_T*h_T + H_G*h_G) * B_sc + M_oe) * F_sr),
            PressureType.external, abs_expr((H_D*(h_D-h_G) + H_T*(h_T-h_G) + M_oe)  * F_sr)
        )
    )



    # I =  bending moment of inertia of the flange cross-section
    # I_p = polar moment of inertia of the flange cross-section
    I = SecondMomentOfArea("bending moment of inertia of the flange cross-section")
    I_p = SecondMomentOfArea("polar moment of inertia of the flange cross-section")

    I_eqn = equation(
        I,
        (B*t**3*ln(K)) / 24
    )

    A_R = Length("intermediate variable unknown description")
    A_R_eqn = equation(
        A_R,
        0.5*(A-B)
    )

    I_p_eqn = equation(
        I_p,
        A_R*t**3*((1/3) - 0.21*(t/A_R) * (1 - (1/12)*(t/A_R)**4))
    )

    # TODO: Complete match criteria
    T_eqn = equation(
        I,
        match_expr(
            flange_type,
            FlangeType.loose_type_lap_without_hub, (B*t**3*ln(K))/24,
        )
    )

    M_oe_eqn = equation(
        M_oe,
        4*M_E*(I/(0.3846*I_p + I)) * (h_D/(C-2*h_D)) + F_A*h_D
    )

    # Step 7. Determine the flange moment for the gasket seating condition using eq. (4.16.17) or eq. (4.16.18), as applicable.
    M_g = Torque("flange design moment for the gasket seating condition")
    M_g_eqn = equation(
        M_g,
        match_expr(
            pressure_type,
            PressureType.internal, (W_g*(C-G)*B_sc*F_sr) / 2,
            PressureType.external, W_g*h_G*F_sr
        )
    )

    # Step 8. Determine the flange stresses for the operating and gasket seating conditions using the equations in Table 4.16.8.
    Y = Dimensionless("flange stress factor")
    Y_eqn = equation(
        Y,
        (1/(K-1)) * (0.66845 + 5.71690 * ((K**2 * log10(K)) / (K**2 - 1)))
    )
    # TODO: Complete match criteria
    S_Ho = Pressure("flange hub stress operating")
    S_Ro = Pressure("flange radial stress operating")
    S_To = Pressure("flange tangential stress operating")
    S_Ho_eqn = equation(
        S_Ho,
        0,
    )
    S_Ro_eqn = equation(
        S_Ro,
        0,
    )
    S_To_eqn = equation(
        S_To,
        (Y*M_o) / (t**2*B)
    )

    # TODO: Complete match criteria
    S_Hg = Pressure("flange hub stress gasket seating")
    S_Rg = Pressure("flange radial stress gasket seating")
    S_Tg = Pressure("flange tangential stress gasket seating")
    S_Hg_eqn = equation(
        S_Hg,
        0,
    )
    S_Rg_eqn = equation(
        S_Rg,
        0,
    )
    S_Tg_eqn = equation(
        S_Tg,
        (Y*M_g) / (t**2*B)
    )

    # Step 9. Check the flange stress acceptance criteria. The two criteria shown below shall be evaluated. If the stress criteria are satisfied, go to Step 10. If the stress criteria are not satisfied, re-proportion the flange dimensions and go to Step 4.
        # (a) Allowable Normal Stress - The criteria to evaluate the normal stresses for the operating and gasket seating conditions are shown in Table 4.16.9.
    S_fo = Pressure("allowable stress from Annex 3-A for the flange evaluated at the design temperature").set(20000).pound_force_per_square_inch
    S_fg = Pressure("allowable stress from Annex 3-A for the flange evaluated at the gasket seating temperature").set(20000).pound_force_per_square_inch
    allowable_normal_stress_check_operating = add_rule(
        leq(S_To, S_fo),
        "Flange tangential stress for operating condition exceeds allowable stress S_fo.",
        warning_type="DESIGN_CHECK",
        severity="ERROR",
    )
    allowable_normal_stress_check_gasket_seating = add_rule(
        leq(S_Tg, S_fg),
        "Flange tangential stress for gasket seating condition exceeds allowable stress S_fg.",
        warning_type="DESIGN_CHECK",
        severity="ERROR",
    )
        # (b) Allowable Shear Stresses - In the case of loose type flanges with lap, as shown in Figure 4.16.5 where the gasket is so located that the lap is subjected to shear, the shearing stress shall not exceed 0.8*S_no or 0.8*S_ng, as applicable, for the material of the lap. In the case of welded flanges where the nozzle neck, vessel, or pipe wall extends near to the flange face and may form the gasket contact face, the shearing stress carried by the welds shall not exceed 0.8*S_no or 0.8*S_ng, as applicable. The shearing stress shall be calculated for both the operating and gasket seating load cases. Similar situations where flange parts are subjected to shearing stresses shall be checked using the same requirement.
    # TODO: How to calculating shearing stresses in these cases?

    # Step 10. Check the flange rigidity criterion in Table 4.16.10. If the flange rigidity criterion is satisfied, then the design is complete. If the flange rigidity criterion is not satisfied, then re-proportion the flange dimensions and go to Step 3. The flange moment M_o for the operating condition (see Step 6) and flange moment M_g for the gasket seating condition (see Step 7) without correction for bolt spacing B_sc = 1 is used for the calculation of the rigidity index.
    J_o = Dimensionless("rigidity index for the operating condition")
    J_g = Dimensionless("rigidity index for the gasket seating condition")
    # TODO: Secondary criteria for K_R to implement
    K_R = Dimensionless("rigidity index factor").set(0.2).dimensionless


    E_yo = Pressure("modulus of elasticity factor for operating condition").set(27900000).pound_force_per_square_inch
    E_yg = Pressure("modulus of elasticity factor for gasket seating condition").set(27900000).pound_force_per_square_inch

    # TODO: These need match criteria from Table 4.16.10, loose-type and reverse loose-type flange without a hub
    J_o_eqn = equation(
        J_o,
        (109.4*M_o) / (E_yo*t**3*K_R*(ln(K)))
    )

    J_g_eqn = equation(
        J_g,
        (109.4*M_g) / (E_yg*t**3*K_R*(ln(K)))
    )

def create_flange_design():
    return FlangeDesign()


def test_simple_problem(capsys):
    problem = create_flange_design()

    problem.m.set(2).dimensionless
    problem.y.set(2000).pound_force_per_square_inch

    problem.C.set(4.25).inch

    problem.t.set(0.75).inch
    problem.n_b.set(4).dimensionless

    problem.solve()



    with capsys.disabled():
        print("\nFinal Results:")

        # Bolt Loads
        print(problem.A_m.to_unit("inch2"))
        print(problem.A_b.to_unit("inch2"))

        print(f'W_o = {problem.W_o.to_unit("lbf")}')
        print(f'W_g = {problem.W_g.to_unit("lbf")}')

        # Flange moment arms
        print(f'h_D = {problem.h_D.to_unit("inch")}')
        print(f'h_T = {problem.h_T.to_unit("inch")}')
        print(f'h_G = {problem.h_G.to_unit("inch")}')

        # Flange Moments
        print(f'B_sc = {problem.B_sc}')
        print(f'M_o = {problem.M_o.to_unit("in*lbf")}')
        print(f'M_oe = {problem.M_oe.to_unit("in*lbf")}')
        print(f'M_g = {problem.M_g.to_unit("in*lbf")}')

        print(f'S_To = {problem.S_To.to_unit("psi")}')
        print(f'S_Tg = {problem.S_Tg.to_unit("psi")}')
        print(f'S_fo = {problem.S_fo.to_unit("psi")}')
        print(f'S_fg = {problem.S_fg.to_unit("psi")}')

        print(f'Y = {problem.Y}')

        print(f'J_o = {problem.J_o}')
        print(f'J_g = {problem.J_g}')


def test_example_problem(capsys):
    problem = create_flange_design()

    # Flange Type Integral type flange with hub
    problem.flange_type.set(FlangeType.integral_welded_slip)

    # Flange Design
    problem.A.set(22).inch
    problem.B.set(16).inch
    problem.t.set(1.75).inch
    problem.r_1.set(0.375).inch
    problem.g_0.set(0.75).inch
    problem.g_1.set(0.75).inch

    # Gasket Design
    problem.G_c.set(17.75).inch
    problem.N.set(0.75).inch
    problem.m.set(3).dimensionless
    problem.y.set(10000).pound_force_per_square_inch

    # Bolting Design
    problem.C.set(20.25).inch
    problem.n_b.set(16).dimensionless
    problem.a.set(1).inch
    problem.d_b.set(0.875).inch

    # Operating Conditions
    problem.P.set(100).pound_force_per_square_inch

    # Material Properties
    problem.S_fo.set(20000).pound_force_per_square_inch
    problem.S_fg.set(20000).pound_force_per_square_inch
    problem.E_yo.set(27900000).pound_force_per_square_inch
    problem.E_yg.set(27900000).pound_force_per_square_inch
    problem.S_bo.set(20000).pound_force_per_square_inch
    problem.S_bg.set(20000).pound_force_per_square_inch

    problem.solve()

    with capsys.disabled():
        print("\nFinal Results:")
        print(problem.g_0)
        print(problem.g_1)
        print(problem.B)
        print(problem.b_0.to_unit("inch"))
        print(problem.b.to_unit("inch"))

        # Bolt Loads
        print(f'H = {problem.H.to_unit("lbf")}')
        print(f'H_G = {problem.H_G.to_unit("lbf")}') # HP in example document
        print(f'H_D = {problem.H_D.to_unit("lbf")}')
        print(f'H_T = {problem.H_T.to_unit("lbf")}')
        print(f'W_o = {problem.W_o.to_unit("lbf")}') # Wm1 in example document
        print(f'W_gs = {problem.W_gs.to_unit("lbf")}') # Wm2 in example document
        print(f'A_m = {problem.A_m.to_unit("inch2")}')
        print(f'A_b = {problem.A_b.to_unit("inch2")}')

        # Flange Loads
        print(f'W_g = {problem.W_g.to_unit("lbf")}') # W in example document
        print(f'H_G = {problem.H_G.to_unit("lbf")}') # Mo in example document
        # TODO: Maybe add individual bolt load calculation?

        # Flange moment arms
        print(f'h_D = {problem.h_D.to_unit("inch")}')
        print(f'h_T = {problem.h_T.to_unit("inch")}')
        print(f'h_G = {problem.h_G.to_unit("inch")}')

        # Flange Moments
        print(f'B_sc = {problem.B_sc}')
        print(f'M_o = {problem.M_o.to_unit("in*lbf")}')
        print(f'M_oe = {problem.M_oe.to_unit("in*lbf")}')
        print(f'M_g = {problem.M_g.to_unit("in*lbf")}')

        print(problem.H_D.to_unit("lbf") * problem.h_D.to_unit("inch") + problem.H_T.to_unit("lbf") * problem.h_T.to_unit("inch") + problem.H_G.to_unit("lbf") * problem.h_G.to_unit("inch"))

        print(f'Y = {problem.Y}')