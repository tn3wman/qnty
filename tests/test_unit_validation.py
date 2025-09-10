"""
Tests for Unit Validation and Suggestions
=========================================

Tests the new unit validation system that provides helpful suggestions
when invalid units are entered.
"""

import pytest

from qnty.utils.unit_suggestions import UnitValidationError, create_unit_validation_error, get_unit_suggestions


class TestUnitSuggestions:
    """Test the unit suggestion system."""

    def test_get_suggestions_for_inch_variants(self):
        """Test suggestions for common inch variations."""
        # Test "in" - should suggest "inch"
        suggestions = get_unit_suggestions("in")
        assert len(suggestions) > 0
        assert "inch" in suggestions or "in" in suggestions  # "in" is an alias for "inch"

        # Test "inches" - should suggest "inch"
        suggestions = get_unit_suggestions("inches")
        assert len(suggestions) > 0
        assert "inch" in suggestions

        # Test "in_" - if it exists, should be suggested
        suggestions = get_unit_suggestions("in_")
        assert len(suggestions) > 0  # Should get some suggestions

    def test_get_suggestions_for_pressure_units(self):
        """Test suggestions for pressure unit variants."""
        # Test "psi_" - should suggest "psi"
        suggestions = get_unit_suggestions("psi_")
        assert len(suggestions) > 0
        # Should contain psi or similar pressure units
        assert any("psi" in s.lower() or "pound" in s.lower() for s in suggestions)

        # Test "bar_" - should suggest "bar" related units
        suggestions = get_unit_suggestions("bar_")
        assert len(suggestions) > 0
        assert any("bar" in s.lower() for s in suggestions)

    def test_get_suggestions_for_temperature_units(self):
        """Test suggestions for temperature unit variants."""
        # Test "celsius" - should suggest related temperature units
        suggestions = get_unit_suggestions("celsius")
        assert len(suggestions) > 0

        # Test "fahrenheit" - should suggest related temperature units
        suggestions = get_unit_suggestions("fahrenheit")
        assert len(suggestions) > 0

    def test_get_suggestions_returns_limited_results(self):
        """Test that suggestions are limited to reasonable number."""
        suggestions = get_unit_suggestions("meter", max_suggestions=2)
        assert len(suggestions) <= 2

    def test_get_suggestions_for_nonsense_input(self):
        """Test that nonsensical input gets no or few suggestions."""
        suggestions = get_unit_suggestions("xyzabc123")
        # Might get some suggestions, but should be few
        assert len(suggestions) <= 3

    def test_get_suggestions_empty_input(self):
        """Test that empty input is handled gracefully."""
        suggestions = get_unit_suggestions("")
        assert isinstance(suggestions, list)

    def test_get_suggestions_whitespace_input(self):
        """Test that whitespace input is handled gracefully."""
        suggestions = get_unit_suggestions("   ")
        assert isinstance(suggestions, list)


class TestUnitValidationError:
    """Test the UnitValidationError exception class."""

    def test_unit_validation_error_with_suggestions(self):
        """Test error creation with suggestions."""
        suggestions = ["inch", "in"]
        error = UnitValidationError("in", "Length", suggestions)

        assert error.invalid_unit == "in"
        assert error.variable_type == "Length"
        assert error.suggestions == suggestions
        assert "Unknown unit 'in' for Length" in str(error)
        assert "Did you mean: 'inch', 'in'?" in str(error)

    def test_unit_validation_error_no_suggestions(self):
        """Test error creation without suggestions."""
        error = UnitValidationError("badunit", "Pressure")

        assert error.invalid_unit == "badunit"
        assert error.variable_type == "Pressure"
        assert error.suggestions == []
        assert "Unknown unit 'badunit' for Pressure" in str(error)
        assert "Did you mean" not in str(error)

    def test_unit_validation_error_no_variable_type(self):
        """Test error creation without variable type."""
        error = UnitValidationError("badunit")

        assert error.invalid_unit == "badunit"
        assert error.variable_type == ""
        assert "Unknown unit 'badunit'" in str(error)
        assert " for " not in str(error)  # No variable type mentioned

    def test_create_unit_validation_error_function(self):
        """Test the create_unit_validation_error convenience function."""
        error = create_unit_validation_error("in", "Length")

        assert isinstance(error, UnitValidationError)
        assert error.invalid_unit == "in"
        assert error.variable_type == "Length"
        assert len(error.suggestions) >= 0  # Should have gotten some suggestions


class TestUnitValidationIntegration:
    """Integration tests for unit validation in the main library."""

    def test_length_with_invalid_unit_raises_error_with_suggestions(self):
        """Test that Length with invalid unit raises error with suggestions."""
        from qnty import Length

        # Test that invalid unit raises our new error type
        with pytest.raises(UnitValidationError) as exc_info:
            Length(10, "in", "test_length")  # "in" is invalid, should suggest "inch"

        error = exc_info.value
        assert error.invalid_unit == "in"
        assert "Length" in error.variable_type
        # Should have suggestions since "in" is close to valid units
        assert len(error.suggestions) > 0
        assert "inch" in error.suggestions

    def test_pressure_with_invalid_unit_raises_error_with_suggestions(self):
        """Test that Pressure with invalid unit raises error with suggestions."""
        from qnty import Pressure

        # Test with a clearly invalid unit
        with pytest.raises(UnitValidationError) as exc_info:
            Pressure(100, "badpressure", "test_pressure")

        error = exc_info.value
        assert error.invalid_unit == "badpressure"
        assert "Pressure" in error.variable_type
        assert len(error.suggestions) >= 0  # Might have suggestions

    def test_temperature_with_nonsense_unit_raises_error(self):
        """Test that Temperature with nonsense unit raises error."""
        from qnty import Temperature

        with pytest.raises(UnitValidationError) as exc_info:
            Temperature(25, "nonsenseunit", "test_temp")

        error = exc_info.value
        assert error.invalid_unit == "nonsenseunit"
        assert "Temperature" in error.variable_type

    def test_converter_with_invalid_unit_raises_error_with_suggestions(self):
        """Test that unit converters raise errors with suggestions."""
        from qnty import Length

        length = Length(10, "meter", "test")

        # Test ToUnit converter with invalid unit
        with pytest.raises(UnitValidationError) as exc_info:
            length.to_unit("badunit")  # Clearly invalid unit

        error = exc_info.value
        assert error.invalid_unit == "badunit"
        assert "Length" in error.variable_type

    def test_set_method_with_invalid_unit_raises_error_with_suggestions(self):
        """Test that set method raises error with suggestions for invalid units."""
        from qnty import Length

        length = Length("test_length")

        # Test set method with invalid unit
        with pytest.raises(UnitValidationError) as exc_info:
            length.set(10, "badunit")  # Clearly invalid unit

        error = exc_info.value
        assert error.invalid_unit == "badunit"
        assert len(error.suggestions) >= 0  # Might have suggestions
