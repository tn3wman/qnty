"""Comprehensive tests for setters.py module.

Tests specialized setter classes that provide fluent API patterns for setting values
with type safety. Covers TypeSafeSetter, LengthSetter, and PressureSetter classes
with focus on dimensional compatibility, fluent API functionality, and integration
with the broader OptiUnit system.
"""

import pytest

from qnty.dimensions.field_dims import LENGTH, PRESSURE
from qnty.quantities import FieldQnty
from qnty.quantities.field_vars import Length, Pressure
from qnty.quantities.field_setter import LengthSetter, PressureSetter
from qnty.quantities.base_qnty import Quantity, TypeSafeSetter
from qnty.units.field_units import LengthUnits, PressureUnits


class TestTypeSafeSetterInitialization:
    """Test TypeSafeSetter initialization and basic properties."""

    def test_typesafe_setter_basic_initialization(self):
        """Test basic TypeSafeSetter construction."""
        length_var = Length("test_length")
        setter = TypeSafeSetter(length_var, 100.0)

        assert setter.variable == length_var
        assert setter.value == 100.0
        assert isinstance(setter.variable, FieldQnty)

    def test_typesafe_setter_with_different_types(self):
        """Test TypeSafeSetter with different variable types."""
        length_var = Length("length_test")
        pressure_var = Pressure("pressure_test")

        length_setter = TypeSafeSetter(length_var, 50.0)
        pressure_setter = TypeSafeSetter(pressure_var, 200.0)

        assert length_setter.variable.expected_dimension == LENGTH
        assert pressure_setter.variable.expected_dimension == PRESSURE
        assert length_setter.value == 50.0
        assert pressure_setter.value == 200.0

    @pytest.mark.parametrize("value", [0.0, -10.5, 1e6, 1e-9, float("inf")])
    def test_typesafe_setter_various_values(self, value):
        """Test TypeSafeSetter with various numeric values."""
        var = Length("test_var")
        setter = TypeSafeSetter(var, value)

        assert setter.value == value


class TestTypeSafeSetterWithUnit:
    """Test TypeSafeSetter with_unit method and dimensional compatibility."""

    def test_with_unit_compatible_dimension(self):
        """Test with_unit method with compatible dimension."""
        length_var = Length("beam_length")
        setter = TypeSafeSetter(length_var, 100.0)

        result = setter.with_unit(LengthUnits.millimeter)

        assert result is length_var  # Should return the same variable
        assert length_var.quantity is not None
        assert isinstance(length_var.quantity, Quantity)
        assert length_var.quantity.value == 100.0
        assert length_var.quantity.unit == LengthUnits.millimeter

    def test_with_unit_incompatible_dimension(self):
        """Test with_unit method with incompatible dimension."""
        length_var = Length("test_length")
        setter = TypeSafeSetter(length_var, 50.0)

        # Should raise TypeError for incompatible unit
        with pytest.raises(TypeError, match="Unit .* incompatible with expected dimension"):
            setter.with_unit(PressureUnits.pound_force_per_square_inch)

    @pytest.mark.parametrize("length_unit", [LengthUnits.meter, LengthUnits.millimeter, LengthUnits.centimeter, LengthUnits.inch, LengthUnits.foot])
    def test_with_unit_all_length_units(self, length_unit):
        """Test with_unit method with all length units."""
        length_var = Length("test_length")
        setter = TypeSafeSetter(length_var, 123.45)

        result = setter.with_unit(length_unit)

        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 123.45
        assert length_var.quantity.unit == length_unit
        assert length_var.quantity.dimension == LENGTH

    @pytest.mark.parametrize("pressure_unit", [PressureUnits.pascal, PressureUnits.kilopascal, PressureUnits.megapascal, PressureUnits.pound_force_per_square_inch, PressureUnits.bar])
    def test_with_unit_all_pressure_units(self, pressure_unit):
        """Test with_unit method with all pressure units."""
        pressure_var = Pressure("test_pressure")
        setter = TypeSafeSetter(pressure_var, 456.78)

        result = setter.with_unit(pressure_unit)

        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 456.78
        assert pressure_var.quantity.unit == pressure_unit
        assert pressure_var.quantity.dimension == PRESSURE

    def test_with_unit_method_chaining(self):
        """Test that with_unit supports method chaining."""
        var1 = Length("var1")
        var2 = Length("var2")

        # Method chaining should work
        result1 = TypeSafeSetter(var1, 100.0).with_unit(LengthUnits.meter)
        result2 = TypeSafeSetter(var2, 200.0).with_unit(LengthUnits.millimeter)

        assert result1.quantity is not None and result2.quantity is not None
        assert result1.quantity.value == 100.0
        assert result1.quantity.unit == LengthUnits.meter
        assert result2.quantity.value == 200.0
        assert result2.quantity.unit == LengthUnits.millimeter


