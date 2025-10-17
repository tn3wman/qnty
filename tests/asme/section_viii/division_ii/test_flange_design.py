from encodings.punycode import T
import pytest
from dataclasses import dataclass
import math

from qnty import Dimensionless, Length, Pressure, Problem, Force
from qnty.core.quantity import Quantity
from qnty.core.dimension import Dimension
from qnty.algebra import SelectOption, SelectVariable, equation, geq, gt, cond_expr, leq, match_expr, sqrt, max_expr
from qnty.problems.rules import add_rule


@dataclass(frozen=True)
class GasketType(SelectOption):
    """ASME gasket types for bolt load calculations."""
    non_self_energized: str = "non_self_energized"
    self_energized: str = "self_energized"


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
    F_A = Force("External Net-Section Axial Force F_A").set(0).pound_force
    M_E = Torque("External Net-Section Bending Moment M_E").set(0).pound_force_inch

    # Step 2. Determine the design bolt loads for operating condition, W_o , and the gasket seating condition, W_g , and corresponding actual bolt area, A_b , from 4.16.6.
    # Step 2.1. Determine the design pressure and temperature of the flange joint.
        # Pressure is already defined above as P
        # TODO: Add temperature handling
    # Step 2. Select a gasket and determine the gasket factors m and y from Table 4.16.1, or other sources. The selected gasket width should comply with the guidelines detailed in Table 4.16.2.
    gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)
    m = Dimensionless("Gasket Factor m").set(2.0).dimensionless
    y = Pressure("Gasket Factor y").set(2000).pound_force_per_square_inch

    # Step 3. Determine the width of the gasket, N, basic gasket seating width, b_0, the effective gasket seating width, b, and the location of the gasket reaction, G, based on the flange and gasket geometry, the information in Table 4.16.3 and Figure 4.16.8, and the equations shown below. Note that for lap joint flanges, G is equal to the midpoint of contact between the flange and the lap, see Figures 4.16.5 and 4.16.8.
    N = Length("Gasket Width N").set(0.3).inch

    b_0 = Length("Basic Gasket Seating Width b_0")
    _b_0_cond = Length("Condition for b_0").set(6).millimeter

    b = Length("Effective Gasket Seating Width b")
    C_ul = Length("Conversion factor for length").set(1).inch

    G = Length("Location of Gasket Reaction G")
    G_c = Length("Outside Diameter of Gasket Contact Area").set(3).inch

    b_0_eqn = equation(b_0, N / 2)
    b_eqn = equation(
        b,
        cond_expr(
            leq(b_0, _b_0_cond),
            b_0,
            0.5*C_ul*sqrt(b_0/C_ul)
        )
    )
    G_eqn = equation(
        G,
        cond_expr(
            leq(b_0, _b_0_cond),
            G_c - N,
            G_c - 2*b
        )
    )

    # Step 4. Determine the design bolt load for the operating condition.
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

    # Step 5. Determine the design bolt load for the gasket seating condition.
    A_b = Length("Total cross-sectional area of all bolts")
    n_b = Dimensionless("Number of Bolts").set(6).dimensionless
    d_b = Length("Specified Bolt Diameter").set(0.4041).inch

    A_b_eqn = equation(A_b, n_b * pi * (d_b / 2)**2)

    A_m = Length("Total minimum required cross-sectional area of bolts")

    A_m_eqn = equation(
        A_m,
        max_expr(
            (W_o + F_A + (4*M_E) / G) / S_bo,
            W_gs/S_bg
        )
    )
    S_bg = Pressure("Bolt Allowable Stress for Gasket Seating Condition")
    W_g = Force("Design Bolt Load for Gasket Seating Condition W_g")


    W_g_eqn = equation(
        W_g,
        match_expr(
            gasket_type,
            GasketType.non_self_energized, 0.785 * G**2 * y + 2 * b * pi * G * m * y,  # Equation 4.16.6
            GasketType.self_energized, 0.785 * G**2 * y  # Equation 4.16.7
        )
    )

    # A_w_b_eqn = equation(
    #     A_w_b,
    #     cond_expr(
    #         leq(T_r, 0),
    #         2 * 0.5 * max_expr((t_c_b / 0.707), z_b) ** 2,
    #         cond_expr(
    #             leq(T_r, L_4),
    #             2 * 0.5 * max_expr((t_c_b / 0.707), z_b) ** 2,
    #             0
    #         )
    #     )
    # )

    # D = Length("Outside Diameter").set(0.84).inch
    # T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    # U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    # c = Length("Mechanical Allowances").set(0.0).inch
    # S = Pressure("Allowable Stress").set(20000).pound_force_per_square_inch
    # E = Dimensionless("Quality Factor").set(0.8).dimensionless
    # W = Dimensionless("Weld Joint Strength Reduction Factor").set(1).dimensionless

    # Y = Dimensionless("Y Coefficient").set(0.4).dimensionless

    # T = Length("Wall Thickness")
    # d = Length("Inside Diameter")
    # t = Length("Pressure Design Thickness")
    # t_m = Length("Minimum Required Thickness")
    # P_max = Pressure("Pressure, Maximum")

    # # Equations
    # T_eqn = equation(T, T_bar * (1 - U_m))
    # d_eqn = equation(d, D - 2 * T)
    # t_eqn = equation(t, (P * D) / (2 * (S * E * W + P * Y)))
    # t_m_eqn = equation(t_m, t + c)
    # P_max_eqn = equation(P_max, (2 * (T - c) * S * E * W) / (D - 2 * (T - c) * Y))

    # # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    # thick_wall_check = add_rule(
    #     geq(t, D / 6),
    #     "Thick wall condition detected (t >= D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
    #     warning_type="CODE_COMPLIANCE",
    #     severity="WARNING",
    # )

    # pressure_ratio_check = add_rule(
    #     gt(P, (S * E) * 0.385),
    #     "High pressure ratio detected (P/(S*E) > 0.385). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
    #     warning_type="CODE_COMPLIANCE",
    #     severity="WARNING",
    # )


