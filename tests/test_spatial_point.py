"""
Comprehensive tests for the Point class.

Tests cover:
- Point creation with various units
- Coordinate access as Quantities
- Point-to-Point operations (displacement, distance)
- Unit conversions
- Edge cases and error handling
"""

import math

import pytest

from qnty.core import Q, u
from qnty.spatial import Point, Vector


class TestPointCreation:
    """Test Point creation and initialization."""

    def test_create_point_with_unit(self):
        """Test creating a point with explicit unit."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)

        assert p is not None
        # Verify internal SI storage
        assert p._coords[0] == 10.0  # 10 m in SI
        assert p._coords[1] == 20.0  # 20 m in SI
        assert p._coords[2] == 30.0  # 30 m in SI

    def test_create_point_2d_default_z(self):
        """Test creating a 2D point (z defaults to 0)."""
        p = Point(5.0, 10.0, unit=u.meter)

        assert p._coords[2] == 0.0

    def test_create_point_from_quantities(self):
        """Test creating point from Quantity objects."""
        x = Q(10.0, u.meter)
        y = Q(20.0, u.meter)
        z = Q(30.0, u.meter)

        p = Point.from_quantities(x, y, z)

        assert p.x == x
        assert p.y == y
        assert p.z == z

    def test_create_point_from_quantities_2d(self):
        """Test creating 2D point from quantities (z defaults to 0)."""
        x = Q(5.0, u.meter)
        y = Q(10.0, u.meter)

        p = Point.from_quantities(x, y)

        assert p.x == x
        assert p.y == y
        assert p.z.magnitude() == 0.0

    def test_create_point_different_units_converts_to_si(self):
        """Test that different units are converted to SI internally."""
        # Create point in feet
        p_ft = Point(10.0, 20.0, 30.0, unit=u.foot)

        # Create equivalent point in meters
        # 1 foot = 0.3048 meters
        p_m = Point(10.0 * 0.3048, 20.0 * 0.3048, 30.0 * 0.3048, unit=u.meter)

        # Internal SI values should be equal
        assert abs(p_ft._coords[0] - p_m._coords[0]) < 1e-10
        assert abs(p_ft._coords[1] - p_m._coords[1]) < 1e-10
        assert abs(p_ft._coords[2] - p_m._coords[2]) < 1e-10

    def test_create_point_from_mismatched_dimensions_raises(self):
        """Test that creating point from quantities with different dimensions raises error."""
        x = Q(10.0, u.meter)
        y = Q(20.0, u.newton)  # Wrong dimension!

        with pytest.raises(ValueError, match="same dimension"):
            Point.from_quantities(x, y)


class TestPointCoordinateAccess:
    """Test accessing point coordinates as Quantities."""

    def test_access_x_coordinate(self):
        """Test accessing x coordinate as Quantity."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        x = p.x

        assert x.magnitude() == 10.0
        assert x.dim == u.meter.dim

    def test_access_y_coordinate(self):
        """Test accessing y coordinate as Quantity."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        y = p.y

        assert y.magnitude() == 20.0
        assert y.dim == u.meter.dim

    def test_access_z_coordinate(self):
        """Test accessing z coordinate as Quantity."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        z = p.z

        assert z.magnitude() == 30.0
        assert z.dim == u.meter.dim

    def test_coordinate_respects_display_unit(self):
        """Test that coordinates are displayed in preferred unit."""
        p = Point(10.0, 20.0, 30.0, unit=u.foot)

        x = p.x
        # Should display in feet
        assert abs(x.magnitude() - 10.0) < 1e-10


class TestPointOperations:
    """Test operations between points."""

    def test_point_subtraction_creates_vector(self):
        """Test that subtracting points creates a displacement vector."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(5.0, 10.0, 15.0, unit=u.meter)

        v = p1 - p2

        assert isinstance(v, Vector)
        assert v.u.magnitude() == 5.0  # 10 - 5
        assert v.v.magnitude() == 10.0  # 20 - 10
        assert v.w.magnitude() == 15.0  # 30 - 15

    def test_point_subtraction_different_dimensions_raises(self):
        """Test that subtracting points with different dimensions raises error."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(5.0, 10.0, 15.0, unit=u.newton)

        with pytest.raises(ValueError, match="different dimensions"):
            _ = p1 - p2

    def test_distance_between_points(self):
        """Test computing Euclidean distance between points."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(3.0, 4.0, 0.0, unit=u.meter)

        distance = p1.distance_to(p2)

        # 3-4-5 right triangle
        assert abs(distance.magnitude() - 5.0) < 1e-10

    def test_distance_3d_points(self):
        """Test distance calculation in 3D."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(1.0, 2.0, 2.0, unit=u.meter)

        distance = p1.distance_to(p2)

        # sqrt(1² + 2² + 2²) = sqrt(9) = 3
        expected = math.sqrt(1**2 + 2**2 + 2**2)
        assert abs(distance.magnitude() - expected) < 1e-10

    def test_distance_different_dimensions_raises(self):
        """Test that distance between points with different dimensions raises error."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(5.0, 10.0, 15.0, unit=u.newton)

        with pytest.raises(ValueError, match="different dimensions"):
            _ = p1.distance_to(p2)

    def test_displaced_point(self):
        """Test displacing a point by a vector."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        v = Vector(5.0, -10.0, 15.0, unit=u.meter)

        p_new = p.displaced(v)

        assert p_new.x.magnitude() == 15.0  # 10 + 5
        assert p_new.y.magnitude() == 10.0  # 20 - 10
        assert p_new.z.magnitude() == 45.0  # 30 + 15

    def test_displaced_point_with_scaling(self):
        """Test displacing a point by a scaled vector."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        v = Vector(1.0, 0.0, 0.0, unit=u.meter)

        p_new = p.displaced(v, times=5.0)

        assert p_new.x.magnitude() == 15.0  # 10 + 5*1
        assert p_new.y.magnitude() == 20.0
        assert p_new.z.magnitude() == 30.0

    def test_displaced_different_dimensions_raises(self):
        """Test that displacing with vector of different dimension raises error."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        v = Vector(5.0, 10.0, 15.0, unit=u.newton)

        with pytest.raises(ValueError, match="different dimension"):
            _ = p.displaced(v)