class TestLengthSetterInitialization:
    """Test LengthSetter initialization and basic properties."""

    def test_length_setter_basic_initialization(self):
        """Test basic LengthSetter construction."""
        length_var = Length("beam_width")
        setter = LengthSetter(length_var, 250.0)

        assert setter.variable == length_var
        assert setter.value == 250.0
        assert isinstance(setter.variable, Length)

    def test_length_setter_type_specialization(self):
        """Test that LengthSetter only accepts Length variables."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 100.0)

        # Should be properly typed for Length
        assert setter.variable.expected_dimension == LENGTH

    @pytest.mark.parametrize("value", [0.001, 25.4, 100.0, 1000.0, 1e6])
    def test_length_setter_various_values(self, value):
        """Test LengthSetter with various numeric values."""
        length_var = Length("test_var")
        setter = LengthSetter(length_var, value)

        assert setter.value == value


class TestLengthSetterProperties:
    """Test LengthSetter unit properties."""

    def test_meter_property(self):
        """Test meter property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 5.0)

        result = setter.meter

        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 5.0
        assert length_var.quantity.unit == LengthUnits.meter

    def test_millimeter_property(self):
        """Test millimeter property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 1500.0)

        result = setter.millimeter

        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 1500.0
        assert length_var.quantity.unit == LengthUnits.millimeter

    def test_inch_property(self):
        """Test inch property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 12.0)

        result = setter.inch

        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 12.0
        assert length_var.quantity.unit == LengthUnits.inch

    def test_foot_property(self):
        """Test foot property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 3.5)

        result = setter.foot

        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 3.5
        assert length_var.quantity.unit == LengthUnits.foot

    @pytest.mark.parametrize("property_name,expected_unit", [("meter", LengthUnits.meter), ("millimeter", LengthUnits.millimeter), ("inch", LengthUnits.inch), ("foot", LengthUnits.foot)])
    def test_all_length_properties(self, property_name, expected_unit):
        """Test all length properties with parametrization."""
        length_var = Length("parametrized_test")
        setter = LengthSetter(length_var, 42.0)

        result = getattr(setter, property_name)

        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 42.0
        assert length_var.quantity.unit == expected_unit
        assert length_var.quantity.dimension == LENGTH


class TestPressureSetterInitialization:
    """Test PressureSetter initialization and basic properties."""

    def test_pressure_setter_basic_initialization(self):
        """Test basic PressureSetter construction."""
        pressure_var = Pressure("system_pressure")
        setter = PressureSetter(pressure_var, 150.0)

        assert setter.variable == pressure_var
        assert setter.value == 150.0
        assert isinstance(setter.variable, Pressure)

    def test_pressure_setter_type_specialization(self):
        """Test that PressureSetter only accepts Pressure variables."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 200.0)

        # Should be properly typed for Pressure
        assert setter.variable.expected_dimension == PRESSURE

    @pytest.mark.parametrize("value", [0.1, 14.7, 101.325, 1000.0, 10e6])
    def test_pressure_setter_various_values(self, value):
        """Test PressureSetter with various pressure values."""
        pressure_var = Pressure("test_var")
        setter = PressureSetter(pressure_var, value)

        assert setter.value == value


class TestPressureSetterProperties:
    """Test PressureSetter unit properties."""

    def test_psi_property(self):
        """Test psi property sets unit correctly."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 14.7)

        result = setter.pound_force_per_square_inch

        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 14.7
        assert pressure_var.quantity.unit.name == "pound_force_per_square_inch"

    def test_kPa_property(self):
        """Test kPa property sets unit correctly."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 101.325)

        result = setter.newton_per_square_meter

        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 101.325
        assert pressure_var.quantity.unit.name == "newton_per_square_meter"

    def test_MPa_property(self):
        """Test MPa property sets unit correctly."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 1.5)

        result = setter.megapascal

        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 1.5
        assert pressure_var.quantity.unit == PressureUnits.megapascal

    def test_bar_property(self):
        """Test bar property sets unit correctly."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 2.0)

        result = setter.bar

        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 2.0
        assert pressure_var.quantity.unit == PressureUnits.bar

    @pytest.mark.parametrize(
        "property_name,expected_unit_name",
        [("pound_force_per_square_inch", "pound_force_per_square_inch"), ("newton_per_square_meter", "newton_per_square_meter"), ("megapascal", "megapascal"), ("bar", "bar")],
    )
    def test_all_pressure_properties(self, property_name, expected_unit_name):
        """Test all pressure properties with parametrization."""
        pressure_var = Pressure("parametrized_test")
        setter = PressureSetter(pressure_var, 500.0)

        result = getattr(setter, property_name)

        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 500.0
        assert pressure_var.quantity.unit.name == expected_unit_name
        assert pressure_var.quantity.dimension == PRESSURE


