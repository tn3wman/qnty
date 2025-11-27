"""
Tests for the DTO-based integration layer.

These tests verify that:
1. DTOs are properly JSON-serializable
2. Converters correctly transform between DTOs and domain objects
3. Solver service returns correct results
"""

from dataclasses import asdict
import json
import math
import pytest

from qnty.integration import (
    PointDTO,
    ProblemInputDTO,
    QuantityDTO,
    SolutionDTO,
    SolutionStepDTO,
    VectorDTO,
    dto_to_point,
    dto_to_quantity,
    dto_to_vector,
    get_components,
    point_to_dto,
    quantity_to_dto,
    solve_problem,
    sum_vectors,
    vector_to_dto,
)


class TestDTOSerialization:
    """Test that all DTOs are JSON-serializable."""

    def test_vector_dto_serializes(self):
        """VectorDTO should be JSON-serializable."""
        dto = VectorDTO(
            u=100.0,
            v=200.0,
            w=0.0,
            unit="N",
            name="F1",
            magnitude=223.6,
            angle=63.43,
        )
        json_str = json.dumps(asdict(dto))
        loaded = json.loads(json_str)
        assert loaded["u"] == 100.0
        assert loaded["name"] == "F1"

    def test_point_dto_serializes(self):
        """PointDTO should be JSON-serializable."""
        dto = PointDTO(x=3.0, y=4.0, z=0.0, unit="m", name="A")
        json_str = json.dumps(asdict(dto))
        loaded = json.loads(json_str)
        assert loaded["x"] == 3.0
        assert loaded["name"] == "A"

    def test_quantity_dto_serializes(self):
        """QuantityDTO should be JSON-serializable."""
        dto = QuantityDTO(value=100.0, unit="N", name="Force", dimension="Force")
        json_str = json.dumps(asdict(dto))
        loaded = json.loads(json_str)
        assert loaded["value"] == 100.0

    def test_solution_dto_serializes(self):
        """SolutionDTO should be JSON-serializable."""
        dto = SolutionDTO(
            success=True,
            vectors={"F_R": VectorDTO(u=100, v=100, unit="N", name="F_R")},
            steps=[SolutionStepDTO(description="Test step", result="OK")],
        )
        json_str = json.dumps(asdict(dto))
        loaded = json.loads(json_str)
        assert loaded["success"] is True
        assert "F_R" in loaded["vectors"]

    def test_problem_input_dto_serializes(self):
        """ProblemInputDTO should be JSON-serializable."""
        dto = ProblemInputDTO(
            problem_type="parallelogram_law",
            vectors=[VectorDTO(u=100, v=0, unit="N", name="F1")],
            output_unit="N",
        )
        json_str = json.dumps(asdict(dto))
        loaded = json.loads(json_str)
        assert loaded["problem_type"] == "parallelogram_law"


class TestVectorDTOConversion:
    """Test conversion between VectorDTO and _Vector."""

    def test_cartesian_dto_to_vector(self):
        """Converting Cartesian VectorDTO to _Vector should preserve components."""
        dto = VectorDTO(u=100.0, v=200.0, w=0.0, unit="N", name="F1")
        vec = dto_to_vector(dto)

        assert vec.name == "F1"
        # Components should match (in SI)
        coords = vec._coords
        assert abs(coords[0] - 100.0) < 1e-6
        assert abs(coords[1] - 200.0) < 1e-6

    def test_polar_dto_to_vector(self):
        """Converting polar VectorDTO to _Vector should compute correct components."""
        dto = VectorDTO(
            u=0, v=0, w=0,
            magnitude=100.0,
            angle=30.0,
            angle_unit="degree",
            angle_wrt="+x",
            unit="N",
            name="F1",
        )
        vec = dto_to_vector(dto)

        # Check computed components
        coords = vec._coords
        expected_u = 100.0 * math.cos(math.radians(30))  # ~86.6
        expected_v = 100.0 * math.sin(math.radians(30))  # 50.0

        assert abs(coords[0] - expected_u) < 1e-6
        assert abs(coords[1] - expected_v) < 1e-6

    def test_vector_to_dto(self):
        """Converting _Vector to VectorDTO should preserve values."""
        from qnty.spatial.vectors import create_vector_cartesian

        vec = create_vector_cartesian(u=100, v=200, w=0, unit="N", name="F1")
        dto = vector_to_dto(vec, output_unit="N")

        assert dto.name == "F1"
        assert abs(dto.u - 100.0) < 1e-6
        assert abs(dto.v - 200.0) < 1e-6
        assert dto.unit == "N"

    def test_roundtrip_cartesian(self):
        """Cartesian vector should survive DTO roundtrip."""
        original = VectorDTO(u=100.0, v=200.0, w=50.0, unit="N", name="F1")
        vec = dto_to_vector(original)
        result = vector_to_dto(vec, output_unit="N")

        assert abs(result.u - original.u) < 1e-6
        assert abs(result.v - original.v) < 1e-6
        assert abs(result.w - original.w) < 1e-6

    def test_unit_conversion(self):
        """Converting to different output unit should scale correctly."""
        from qnty.spatial.vectors import create_vector_cartesian

        # 100 N ≈ 22.48 lbf
        vec = create_vector_cartesian(u=100, v=0, w=0, unit="N", name="F1")
        dto = vector_to_dto(vec, output_unit="lbf")

        # 1 N = 0.224809 lbf
        expected_lbf = 100.0 / 4.44822  # ~22.48
        assert abs(dto.u - expected_lbf) < 0.1


