"""
Comprehensive tests for the Vector class.

Tests cover:
- Vector creation with various units
- Component access as Quantities
- Vector arithmetic (addition, subtraction, scaling)
- Vector operations (dot product, cross product, normalization)
- Geometric operations (angle, projection, parallel/perpendicular tests)
- Unit conversions
- Edge cases and error handling
"""

import math

import pytest

from qnty.core import Q, u
from qnty.spatial import _Vector


class TestVectorCreation:
    """Test Vector creation and initialization."""

    def test_create_vector_with_unit(self):
        """Test creating a vector with explicit unit."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        assert v is not None
        # Verify internal SI storage
        assert v._coords[0] == 1.0
        assert v._coords[1] == 2.0
        assert v._coords[2] == 3.0

    def test_create_vector_2d_default_w(self):
        """Test creating a 2D vector (w defaults to 0)."""
        v = _Vector(1.0, 2.0, unit=u.meter)

        assert v._coords[2] == 0.0

    def test_create_vector_from_quantities(self):
        """Test creating vector from Quantity objects."""
        u_comp = Q(1.0, u.meter)
        v_comp = Q(2.0, u.meter)
        w_comp = Q(3.0, u.meter)

        vec = _Vector.from_quantities(u_comp, v_comp, w_comp)

        assert vec.u == u_comp
        assert vec.v == v_comp
        assert vec.w == w_comp

    def test_create_vector_from_quantities_2d(self):
        """Test creating 2D vector from quantities (w defaults to 0)."""
        u_comp = Q(1.0, u.meter)
        v_comp = Q(2.0, u.meter)

        vec = _Vector.from_quantities(u_comp, v_comp)

        assert vec.u == u_comp
        assert vec.v == v_comp
        assert vec.w.magnitude() == 0.0

    def test_create_vector_from_mismatched_dimensions_raises(self):
        """Test that creating vector from quantities with different dimensions raises error."""
        u_comp = Q(1.0, u.meter)
        v_comp = Q(2.0, u.newton)  # Wrong dimension!

        with pytest.raises(ValueError, match="same dimension"):
            _Vector.from_quantities(u_comp, v_comp)


class TestVectorComponentAccess:
    """Test accessing vector components as Quantities."""

    def test_access_u_component(self):
        """Test accessing u component as Quantity."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        u_comp = v.u

        assert u_comp.magnitude() == 1.0
        assert u_comp.dim == u.meter.dim

    def test_access_v_component(self):
        """Test accessing v component as Quantity."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v_comp = v.v

        assert v_comp.magnitude() == 2.0
        assert v_comp.dim == u.meter.dim

    def test_access_w_component(self):
        """Test accessing w component as Quantity."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        w = v.w

        assert w.magnitude() == 3.0
        assert w.dim == u.meter.dim


class TestVectorMagnitude:
    """Test vector magnitude calculations."""

    def test_magnitude_2d_vector(self):
        """Test magnitude of 2D vector."""
        v = _Vector(3.0, 4.0, 0.0, unit=u.meter)
        mag = v.magnitude

        # 3-4-5 triangle
        assert abs(mag.magnitude() - 5.0) < 1e-10

    def test_magnitude_3d_vector(self):
        """Test magnitude of 3D vector."""
        v = _Vector(1.0, 2.0, 2.0, unit=u.meter)
        mag = v.magnitude

        # sqrt(1² + 2² + 2²) = sqrt(9) = 3
        expected = math.sqrt(1**2 + 2**2 + 2**2)
        assert abs(mag.magnitude() - expected) < 1e-10

    def test_magnitude_unit_vector(self):
        """Test magnitude of unit vector."""
        v = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        mag = v.magnitude

        assert abs(mag.magnitude() - 1.0) < 1e-10

    def test_magnitude_zero_vector(self):
        """Test magnitude of zero vector."""
        v = _Vector(0.0, 0.0, 0.0, unit=u.meter)
        mag = v.magnitude

        assert abs(mag.magnitude()) < 1e-10


