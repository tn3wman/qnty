"""
Tests for the unified parallelogram_law API.

These tests verify that the unified API works for both:
- Code-based analysis (rich objects)
- Frontend integration (DTOs)
"""

import json
import math
from dataclasses import asdict

import pytest

from qnty.problems.statics import parallelogram_law as pl


class TestVectorCreation:
    """Test vector creation with unified API."""

    def test_create_vector_polar(self):
        """Create vector with polar coordinates."""
        v = pl.create_vector_polar(magnitude=100, angle=30, unit="N", name="F_1")

        assert v.name == "F_1"
        # Check components (100 * cos(30°), 100 * sin(30°))
        expected_u = 100 * math.cos(math.radians(30))
        expected_v = 100 * math.sin(math.radians(30))
        assert abs(v._coords[0] - expected_u) < 0.01
        assert abs(v._coords[1] - expected_v) < 0.01

    def test_create_vector_cartesian(self):
        """Create vector with Cartesian coordinates."""
        v = pl.create_vector_cartesian(u=100, v=200, unit="N", name="F_2")

        assert v.name == "F_2"
        assert abs(v._coords[0] - 100) < 0.01
        assert abs(v._coords[1] - 200) < 0.01

    def test_create_vector_resultant(self):
        """Create resultant vector from input vectors."""
        F_1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N", name="F_1")
        F_2 = pl.create_vector_polar(magnitude=100, angle=90, unit="N", name="F_2")
        F_R = pl.create_vector_resultant(F_1, F_2, name="F_R")

        assert F_R.name == "F_R"
        assert F_R.is_resultant is True


class TestSolveClass:
    """Test solve_class() with problem classes."""

    def test_solve_class_two_vectors(self):
        """Solve a class with two vectors."""
        class TwoVectorProblem:
            F_1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N")
            F_2 = pl.create_vector_polar(magnitude=100, angle=90, unit="N")
            F_R = pl.create_vector_resultant(F_1, F_2)

        result = pl.solve_class(TwoVectorProblem)

        assert result.success
        assert result.resultant is not None
        assert "F_R" in result.vectors
        assert "F_1" in result.vectors
        assert "F_2" in result.vectors

    def test_solve_class_resultant_magnitude(self):
        """Verify resultant magnitude calculation."""
        class Problem:
            F_1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N")
            F_2 = pl.create_vector_polar(magnitude=100, angle=90, unit="N")
            F_R = pl.create_vector_resultant(F_1, F_2)

        result = pl.solve_class(Problem)
        dto = result.to_dto()

        # Resultant of (100, 0) + (0, 100) = (100, 100)
        # Magnitude = sqrt(100^2 + 100^2) = 141.42
        assert abs(dto.resultant.magnitude - 141.421) < 0.1

    def test_solve_class_resultant_angle(self):
        """Verify resultant angle calculation."""
        class Problem:
            F_1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N")
            F_2 = pl.create_vector_polar(magnitude=100, angle=90, unit="N")
            F_R = pl.create_vector_resultant(F_1, F_2)

        result = pl.solve_class(Problem)
        dto = result.to_dto()

        # Resultant of (100, 0) + (0, 100) should be at 45°
        assert abs(dto.resultant.angle - 45.0) < 0.1

    def test_solve_class_three_vectors(self):
        """Solve with three vectors."""
        class Problem:
            F_1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N")
            F_2 = pl.create_vector_polar(magnitude=100, angle=120, unit="N")
            F_3 = pl.create_vector_polar(magnitude=100, angle=240, unit="N")
            F_R = pl.create_vector_resultant(F_1, F_2, F_3)

        result = pl.solve_class(Problem)

        assert result.success
        # Three equal vectors at 120° apart should sum to ~0
        dto = result.to_dto()
        assert dto.resultant.magnitude < 1.0  # Should be very small

    def test_solve_empty_returns_error(self):
        """Solve with no vectors returns error."""
        result = pl.solve()

        assert not result.success
        assert "No vectors" in result.error


class TestResultToDTO:
    """Test Result.to_dto() conversion."""

    def test_to_dto_returns_result_dto(self):
        """to_dto() returns a ResultDTO."""
        class Problem:
            F_1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N")
            F_R = pl.create_vector_resultant(F_1)

        result = pl.solve_class(Problem)
        dto = result.to_dto()

        assert isinstance(dto, pl.ResultDTO)

    def test_to_dto_is_json_serializable(self):
        """ResultDTO is JSON-serializable."""
        class Problem:
            F_1 = pl.create_vector_polar(magnitude=100, angle=30, unit="N")
            F_2 = pl.create_vector_polar(magnitude=200, angle=60, unit="N")
            F_R = pl.create_vector_resultant(F_1, F_2)

        result = pl.solve_class(Problem)

        dto = result.to_dto()
        json_str = json.dumps(asdict(dto))

        # Should not raise
        loaded = json.loads(json_str)
        assert loaded["success"] is True
        assert "resultant" in loaded

    def test_to_dto_preserves_values(self):
        """DTO preserves computed values."""
        class Problem:
            F_1 = pl.create_vector_cartesian(u=100, v=0, unit="N")
            F_2 = pl.create_vector_cartesian(u=0, v=100, unit="N")
            F_R = pl.create_vector_resultant(F_1, F_2)

        result = pl.solve_class(Problem)
        dto = result.to_dto()

        assert abs(dto.resultant.u - 100) < 0.01
        assert abs(dto.resultant.v - 100) < 0.01


