"""
Integration tests for Point and Vector classes working together.

Tests cover:
- Creating vectors from point differences
- Displacing points with vectors
- Complex geometric operations
- Real-world engineering scenarios
- Unit conversions in combined operations
"""

import math

from qnty.core import u
from qnty.spatial import Point, _Vector


class TestPointVectorIntegration:
    """Test Point and Vector working together."""

    def test_point_difference_creates_vector(self):
        """Test that subtracting points creates a vector."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        p2 = Point(5.0, 15.0, 25.0, unit=u.meter)

        v = p1 - p2

        assert isinstance(v, _Vector)
        assert v.u.magnitude() == 5.0
        assert v.v.magnitude() == 5.0
        assert v.w.magnitude() == 5.0

    def test_point_displacement_and_back(self):
        """Test displacing a point and returning to origin."""
        p1 = Point(10.0, 20.0, 30.0, unit=u.meter)
        v = _Vector(5.0, -10.0, 15.0, unit=u.meter)

        # Displace forward
        p2 = p1.displaced(v)

        # Displace back
        p3 = p2.displaced(-v)

        # Should be back at original position
        assert p3 == p1

    def test_round_trip_displacement(self):
        """Test creating vector from points, then using it to displace."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(3.0, 4.0, 5.0, unit=u.meter)

        # Create vector from point difference
        v = p2 - p1

        # Use it to displace origin
        p3 = p1.displaced(v)

        # Should arrive at p2
        assert p3 == p2

    def test_vector_magnitude_equals_distance(self):
        """Test that vector magnitude equals point distance."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(3.0, 4.0, 0.0, unit=u.meter)

        # Vector from p1 to p2
        v = p2 - p1

        # Distance from p1 to p2
        distance = p1.distance_to(p2)

        # Magnitudes should be equal
        assert v.magnitude is not None
        assert abs(v.magnitude.magnitude() - distance.magnitude()) < 1e-10

    def test_triangle_inequality(self):
        """Test triangle inequality: |a+b| <= |a| + |b|."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(3.0, 0.0, 0.0, unit=u.meter)
        p3 = Point(3.0, 4.0, 0.0, unit=u.meter)

        # Vectors forming a triangle
        v1 = p2 - p1  # (3, 0, 0)
        v2 = p3 - p2  # (0, 4, 0)
        v3 = p3 - p1  # (3, 4, 0) - should be v1 + v2

        # Check vector addition
        v_sum = v1 + v2
        assert v_sum == v3

        # Triangle inequality
        assert v_sum.magnitude is not None
        assert v1.magnitude is not None
        assert v2.magnitude is not None
        mag_sum = v_sum.magnitude.magnitude()
        mag1 = v1.magnitude.magnitude()
        mag2 = v2.magnitude.magnitude()

        assert mag_sum <= mag1 + mag2 + 1e-10


