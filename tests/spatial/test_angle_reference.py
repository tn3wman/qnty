"""
Tests for AngleReference class.

Tests the angle reference system that allows specifying:
- Different reference axes (positive x, positive y, custom vectors)
- Measurement direction (counterclockwise or clockwise)
- Conversion between different angle reference systems
"""

import math

import pytest

from qnty.spatial.angle_reference import AngleDirection, AngleReference
from qnty.spatial import _Vector


class TestAngleReference:
    """Test AngleReference class."""

    def test_standard_reference(self):
        """Test standard angle reference (CCW from +x)."""
        ref = AngleReference.standard()
        assert ref.axis_angle == 0.0
        assert ref.direction == AngleDirection.COUNTERCLOCKWISE
        assert ref.axis_label == "+x"
        assert "counterclockwise from +x-axis" in ref.description

    def test_from_axis_positive_x(self):
        """Test creating reference from +x axis."""
        ref = AngleReference.from_axis("+x")
        assert ref.axis_angle == 0.0
        assert ref.direction == AngleDirection.COUNTERCLOCKWISE

    def test_from_axis_positive_y(self):
        """Test creating reference from +y axis."""
        ref = AngleReference.from_axis("+y")
        assert math.isclose(ref.axis_angle, math.radians(90), abs_tol=1e-9)
        assert ref.direction == AngleDirection.COUNTERCLOCKWISE

    def test_from_axis_negative_x(self):
        """Test creating reference from -x axis."""
        ref = AngleReference.from_axis("-x")
        assert math.isclose(ref.axis_angle, math.radians(180), abs_tol=1e-9)
        assert ref.direction == AngleDirection.COUNTERCLOCKWISE

    def test_from_axis_clockwise(self):
        """Test creating clockwise reference."""
        ref = AngleReference.from_axis("+x", direction="clockwise")
        assert ref.axis_angle == 0.0
        assert ref.direction == AngleDirection.CLOCKWISE

    def test_to_standard_ccw_from_x(self):
        """Test converting CCW from +x to standard (no change)."""
        ref = AngleReference.standard()
        # 30° CCW from +x should remain 30° in standard
        angle_standard = ref.to_standard(30, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(30), abs_tol=1e-9)

    def test_to_standard_cw_from_x(self):
        """Test converting CW from +x to standard."""
        ref = AngleReference.from_axis("+x", direction="clockwise")
        # 30° CW from +x = -30° CCW from +x = 330° CCW from +x
        angle_standard = ref.to_standard(30, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(330), abs_tol=1e-6)

    def test_to_standard_ccw_from_y(self):
        """Test converting CCW from +y to standard."""
        ref = AngleReference.from_axis("+y")
        # 0° CCW from +y = 90° CCW from +x
        angle_standard = ref.to_standard(0, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(90), abs_tol=1e-9)

        # 90° CCW from +y = 180° CCW from +x
        angle_standard = ref.to_standard(90, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(180), abs_tol=1e-6)

    def test_to_standard_cw_from_y(self):
        """Test converting CW from +y to standard."""
        ref = AngleReference.from_axis("+y", direction="clockwise")
        # 0° CW from +y = 90° CCW from +x (same as reference axis)
        angle_standard = ref.to_standard(0, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(90), abs_tol=1e-9)

        # 90° CW from +y = 0° CCW from +x
        angle_standard = ref.to_standard(90, angle_unit="degree")
        assert math.isclose(angle_standard, 0.0, abs_tol=1e-6)

    def test_from_standard_ccw_from_x(self):
        """Test converting standard to CCW from +x (no change)."""
        ref = AngleReference.standard()
        # 30° CCW from +x in standard should remain 30°
        angle_ref = ref.from_standard(math.radians(30), angle_unit="degree")
        assert math.isclose(angle_ref, 30, abs_tol=1e-6)

    def test_from_standard_cw_from_x(self):
        """Test converting standard to CW from +x."""
        ref = AngleReference.from_axis("+x", direction="clockwise")
        # 330° CCW from +x = 30° CW from +x
        angle_ref = ref.from_standard(math.radians(330), angle_unit="degree")
        assert math.isclose(angle_ref, 30, abs_tol=1e-6)

    def test_from_standard_ccw_from_y(self):
        """Test converting standard to CCW from +y."""
        ref = AngleReference.from_axis("+y")
        # 90° CCW from +x = 0° CCW from +y
        angle_ref = ref.from_standard(math.radians(90), angle_unit="degree")
        assert math.isclose(angle_ref, 0, abs_tol=1e-6)

        # 180° CCW from +x = 90° CCW from +y
        angle_ref = ref.from_standard(math.radians(180), angle_unit="degree")
        assert math.isclose(angle_ref, 90, abs_tol=1e-6)

    def test_custom_reference_axis(self):
        """Test custom reference axis at 30°."""
        ref = AngleReference(axis_angle=30, direction="counterclockwise", axis_label="custom")
        # 0° from custom axis = 30° from +x
        angle_standard = ref.to_standard(0, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(30), abs_tol=1e-9)

        # 45° from custom axis = 75° from +x
        angle_standard = ref.to_standard(45, angle_unit="degree")
        assert math.isclose(angle_standard, math.radians(75), abs_tol=1e-6)

    def test_roundtrip_conversion(self):
        """Test that converting to standard and back gives original angle."""
        ref = AngleReference.from_axis("+y", direction="clockwise")
        original_angle = 45.0  # degrees

        # Convert to standard and back
        standard = ref.to_standard(original_angle, angle_unit="degree")
        back_to_ref = ref.from_standard(standard, angle_unit="degree")

        assert math.isclose(back_to_ref, original_angle, abs_tol=1e-6)

    def test_equality(self):
        """Test equality comparison."""
        ref1 = AngleReference.standard()
        ref2 = AngleReference(axis_angle=0, direction="counterclockwise")
        ref3 = AngleReference.from_axis("+x", direction="clockwise")

        assert ref1 == ref2  # Same axis and direction
        assert ref1 != ref3  # Different direction

    def test_string_representation(self):
        """Test string representation."""
        ref = AngleReference.from_axis("+y", direction="clockwise")
        assert "clockwise" in str(ref).lower()
        assert "+y" in str(ref)