class TestPointDTOConversion:
    """Test conversion between PointDTO and _Point."""

    def test_dto_to_point(self):
        """Converting PointDTO to _Point should preserve coordinates."""
        dto = PointDTO(x=3.0, y=4.0, z=0.0, unit="m", name="A")
        point = dto_to_point(dto)

        coords = point._coords
        assert abs(coords[0] - 3.0) < 1e-6
        assert abs(coords[1] - 4.0) < 1e-6

    def test_point_to_dto(self):
        """Converting _Point to PointDTO should preserve coordinates."""
        from qnty.spatial.points import create_point_cartesian

        point = create_point_cartesian(x=3, y=4, z=5, unit="m")
        dto = point_to_dto(point, output_unit="m")

        assert abs(dto.x - 3.0) < 1e-6
        assert abs(dto.y - 4.0) < 1e-6
        assert abs(dto.z - 5.0) < 1e-6


class TestSolverService:
    """Test the solver service functions."""

    def test_solve_parallelogram_law_basic(self):
        """Solving parallelogram law should return correct resultant."""
        input_dto = ProblemInputDTO(
            problem_type="parallelogram_law",
            vectors=[
                VectorDTO(u=100, v=0, unit="N", name="F1"),
                VectorDTO(u=0, v=100, unit="N", name="F2"),
            ],
            output_unit="N",
        )
        result = solve_problem(input_dto)

        assert result.success
        assert "F_R" in result.vectors

        fr = result.vectors["F_R"]
        assert abs(fr.u - 100.0) < 1e-6
        assert abs(fr.v - 100.0) < 1e-6
        assert abs(fr.magnitude - 141.421) < 0.1

    def test_solve_parallelogram_law_polar(self):
        """Solving with polar input should work correctly."""
        input_dto = ProblemInputDTO(
            problem_type="parallelogram_law",
            vectors=[
                VectorDTO(u=0, v=0, magnitude=100, angle=0, unit="N", name="F1"),
                VectorDTO(u=0, v=0, magnitude=100, angle=90, unit="N", name="F2"),
            ],
            output_unit="N",
        )
        result = solve_problem(input_dto)

        assert result.success
        fr = result.vectors["F_R"]
        assert abs(fr.magnitude - 141.421) < 0.1
        assert abs(fr.angle - 45.0) < 0.1

    def test_solve_component_method(self):
        """Component method should break down vectors correctly."""
        input_dto = ProblemInputDTO(
            problem_type="component_method",
            vectors=[
                VectorDTO(u=0, v=0, magnitude=100, angle=30, unit="N", name="F"),
            ],
            output_unit="N",
        )
        result = solve_problem(input_dto)

        assert result.success
        f = result.vectors.get("F")
        assert f is not None
        assert abs(f.u - 86.603) < 0.1  # 100 * cos(30°)
        assert abs(f.v - 50.0) < 0.1    # 100 * sin(30°)

    def test_solve_equilibrium_satisfied(self):
        """Equilibrium check should pass when forces sum to zero."""
        input_dto = ProblemInputDTO(
            problem_type="equilibrium",
            vectors=[
                VectorDTO(u=100, v=0, unit="N", name="F1"),
                VectorDTO(u=-100, v=0, unit="N", name="F2"),
            ],
            output_unit="N",
        )
        result = solve_problem(input_dto)

        assert result.success

    def test_solve_equilibrium_not_satisfied(self):
        """Equilibrium check should fail when forces don't sum to zero."""
        input_dto = ProblemInputDTO(
            problem_type="equilibrium",
            vectors=[
                VectorDTO(u=100, v=0, unit="N", name="F1"),
                VectorDTO(u=50, v=0, unit="N", name="F2"),
            ],
            output_unit="N",
        )
        result = solve_problem(input_dto)

        assert not result.success
        assert "not in equilibrium" in result.error.lower()

    def test_unknown_problem_type(self):
        """Unknown problem type should return error."""
        input_dto = ProblemInputDTO(
            problem_type="unknown_type",  # type: ignore
            vectors=[],
        )
        result = solve_problem(input_dto)

        assert not result.success
        assert "Unknown problem type" in result.error


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_sum_vectors(self):
        """sum_vectors should correctly add vectors."""
        vectors = [
            VectorDTO(u=100, v=0, unit="N", name="F1"),
            VectorDTO(u=0, v=100, unit="N", name="F2"),
        ]
        result = sum_vectors(vectors, output_unit="N")

        assert result.success
        fr = result.vectors["F_R"]
        assert abs(fr.magnitude - 141.421) < 0.1

    def test_get_components(self):
        """get_components should break down polar vector."""
        vectors = [
            VectorDTO(u=0, v=0, magnitude=100, angle=45, unit="N", name="F"),
        ]
        result = get_components(vectors, output_unit="N")

        assert result.success
        f = result.vectors.get("F")
        expected = 100 * math.cos(math.radians(45))  # ~70.7
        assert abs(f.u - expected) < 0.1
        assert abs(f.v - expected) < 0.1


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_vectors(self):
        """Solving with no vectors should return error."""
        input_dto = ProblemInputDTO(
            problem_type="parallelogram_law",
            vectors=[],
        )
        result = solve_problem(input_dto)

        assert not result.success
        assert "No vectors" in result.error

    def test_single_vector(self):
        """Single vector should return itself as resultant."""
        input_dto = ProblemInputDTO(
            problem_type="parallelogram_law",
            vectors=[VectorDTO(u=100, v=0, unit="N", name="F1")],
            output_unit="N",
        )
        result = solve_problem(input_dto)

        assert result.success
        fr = result.vectors["F_R"]
        assert abs(fr.u - 100.0) < 1e-6


