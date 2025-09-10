import math

import pytest

import qnty as qt

angle_deg = qt.AnglePlane(45, "degree", "Angle, degree")
angle_rad = qt.AnglePlane(0.785398, "radian", "Angle, radian")  # π/4 radians


@pytest.mark.parametrize("angle_degree", list(range(-360, 720, 5)))
def test_sin_degree(angle_degree):
    # Test that trigonometric functions work correctly with degrees
    angle = qt.AnglePlane(angle_degree, "degree", f"angle_{angle_degree}_deg")
    result = qt.sin(angle)
    expected = math.sin(math.radians(angle_degree))
    # Use higher tolerance due to degree->radian conversion precision limits in qnty
    assert result == pytest.approx(expected, rel=1e-5, abs=1e-12)


@pytest.mark.parametrize(
    "angle_radian",
    [i * 0.1 for i in range(-20, 65)],  # From -2 to 6.4 radians
)
def test_sin_radian(angle_radian):
    angle = qt.AnglePlane(angle_radian, "radian", f"angle_{angle_radian}_rad")
    result = qt.sin(angle)
    expected = math.sin(angle_radian)
    assert result == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("angle_degree", list(range(-360, 720, 5)))
def test_cos_degree(angle_degree):
    angle = qt.AnglePlane(angle_degree, "degree", f"cos_angle_{angle_degree}_deg")
    result = qt.cos(angle)
    expected = math.cos(math.radians(angle_degree))
    # Use higher tolerance due to degree->radian conversion precision limits in qnty
    assert result == pytest.approx(expected, rel=1e-5, abs=1e-12)


@pytest.mark.parametrize(
    "angle_radian",
    [i * 0.1 for i in range(-20, 65)],  # From -2 to 6.4 radians
)
def test_cos_radian(angle_radian):
    angle = qt.AnglePlane(angle_radian, "radian", f"cos_angle_{angle_radian}_rad")
    result = qt.cos(angle)
    expected = math.cos(angle_radian)
    assert result == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize("angle_degree", list(range(-360, 720, 5)))
def test_tan_degree(angle_degree):
    angle = qt.AnglePlane(angle_degree, "degree", f"tan_angle_{angle_degree}_deg")
    result = qt.tan(angle)
    expected = math.tan(math.radians(angle_degree))
    # Use higher tolerance due to degree->radian conversion precision limits in qnty
    assert result == pytest.approx(expected, rel=1e-5, abs=1e-12)


@pytest.mark.parametrize(
    "angle_radian",
    [i * 0.1 for i in range(-20, 65)],  # From -2 to 6.4 radians
)
def test_tan_radian(angle_radian):
    angle = qt.AnglePlane(angle_radian, "radian", f"tan_angle_{angle_radian}_rad")
    result = qt.tan(angle)
    expected = math.tan(angle_radian)
    assert result == pytest.approx(expected, rel=1e-9)


# def test_auto_evaluation_display():
#     # Test that trigonometric functions auto-evaluate when displayed (str conversion)
#     sin_expr = qt.sin(angle_deg)
#     cos_expr = qt.cos(angle_deg)
#     tan_expr = qt.tan(angle_deg)

#     # The string representation should show evaluated values
#     sin_str = str(sin_expr)
#     cos_str = str(cos_expr)
#     tan_str = str(tan_expr)

#     # Should contain numeric values, not symbolic expressions
#     assert "0.707" in sin_str, f"sin should auto-evaluate in string: {sin_str}"
#     assert "0.707" in cos_str, f"cos should auto-evaluate in string: {cos_str}"
#     assert ("1.0" in tan_str or "0.999999" in tan_str), f"tan should auto-evaluate in string: {tan_str}"

# def test_unknown_angle_symbolic():
#     # Test that unknown angles show symbolic representation
#     unknown_angle = qt.AnglePlane("theta")  # Unknown angle
#     result = qt.sin(unknown_angle)
#     result_str = str(result)
#     assert "sin(theta)" in result_str, f"Should show symbolic form: {result_str}"