class TestVectorNormalization:
    """Test vector normalization operations."""

    def test_normalize_vector(self):
        """Test normalizing a vector."""
        v = _Vector(3.0, 4.0, 0.0, unit=u.meter)
        v_norm = v.normalized()

        # Magnitude should be 1
        assert abs(v_norm.magnitude.magnitude() - 1.0) < 1e-10

        # Components should be scaled
        assert abs(v_norm.u.magnitude() - 0.6) < 1e-10  # 3/5
        assert abs(v_norm.v.magnitude() - 0.8) < 1e-10  # 4/5

    def test_normalize_3d_vector(self):
        """Test normalizing a 3D vector."""
        v = _Vector(1.0, 2.0, 2.0, unit=u.meter)
        v_norm = v.normalized()

        # Magnitude should be 1
        assert abs(v_norm.magnitude.magnitude() - 1.0) < 1e-10

    def test_normalize_zero_vector_raises(self):
        """Test that normalizing zero vector raises error."""
        v = _Vector(0.0, 0.0, 0.0, unit=u.meter)

        with pytest.raises(ValueError, match="Cannot normalize zero vector"):
            _ = v.normalized()

    def test_normalize_already_normalized(self):
        """Test normalizing an already normalized vector."""
        v = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v_norm = v.normalized()

        # Should be essentially the same
        assert abs(v_norm.magnitude.magnitude() - 1.0) < 1e-10
        assert abs(v_norm.u.magnitude() - 1.0) < 1e-10


class TestVectorWithMagnitude:
    """Test setting vector magnitude."""

    def test_with_magnitude_quantity(self):
        """Test setting vector magnitude using Quantity."""
        v = _Vector(3.0, 4.0, 0.0, unit=u.meter)  # mag = 5
        new_mag = Q(10.0, u.meter)

        v_scaled = v.with_magnitude(new_mag)

        # Magnitude should be 10
        assert abs(v_scaled.magnitude.magnitude() - 10.0) < 1e-10

        # Direction should be preserved (components doubled)
        assert abs(v_scaled.u.magnitude() - 6.0) < 1e-10
        assert abs(v_scaled.v.magnitude() - 8.0) < 1e-10

    def test_with_magnitude_float(self):
        """Test setting vector magnitude using float (SI units)."""
        v = _Vector(1.0, 0.0, 0.0, unit=u.meter)

        v_scaled = v.with_magnitude(5.0)

        assert abs(v_scaled.magnitude.magnitude() - 5.0) < 1e-10
        assert abs(v_scaled.u.magnitude() - 5.0) < 1e-10

    def test_with_magnitude_zero_vector_raises(self):
        """Test that setting magnitude of zero vector raises error."""
        v = _Vector(0.0, 0.0, 0.0, unit=u.meter)

        with pytest.raises(ValueError, match="Cannot scale zero vector"):
            _ = v.with_magnitude(5.0)


class TestVectorArithmetic:
    """Test vector arithmetic operations."""

    def test_vector_addition(self):
        """Test adding two vectors."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(4.0, 5.0, 6.0, unit=u.meter)

        v3 = v1 + v2

        assert v3.u.magnitude() == 5.0
        assert v3.v.magnitude() == 7.0
        assert v3.w.magnitude() == 9.0

    def test_vector_subtraction(self):
        """Test subtracting two vectors."""
        v1 = _Vector(5.0, 7.0, 9.0, unit=u.meter)
        v2 = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        v3 = v1 - v2

        assert v3.u.magnitude() == 4.0
        assert v3.v.magnitude() == 5.0
        assert v3.w.magnitude() == 6.0

    def test_vector_addition_different_dimensions_raises(self):
        """Test that adding vectors with different dimensions raises error."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(4.0, 5.0, 6.0, unit=u.newton)

        with pytest.raises(ValueError, match="different dimensions"):
            _ = v1 + v2

    def test_scalar_multiplication(self):
        """Test multiplying vector by scalar."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        v_scaled = v * 2.0

        assert v_scaled.u.magnitude() == 2.0
        assert v_scaled.v.magnitude() == 4.0
        assert v_scaled.w.magnitude() == 6.0

    def test_scalar_multiplication_reverse(self):
        """Test multiplying scalar by vector (reverse order)."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        v_scaled = 3.0 * v

        assert v_scaled.u.magnitude() == 3.0
        assert v_scaled.v.magnitude() == 6.0
        assert v_scaled.w.magnitude() == 9.0

    def test_scalar_division(self):
        """Test dividing vector by scalar."""
        v = _Vector(10.0, 20.0, 30.0, unit=u.meter)

        v_scaled = v / 10.0

        assert v_scaled.u.magnitude() == 1.0
        assert v_scaled.v.magnitude() == 2.0
        assert v_scaled.w.magnitude() == 3.0

    def test_scalar_division_by_zero_raises(self):
        """Test that dividing by zero raises error."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        with pytest.raises(ZeroDivisionError):
            _ = v / 0.0

    def test_vector_negation(self):
        """Test negating a vector."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        v_neg = -v

        assert v_neg.u.magnitude() == -1.0
        assert v_neg.v.magnitude() == -2.0
        assert v_neg.w.magnitude() == -3.0


