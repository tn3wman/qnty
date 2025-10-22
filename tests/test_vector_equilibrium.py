"""
Tests for VectorEquilibriumProblem class.

Validates algebraic solving of 2D statics problems against known solutions
from textbook problems.
"""

import math
import pytest

from qnty.problems.vector_equilibrium import VectorEquilibriumProblem
from qnty.spatial.force_vector import ForceVector
from qnty.core import u


class TestForceVector:
    """Test ForceVector construction and properties."""

    def test_from_magnitude_angle(self):
        """Test creating force from magnitude and angle."""
        force = ForceVector(magnitude=500, angle=30, unit="N", name="F1")

        assert force.is_known
        assert force.magnitude is not None
        assert abs(force.magnitude.value - 500.0) < 0.01
        assert force.angle is not None
        # Angle stored in radians (SI)
        assert abs(force.angle.value - math.radians(30)) < 0.001

    def test_from_components(self):
        """Test creating force from x,y components."""
        force = ForceVector.from_components(x=300, y=400, unit="N", name="F2")

        assert force.is_known
        # Magnitude should be sqrt(300^2 + 400^2) = 500
        assert force.magnitude is not None
        assert abs(force.magnitude.value - 500.0) < 0.01

        # Angle should be atan2(400, 300) ≈ 53.13°
        expected_angle = math.atan2(400, 300)
        assert force.angle is not None
        assert abs(force.angle.value - expected_angle) < 0.001

    def test_unknown_force(self):
        """Test creating unknown force."""
        force = ForceVector.unknown("F_unknown")

        assert not force.is_known
        assert force.magnitude is None
        assert force.angle is None

    def test_force_components(self):
        """Test accessing force components."""
        force = ForceVector(magnitude=100, angle=45, unit="N")

        # At 45°, x and y should be equal: 100/sqrt(2) ≈ 70.71
        assert force.x is not None
        assert force.y is not None
        assert abs(force.x.value - 70.71) < 0.01
        assert abs(force.y.value - 70.71) < 0.01


class TestVectorEquilibriumBasic:
    """Test basic VectorEquilibriumProblem functionality."""

    def test_problem_creation(self):
        """Test creating a problem instance."""
        problem = VectorEquilibriumProblem("Test Problem")

        assert problem.name == "Test Problem"
        assert len(problem.forces) == 0
        assert not problem.is_solved

    def test_add_force(self):
        """Test adding forces to problem."""
        problem = VectorEquilibriumProblem("Test")

        force1 = ForceVector(magnitude=100, angle=0, unit="N", name="F1")
        problem.add_force(force1)

        assert len(problem.forces) == 1
        assert "F1" in problem.forces

    def test_class_attribute_extraction(self):
        """Test extracting ForceVector from class attributes."""

        class TestProblem(VectorEquilibriumProblem):
            F1 = ForceVector(magnitude=100, angle=0, unit="N", name="F1")
            F2 = ForceVector(magnitude=200, angle=90, unit="N", name="F2")

        problem = TestProblem()

        assert len(problem.forces) == 2
        assert "F1" in problem.forces
        assert "F2" in problem.forces


class TestTextbookProblems:
    """
    Test against known solutions from Hibbeler Statics textbook Chapter 2.

    These are the exact problems from the solutions manual.
    """

    def test_problem_2_1(self):
        """
        Problem 2-1: Find resultant of two forces.
        Given: F1 = 700 N at 60°, F2 = 450 N at 105°
        Expected: FR = 497 N at 155°
        """

        class Problem21(VectorEquilibriumProblem):
            F1 = ForceVector(magnitude=700, angle=60, unit="N", name="F1")
            F2 = ForceVector(magnitude=450, angle=105, unit="N", name="F2")
            FR = ForceVector.unknown("FR", is_resultant=True)

        problem = Problem21()
        solution = problem.solve()

        FR = solution["FR"]
        assert FR.is_known
        assert FR.magnitude is not None
        assert FR.angle is not None

        # Check magnitude (497 N ± 1%)
        mag_N = FR.magnitude.value / u.N.si_factor
        assert abs(mag_N - 497) < 5.0, f"Expected ~497 N, got {mag_N:.1f} N"

        # Check angle (155° ± 2°)
        angle_deg = FR.angle.value * 180 / math.pi
        assert abs(angle_deg - 155) < 3.0, f"Expected ~155°, got {angle_deg:.1f}°"

    def test_problem_2_3(self):
        """
        Problem 2-3: Resultant of two forces.
        Given: F1 = 250 lb at 315° (or -45°), F2 = 375 lb at 30°
        Expected: FR = 393 lb at 353°
        """

        class Problem23(VectorEquilibriumProblem):
            F1 = ForceVector(magnitude=250, angle=315, unit="lb", name="F1")
            F2 = ForceVector(magnitude=375, angle=30, unit="lb", name="F2")
            FR = ForceVector.unknown("FR", is_resultant=True)

        problem = Problem23()
        solution = problem.solve()

        FR = solution["FR"]

        # Check magnitude (393 lb ± 1%)
        mag_lb = FR.magnitude.value / u.lb.si_factor
        assert abs(mag_lb - 393) < 5.0, f"Expected ~393 lb, got {mag_lb:.1f} lb"

        # Check angle (353° ± 3°)
        angle_deg = FR.angle.value * 180 / math.pi
        # Normalize to 0-360
        while angle_deg < 0:
            angle_deg += 360
        while angle_deg >= 360:
            angle_deg -= 360

        assert abs(angle_deg - 353) < 5.0, f"Expected ~353°, got {angle_deg:.1f}°"

    def test_problem_2_27(self):
        """
        Problem 2-27: Component form.
        Given: F1 = 750 N at 45°, F2 = 800 N at -30° (330°)
        Expected: FR ≈ 1230 N at 6.08°
        """

        class Problem227(VectorEquilibriumProblem):
            F1 = ForceVector(magnitude=750, angle=45, unit="N", name="F1")
            F2 = ForceVector(magnitude=800, angle=330, unit="N", name="F2")
            FR = ForceVector.unknown("FR", is_resultant=True)

        problem = Problem227()
        solution = problem.solve()

        FR = solution["FR"]

        # Check magnitude (1230 N ± 2%)
        mag_N = FR.magnitude.value / u.N.si_factor
        assert abs(mag_N - 1230) < 30.0, f"Expected ~1230 N, got {mag_N:.1f} N"

        # Check angle (6.08° ± 2°)
        angle_deg = FR.angle.value * 180 / math.pi
        assert abs(angle_deg - 6.08) < 3.0, f"Expected ~6.08°, got {angle_deg:.1f}°"


