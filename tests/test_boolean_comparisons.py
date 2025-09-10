"""
Tests for Boolean Comparison Results
====================================

Tests that comparison operations return proper boolean values (True/False)
instead of numeric values (1.0/0.0).
"""

from typing import cast

from qnty import Length, Pressure, Temperature
from qnty.quantities.base_qnty import BooleanQuantity


class TestBooleanComparisons:
    """Test that comparisons return boolean values."""

    def test_comparison_operators_return_boolean_quantity(self):
        """Test that comparison operators return BooleanQuantity objects."""
        pressure1 = Pressure(100, "kilopascal", "P1")
        pressure2 = Pressure(150, "kilopascal", "P2")

        # Test all comparison operators
        comparisons = [
            pressure1 < pressure2,  # Less than
            pressure1 > pressure2,  # Greater than
            pressure1 <= pressure2,  # Less than or equal
            pressure1 >= pressure2,  # Greater than or equal
            pressure1 == pressure2,  # Equal
            pressure1 != pressure2,  # Not equal
        ]

        context: dict[str, Pressure] = {pressure1.name: pressure1, pressure2.name: pressure2}

        for comparison in comparisons:
            # Type ignore for the evaluate call due to dict variance
            result = comparison.evaluate(context)  # type: ignore[arg-type]
            assert isinstance(result, BooleanQuantity)
            assert isinstance(result.boolean_value, bool)

    def test_comparison_methods_return_boolean_quantity(self):
        """Test that comparison methods return BooleanQuantity objects."""
        length1 = Length(1, "meter", "L1")
        length2 = Length(2, "meter", "L2")

        # Test comparison methods
        comparisons = [
            length1.lt(length2),  # Less than
            length1.gt(length2),  # Greater than
            length1.leq(length2),  # Less than or equal
            length1.geq(length2),  # Greater than or equal
            length1.eq(length2),  # Equal
            length1.ne(length2),  # Not equal
        ]

        context: dict[str, Length] = {length1.name: length1, length2.name: length2}

        for comparison in comparisons:
            # Type ignore for the evaluate call due to dict variance
            result = comparison.evaluate(context)  # type: ignore[arg-type]
            assert isinstance(result, BooleanQuantity)

    def test_boolean_comparison_display(self):
        """Test that boolean comparisons display as True/False."""
        temp1 = Temperature(273.15, "K", "T1")  # 0°C
        temp2 = Temperature(373.15, "K", "T2")  # 100°C

        context: dict[str, Temperature] = {temp1.name: temp1, temp2.name: temp2}

        # True comparison
        true_comparison = temp1 < temp2
        true_result = true_comparison.evaluate(context)  # type: ignore[arg-type]
        assert str(true_result) == "True"
        assert repr(true_result) == "BooleanQuantity(True)"
        assert bool(true_result) is True

        # False comparison
        false_comparison = temp1 > temp2
        false_result = false_comparison.evaluate(context)  # type: ignore[arg-type]
        assert str(false_result) == "False"
        assert repr(false_result) == "BooleanQuantity(False)"
        assert bool(false_result) is False

    def test_cross_unit_boolean_comparisons(self):
        """Test that cross-unit comparisons work with boolean results."""
        length_m = Length(1, "meter", "L_m")
        length_cm = Length(100, "centimeter", "L_cm")  # Equal to 1 meter
        length_mm = Length(1500, "millimeter", "L_mm")  # 1.5 meters

        context: dict[str, Length] = {length_m.name: length_m, length_cm.name: length_cm, length_mm.name: length_mm}

        # Equal values in different units
        equal_result = (length_m == length_cm).evaluate(context)  # type: ignore[arg-type]
        assert isinstance(equal_result, BooleanQuantity)
        assert equal_result.boolean_value is True
        assert str(equal_result) == "True"

        # Less than with unit conversion
        less_result = (length_m < length_mm).evaluate(context)  # type: ignore[arg-type]
        assert isinstance(less_result, BooleanQuantity)
        assert less_result.boolean_value is True
        assert str(less_result) == "True"

    def test_backward_compatibility(self):
        """Test that BooleanQuantity maintains backward compatibility."""
        pressure1 = Pressure(50, "kilopascal", "P1")
        pressure2 = Pressure(100, "kilopascal", "P2")

        context: dict[str, Pressure] = {pressure1.name: pressure1, pressure2.name: pressure2}

        result = (pressure1 < pressure2).evaluate(context)  # type: ignore[arg-type]

        # Should still be usable as a numeric value for compatibility
        assert result.value == 1.0  # True -> 1.0
        assert result.unit.symbol == ""  # Dimensionless

        # But should display as boolean
        assert str(result) == "True"
        assert bool(result) is True

        # False case
        false_result = (pressure1 > pressure2).evaluate(context)  # type: ignore[arg-type]
        assert false_result.value == 0.0  # False -> 0.0
        assert str(false_result) == "False"
        assert bool(false_result) is False

    def test_boolean_quantity_properties(self):
        """Test BooleanQuantity specific properties."""
        # Test True case
        true_qty = BooleanQuantity(True)
        assert true_qty.boolean_value is True
        assert true_qty.value == 1.0
        assert str(true_qty) == "True"
        assert bool(true_qty) is True

        # Test False case
        false_qty = BooleanQuantity(False)
        assert false_qty.boolean_value is False
        assert false_qty.value == 0.0
        assert str(false_qty) == "False"
        assert bool(false_qty) is False


class TestComparisonBehaviorChange:
    """Test the behavioral change from numeric to boolean results."""

    def test_comparison_results_are_boolean_not_numeric(self):
        """Verify that comparisons now return True/False, not 1.0/0.0."""
        pressure1 = Pressure(100, "pascal", "P1")
        pressure2 = Pressure(200, "pascal", "P2")

        context: dict[str, Pressure] = {pressure1.name: pressure1, pressure2.name: pressure2}

        # All these should return BooleanQuantity with True/False display
        test_cases = [
            (pressure1 < pressure2, True),  # 100 < 200
            (pressure1 > pressure2, False),  # 100 > 200
            (pressure1 <= pressure2, True),  # 100 <= 200
            (pressure1 >= pressure2, False),  # 100 >= 200
            (pressure1 == pressure1, True),  # 100 == 100
            (pressure1 != pressure2, True),  # 100 != 200
        ]

        for comparison_expr, expected_bool in test_cases:
            result = comparison_expr.evaluate(context)  # type: ignore[arg-type]
            result = cast(BooleanQuantity, result)  # We know this returns BooleanQuantity

            # New behavior: displays as True/False
            assert str(result) == str(expected_bool)
            assert result.boolean_value is expected_bool

            # Backward compatibility: numeric value still accessible
            assert result.value == (1.0 if expected_bool else 0.0)

            # Boolean conversion works correctly
            assert bool(result) is expected_bool