class TestGeometricScenarios:
    """Test real-world geometric scenarios."""

    def test_midpoint_calculation(self):
        """Test finding midpoint between two points."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(10.0, 20.0, 30.0, unit=u.meter)

        # Midpoint is p1 + (p2-p1)/2
        v = p2 - p1
        midpoint = p1.displaced(v, times=0.5)

        assert midpoint.x.magnitude() == 5.0
        assert midpoint.y.magnitude() == 10.0
        assert midpoint.z.magnitude() == 15.0

    def test_perpendicular_projection(self):
        """Test projecting a point onto a line."""
        # Line along x-axis through origin
        line_direction = _Vector(1.0, 0.0, 0.0, unit=u.meter)

        # Point off the line
        p = Point(5.0, 3.0, 0.0, unit=u.meter)
        origin = Point(0.0, 0.0, 0.0, unit=u.meter)

        # Vector from origin to point
        v = p - origin

        # Project onto line direction
        proj = v.projection_onto(line_direction)

        # Result should be along x-axis at x=5
        projected_point = origin.displaced(proj)

        assert abs(projected_point.x.magnitude() - 5.0) < 1e-10
        assert abs(projected_point.y.magnitude()) < 1e-10
        assert abs(projected_point.z.magnitude()) < 1e-10

    def test_circle_on_plane(self):
        """Test points on a circle in xy-plane."""
        center = Point(0.0, 0.0, 0.0, unit=u.meter)
        radius = 5.0

        # Points at 0, 90, 180, 270 degrees
        angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]

        for angle in angles:
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            p = Point(x, y, 0.0, unit=u.meter)

            # Distance to center should be radius
            dist = center.distance_to(p)
            assert abs(dist.magnitude() - radius) < 1e-10

    def test_vector_decomposition(self):
        """Test decomposing a vector into orthogonal components."""
        # Basis vectors
        e_x = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        e_y = _Vector(0.0, 1.0, 0.0, unit=u.meter)
        e_z = _Vector(0.0, 0.0, 1.0, unit=u.meter)

        # General vector
        v = _Vector(3.0, 4.0, 5.0, unit=u.meter)

        # Project onto each axis
        proj_x = v.projection_onto(e_x)
        proj_y = v.projection_onto(e_y)
        proj_z = v.projection_onto(e_z)

        # Sum of projections should equal original
        v_reconstructed = proj_x + proj_y + proj_z

        assert abs(v_reconstructed.u.magnitude() - v.u.magnitude()) < 1e-10
        assert abs(v_reconstructed.v.magnitude() - v.v.magnitude()) < 1e-10
        assert abs(v_reconstructed.w.magnitude() - v.w.magnitude()) < 1e-10


class TestUnitConversionsIntegrated:
    """Test unit conversions in integrated scenarios."""

    def test_point_displacement_different_units(self):
        """Test displacing point when vector has different display units."""
        p_m = Point(100.0, 200.0, 0.0, unit=u.meter)
        v_cm = _Vector(50.0, -100.0, 0.0, unit=u.centimeter)

        # Displacement should work (both are lengths)
        p_new = p_m.displaced(v_cm)

        # New point should be at (100.5, 199.0) meters
        # (50 cm = 0.5 m, -100 cm = -1.0 m)
        assert abs(p_new.x.magnitude() - 100.5) < 1e-10
        assert abs(p_new.y.magnitude() - 199.0) < 1e-10

    def test_distance_with_unit_conversion(self):
        """Test computing distance and converting result."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(1000.0, 0.0, 0.0, unit=u.meter)

        distance = p1.distance_to(p2)

        # Convert to kilometers
        distance_km = distance.to_unit.kilometer

        assert abs(distance_km.magnitude() - 1.0) < 1e-10

    def test_vector_operations_preserve_units(self):
        """Test that vector operations preserve internal SI consistency."""
        v1_m = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2_cm = _Vector(100.0, 0.0, 0.0, unit=u.centimeter)  # Also 1 meter

        # Both represent the same displacement
        v_sum = v1_m + v2_cm

        # Should be 2 meters total
        assert v_sum.magnitude is not None
        assert abs(v_sum.magnitude.magnitude() - 2.0) < 1e-10


class TestEngineeringScenarios:
    """Test realistic engineering scenarios."""

    def test_structural_node_displacement(self):
        """Test structural analysis node displacement scenario."""
        # Original position of a structural node
        original = Point(10.0, 5.0, 0.0, unit=u.meter)

        # Applied displacement (in mm, typical for structural analysis)
        displacement = _Vector(2.5, -1.8, 0.0, unit=u.millimeter)

        # New position
        deformed = original.displaced(displacement)

        # Verify in meters
        assert abs(deformed.x.magnitude() - 10.0025) < 1e-10
        assert abs(deformed.y.magnitude() - 4.9982) < 1e-10

    def test_surveying_traverse(self):
        """Test surveying traverse calculation."""
        # Starting point
        station_a = Point(1000.0, 2000.0, 100.0, unit=u.meter)

        # Traverse legs
        leg1 = _Vector(50.0, 30.0, 0.0, unit=u.meter)
        leg2 = _Vector(40.0, -20.0, 0.0, unit=u.meter)
        leg3 = _Vector(-30.0, 25.0, 0.0, unit=u.meter)

        # Compute positions
        station_b = station_a.displaced(leg1)
        station_c = station_b.displaced(leg2)
        station_d = station_c.displaced(leg3)

        # Final position
        assert abs(station_d.x.magnitude() - 1060.0) < 1e-10
        assert abs(station_d.y.magnitude() - 2035.0) < 1e-10
        assert abs(station_d.z.magnitude() - 100.0) < 1e-10

        # Verify closure error (should return to near starting point for a closed traverse)
        # For this open traverse, we can compute the total displacement
        total_displacement = leg1 + leg2 + leg3
        expected_final = station_a.displaced(total_displacement)

        assert expected_final == station_d

    def test_robot_path_planning(self):
        """Test robot end-effector path planning."""
        # Start position
        start = Point(0.0, 0.0, 0.5, unit=u.meter)

        # Move sequence
        move1 = _Vector(0.2, 0.0, 0.0, unit=u.meter)  # Forward
        move2 = _Vector(0.0, 0.15, 0.0, unit=u.meter)  # Right
        move3 = _Vector(0.0, 0.0, -0.1, unit=u.meter)  # Down

        # Execute path
        pos1 = start.displaced(move1)
        pos2 = pos1.displaced(move2)
        final = pos2.displaced(move3)

        # Final position
        assert abs(final.x.magnitude() - 0.2) < 1e-10
        assert abs(final.y.magnitude() - 0.15) < 1e-10
        assert abs(final.z.magnitude() - 0.4) < 1e-10

        # Total distance traveled
        assert move1.magnitude is not None
        assert move2.magnitude is not None
        assert move3.magnitude is not None
        total_distance = move1.magnitude.magnitude() + move2.magnitude.magnitude() + move3.magnitude.magnitude()
        expected_total = 0.2 + 0.15 + 0.1  # 0.45 m

        assert abs(total_distance - expected_total) < 1e-10

    def test_antenna_placement(self):
        """Test antenna positioning and line-of-sight calculation."""
        # Tower base
        tower_base = Point(0.0, 0.0, 0.0, unit=u.meter)

        # Antenna height
        antenna_height = _Vector(0.0, 0.0, 50.0, unit=u.meter)

        # Antenna position
        antenna = tower_base.displaced(antenna_height)

        # Receiver position (1 km away, 2m high)
        receiver = Point(1000.0, 0.0, 2.0, unit=u.meter)

        # Line-of-sight vector
        los = receiver - antenna

        # Verify it points downward (negative z component)
        assert los.w.magnitude() < 0

        # Calculate distance
        distance = antenna.distance_to(receiver)

        # Should be approximately sqrt(1000² + 48²) ≈ 1001.15 m
        expected = math.sqrt(1000**2 + 48**2)
        assert abs(distance.magnitude() - expected) < 1e-1


