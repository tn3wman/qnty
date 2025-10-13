from pathlib import Path

from qnty.extensions.reporting import generate_report
from qnty.problems import problem
from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.force_vector import ForceVector


def test_problem_2_1():
    class ProblemC2P1(VectorEquilibriumProblem):
        name = "Problem 1"
        description = """
        If theta=60 degrees and F=450 N, determine the magnitude of the resultant force and its direction, measured counterclockwise from the positive x axis.
        """

        # Define known forces
        F_1 = ForceVector(
            magnitude=450,
            angle=60,
            unit="N",
            name="F_1",
            description="Force 1"
        )

        F_2 = ForceVector(
            magnitude=700,
            angle=195,
            unit="N",
            name="F_2",
            description="Force 2"
        )

        # Define unknown resultant
        F_R = ForceVector.unknown("F_R", is_resultant=True)

    problem_instance = ProblemC2P1()
    solution = problem_instance.solve()
    F_1_solution = solution["F_1"]
    F_2_solution = solution["F_2"]
    F_R_solution = solution["F_R"]

    F_1_expected = ForceVector(
        magnitude=450,
        angle=60,
        unit="N",
        name="F_1",
        description="Force 1"
    )

    F_2_expected = ForceVector(
        magnitude=700,
        angle=195,
        unit="N",
        name="F_2",
        description="Force 2"
    )

    F_R_expected = ForceVector(
        magnitude=497.014,
        angle=155.2,
        unit="N",
        name="F_R",
        description="Resultant Force"
    )

    assert F_1_solution == F_1_expected
    assert F_2_solution == F_2_expected
    assert F_R_solution == F_R_expected

def test_problem_2_2():
    class ProblemC2P2(VectorEquilibriumProblem):
        name = "Problem 2"
        description = """
        If the magnitude of the resultant force is to be 500 N, directed along the positive y axis, determine the magnitude of force F and its direction u.
        """

        # Define known forces
        F_1 = ForceVector.unknown("F_1")

        F_2 = ForceVector(
            magnitude=700,
            angle=195,
            unit="N",
            name="F_2",
            description="Force 2"
        )

        # Define unknown resultant
        F_R = ForceVector(
            magnitude=500,
            angle=90,
            unit="N",
            name="F_R",
            description="Resultant Force",
            is_resultant=True
        )

    problem_instance = ProblemC2P2()
    solution = problem_instance.solve()
    F_1_solution = solution["F_1"]
    F_2_solution = solution["F_2"]
    F_R_solution = solution["F_R"]

    F_1_expected = ForceVector(
        magnitude=959.778,
        angle=45.212,
        unit="N",
        name="F_1",
        description="Force 1"
    )

    F_2_expected = ForceVector(
        magnitude=700,
        angle=195,
        unit="N",
        name="F_2",
        description="Force 2"
    )

    F_R_expected = ForceVector(
        magnitude=500,
        angle=90,
        unit="N",
        name="F_R",
        description="Resultant Force"
    )

    assert F_1_solution == F_1_expected
    assert F_2_solution == F_2_expected
    assert F_R_solution == F_R_expected
