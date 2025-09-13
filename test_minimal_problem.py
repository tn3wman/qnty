from qnty import Dimensionless, Length, Problem
from qnty.algebra import equation

class MinimalProblem(Problem):
    name = "Minimal Test Problem"
    description = "Test basic equation solving"

    # Known variables
    T_bar = Length("Nominal Wall Thickness").set(0.147).inch
    U_m = Dimensionless("Mill Undertolerance").set(0.125).dimensionless

    # Unknown variable
    T = Length("Wall Thickness")

    # Simple equation: T = T_bar * (1 - U_m)
    T_eqn = equation(T, T_bar * (1 - U_m))

def test_minimal():
    problem = MinimalProblem()

    print("Variables:")
    for name, var in problem.variables.items():
        print(f"  {name}: known={var.is_known}, value={var.value}")

    print(f"\nEquations: {len(problem.equations)}")
    for eq in problem.equations:
        print(f"  {eq}")

    try:
        problem.solve()
        print("\n✅ Solving successful!")
        print(f"T: {problem.T}")
    except Exception as e:
        print(f"\n❌ Solving failed: {e}")

if __name__ == "__main__":
    test_minimal()