class TestFluentAPIAndMethodChaining:
    """Test fluent API patterns and method chaining capabilities."""

    def test_length_fluent_api_chain(self):
        """Test fluent API with length variables."""
        # Create multiple length variables and set them in chain
        width = Length("width")
        height = Length("height")
        depth = Length("depth")

        # Set values using fluent API
        width_result = width.set(100.0).millimeter
        height_result = height.set(50.0).inch
        depth_result = depth.set(2.5).foot

        assert width_result is width
        assert height_result is height
        assert depth_result is depth

        # Verify all quantities are set correctly
        assert width.quantity is not None and height.quantity is not None and depth.quantity is not None
        assert width.quantity.value == 100.0
        assert width.quantity.unit == LengthUnits.millimeter
        assert height.quantity.value == 50.0
        assert height.quantity.unit == LengthUnits.inch
        assert depth.quantity.value == 2.5
        assert depth.quantity.unit == LengthUnits.foot

    def test_pressure_fluent_api_chain(self):
        """Test fluent API with pressure variables."""
        # Create multiple pressure variables and set them in chain
        inlet = Pressure("inlet_pressure")
        outlet = Pressure("outlet_pressure")
        system = Pressure("system_pressure")

        # Set values using fluent API
        inlet_result = inlet.set(150.0).pound_force_per_square_inch
        outlet_result = outlet.set(200.0).newton_per_square_meter
        system_result = system.set(2.5).megapascal

        assert inlet_result is inlet
        assert outlet_result is outlet
        assert system_result is system

        # Verify all quantities are set correctly
        assert inlet.quantity is not None and outlet.quantity is not None and system.quantity is not None
        assert inlet.quantity.value == 150.0
        assert inlet.quantity.unit.name == "pound_force_per_square_inch"
        assert outlet.quantity.value == 200.0
        assert outlet.quantity.unit.name == "newton_per_square_meter"
        assert system.quantity.value == 2.5
        assert system.quantity.unit == PressureUnits.megapascal

    def test_mixed_setter_types(self):
        """Test using both specialized and type-safe setters."""
        length_var = Length("test_length")
        pressure_var = Pressure("test_pressure")

        # Use specialized setters
        length_var.set(100.0).meter
        pressure_var.set(14.7).pound_force_per_square_inch

        # Use type-safe setter
        TypeSafeSetter(length_var, 200.0).with_unit(LengthUnits.millimeter)
        TypeSafeSetter(pressure_var, 101.325).with_unit(PressureUnits.kilopascal)

        # Should have updated values
        assert length_var.quantity is not None and pressure_var.quantity is not None
        assert length_var.quantity.value == 200.0  # Last set wins
        assert length_var.quantity.unit == LengthUnits.millimeter
        assert pressure_var.quantity.value == 101.325  # Last set wins
        assert pressure_var.quantity.unit.name == "kilopascal"

    def test_setter_return_consistency(self):
        """Test that all setters return the correct variable instance."""
        length_var = Length("consistency_test")

        # All setter methods should return the same variable instance
        meter_result = length_var.set(1.0).meter
        mm_result = length_var.set(1000.0).millimeter
        inch_result = length_var.set(39.37).inch
        foot_result = length_var.set(3.28).foot

        assert meter_result is length_var
        assert mm_result is length_var
        assert inch_result is length_var
        assert foot_result is length_var


