"""
Tests for SelectVariable.set() method with type validation.
"""

import pytest
from dataclasses import dataclass

from qnty.algebra.select import SelectOption, SelectVariable


@dataclass(frozen=True)
class FlangeType(SelectOption):
    """Test flange types for SelectVariable."""
    integral_welded_slip: str = "integral_welded_slip"
    loose_type_lap_with_hub: str = "loose_type_lap_with_hub"
    loose_type_lap_without_hub: str = "loose_type_lap_without_hub"
    reverse_integral_type: str = "reverse_integral_type"
    reverse_loose_type: str = "reverse_loose_type"


@dataclass(frozen=True)
class GasketType(SelectOption):
    """Test gasket types for SelectVariable."""
    non_self_energized: str = "non_self_energized"
    self_energized: str = "self_energized"


class TestSelectVariableSet:
    """Test the SelectVariable.set() method."""

    def test_set_with_correct_option_class(self):
        """Setting with correct option class should succeed."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        # Should work - using the correct class
        result = flange_type.set(FlangeType.integral_welded_slip)

        assert flange_type.selected == FlangeType.integral_welded_slip
        assert flange_type.value == "integral_welded_slip"
        assert result is flange_type  # Should return self for chaining

    def test_set_with_string_raises_error(self):
        """Setting with a string value should raise TypeError with helpful message."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        with pytest.raises(TypeError) as exc_info:
            flange_type.set("integral_welded_slip")

        error_msg = str(exc_info.value)
        assert "Cannot set Flange Type to string 'integral_welded_slip'" in error_msg
        assert "Use FlangeType.integral_welded_slip instead" in error_msg
        assert "FlangeType.integral_welded_slip" in error_msg

    def test_set_with_invalid_value_raises_error(self):
        """Setting with an invalid value should raise TypeError."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        with pytest.raises(TypeError) as exc_info:
            flange_type.set("not_a_valid_option")

        error_msg = str(exc_info.value)
        assert "not_a_valid_option" in error_msg

    def test_set_with_wrong_option_class_raises_error(self):
        """Setting with an option from a different SelectOption class should raise TypeError."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        # Try to set with an option from a different class
        with pytest.raises(TypeError) as exc_info:
            flange_type.set(GasketType.self_energized)

        error_msg = str(exc_info.value)
        assert "Invalid option for Flange Type" in error_msg
        assert "Expected an attribute from FlangeType" in error_msg

    def test_set_multiple_times(self):
        """Setting multiple times should work correctly."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        # First set
        flange_type.set(FlangeType.integral_welded_slip)
        assert flange_type.value == "integral_welded_slip"

        # Second set
        flange_type.set(FlangeType.reverse_integral_type)
        assert flange_type.value == "reverse_integral_type"

        # Third set
        flange_type.set(FlangeType.loose_type_lap_with_hub)
        assert flange_type.value == "loose_type_lap_with_hub"

    def test_set_returns_self_for_chaining(self):
        """set() should return self to allow method chaining."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        result = flange_type.set(FlangeType.integral_welded_slip)

        assert result is flange_type
        assert isinstance(result, SelectVariable)

    def test_set_all_valid_options(self):
        """Should be able to set all valid options."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        # Try all valid options
        flange_type.set(FlangeType.integral_welded_slip)
        assert flange_type.value == "integral_welded_slip"

        flange_type.set(FlangeType.loose_type_lap_with_hub)
        assert flange_type.value == "loose_type_lap_with_hub"

        flange_type.set(FlangeType.loose_type_lap_without_hub)
        assert flange_type.value == "loose_type_lap_without_hub"

        flange_type.set(FlangeType.reverse_integral_type)
        assert flange_type.value == "reverse_integral_type"

        flange_type.set(FlangeType.reverse_loose_type)
        assert flange_type.value == "reverse_loose_type"

    def test_gasket_type_set(self):
        """Test set() with a different SelectOption class."""
        gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

        gasket_type.set(GasketType.self_energized)
        assert gasket_type.value == "self_energized"

        gasket_type.set(GasketType.non_self_energized)
        assert gasket_type.value == "non_self_energized"

    def test_set_vs_select_behavior(self):
        """Compare set() and select() behavior."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        # select() allows string values (legacy behavior)
        flange_type.select("integral_welded_slip")
        assert flange_type.value == "integral_welded_slip"

        # set() requires proper class attribute access (type-safe)
        flange_type.set(FlangeType.reverse_integral_type)
        assert flange_type.value == "reverse_integral_type"

        # set() rejects string values
        with pytest.raises(TypeError):
            flange_type.set("loose_type_lap_with_hub")

    def test_error_message_shows_valid_options(self):
        """Error messages should show valid options for better UX."""
        flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)

        with pytest.raises(TypeError) as exc_info:
            flange_type.set("invalid")

        error_msg = str(exc_info.value)
        # Should show valid options in the error message
        assert "FlangeType." in error_msg


class TestSelectVariableInProblemContext:
    """Test SelectVariable.set() in a Problem-like context."""

    def test_problem_like_usage(self):
        """Test usage pattern similar to problem.flange_type.set(FlangeType.integral_welded_slip)."""

        # Simulate a Problem class attribute
        class MockProblem:
            flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)
            gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

        problem = MockProblem()

        # User-friendly API: problem.flange_type.set(FlangeType.integral_welded_slip)
        problem.flange_type.set(FlangeType.integral_welded_slip)
        assert problem.flange_type.value == "integral_welded_slip"

        problem.gasket_type.set(GasketType.self_energized)
        assert problem.gasket_type.value == "self_energized"

    def test_problem_prevents_wrong_type_assignment(self):
        """Test that problem prevents assigning wrong SelectOption type."""

        class MockProblem:
            flange_type = SelectVariable("Flange Type", FlangeType, FlangeType.loose_type_lap_without_hub)
            gasket_type = SelectVariable("Gasket Type", GasketType, GasketType.non_self_energized)

        problem = MockProblem()

        # Should reject setting flange_type with a GasketType option
        with pytest.raises(TypeError) as exc_info:
            problem.flange_type.set(GasketType.self_energized)

        assert "Expected an attribute from FlangeType" in str(exc_info.value)

        # Should reject setting gasket_type with a FlangeType option
        with pytest.raises(TypeError) as exc_info:
            problem.gasket_type.set(FlangeType.integral_welded_slip)

        assert "Expected an attribute from GasketType" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
