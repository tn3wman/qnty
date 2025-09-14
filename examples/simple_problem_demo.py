from qnty import Dimensionless, Length, Pressure, Problem, cond_expr
from qnty.algebra.nodes import Expression
from qnty.algebra import equation
from qnty.problems.rules import add_rule


class StraightPipeInternal(Problem):
    name = "Pressure Design of a Straight Pipe Under Internal Pressure"
    description = "Calculate the minimum wall thickness of a straight pipe under internal pressure."

    # Known variables - using new simplified syntax
    # P = Pressure(90, "psi", "Design Pressure")
    # D = Length(0.84, "inch", "Outside Diameter")
    # T_bar = Length(0.147, "inch", "Nominal Wall Thickness")
    # U_m = Dimensionless(0.125, "Mill Undertolerance")
    # c = Length(0.0, "inch", "Mechanical Allowances")
    # S = Pressure(20000, "psi", "Allowable Stress")
    # E = Dimensionless(0.8, "Quality Factor")
    # W = Dimensionless(1, "Weld Joint Strength Reduction Factor")
    P = Pressure("Design Pressure").set(90).psi
    D = Length("Outside Diameter").set(0.84).inch
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless
    c = Length("Mechanical Allowances").set(0.0).inch
    S = Pressure("Allowable Stress").set(20000).psi
    E = Dimensionless("Quality Factor").set(0.8).dimensionless
    W = Dimensionless("Weld Joint Strength Reduction Factor").set(1).dimensionless

    Y = Dimensionless("Y Coefficient").set(0.4).dimensionless  # Default value; will be updated by equation


    # Unknown variables - using new simplified syntax
    # Y = Dimensionless(0.4, "Y Coefficient")

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


    # # ASME B31.3 Code Compliance Checks - defined at class level like variables and equations
    # TODO: Work on the validation system later
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
    
    # Debug: Check equation types at class level
    print("Class-level equations:")
    print(f"  T_eqn type: {type(StraightPipeInternal.T_eqn)}")
    print(f"  T_eqn value: {StraightPipeInternal.T_eqn}")
    
    print("✅ DelayedExpression system successfully resolving equations!")

    # Debug: Print variable info
    print("\nVariables:")
    for name, var in problem.variables.items():
        print(f"  {name} (symbol: {var.symbol}): known={var.is_known}, value={var.quantity}")
    
    print(f"\nEquations: {len(problem.equations)}")
    for eq in problem.equations:
        print(f"  {eq}")
    
    try:
        problem.solve()
        print("\nSolving successful!")
        print(f"P_max: {problem.P_max}")
        
        # Test the validation system
        warnings = problem.validate()
        print(f"\nValidation warnings: {len(warnings)}")
        for warning in warnings:
            print(f"  {warning}")
        
    except Exception as e:
        print(f"\nSolving failed: {e}")
        # Still print some results for debugging
        print("Final variable states:")
        for _, var in problem.variables.items():
            print(f"  {var.symbol}: known={var.is_known}, value={var.quantity}")

    # Try changing the value and re-solving
    print("\nModifying known variable D to 1 inch and re-solving...")
    problem.D.set(1, "inch")
    problem.solve()
    print(f"P_max after modification: {problem.P_max}")

if __name__ == "__main__":
    test_simple_problem()