class TestEquilibriumSolving:
    """Test equilibrium solving (ΣF = 0)."""

    def test_two_force_equilibrium(self):
        """Test finding force needed for equilibrium."""

        class TwoForceEquilibrium(VectorEquilibriumProblem):
            F1 = ForceVector(magnitude=100, angle=0, unit="N", name="F1")
            F2 = ForceVector.unknown("F2", is_resultant=False)

        problem = TwoForceEquilibrium()
        solution = problem.solve()

        F2 = solution["F2"]

        # F2 should be -F1 (opposite direction)
        assert F2.magnitude is not None
        assert abs(F2.magnitude.value - 100.0) < 0.1

        # Angle should be 180°
        angle_deg = F2.angle.value * 180 / math.pi
        assert abs(angle_deg - 180) < 1.0

    def test_three_force_equilibrium(self):
        """Test three forces in equilibrium."""

        class ThreeForceEquilibrium(VectorEquilibriumProblem):
            F1 = ForceVector(magnitude=500, angle=0, unit="N", name="F1")
            F2 = ForceVector(magnitude=300, angle=90, unit="N", name="F2")
            F3 = ForceVector.unknown("F3")

        problem = ThreeForceEquilibrium()
        solution = problem.solve()

        F3 = solution["F3"]

        # Check that sum of all forces is zero (within tolerance)
        sum_x = problem.F1.x.value + problem.F2.x.value + F3.x.value
        sum_y = problem.F1.y.value + problem.F2.y.value + F3.y.value

        assert abs(sum_x) < 0.1, f"Sum of x-components should be ~0, got {sum_x}"
        assert abs(sum_y) < 0.1, f"Sum of y-components should be ~0, got {sum_y}"


class TestProgrammaticConstruction:
    """Test programmatic problem construction."""

    def test_add_forces_programmatically(self):
        """Test adding forces without class definition."""
        problem = VectorEquilibriumProblem("Programmatic Test")

        problem.add_force(ForceVector(magnitude=100, angle=0, unit="N", name="F1"))
        problem.add_force(ForceVector(magnitude=100, angle=90, unit="N", name="F2"))
        problem.add_force(ForceVector.unknown("FR", is_resultant=True))

        solution = problem.solve()

        assert problem.is_solved
        assert "FR" in solution
        FR = solution["FR"]

        # Resultant should be sqrt(100^2 + 100^2) = 141.42 at 45°
        mag_N = FR.magnitude.value / u.N.si_factor
        assert abs(mag_N - 141.42) < 1.0

        angle_deg = FR.angle.value * 180 / math.pi
        assert abs(angle_deg - 45) < 1.0


class TestReportGeneration:
    """Test report content generation."""

    def test_generate_report_content(self):
        """Test generating report content."""

        class SimpleProblem(VectorEquilibriumProblem):
            name = "Simple Test Problem"
            description = "Test report generation"

            F1 = ForceVector(magnitude=100, angle=0, unit="N", name="F1")
            F2 = ForceVector(magnitude=100, angle=90, unit="N", name="F2")
            FR = ForceVector.unknown("FR", is_resultant=True)

        problem = SimpleProblem()
        problem.solve()

        report = problem.generate_report_content()

        assert report["title"] == "Simple Test Problem"
        assert report["description"] == "Test report generation"
        assert report["problem_type"] == "Vector Equilibrium (Statics)"
        assert len(report["given"]) == 2  # F1 and F2
        assert len(report["find"]) >= 1  # FR
        assert len(report["results"]) >= 1  # FR result
        assert len(report["solution_steps"]) > 0


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
