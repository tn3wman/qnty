"""
Tests for Quantity comparison methods
=====================================

Tests that comparison operations properly account for units.
"""

import pytest

from qnty.core.quantity import Q, Quantity


class TestQuantityComparisons:
    """Test Quantity comparison methods with unit conversions."""

    def test_equality_same_units(self):
        """Test equality between quantities with the same units."""
        q1 = Q(100, "meter")
        q2 = Q(100, "meter")
        q3 = Q(200, "meter")

        assert q1 == q2
        assert not (q1 == q3)
        assert q1 != q3
        assert not (q1 != q2)

    def test_equality_different_units(self):
        """Test equality between quantities with different but compatible units."""
        # 1 meter = 100 centimeters = 1000 millimeters
        q_m = Q(1, "meter")
        q_cm = Q(100, "centimeter")
        q_mm = Q(1000, "millimeter")
        q_km = Q(0.001, "kilometer")

        assert q_m == q_cm
        assert q_m == q_mm
        assert q_m == q_km
        assert q_cm == q_mm
        assert q_cm == q_km
        assert q_mm == q_km

    def test_equality_incompatible_dimensions(self):
        """Test that quantities with different dimensions are not equal."""
        length = Q(100, "meter")
        time = Q(100, "second")

        assert length != time
        assert not (length == time)

    def test_inequality_same_units(self):
        """Test inequality operations with same units."""
        q1 = Q(100, "meter")
        q2 = Q(200, "meter")
        q3 = Q(100, "meter")

        assert q1 < q2
        assert q1 <= q2
        assert q1 <= q3
        assert q2 > q1
        assert q2 >= q1
        assert q3 >= q1

    def test_inequality_different_units(self):
        """Test inequality operations with different but compatible units."""
        # Test with length units
        q_m = Q(1, "meter")
        q_cm = Q(150, "centimeter")  # 1.5 meters
        q_mm = Q(500, "millimeter")  # 0.5 meters

        assert q_mm < q_m
        assert q_mm < q_cm
        assert q_m < q_cm

        assert q_cm > q_m
        assert q_cm > q_mm
        assert q_m > q_mm

        assert q_mm <= q_m
        assert q_m <= q_cm
        assert q_cm >= q_m
        assert q_m >= q_mm

    def test_comparison_with_unknown_quantities(self):
        """Test that comparisons with unknown quantities raise errors."""
        known = Q(100, "meter")
        unknown = Quantity.unknown("x", known.dim)

        with pytest.raises(ValueError, match="Cannot compare unknown quantities"):
            _ = known < unknown

        with pytest.raises(ValueError, match="Cannot compare unknown quantities"):
            _ = known > unknown

        with pytest.raises(ValueError, match="Cannot compare unknown quantities"):
            _ = known <= unknown

        with pytest.raises(ValueError, match="Cannot compare unknown quantities"):
            _ = known >= unknown

        # Equality should return False, not raise
        assert known != unknown
        assert not (known == unknown)

    def test_comparison_incompatible_dimensions(self):
        """Test that comparisons between incompatible dimensions raise errors."""
        length = Q(100, "meter")
        time = Q(100, "second")

        with pytest.raises(TypeError, match="Cannot compare quantities with different dimensions"):
            _ = length < time

        with pytest.raises(TypeError, match="Cannot compare quantities with different dimensions"):
            _ = length > time

        with pytest.raises(TypeError, match="Cannot compare quantities with different dimensions"):
            _ = length <= time

        with pytest.raises(TypeError, match="Cannot compare quantities with different dimensions"):
            _ = length >= time

    def test_comparison_with_non_quantity(self):
        """Test comparison with non-Quantity objects."""
        q = Q(100, "meter")

        # Should return NotImplemented (which Python converts to False for ==)
        assert not (q == 100)
        assert q != 100
        assert not (q == "100 meter")
        assert q != "100 meter"

    def test_equality_near_floating_point(self):
        """Test equality handles floating point precision properly."""
        # Test values that are very close but might differ due to floating point
        q1 = Q(1.0 / 3.0, "meter")
        q2 = Q(0.3333333333333333, "meter")

        # These should be equal within tolerance
        assert q1 == q2

        # Test conversion that might introduce small errors
        q_inch = Q(1, "inch")  # 0.0254 meters
        q_meter = Q(0.0254, "meter")

        assert q_inch == q_meter

    @pytest.mark.parametrize(
        "val1, unit1, val2, unit2, expected_eq",
        [
            # Same dimension, different units
            (1, "meter", 100, "centimeter", True),
            (1, "kilometer", 1000, "meter", True),
            (1, "foot", 12, "inch", True),
            (1, "meter", 99, "centimeter", False),
            # Additional length conversions
            (1, "meter", 1000, "millimeter", True),
            (1, "meter", 0.001, "kilometer", True),
            (2.54, "centimeter", 1, "inch", True),
            (1, "foot", 0.3048, "meter", True),
        ],
    )
    def test_parametrized_equality(self, val1, unit1, val2, unit2, expected_eq):
        """Parametrized test for equality with various unit conversions."""
        try:
            q1 = Q(val1, unit1)
            q2 = Q(val2, unit2)

            if expected_eq:
                assert q1 == q2, f"{val1} {unit1} should equal {val2} {unit2}"
                assert not (q1 != q2)
            else:
                assert q1 != q2, f"{val1} {unit1} should not equal {val2} {unit2}"
                assert not (q1 == q2)
        except ValueError:
            # Skip if units are not supported
            pytest.skip(f"Unit not supported: {unit1} or {unit2}")

    @pytest.mark.parametrize(
        "val1, unit1, val2, unit2, expected_lt",
        [
            # Length comparisons
            (1, "meter", 2, "meter", True),
            (1, "meter", 150, "centimeter", True),
            (1, "meter", 100, "centimeter", False),
            (1, "meter", 50, "centimeter", False),
            # Mixed unit comparisons
            (1, "foot", 1, "meter", True),  # 1 foot < 1 meter
            (1, "inch", 1, "centimeter", False),  # 1 inch > 1 centimeter
            # Additional comparisons
            (1, "millimeter", 1, "meter", True),
            (1, "kilometer", 1, "meter", False),
        ],
    )
    def test_parametrized_less_than(self, val1, unit1, val2, unit2, expected_lt):
        """Parametrized test for less than comparisons."""
        try:
            q1 = Q(val1, unit1)
            q2 = Q(val2, unit2)

            assert (q1 < q2) == expected_lt
            assert (q1 > q2) == (not expected_lt and q1 != q2)
            assert (q1 <= q2) == (expected_lt or q1 == q2)
            assert (q1 >= q2) == (not expected_lt or q1 == q2)
        except ValueError:
            # Skip if units are not supported
            pytest.skip(f"Unit not supported: {unit1} or {unit2}")