class TestVectorDotProduct:
    """Test dot product operations."""

    def test_dot_product_perpendicular_vectors(self):
        """Test dot product of perpendicular vectors is zero."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        dot = v1.dot(v2)

        assert abs(dot.magnitude()) < 1e-10

    def test_dot_product_parallel_vectors(self):
        """Test dot product of parallel vectors."""
        v1 = _Vector(2.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(3.0, 0.0, 0.0, unit=u.meter)

        dot = v1.dot(v2)

        # 2 * 3 = 6 (in m²)
        assert abs(dot.magnitude() - 6.0) < 1e-10

    def test_dot_product_general_vectors(self):
        """Test dot product of general vectors."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(4.0, 5.0, 6.0, unit=u.meter)

        dot = v1.dot(v2)

        # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
        expected = 1.0 * 4.0 + 2.0 * 5.0 + 3.0 * 6.0
        assert abs(dot.magnitude() - expected) < 1e-10


class TestVectorCrossProduct:
    """Test cross product operations."""

    def test_cross_product_orthogonal_unit_vectors(self):
        """Test cross product of orthogonal unit vectors."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        v3 = v1.cross(v2)

        # Should give unit vector in z direction
        assert abs(v3.u.magnitude()) < 1e-10
        assert abs(v3.v.magnitude()) < 1e-10
        assert abs(v3.w.magnitude() - 1.0) < 1e-10

    def test_cross_product_reverse_order(self):
        """Test that cross product is anti-commutative."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        v3 = v2.cross(v1)

        # Should give negative of previous result
        assert abs(v3.u.magnitude()) < 1e-10
        assert abs(v3.v.magnitude()) < 1e-10
        assert abs(v3.w.magnitude() + 1.0) < 1e-10

    def test_cross_product_parallel_vectors_is_zero(self):
        """Test cross product of parallel vectors is zero."""
        v1 = _Vector(2.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(4.0, 0.0, 0.0, unit=u.meter)

        v3 = v1.cross(v2)

        # Should be zero vector
        assert abs(v3.u.magnitude()) < 1e-10
        assert abs(v3.v.magnitude()) < 1e-10
        assert abs(v3.w.magnitude()) < 1e-10

    def test_cross_product_general_vectors(self):
        """Test cross product of general vectors."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(4.0, 5.0, 6.0, unit=u.meter)

        v3 = v1.cross(v2)

        # Expected: (2*6 - 3*5, 3*4 - 1*6, 1*5 - 2*4) = (-3, 6, -3)
        assert abs(v3.u.magnitude() - (-3.0)) < 1e-10
        assert abs(v3.v.magnitude() - 6.0) < 1e-10
        assert abs(v3.w.magnitude() - (-3.0)) < 1e-10


class TestVectorGeometricTests:
    """Test geometric relationship tests."""

    def test_is_parallel_to_same_direction(self):
        """Test parallel test for vectors in same direction."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(2.0, 4.0, 6.0, unit=u.meter)

        assert v1.is_parallel_to(v2)

    def test_is_parallel_to_opposite_direction(self):
        """Test parallel test for vectors in opposite directions."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(-1.0, -2.0, -3.0, unit=u.meter)

        assert v1.is_parallel_to(v2)

    def test_is_not_parallel(self):
        """Test parallel test for non-parallel vectors."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        assert not v1.is_parallel_to(v2)

    def test_is_perpendicular_to(self):
        """Test perpendicular test for orthogonal vectors."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        assert v1.is_perpendicular_to(v2)

    def test_is_not_perpendicular(self):
        """Test perpendicular test for non-orthogonal vectors."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(1.0, 1.0, 0.0, unit=u.meter)

        assert not v1.is_perpendicular_to(v2)


class TestVectorAngle:
    """Test angle calculations between vectors."""

    def test_angle_between_perpendicular_vectors(self):
        """Test angle between perpendicular vectors is 90 degrees."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        angle = v1.angle_to(v2)

        # Should be π/2 radians (90 degrees)
        expected = math.pi / 2
        assert abs(angle.magnitude() - expected) < 1e-10

    def test_angle_between_parallel_vectors(self):
        """Test angle between parallel vectors is 0."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(2.0, 0.0, 0.0, unit=u.meter)

        angle = v1.angle_to(v2)

        assert abs(angle.magnitude()) < 1e-10

    def test_angle_between_opposite_vectors(self):
        """Test angle between opposite vectors is 180 degrees."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(-1.0, 0.0, 0.0, unit=u.meter)

        angle = v1.angle_to(v2)

        # Should be π radians (180 degrees)
        expected = math.pi
        assert abs(angle.magnitude() - expected) < 1e-10

    def test_angle_45_degrees(self):
        """Test angle calculation for 45 degree angle."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(1.0, 1.0, 0.0, unit=u.meter)

        angle = v1.angle_to(v2)

        # Should be π/4 radians (45 degrees)
        expected = math.pi / 4
        assert abs(angle.magnitude() - expected) < 1e-10

    def test_angle_with_zero_vector_raises(self):
        """Test that angle with zero vector raises error."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 0.0, 0.0, unit=u.meter)

        with pytest.raises(ValueError, match="zero vector"):
            _ = v1.angle_to(v2)


class TestVectorProjection:
    """Test vector projection operations."""

    def test_projection_onto_parallel_vector(self):
        """Test projection onto parallel vector gives the original vector."""
        v1 = _Vector(3.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(1.0, 0.0, 0.0, unit=u.meter)

        proj = v1.projection_onto(v2)

        # Should be same as v1
        assert abs(proj.u.magnitude() - 3.0) < 1e-10
        assert abs(proj.v.magnitude()) < 1e-10
        assert abs(proj.w.magnitude()) < 1e-10

    def test_projection_onto_perpendicular_vector(self):
        """Test projection onto perpendicular vector gives zero vector."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(0.0, 1.0, 0.0, unit=u.meter)

        proj = v1.projection_onto(v2)

        # Should be zero vector
        assert abs(proj.u.magnitude()) < 1e-10
        assert abs(proj.v.magnitude()) < 1e-10
        assert abs(proj.w.magnitude()) < 1e-10

    def test_projection_general_case(self):
        """Test projection in general case."""
        v1 = _Vector(3.0, 4.0, 0.0, unit=u.meter)
        v2 = _Vector(1.0, 0.0, 0.0, unit=u.meter)

        proj = v1.projection_onto(v2)

        # Should project to x-axis component only
        assert abs(proj.u.magnitude() - 3.0) < 1e-10
        assert abs(proj.v.magnitude()) < 1e-10

    def test_projection_onto_zero_vector_raises(self):
        """Test that projection onto zero vector raises error."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(0.0, 0.0, 0.0, unit=u.meter)

        with pytest.raises(ValueError, match="Cannot project onto zero vector"):
            _ = v1.projection_onto(v2)


class TestVectorUnitConversions:
    """Test unit conversion operations."""

    def test_convert_vector_to_different_unit(self):
        """Test converting vector to different display unit."""
        v_m = _Vector(10.0, 20.0, 30.0, unit=u.meter)
        v_ft = v_m.to_unit(u.foot)

        # 1 meter = 3.28084 feet
        expected_u = 10.0 * 3.28084
        expected_v = 20.0 * 3.28084
        expected_w = 30.0 * 3.28084

        assert abs(v_ft.u.magnitude() - expected_u) < 1e-4
        assert abs(v_ft.v.magnitude() - expected_v) < 1e-4
        assert abs(v_ft.w.magnitude() - expected_w) < 1e-4

    def test_to_array_returns_display_values(self):
        """Test that to_array returns values in display unit."""
        v = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        arr = v.to_array()

        assert arr[0] == 1.0
        assert arr[1] == 2.0
        assert arr[2] == 3.0


class TestVectorEquality:
    """Test vector equality comparisons."""

    def test_equal_vectors(self):
        """Test that identical vectors are equal."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(1.0, 2.0, 3.0, unit=u.meter)

        assert v1 == v2

    def test_equal_vectors_different_units(self):
        """Test that vectors with same components but different units are equal."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(100.0, 200.0, 300.0, unit=u.centimeter)

        # Should be equal because internal SI values are the same
        assert v1 == v2

    def test_unequal_vectors(self):
        """Test that different vectors are not equal."""
        v1 = _Vector(1.0, 2.0, 3.0, unit=u.meter)
        v2 = _Vector(1.1, 2.0, 3.0, unit=u.meter)

        assert v1 != v2


class TestVectorEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_vector(self):
        """Test creating zero vector."""
        v = _Vector(0.0, 0.0, 0.0, unit=u.meter)

        assert abs(v.magnitude.magnitude()) < 1e-10

    def test_negative_components(self):
        """Test vector with negative components."""
        v = _Vector(-1.0, -2.0, -3.0, unit=u.meter)

        assert v.u.magnitude() == -1.0
        assert v.v.magnitude() == -2.0
        assert v.w.magnitude() == -3.0

    def test_very_large_components(self):
        """Test vector with very large components."""
        large_val = 1e10
        v = _Vector(large_val, large_val, large_val, unit=u.meter)

        assert v.u.magnitude() == large_val

    def test_very_small_components(self):
        """Test vector with very small components."""
        small_val = 1e-10
        v = _Vector(small_val, small_val, small_val, unit=u.meter)

        assert abs(v.u.magnitude() - small_val) < 1e-20