class TestFacadePattern:
    """Test the facade pattern for single-import usage."""

    def test_parallelogram_law_type_aliases(self):
        """Facade should expose type aliases."""
        from qnty.integration import parallelogram_law

        # Type aliases should be the DTO classes
        assert parallelogram_law.Vector is VectorDTO
        assert parallelogram_law.Solution is SolutionDTO
        assert parallelogram_law.Point is PointDTO
        assert parallelogram_law.Input is ProblemInputDTO

    def test_parallelogram_law_create_vector(self):
        """Facade should create VectorDTO via factory method."""
        from qnty.integration import parallelogram_law

        v = parallelogram_law.create_vector(
            magnitude=100, angle=30, unit="N", name="F1"
        )

        assert isinstance(v, VectorDTO)
        assert v.magnitude == 100
        assert v.angle == 30
        assert v.unit == "N"
        assert v.name == "F1"

    def test_parallelogram_law_create_point(self):
        """Facade should create PointDTO via factory method."""
        from qnty.integration import parallelogram_law

        p = parallelogram_law.create_point(x=3, y=4, z=0, unit="m", name="A")

        assert isinstance(p, PointDTO)
        assert p.x == 3
        assert p.y == 4
        assert p.unit == "m"

    def test_parallelogram_law_solve(self):
        """Facade should solve problems directly."""
        from qnty.integration import parallelogram_law

        v1 = parallelogram_law.create_vector(u=100, v=0, unit="N", name="F1")
        v2 = parallelogram_law.create_vector(u=0, v=100, unit="N", name="F2")

        result = parallelogram_law.solve(vectors=[v1, v2])

        assert result.success
        assert "F_R" in result.vectors
        fr = result.vectors["F_R"]
        assert abs(fr.magnitude - 141.421) < 0.1

    def test_equilibrium_facade(self):
        """Equilibrium facade should work."""
        from qnty.integration import equilibrium

        v1 = equilibrium.create_vector(u=100, v=0, unit="N", name="F1")
        v2 = equilibrium.create_vector(u=-100, v=0, unit="N", name="F2")

        result = equilibrium.solve(vectors=[v1, v2])
        assert result.success

    def test_component_method_facade(self):
        """Component method facade should work."""
        from qnty.integration import component_method

        v = component_method.create_vector(magnitude=100, angle=30, unit="N", name="F")
        result = component_method.solve(vectors=[v])

        assert result.success
        f = result.vectors.get("F")
        assert abs(f.u - 86.603) < 0.1

    def test_facade_with_input_dto(self):
        """Facade should accept input_dto for full control."""
        from qnty.integration import parallelogram_law

        input_dto = parallelogram_law.create_input(
            vectors=[
                parallelogram_law.create_vector(u=100, v=0, unit="N", name="F1"),
            ],
            output_unit="lbf",
        )

        result = parallelogram_law.solve(input_dto=input_dto)

        assert result.success
        fr = result.vectors["F_R"]
        assert fr.unit == "lbf"