class TestVectorFieldOperations:
    """Test operations that might be used in vector field analysis."""

    def test_gradient_approximation(self):
        """Test finite difference approximation to a gradient."""
        # Sample points around a center
        center = Point(0.0, 0.0, 0.0, unit=u.meter)
        dx = 0.01
        dy = 0.01

        p_x_plus = Point(dx, 0.0, 0.0, unit=u.meter)
        p_y_plus = Point(0.0, dy, 0.0, unit=u.meter)

        # Vectors from center
        v_x = p_x_plus - center
        v_y = p_y_plus - center

        # These should be orthogonal
        assert v_x.is_perpendicular_to(v_y)

        # Magnitudes should match step sizes
        assert v_x.magnitude is not None
        assert v_y.magnitude is not None
        assert abs(v_x.magnitude.magnitude() - dx) < 1e-10
        assert abs(v_y.magnitude.magnitude() - dy) < 1e-10

    def test_circulation_around_loop(self):
        """Test vector circulation around a closed loop."""
        # Square loop in xy-plane
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(1.0, 0.0, 0.0, unit=u.meter)
        p3 = Point(1.0, 1.0, 0.0, unit=u.meter)
        p4 = Point(0.0, 1.0, 0.0, unit=u.meter)

        # Edges of the loop
        e1 = p2 - p1
        e2 = p3 - p2
        e3 = p4 - p3
        e4 = p1 - p4

        # Sum should be zero (closed loop)
        total = e1 + e2 + e3 + e4

        assert abs(total.u.magnitude()) < 1e-10
        assert abs(total.v.magnitude()) < 1e-10
        assert abs(total.w.magnitude()) < 1e-10


class TestNumericalStability:
    """Test numerical stability in various scenarios."""

    def test_very_small_displacements(self):
        """Test numerical stability with very small displacements."""
        p = Point(1000.0, 2000.0, 3000.0, unit=u.meter)
        v = _Vector(1e-10, 1e-10, 1e-10, unit=u.meter)

        p_new = p.displaced(v)

        # Should still be able to compute distance accurately
        distance = p.distance_to(p_new)

        expected = math.sqrt(3) * 1e-10
        # Use relative tolerance appropriate for the scale (1e-10)
        # Allow 0.1% relative error for very small values
        assert abs(distance.magnitude() - expected) < expected * 1e-3

    def test_large_coordinate_differences(self):
        """Test handling large coordinate differences."""
        p1 = Point(0.0, 0.0, 0.0, unit=u.meter)
        p2 = Point(1e6, 1e6, 1e6, unit=u.meter)

        v = p2 - p1
        distance = p1.distance_to(p2)

        # Magnitude should equal distance
        assert v.magnitude is not None
        assert abs(v.magnitude.magnitude() - distance.magnitude()) < 1e-3

    def test_nearly_parallel_vectors(self):
        """Test detection of nearly parallel vectors."""
        v1 = _Vector(1.0, 0.0, 0.0, unit=u.meter)
        v2 = _Vector(1.0, 1e-12, 0.0, unit=u.meter)

        # Should be detected as parallel with default tolerance
        assert v1.is_parallel_to(v2)

        # But not with very strict tolerance
        assert not v1.is_parallel_to(v2, tolerance=1e-15)