class TestForceVectorWithAngleReference:
    """Test ForceVector with angle references."""

    def test_force_with_standard_reference(self):
        """Test force with standard angle reference (default)."""
        # 30° CCW from +x
        force = _Vector(magnitude=100, angle=30, unit="N", name="F")
        assert force.angle_reference == AngleReference.standard()

        # Components should be correct
        assert force.x is not None
        assert force.y is not None
        assert math.isclose(force.x.value, 100 * math.cos(math.radians(30)), rel_tol=1e-6)
        assert math.isclose(force.y.value, 100 * math.sin(math.radians(30)), rel_tol=1e-6)

    def test_force_with_cw_from_x_reference(self):
        """Test force with clockwise from +x reference."""
        # 30° CW from +x = 330° CCW from +x
        ref = AngleReference.from_axis("+x", direction="clockwise")
        force = _Vector(magnitude=100, angle=30, unit="N", name="F", angle_reference=ref)

        # Components should be at 330° standard
        assert force.x is not None
        assert force.y is not None
        assert math.isclose(force.x.value, 100 * math.cos(math.radians(330)), rel_tol=1e-6)
        assert math.isclose(force.y.value, 100 * math.sin(math.radians(330)), rel_tol=1e-6)

    def test_force_with_ccw_from_y_reference(self):
        """Test force with CCW from +y reference."""
        # 45° CCW from +y = 135° CCW from +x
        ref = AngleReference.from_axis("+y", direction="counterclockwise")
        force = _Vector(magnitude=100, angle=45, unit="N", name="F", angle_reference=ref)

        # Components should be at 135° standard
        assert force.x is not None
        assert force.y is not None
        assert math.isclose(force.x.value, 100 * math.cos(math.radians(135)), rel_tol=1e-6)
        assert math.isclose(force.y.value, 100 * math.sin(math.radians(135)), rel_tol=1e-6)

    def test_force_with_cw_from_y_reference(self):
        """Test force with CW from +y reference."""
        # 45° CW from +y = 45° CCW from +x
        ref = AngleReference.from_axis("+y", direction="clockwise")
        force = _Vector(magnitude=100, angle=45, unit="N", name="F", angle_reference=ref)

        # Components should be at 45° standard
        assert force.x is not None
        assert force.y is not None
        assert math.isclose(force.x.value, 100 * math.cos(math.radians(45)), rel_tol=1e-6)
        assert math.isclose(force.y.value, 100 * math.sin(math.radians(45)), rel_tol=1e-6)

    def test_problem_2_6_angle_reference(self):
        """
        Test Problem 2-6 scenario: angle measured clockwise from positive u axis.

        This tests the real-world use case from the textbook problems.
        """
        # Problem 2-6 asks for "direction measured clockwise from the positive u axis"
        # If u-axis is at 0° and we measure clockwise, we need CW from +u reference
        ref_cw_from_u = AngleReference.from_axis("+x", direction="clockwise")  # u is at 0° (same as +x)

        # Example: if the answer is 1.22° clockwise from +u
        # That means the force is at 358.78° CCW from +x (standard)
        force_result = _Vector(magnitude=8026, angle=1.22, unit="N", name="F_R", angle_reference=ref_cw_from_u)

        # Check internal angle (should be 358.78° in standard form)
        assert force_result._angle is not None
        standard_angle_deg = math.degrees(force_result._angle.value)
        assert math.isclose(standard_angle_deg, 358.78, abs_tol=0.1)

    def test_unknown_force_with_angle_reference(self):
        """Test unknown force with known angle in custom reference system."""
        ref = AngleReference.from_axis("+x", direction="clockwise")
        force = _Vector.unknown("F", angle=30, angle_unit="degree", angle_reference=ref)

        assert not force.is_known
        assert force.angle is not None
        # Angle should be stored as 330° (standard form)
        assert math.isclose(math.degrees(force.angle.value), 330, abs_tol=1e-6)

    def test_angle_reference_preservation_in_unknown(self):
        """Test that angle_reference is preserved when creating unknown force."""
        ref = AngleReference.from_axis("+y", direction="clockwise")
        force = _Vector.unknown("F", angle=45, angle_reference=ref)

        assert force.angle_reference == ref
        assert force.angle_reference.direction == AngleDirection.CLOCKWISE