class TestDTOConversion:
    """Test to_vector_dto and from_vector_dto."""

    def test_to_vector_dto(self):
        """Convert vector to DTO."""
        v = pl.create_vector_polar(magnitude=100, angle=45, unit="N", name="F_1")
        dto = pl.to_vector_dto(v)

        assert isinstance(dto, pl.Vector)
        assert dto.name == "F_1"
        assert dto.unit == "N"
        assert abs(dto.magnitude - 100) < 0.1

    def test_from_vector_dto(self):
        """Convert DTO back to vector."""
        dto = pl.Vector(
            u=0, v=0, magnitude=100, angle=45, unit="N", name="F_1"
        )
        v = pl.from_vector_dto(dto)

        assert v.name == "F_1"
        # Check components (100 * cos(45°), 100 * sin(45°))
        expected = 100 * math.cos(math.radians(45))
        assert abs(v._coords[0] - expected) < 0.1
        assert abs(v._coords[1] - expected) < 0.1

    def test_roundtrip_conversion(self):
        """Vector survives DTO roundtrip."""
        original = pl.create_vector_polar(magnitude=123.45, angle=67.8, unit="N", name="test")

        dto = pl.to_vector_dto(original)
        restored = pl.from_vector_dto(dto)

        # Check coordinates match
        assert abs(original._coords[0] - restored._coords[0]) < 0.01
        assert abs(original._coords[1] - restored._coords[1]) < 0.01


class TestTypeAliases:
    """Test that type aliases are correct."""

    def test_vector_is_vector_dto(self):
        """Vector alias points to VectorDTO."""
        from qnty.integration.dto import VectorDTO

        assert pl.Vector is VectorDTO

    def test_solution_is_result_dto(self):
        """Solution alias points to ResultDTO."""
        assert pl.Solution is pl.ResultDTO


class TestUnitConversion:
    """Test unit conversion in output."""

    def test_output_unit_conversion(self):
        """Results are converted to output unit."""
        class Problem:
            F_1 = pl.create_vector_cartesian(u=100, v=0, unit="N")
            F_R = pl.create_vector_resultant(F_1)

        result = pl.solve_class(Problem, output_unit="lbf")
        dto = result.to_dto()

        # 100 N ≈ 22.48 lbf
        assert dto.resultant.unit == "lbf"
        assert abs(dto.resultant.magnitude - 22.48) < 0.1


class TestReflexIntegration:
    """Test patterns used in Reflex integration."""

    def test_state_management_pattern(self):
        """Test the state management pattern for Reflex."""
        # Simulate Reflex state with DTOs
        state_vectors: list[pl.Vector] = []
        state_result: pl.ResultDTO | None = None

        # Add vectors (storing as DTOs)
        v1 = pl.create_vector_polar(magnitude=100, angle=0, unit="N", name="F_1")
        state_vectors.append(pl.to_vector_dto(v1))

        v2 = pl.create_vector_polar(magnitude=100, angle=90, unit="N", name="F_2")
        state_vectors.append(pl.to_vector_dto(v2))

        # Solve (converting DTOs back to vectors)
        vectors = [pl.from_vector_dto(d) for d in state_vectors]
        result = pl.solve(*vectors)
        state_result = result.to_dto()

        # Verify
        assert len(state_vectors) == 2
        assert state_result.success
        assert abs(state_result.resultant.magnitude - 141.421) < 0.1

    def test_state_is_json_serializable(self):
        """State can be JSON-serialized (for Reflex)."""
        state_vectors = []

        v = pl.create_vector_polar(magnitude=100, angle=45, unit="N", name="F")
        state_vectors.append(pl.to_vector_dto(v))

        result = pl.solve(v)
        state_result = result.to_dto()

        # Serialize entire state
        state = {
            "vectors": [asdict(v) for v in state_vectors],
            "result": asdict(state_result),
        }
        json_str = json.dumps(state)

        # Should not raise
        loaded = json.loads(json_str)
        assert len(loaded["vectors"]) == 1
        assert loaded["result"]["success"] is True