class TestSetterErrorHandling:
    """Test error handling and edge cases for setter classes."""

    def test_typesafe_setter_error_messages(self):
        """Test that TypeSafeSetter provides informative error messages."""
        length_var = Length("test_length")
        setter = TypeSafeSetter(length_var, 100.0)

        # Should provide clear error message for incompatible unit
        with pytest.raises(TypeError) as exc_info:
            setter.with_unit(PressureUnits.pound_force_per_square_inch)

        assert "incompatible with expected dimension" in str(exc_info.value)

    def test_dimensional_compatibility_edge_cases(self):
        """Test dimensional compatibility with edge cases."""
        # Create variables with different dimensions
        length_var = Length("length_test")
        pressure_var = Pressure("pressure_test")

        # Test cross-dimensional incompatibility
        length_setter = TypeSafeSetter(length_var, 50.0)
        pressure_setter = TypeSafeSetter(pressure_var, 100.0)

        # Length setter should reject pressure units
        with pytest.raises(TypeError):
            length_setter.with_unit(PressureUnits.bar)

        # Pressure setter should reject length units
        with pytest.raises(TypeError):
            pressure_setter.with_unit(LengthUnits.meter)

    @pytest.mark.parametrize("invalid_value", [float("nan")])
    def test_setter_with_special_float_values(self, invalid_value):
        """Test setters with special float values."""
        length_var = Length("special_test")
        setter = LengthSetter(length_var, invalid_value)

        result = setter.meter

        # Should handle special values without crashing
        assert result is length_var
        # Note: NaN comparison is always False, so we check differently
        if invalid_value != invalid_value:  # NaN check
            assert setter.value != setter.value  # NaN property

    def test_zero_and_negative_values(self):
        """Test setters with zero and negative values."""
        length_var = Length("zero_test")
        pressure_var = Pressure("negative_test")

        # Zero values should work
        zero_result = LengthSetter(length_var, 0.0).meter
        assert zero_result.quantity is not None
        assert zero_result.quantity.value == 0.0

        # Negative values should work (physics may allow negative measurements)
        negative_result = PressureSetter(pressure_var, -10.0).pound_force_per_square_inch
        assert negative_result.quantity is not None
        assert negative_result.quantity.value == -10.0


class TestSetterIntegration:
    """Test integration between setters and the broader OptiUnit system."""

    def test_setter_fastquantity_integration(self):
        """Test that setters create proper FastQuantity instances."""
        length_var = Length("integration_test")
        setter = LengthSetter(length_var, 123.45)

        result = setter.millimeter

        # Should create a proper FastQuantity
        assert result.quantity is not None
        assert isinstance(result.quantity, Quantity)
        assert result.quantity.value == 123.45
        assert result.quantity.unit == LengthUnits.millimeter
        assert result.quantity._si_factor == LengthUnits.millimeter.si_factor
        assert result.quantity._dimension_sig == LENGTH._signature

    def test_setter_dimension_signature_consistency(self):
        """Test that setters maintain dimensional consistency."""
        pressure_var = Pressure("dimension_test")
        setter = PressureSetter(pressure_var, 200.0)

        result = setter.newton_per_square_meter

        # FastQuantity should have correct dimension signature
        assert result.quantity is not None
        assert result.quantity.dimension == PRESSURE
        assert result.quantity._dimension_sig == PRESSURE._signature
        assert result.quantity.dimension.is_compatible(PressureUnits.newton_per_square_meter.dimension)

    def test_setter_variable_state_changes(self):
        """Test that setters properly change variable state."""
        length_var = Length("state_test")

        # Initially should be unset
        assert length_var.quantity is None
        assert "unset" in str(length_var)

        # After setting should have quantity
        length_var.set(500.0).millimeter
        assert length_var.quantity is not None
        assert "unset" not in str(length_var)
        assert str(length_var.quantity) in str(length_var)

    def test_setter_with_variable_polymorphism(self):
        """Test setters work with variable polymorphism."""
        # Create variables as base UnifiedVariable references
        length_var: FieldQnty = Length("poly_length")
        pressure_var: FieldQnty = Pressure("poly_pressure")

        # TypeSafeSetter should work with polymorphic variables
        TypeSafeSetter(length_var, 100.0).with_unit(LengthUnits.meter)
        TypeSafeSetter(pressure_var, 200.0).with_unit(PressureUnits.pound_force_per_square_inch)

        assert length_var.quantity is not None and pressure_var.quantity is not None
        assert length_var.quantity.value == 100.0
        assert length_var.quantity.unit == LengthUnits.meter
        assert pressure_var.quantity.value == 200.0
        assert pressure_var.quantity.unit.name == "pound_force_per_square_inch"

    def test_multiple_assignments_to_same_variable(self):
        """Test multiple assignments to the same variable."""
        length_var = Length("multi_assign_test")

        # Multiple assignments should update the variable
        length_var.set(100.0).meter
        assert length_var.quantity is not None
        assert length_var.quantity.value == 100.0
        assert length_var.quantity.unit == LengthUnits.meter

        # Second assignment should overwrite
        length_var.set(2540.0).millimeter
        assert length_var.quantity.value == 2540.0
        assert length_var.quantity.unit == LengthUnits.millimeter

        # Third assignment with TypeSafeSetter should also overwrite
        TypeSafeSetter(length_var, 36.0).with_unit(LengthUnits.inch)
        assert length_var.quantity.value == 36.0
        assert length_var.quantity.unit == LengthUnits.inch