class TestForceVectorWrtParameter:
    """Test ForceVector with wrt (with respect to) parameter."""

    def test_wrt_standard(self):
        """Test wrt='+x' (standard reference)."""
        F1 = _Vector(magnitude=100, angle=30, unit="N", wrt="+x")
        assert F1.angle_reference.direction == AngleDirection.COUNTERCLOCKWISE
        assert F1.angle_reference.axis_angle == 0.0

    def test_wrt_clockwise_from_x(self):
        """Test wrt='cw:+x' (clockwise from +x)."""
        F2 = _Vector(magnitude=100, angle=30, unit="N", wrt="cw:+x")
        assert F2.angle_reference.direction == AngleDirection.CLOCKWISE
        # 30° CW from +x = 330° CCW from +x
        assert math.isclose(math.degrees(F2._angle.value), 330, abs_tol=1e-6)

    def test_wrt_y_axis(self):
        """Test wrt='+y' (CCW from +y)."""
        F3 = _Vector(magnitude=100, angle=45, unit="N", wrt="+y")
        # 45° CCW from +y = 135° CCW from +x
        assert math.isclose(math.degrees(F3._angle.value), 135, abs_tol=1e-6)

    def test_wrt_cw_from_y(self):
        """Test wrt='cw:+y' (CW from +y)."""
        F4 = _Vector(magnitude=100, angle=45, unit="N", wrt="cw:+y")
        # 45° CW from +y = 45° CCW from +x
        assert math.isclose(math.degrees(F4._angle.value), 45, abs_tol=1e-6)

    def test_wrt_negative_x(self):
        """Test wrt='-x' (CCW from -x)."""
        F5 = _Vector(magnitude=100, angle=30, unit="N", wrt="-x")
        # 30° CCW from -x (180°) = 210° CCW from +x
        assert math.isclose(math.degrees(F5._angle.value), 210, abs_tol=1e-6)

    def test_wrt_with_coordinate_system_axis(self):
        """Test wrt with custom coordinate system axes."""
        from qnty.spatial.coordinate_system import CoordinateSystem

        # Create u-v system
        uv_system = CoordinateSystem.from_angle_between("u", "v", axis1_angle=0, angle_between=75)

        # Use wrt='u' to reference the u-axis
        F6 = _Vector(magnitude=100, angle=30, unit="N", wrt="u", coordinate_system=uv_system)
        # Since u is at 0°, 30° from u = 30° from +x
        assert math.isclose(math.degrees(F6._angle.value), 30, abs_tol=1e-6)

    def test_wrt_cw_from_custom_axis(self):
        """Test wrt='cw:v' with custom coordinate system."""
        from qnty.spatial.coordinate_system import CoordinateSystem

        # Create u-v system (v at 75°)
        uv_system = CoordinateSystem.from_angle_between("u", "v", axis1_angle=0, angle_between=75)

        # Use wrt='cw:v' to reference v-axis clockwise
        F7 = _Vector(magnitude=100, angle=30, unit="N", wrt="cw:v", coordinate_system=uv_system)
        # 30° CW from v (75°) = 75° - 30° = 45° CCW from +x
        assert math.isclose(math.degrees(F7._angle.value), 45, abs_tol=1e-6)

    def test_wrt_unknown_force(self):
        """Test wrt parameter with unknown force."""
        F8 = _Vector.unknown("F", angle=30, wrt="cw:+x")
        assert not F8.is_known
        # 30° CW from +x = 330° CCW from +x
        assert math.isclose(math.degrees(F8._angle.value), 330, abs_tol=1e-6)

    def test_wrt_and_angle_reference_conflict(self):
        """Test that specifying both wrt and angle_reference raises error."""
        ref = AngleReference.from_axis("+y")
        with pytest.raises(ValueError, match="Cannot specify both"):
            _Vector(magnitude=100, angle=30, unit="N", wrt="+x", angle_reference=ref)

    def test_wrt_invalid_direction(self):
        """Test that invalid direction in wrt raises error."""
        with pytest.raises(ValueError, match="Invalid direction"):
            _Vector(magnitude=100, angle=30, unit="N", wrt="invalid:+x")

    def test_wrt_invalid_axis_not_in_coordinate_system(self):
        """Test that using axis not in coordinate system raises error."""
        # Standard x-y coordinate system doesn't have u-axis
        with pytest.raises(ValueError, match="Invalid wrt axis 'u'"):
            _Vector(magnitude=100, angle=30, unit="N", wrt="u")

    def test_wrt_valid_axis_in_custom_coordinate_system(self):
        """Test that using axis from coordinate system works."""
        from qnty.spatial.coordinate_system import CoordinateSystem

        # Create u-v system
        uv_system = CoordinateSystem.from_angle_between("u", "v", axis1_angle=0, angle_between=75)

        # Using u or v should work
        F1 = _Vector(magnitude=100, angle=30, unit="N", wrt="u", coordinate_system=uv_system)
        assert F1.angle_reference.axis_label == "u"

        F2 = _Vector(magnitude=100, angle=30, unit="N", wrt="cw:v", coordinate_system=uv_system)
        assert F2.angle_reference.axis_label == "v"

    def test_wrt_invalid_axis_not_in_custom_coordinate_system(self):
        """Test that using wrong axis for coordinate system raises error."""
        from qnty.spatial.coordinate_system import CoordinateSystem

        # Create u-v system (no 'w' axis)
        uv_system = CoordinateSystem.from_angle_between("u", "v", axis1_angle=0, angle_between=75)

        # Using w should fail
        with pytest.raises(ValueError, match="Invalid wrt axis 'w'"):
            _Vector(magnitude=100, angle=30, unit="N", wrt="w", coordinate_system=uv_system)
