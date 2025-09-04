from qnty import Dimensionless, Length, Pressure
from qnty.expressions import cond_expr
from qnty.problem.problem import Problem
from qnty.validation import validate

 
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
    thick_wall_check = validate(
        t.geq(D / 6),
        "Thick wall condition detected (t >= D/6). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )

    pressure_ratio_check = validate(
        P.gt((S * E) * 0.385),
        "High pressure ratio detected (P/(S*E) > 0.385). Per ASME B31.3, calculation requires special consideration of theory of failure, effects of fatigue, and thermal stress.",
        warning_type="CODE_COMPLIANCE",
        severity="WARNING",
    )

def create_test_straight_pipe_internal():
    return StraightPipeInternal()

def test_straight_pipe_internal():
    problem = create_test_straight_pipe_internal()
    
    # Debug: Check equation types at class level
    print("Class-level equations:")
    print(f"  T_eqn type: {type(StraightPipeInternal.T_eqn)}")
    print(f"  T_eqn value: {StraightPipeInternal.T_eqn}")
    
    # Debug: Test isinstance check directly
    from qnty.equations.equation import Equation
    print(f"  isinstance check: {isinstance(StraightPipeInternal.T_eqn, Equation)}")
    
    # Debug: Check all class attributes with their types
    print("\nAll class attributes:")
    for attr_name in dir(StraightPipeInternal):
        if not attr_name.startswith('_'):
            attr_value = getattr(StraightPipeInternal, attr_name)
            print(f"  {attr_name}: {type(attr_value)} = {attr_value}")
    
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
        for _name, var in problem.variables.items():
            print(f"  {var.symbol}: known={var.is_known}, value={var.quantity}")

if __name__ == "__main__":
    test_straight_pipe_internal()
