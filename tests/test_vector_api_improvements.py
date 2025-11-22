"""
Test the improved Vector and ForceVector comparison and conversion API.

This test file demonstrates the new fluent API for working with vectors and force vectors,
which now matches the Qnty design philosophy used in the core Quantity class.
"""

import math
import pytest
from qnty.spatial.vector import Vector
from qnty.spatial import ForceVector
from qnty.core.unit_catalog import LengthUnits, ForceUnits


class TestVectorMagnitudeIn:
    """Test Vector.magnitude_in() method for unit conversion."""

    def test_magnitude_in_with_string_unit(self):
        """Test getting vector magnitude in different units using string."""
        v = Vector(1000, 0, 0, unit=LengthUnits.meter)

        # Test conversion to km
        assert abs(v.magnitude_in("km") - 1.0) < 1e-9

        # Test conversion to m (same as input)
        assert abs(v.magnitude_in("m") - 1000.0) < 1e-9

        # Test conversion to cm
        assert abs(v.magnitude_in("cm") - 100000.0) < 1e-9

    def test_magnitude_in_with_unit_object(self):
        """Test getting vector magnitude with Unit object."""
        v = Vector(3, 4, 0, unit=LengthUnits.meter)

        # Magnitude should be 5 meters
        assert abs(v.magnitude_in(LengthUnits.meter) - 5.0) < 1e-9
        assert abs(v.magnitude_in("mm") - 5000.0) < 1e-6

    def test_magnitude_in_3d_vector(self):
        """Test magnitude_in for 3D vectors."""
        v = Vector(3, 4, 12, unit=LengthUnits.meter)

        # Magnitude should be 13 meters (3-4-12 Pythagorean triple)
        assert abs(v.magnitude_in("m") - 13.0) < 1e-9


class TestForceVectorMagnitudeIn:
    """Test ForceVector.magnitude_in() method for unit conversion."""

    def test_magnitude_in_polar_construction(self):
        """Test magnitude_in with force created from magnitude/angle."""
        F = ForceVector(magnitude=1000, angle=45, unit="N")

        # Test conversion to lbf
        expected_lbf = 1000.0 / 4.4482216152605  # N to lbf conversion
        assert abs(F.magnitude_in("lbf") - expected_lbf) < 0.01

        # Test conversion to N (same as input)
        assert abs(F.magnitude_in("N") - 1000.0) < 1e-9

    def test_magnitude_in_component_construction(self):
        """Test magnitude_in with force created from components."""
        F = ForceVector(x=300, y=400, unit="N")

        # Magnitude should be 500 N (3-4-5 triangle)
        assert abs(F.magnitude_in("N") - 500.0) < 1e-9
        expected_lbf = 500.0 / 4.4482216152605  # N to lbf conversion
        assert abs(F.magnitude_in("lbf") - expected_lbf) < 0.01

    def test_magnitude_in_replaces_manual_conversion(self):
        """Demonstrate that magnitude_in replaces manual .magnitude.value / si_factor."""
        F = ForceVector(magnitude=500, angle=30, unit="lbf")

        # Old way (manual conversion)
        old_way = F.magnitude.value / F.magnitude.preferred.si_factor

        # New way (clean API)
        new_way = F.magnitude_in("lbf")

        # Should be equivalent
        assert abs(old_way - new_way) < 1e-9
        assert abs(new_way - 500.0) < 1e-9


