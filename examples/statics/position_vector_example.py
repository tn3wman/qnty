from qnty.problems.position_vector import PositionVectorProblem
from qnty.spatial import create_point_cartesian
from qnty.spatial.vector_between import VectorBetween


class YourProblem(PositionVectorProblem):
    A = create_point_cartesian(x=4, y=2, z=0, unit="m")
    B = create_point_cartesian(x=0, y=0, z=..., unit="m")
    r_AB = VectorBetween(from_point=A, to_point=B, magnitude=8, unit="m")

def create_problem():
    return YourProblem()

if __name__ == "__main__":
    prob = create_problem()
    prob.solve()

    print("=== Initial solve (z unknown) ===")
    print(f"Point A: {prob.A.to_unit('ft')}")
    print(f"Point B: {prob.B}")
    print(f"Vector r_AB: {prob.r_AB}")

    # # Now dynamically change what's known/unknown
    # # Lock z to its solved value, unlock y to solve for it
    # prob.B.set_coordinate('z', 6.0)   # Lock z to 6m
    # prob.B.unlock_coordinate('y')      # Make y unknown

    # # Reset and re-solve
    # prob.reset()
    # prob.solve()

    # print("\n=== Re-solve (y unknown, z=6m) ===")
    # print(f"Point A: {prob.A.to_unit('ft')}")
    # print(f"Point B: {prob.B}")
    # print(f"Vector r_AB: {prob.r_AB}")