class TestSetterPerformanceCharacteristics:
    """Test performance characteristics of setter classes."""

    def test_setter_object_creation_efficiency(self):
        """Test that setter creation is efficient."""
        length_var = Length("perf_test")

        # Creating setters should be fast
        import time

        start_time = time.time()

        for _ in range(1000):
            setter = LengthSetter(length_var, 100.0)
            setter.meter

        end_time = time.time()
        duration = end_time - start_time

        # Should complete 1000 operations in reasonable time (< 1 second)
        assert duration < 1.0

    def test_cached_fastquantity_performance(self):
        """Test that FastQuantity caching works in setters."""
        length_var = Length("cache_test")
        setter = LengthSetter(length_var, 100.0)

        # Set value and check caching
        result = setter.millimeter
        assert result.quantity is not None
        quantity = result.quantity

        # FastQuantity should have cached values
        assert hasattr(quantity, "_si_factor")
        assert hasattr(quantity, "_dimension_sig")
        assert quantity._si_factor == LengthUnits.millimeter.si_factor
        assert quantity._dimension_sig == LENGTH._signature


class TestSetterComprehensiveCoverage:
    """Comprehensive edge case coverage for complete testing."""

    @pytest.mark.parametrize("length_value,length_unit_prop", [(0.001, "millimeter"), (1.0, "meter"), (12.0, "inch"), (3.28084, "foot"), (1e-6, "millimeter"), (1e6, "meter")])
    def test_length_comprehensive_values_and_units(self, length_value, length_unit_prop):
        """Comprehensive test of length values and units."""
        length_var = Length(f"comprehensive_length_{length_unit_prop}")
        setter = LengthSetter(length_var, length_value)

        result = getattr(setter, length_unit_prop)

        assert result is length_var
        assert result.quantity is not None
        assert result.quantity.value == length_value
        assert result.quantity.dimension == LENGTH

    @pytest.mark.parametrize(
        "pressure_value,pressure_unit_prop",
        [(14.7, "pound_force_per_square_inch"), (101.325, "newton_per_square_meter"), (0.101325, "megapascal"), (1.01325, "bar"), (1e-3, "newton_per_square_meter"), (1e3, "megapascal")],
    )
    def test_pressure_comprehensive_values_and_units(self, pressure_value, pressure_unit_prop):
        """Comprehensive test of pressure values and units."""
        pressure_var = Pressure(f"comprehensive_pressure_{pressure_unit_prop}")
        setter = PressureSetter(pressure_var, pressure_value)

        result = getattr(setter, pressure_unit_prop)

        assert result is pressure_var
        assert result.quantity is not None
        assert result.quantity.value == pressure_value
        assert result.quantity.dimension == PRESSURE

    def test_all_setters_return_type_consistency(self):
        """Test that all setter methods have consistent return types."""
        length_var = Length("return_type_test")
        pressure_var = Pressure("return_type_test")

        # All length setter properties should return Length
        length_returns = [LengthSetter(length_var, 1.0).meter, LengthSetter(length_var, 1.0).millimeter, LengthSetter(length_var, 1.0).inch, LengthSetter(length_var, 1.0).foot]

        for returned_var in length_returns:
            assert returned_var is length_var
            assert isinstance(returned_var, Length)

        # All pressure setter properties should return Pressure
        pressure_returns = [
            PressureSetter(pressure_var, 1.0).pound_force_per_square_inch,
            PressureSetter(pressure_var, 1.0).newton_per_square_meter,
            PressureSetter(pressure_var, 1.0).megapascal,
            PressureSetter(pressure_var, 1.0).bar,
        ]

        for returned_var in pressure_returns:
            assert returned_var is pressure_var
            assert isinstance(returned_var, Pressure)

        # TypeSafeSetter should return the variable
        typesafe_returns = [TypeSafeSetter(length_var, 1.0).with_unit(LengthUnits.meter), TypeSafeSetter(pressure_var, 1.0).with_unit(PressureUnits.pound_force_per_square_inch)]

        assert typesafe_returns[0] is length_var
        assert typesafe_returns[1] is pressure_var