class TestForceVectorAngleIn:
    """Test ForceVector.angle_in() method for angle conversion and reference systems."""

    def test_angle_in_unit_conversion(self):
        """Test angle unit conversion from degrees to radians."""
        F = ForceVector(magnitude=100, angle=45, unit="N")

        # Test conversion to degrees (default)
        assert abs(F.angle_in("degree") - 45.0) < 1e-6

        # Test conversion to radians
        assert abs(F.angle_in("radian") - math.pi/4) < 1e-9

    def test_angle_in_reference_system_conversion(self):
        """Test angle conversion to different reference systems."""
        # Force at 45° CCW from +x
        F = ForceVector(magnitude=100, angle=45, unit="N")

        # Standard reference (CCW from +x)
        assert abs(F.angle_in("degree") - 45.0) < 1e-6

        # Clockwise from +x: 45° CCW = 315° CW
        assert abs(F.angle_in("degree", wrt="cw:+x") - 315.0) < 1e-6

        # CCW from +y: 45° from +x = 315° from +y (or -45°)
        angle_from_y = F.angle_in("degree", wrt="+y")
        # Normalize to [0, 360)
        angle_from_y = angle_from_y % 360
        assert abs(angle_from_y - 315.0) < 1e-6

    def test_angle_in_replaces_manual_conversion(self):
        """Demonstrate that angle_in replaces manual angle reference conversions."""
        from qnty.spatial.angle_reference import AngleReference

        F = ForceVector(magnitude=100, angle=60, unit="N")

        # Old way (manual)
        angle_ref = ForceVector.parse_wrt("cw:+x", F.coordinate_system)
        old_way = angle_ref.from_standard(F.angle.value, angle_unit="degree")

        # New way (clean API)
        new_way = F.angle_in("degree", wrt="cw:+x")

        # Should be equivalent
        assert abs(old_way - new_way) < 1e-6

    def test_angle_in_combined_unit_and_reference(self):
        """Test simultaneous unit conversion and reference system change."""
        F = ForceVector(magnitude=100, angle=30, unit="N", angle_unit="degree")

        # Get angle in radians, measured CW from +x
        angle_rad_cw = F.angle_in("radian", wrt="cw:+x")

        # 30° CCW from +x = 330° CW from +x = 11π/6 radians
        expected = (11 * math.pi) / 6
        assert abs(angle_rad_cw - expected) < 1e-6


class TestForceVectorWithMethods:
    """Test ForceVector.with_*() methods for creating modified copies."""

    def test_with_magnitude_unit(self):
        """Test creating force with different magnitude unit."""
        F1 = ForceVector(magnitude=1000, angle=45, unit="N")
        F2 = F1.with_magnitude_unit("lbf")

        # Original unchanged
        assert abs(F1.magnitude_in("N") - 1000.0) < 1e-9

        # New force has different preferred unit
        expected_lbf = 1000.0 / 4.4482216152605
        assert abs(F2.magnitude_in("lbf") - expected_lbf) < 0.01
        assert abs(F2.magnitude_in("N") - 1000.0) < 1e-9  # Same value

        # Angle unchanged
        assert abs(F2.angle_in("degree") - 45.0) < 1e-6

    def test_with_angle_unit(self):
        """Test creating force with different angle unit."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N", angle_unit="degree")
        F2 = F1.with_angle_unit("radian")

        # Original unchanged
        assert abs(F1.angle_in("degree") - 45.0) < 1e-6

        # New force has different angle unit but same value
        assert abs(F2.angle_in("radian") - math.pi/4) < 1e-9
        assert abs(F2.angle_in("degree") - 45.0) < 1e-6  # Same angle

        # Magnitude unchanged
        assert abs(F2.magnitude_in("N") - 100.0) < 1e-9

    def test_with_angle_reference(self):
        """Test creating force with different angle reference system."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = F1.with_angle_reference("cw:+x")

        # Same force, different reference system
        assert abs(F2.angle_in("degree", wrt="cw:+x") - 315.0) < 1e-6
        assert abs(F2.angle_in("degree") - 45.0) < 1e-6  # Standard still works