def create_flange_design():
    return FlangeDesign()


# def test_simple_problem():
#     problem = create_flange_design()

#     problem.solve()

#     expected_results = [
#         # Known variables (exact)
#         ("P", 90, "psi", None),
#         ("D", 0.84, "in", None),
#         ("T_bar", 0.147, "in", None),
#         ("U_m", 0.125, "dimensionless", None),
#         ("c", 0.0, "in", None),
#         ("S", 20000, "psi", None),
#         ("E", 0.8, "dimensionless", None),
#         ("W", 1, "dimensionless", None),
#         ("Y", 0.4, "dimensionless", None),
#         # Calculated variables (with tolerance)
#         ("T", 0.128625, "in", 1e-9),
#         ("d", 0.58275, "in", 1e-9),
#         ("t", 0.002357196308306311, "in", 1e-9),
#         ("t_m", 0.002357196308306311, "in", 1e-9),
#         ("P_max", 5584.045584045583, "psi", 1e-9),
#     ]

#     assert_problem_results(problem, expected_results)

#     problem.D.set(1.315).inch
#     problem.T_bar.set(0.179).inch

#     problem.solve()

#     expected_results = [
#         # Known variables (exact)
#         ("P", 90, "psi", None),
#         ("D", 1.315, "in", None),
#         ("T_bar", 0.179, "in", None),
#         ("U_m", 0.125, "dimensionless", None),
#         ("c", 0.0, "in", None),
#         ("S", 20000, "psi", None),
#         ("E", 0.8, "dimensionless", None),
#         ("W", 1, "dimensionless", None),
#         ("Y", 0.4, "dimensionless", None),
#         # Calculated variables (with tolerance)
#         ("T", 0.156625, "in", 1e-9),
#         ("d", 1.00175, "in", 1e-9),
#         ("t", 0.003690134696931903, "in", 1e-9),
#         ("t_m", 0.003690134696931903, "in", 1e-9),
#         ("P_max", 4212.826763049508, "psi", 1e-9),
#     ]

#     assert_problem_results(problem, expected_results)


# def test_output_unit_preservation():
#     """Test that _output_unit field is preserved during class-level variable extraction."""

#     class TestProblem(Problem):
#         # Variable with output_unit
#         T = Length("Wall Thickness").output_unit("inch")
#         # Variable without output_unit (should preserve None)
#         L = Length("Length")
#         # Variable with both preferred and output_unit
#         P = Pressure("Pressure").set(150).psi.output_unit("Pa")

#     # Create the problem instance
#     problem = TestProblem()

#     # Test variable with output_unit
#     T_var = problem.variables.get("T")
#     assert T_var is not None
#     assert hasattr(T_var, "_output_unit")
#     assert T_var._output_unit is not None
#     assert T_var._output_unit.symbol == "in"
#     assert T_var.name == "Wall Thickness"
#     assert T_var._symbol == "T"

#     # Test variable without output_unit
#     L_var = problem.variables.get("L")
#     assert L_var is not None
#     assert hasattr(L_var, "_output_unit")
#     assert L_var._output_unit is None  # Should be None for variables without output_unit
#     assert L_var.name == "Length"

#     # Test variable with both preferred and output_unit
#     P_var = problem.variables.get("P")
#     assert P_var is not None
#     assert hasattr(P_var, "_output_unit")
#     assert P_var._output_unit is not None
#     assert P_var._output_unit.symbol == "Pa"
#     assert P_var.preferred is not None
#     assert P_var.preferred.symbol == "psi"
#     assert P_var.value is not None  # Should have a value from .set(150).psi

#     # Test instance attributes also have correct _output_unit
#     T_instance = getattr(problem, "T", None)
#     assert T_instance is not None
#     assert hasattr(T_instance, "_output_unit")
#     assert T_instance._output_unit is not None
#     assert T_instance._output_unit.symbol == "in"

#     # Test display behavior: output_unit takes precedence over preferred for display
#     P_instance = getattr(problem, "P", None)
#     assert P_instance is not None
#     P_str = str(P_instance)
#     # Should display in Pa (output_unit), not psi (preferred)
#     assert "Pa" in P_str