class TestPointUnitConversions:
    """Test unit conversion operations."""

    def test_convert_point_to_different_unit(self):
        """Test converting point to different display unit."""
        p_m = Point(10.0, 20.0, 30.0, unit=u.meter)
        p_ft = p_m.to_unit(u.foot)

        # 1 meter = 3.28084 feet
        expected_x = 10.0 * 3.28084
        expected_y = 20.0 * 3.28084
        expected_z = 30.0 * 3.28084

        assert abs(p_ft.x.magnitude() - expected_x) < 1e-4
        assert abs(p_ft.y.magnitude() - expected_y) < 1e-4
        assert abs(p_ft.z.magnitude() - expected_z) < 1e-4

    def test_convert_point_to_unit_by_string(self):
        """Test converting point using unit string."""
        p_m = Point(1000.0, 2000.0, 3000.0, unit=u.meter)
        p_km = p_m.to_unit("kilometer")

        assert abs(p_km.x.magnitude() - 1.0) < 1e-10
        assert abs(p_km.y.magnitude() - 2.0) < 1e-10
        assert abs(p_km.z.magnitude() - 3.0) < 1e-10

    def test_to_array_returns_display_values(self):
        """Test that to_array returns values in display unit."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        arr = p.to_array()

        assert arr[0] == 10.0
        assert arr[1] == 20.0
        assert arr[2] == 30.0

    def test_to_array_with_converted_unit(self):
        """Test to_array after unit conversion."""
        p_m = Point(1.0, 2.0, 3.0, unit=u.meter)
        p_cm = p_m.to_unit(u.centi_meter)

        arr = p_cm.to_array()

        # 1 m = 100 cm
        assert abs(arr[0] - 100.0) < 1e-10
        assert abs(arr[1] - 200.0) < 1e-10
        assert abs(arr[2] - 300.0) < 1e-10


class TestPointEquality:
    """Test point equality comparisons."""

    def test_equal_points(self):
        """Test that identical points are equal."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(10.0, 20.0, 30.0, unit=u.meter)

        assert p1 == p2

    def test_equal_points_different_units(self):
        """Test that points with same position but different units are equal."""
        p1 = Point(1.0, 2.0, 3.0, unit=u.meter)
        p2 = Point(100.0, 200.0, 300.0, unit=u.centi_meter)

        # Should be equal because internal SI values are the same
        assert p1 == p2

    def test_unequal_points(self):
        """Test that different points are not equal."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(11.0, 20.0, 30.0, unit=u.meter)

        assert p1 != p2

    def test_points_different_dimensions_not_equal(self):
        """Test that points with different dimensions are not equal."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(10.0, 20.0, 30.0, unit=u.newton)

        assert p1 != p2


class TestPointStringRepresentation:
    """Test point string formatting."""

    def test_str_representation(self):
        """Test string representation of point."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        s = str(p)

        assert "Point" in s
        assert "10" in s
        assert "20" in s
        assert "30" in s
        assert "m" in s

    def test_repr_representation(self):
        """Test repr representation of point."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        r = repr(p)

        assert "Point" in r


class TestPointEdgeCases:
    """Test edge cases and error conditions."""

    def test_zero_point(self):
        """Test creating point at origin."""
        p = Point(0.0, 0.0, 0.0, unit=u.meter)

        assert p.x.magnitude() == 0.0
        assert p.y.magnitude() == 0.0
        assert p.z.magnitude() == 0.0

    def test_negative_coordinates(self):
        """Test point with negative coordinates."""
        p = Point(-10.0, -20.0, -30.0, unit=u.meter)

        assert p.x.magnitude() == -10.0
        assert p.y.magnitude() == -20.0
        assert p.z.magnitude() == -30.0

    def test_distance_to_self_is_zero(self):
        """Test that distance from point to itself is zero."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)

        distance = p.distance_to(p)

        assert abs(distance.magnitude()) < 1e-10

    def test_displacement_by_zero_vector(self):
        """Test displacing point by zero vector."""
        p = Point(10.0, 20.0, 30.0, unit=u.meter)
        v = Vector(0.0, 0.0, 0.0, unit=u.meter)

        p_new = p.displaced(v)

        assert p_new == p

    def test_large_coordinates(self):
        """Test point with very large coordinates."""
        large_val = 1e10
        p = Point(large_val, large_val, large_val, unit=u.meter)

        assert p.x.magnitude() == large_val
        assert p.y.magnitude() == large_val
        assert p.z.magnitude() == large_val

    def test_small_coordinates(self):
        """Test point with very small coordinates."""
        small_val = 1e-10
        p = Point(small_val, small_val, small_val, unit=u.meter)

        assert abs(p.x.magnitude() - small_val) < 1e-20