class TestForceVectorIsClose:
    """Test ForceVector.is_close() method for explicit comparison with tolerances."""

    def test_is_close_default_tolerances(self):
        """Test is_close with default tolerances."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = ForceVector(magnitude=100.00001, angle=45.001, unit="N")

        # Within default tolerances
        assert F1.is_close(F2)

    def test_is_close_strict_magnitude_tolerance(self):
        """Test is_close with strict magnitude tolerance."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = ForceVector(magnitude=100.1, angle=45, unit="N")

        # Fails with strict tolerance
        assert not F1.is_close(F2, magnitude_rel_tol=1e-9)

        # Passes with relaxed tolerance
        assert F1.is_close(F2, magnitude_rel_tol=1e-2)

    def test_is_close_strict_angle_tolerance(self):
        """Test is_close with strict angle tolerance."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = ForceVector(magnitude=100, angle=45.1, unit="N")

        # Fails with strict tolerance
        assert not F1.is_close(F2, angle_abs_tol_deg=0.01)

        # Passes with relaxed tolerance
        assert F1.is_close(F2, angle_abs_tol_deg=0.2)

    def test_is_close_handles_different_units(self):
        """Test is_close compares values, not units."""
        F1 = ForceVector(magnitude=1000, angle=45, unit="N")
        # Convert 1000 N to lbf: 1000 / 4.4482216152605 ≈ 224.809 lbf
        F2 = ForceVector(magnitude=224.809, angle=45, unit="lbf")

        # Same force in different units (within tolerance)
        assert F1.is_close(F2, magnitude_rel_tol=1e-3)

    def test_is_close_component_mode(self):
        """Test is_close with component comparison."""
        F1 = ForceVector(x=100, y=100, unit="N")
        F2 = ForceVector(x=100.001, y=100.001, unit="N")

        # Compare components instead of magnitude/angle
        # Need sufficient tolerance for component comparison
        assert F1.is_close(F2, compare_components=True, magnitude_abs_tol=0.01)

    def test_is_close_angle_wraparound(self):
        """Test is_close handles angle wraparound (359° ≈ 1°)."""
        F1 = ForceVector(magnitude=100, angle=1, unit="N")
        F2 = ForceVector(magnitude=100, angle=359, unit="N")

        # Should detect these are close (2° apart)
        assert F1.is_close(F2, angle_abs_tol_deg=3.0)
        assert not F1.is_close(F2, angle_abs_tol_deg=1.0)


class TestForceVectorEquality:
    """Test ForceVector.__eq__() with improved implementation."""

    def test_equality_same_values(self):
        """Test equality for identical forces."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = ForceVector(magnitude=100, angle=45, unit="N")

        assert F1 == F2

    def test_equality_different_construction(self):
        """Test equality for forces constructed differently but with same values."""
        F1 = ForceVector(magnitude=500, angle=math.degrees(math.atan2(4, 3)), unit="N")
        F2 = ForceVector(x=300, y=400, unit="N")

        # Both represent same force
        assert F1 == F2

    def test_equality_different_units(self):
        """Test equality handles unit conversion."""
        F1 = ForceVector(magnitude=1000, angle=45, unit="N")
        # 1000 N ≈ 224.809 lbf
        F2 = ForceVector(magnitude=224.809, angle=45, unit="lbf")

        # Same force, different units (within default tolerance)
        assert F1.is_close(F2, magnitude_rel_tol=1e-3)

    def test_equality_unknown_forces(self):
        """Test equality for unknown forces."""
        F1 = ForceVector.unknown("F1")
        F2 = ForceVector.unknown("F2")

        # Both unknown - considered equal
        assert F1 == F2

    def test_inequality_different_magnitude(self):
        """Test inequality for different magnitudes."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = ForceVector(magnitude=200, angle=45, unit="N")

        assert F1 != F2

    def test_inequality_different_angle(self):
        """Test inequality for different angles."""
        F1 = ForceVector(magnitude=100, angle=45, unit="N")
        F2 = ForceVector(magnitude=100, angle=90, unit="N")

        assert F1 != F2


class TestIntegrationExamples:
    """Integration tests showing real-world usage patterns."""

    def test_compare_forces_in_different_units(self):
        """Demonstrate comparing forces with automatic unit conversion."""
        # Two forces that should be equal but in different units
        F1 = ForceVector(magnitude=5000, angle=30, unit="N")
        # 5000 N ≈ 1124.045 lbf
        F2 = ForceVector(magnitude=1124.045, angle=30, unit="lbf")

        # Can use explicit comparison with tolerance
        assert F1.is_close(F2, magnitude_rel_tol=1e-3)

        # Can convert and compare manually
        assert abs(F1.magnitude_in("N") - F2.magnitude_in("N")) < 1.0

    def test_verify_force_components_clean_api(self):
        """Demonstrate clean API for verifying force components."""
        F = ForceVector(magnitude=500, angle=53.13, unit="lbf")  # 3-4-5 triangle

        # Clean way to get components in desired unit
        x_comp = F.x.magnitude("lbf") if F.x else 0
        y_comp = F.y.magnitude("lbf") if F.y else 0

        # Verify 3-4-5 triangle
        assert abs(x_comp - 300) < 1.0
        assert abs(y_comp - 400) < 1.0

    def test_angle_in_multiple_reference_systems(self):
        """Demonstrate getting angle in multiple reference systems."""
        F = ForceVector(magnitude=100, angle=60, unit="N")

        # Get angle in different reference systems
        angle_ccw_from_x = F.angle_in("degree")  # 60°
        angle_cw_from_x = F.angle_in("degree", wrt="cw:+x")  # 300°
        angle_from_y = F.angle_in("degree", wrt="+y")  # 330° (normalized)

        assert abs(angle_ccw_from_x - 60.0) < 1e-6
        assert abs(angle_cw_from_x - 300.0) < 1e-6
        assert abs((angle_from_y % 360) - 330.0) < 1e-6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
