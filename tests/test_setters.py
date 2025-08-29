"""Comprehensive tests for setters.py module.

Tests specialized setter classes that provide fluent API patterns for setting values
with type safety. Covers TypeSafeSetter, LengthSetter, and PressureSetter classes
with focus on dimensional compatibility, fluent API functionality, and integration
with the broader OptiUnit system.
"""

import pytest
from src.qnty.setters import TypeSafeSetter, LengthSetter, PressureSetter
from src.qnty.variables import Length, Pressure
from src.qnty.variable import FastQuantity
from src.qnty.dimension import LENGTH, PRESSURE
from src.qnty.units import LengthUnits, PressureUnits
from src.qnty.types import TypeSafeVariable


class TestTypeSafeSetterInitialization:
    """Test TypeSafeSetter initialization and basic properties."""
    
    def test_typesafe_setter_basic_initialization(self):
        """Test basic TypeSafeSetter construction."""
        length_var = Length("test_length")
        setter = TypeSafeSetter(length_var, 100.0)
        
        assert setter.variable == length_var
        assert setter.value == 100.0
        assert isinstance(setter.variable, TypeSafeVariable)
    
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
    
    @pytest.mark.parametrize("value", [0.0, -10.5, 1e6, 1e-9, float('inf')])
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
        assert isinstance(length_var.quantity, FastQuantity)
        assert length_var.quantity.value == 100.0
        assert length_var.quantity.unit == LengthUnits.millimeter
    
    def test_with_unit_incompatible_dimension(self):
        """Test with_unit method with incompatible dimension."""
        length_var = Length("test_length")
        setter = TypeSafeSetter(length_var, 50.0)
        
        # Should raise TypeError for incompatible unit
        with pytest.raises(TypeError, match="Unit psi incompatible with expected dimension"):
            setter.with_unit(PressureUnits.psi)
    
    @pytest.mark.parametrize("length_unit", [
        LengthUnits.meter,
        LengthUnits.millimeter,
        LengthUnits.centimeter,
        LengthUnits.inch,
        LengthUnits.foot
    ])
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
    
    @pytest.mark.parametrize("pressure_unit", [
        PressureUnits.pascal,
        PressureUnits.kilopascal,
        PressureUnits.megapascal,
        PressureUnits.psi,
        PressureUnits.bar
    ])
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
    
    def test_meters_property(self):
        """Test meters property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 5.0)
        
        result = setter.meters
        
        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 5.0
        assert length_var.quantity.unit == LengthUnits.meter
    
    def test_millimeters_property(self):
        """Test millimeters property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 1500.0)
        
        result = setter.millimeters
        
        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 1500.0
        assert length_var.quantity.unit == LengthUnits.millimeter
    
    def test_inches_property(self):
        """Test inches property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 12.0)
        
        result = setter.inches
        
        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 12.0
        assert length_var.quantity.unit == LengthUnits.inch
    
    def test_feet_property(self):
        """Test feet property sets unit correctly."""
        length_var = Length("test_length")
        setter = LengthSetter(length_var, 3.5)
        
        result = setter.feet
        
        assert result is length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 3.5
        assert length_var.quantity.unit == LengthUnits.foot
    
    @pytest.mark.parametrize("property_name,expected_unit", [
        ("meters", LengthUnits.meter),
        ("millimeters", LengthUnits.millimeter),
        ("inches", LengthUnits.inch),
        ("feet", LengthUnits.foot)
    ])
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
        
        result = setter.psi
        
        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 14.7
        assert pressure_var.quantity.unit == PressureUnits.psi
    
    def test_kPa_property(self):
        """Test kPa property sets unit correctly."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 101.325)
        
        result = setter.kPa
        
        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 101.325
        assert pressure_var.quantity.unit == PressureUnits.kilopascal
    
    def test_MPa_property(self):
        """Test MPa property sets unit correctly."""
        pressure_var = Pressure("test_pressure")
        setter = PressureSetter(pressure_var, 1.5)
        
        result = setter.MPa
        
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
    
    @pytest.mark.parametrize("property_name,expected_unit", [
        ("psi", PressureUnits.psi),
        ("kPa", PressureUnits.kilopascal),
        ("MPa", PressureUnits.megapascal),
        ("bar", PressureUnits.bar)
    ])
    def test_all_pressure_properties(self, property_name, expected_unit):
        """Test all pressure properties with parametrization."""
        pressure_var = Pressure("parametrized_test")
        setter = PressureSetter(pressure_var, 500.0)
        
        result = getattr(setter, property_name)
        
        assert result is pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 500.0
        assert pressure_var.quantity.unit == expected_unit
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
        width_result = width.set(100.0).millimeters
        height_result = height.set(50.0).inches
        depth_result = depth.set(2.5).feet
        
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
        inlet_result = inlet.set(150.0).psi
        outlet_result = outlet.set(200.0).kPa
        system_result = system.set(2.5).MPa
        
        assert inlet_result is inlet
        assert outlet_result is outlet
        assert system_result is system
        
        # Verify all quantities are set correctly
        assert inlet.quantity is not None and outlet.quantity is not None and system.quantity is not None
        assert inlet.quantity.value == 150.0
        assert inlet.quantity.unit == PressureUnits.psi
        assert outlet.quantity.value == 200.0
        assert outlet.quantity.unit == PressureUnits.kilopascal
        assert system.quantity.value == 2.5
        assert system.quantity.unit == PressureUnits.megapascal
    
    def test_mixed_setter_types(self):
        """Test using both specialized and type-safe setters."""
        length_var = Length("test_length")
        pressure_var = Pressure("test_pressure")
        
        # Use specialized setters
        length_var.set(100.0).meters
        pressure_var.set(14.7).psi
        
        # Use type-safe setter
        TypeSafeSetter(length_var, 200.0).with_unit(LengthUnits.millimeter)
        TypeSafeSetter(pressure_var, 101.325).with_unit(PressureUnits.kilopascal)
        
        # Should have updated values
        assert length_var.quantity is not None and pressure_var.quantity is not None
        assert length_var.quantity.value == 200.0  # Last set wins
        assert length_var.quantity.unit == LengthUnits.millimeter
        assert pressure_var.quantity.value == 101.325  # Last set wins
        assert pressure_var.quantity.unit == PressureUnits.kilopascal
    
    def test_setter_return_consistency(self):
        """Test that all setters return the correct variable instance."""
        length_var = Length("consistency_test")
        
        # All setter methods should return the same variable instance
        meter_result = length_var.set(1.0).meters
        mm_result = length_var.set(1000.0).millimeters
        inch_result = length_var.set(39.37).inches
        foot_result = length_var.set(3.28).feet
        
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
            setter.with_unit(PressureUnits.psi)
        
        assert "psi incompatible with expected dimension" in str(exc_info.value)
    
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
    
    @pytest.mark.parametrize("invalid_value", [float('nan')])
    def test_setter_with_special_float_values(self, invalid_value):
        """Test setters with special float values."""
        length_var = Length("special_test")
        setter = LengthSetter(length_var, invalid_value)
        
        result = setter.meters
        
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
        zero_result = LengthSetter(length_var, 0.0).meters
        assert zero_result.quantity is not None
        assert zero_result.quantity.value == 0.0
        
        # Negative values should work (physics may allow negative measurements)
        negative_result = PressureSetter(pressure_var, -10.0).psi
        assert negative_result.quantity is not None
        assert negative_result.quantity.value == -10.0


class TestSetterIntegration:
    """Test integration between setters and the broader OptiUnit system."""
    
    def test_setter_fastquantity_integration(self):
        """Test that setters create proper FastQuantity instances."""
        length_var = Length("integration_test")
        setter = LengthSetter(length_var, 123.45)
        
        result = setter.millimeters
        
        # Should create a proper FastQuantity
        assert result.quantity is not None
        assert isinstance(result.quantity, FastQuantity)
        assert result.quantity.value == 123.45
        assert result.quantity.unit == LengthUnits.millimeter
        assert result.quantity._si_factor == LengthUnits.millimeter.si_factor
        assert result.quantity._dimension_sig == LENGTH._signature
    
    def test_setter_dimension_signature_consistency(self):
        """Test that setters maintain dimensional consistency."""
        pressure_var = Pressure("dimension_test")
        setter = PressureSetter(pressure_var, 200.0)
        
        result = setter.kPa
        
        # FastQuantity should have correct dimension signature
        assert result.quantity is not None
        assert result.quantity.dimension == PRESSURE
        assert result.quantity._dimension_sig == PRESSURE._signature
        assert result.quantity.dimension.is_compatible(PressureUnits.kilopascal.dimension)
    
    def test_setter_variable_state_changes(self):
        """Test that setters properly change variable state."""
        length_var = Length("state_test")
        
        # Initially should be unset
        assert length_var.quantity is None
        assert "unset" in str(length_var)
        
        # After setting should have quantity
        length_var.set(500.0).millimeters
        assert length_var.quantity is not None
        assert "unset" not in str(length_var)
        assert str(length_var.quantity) in str(length_var)
    
    def test_setter_with_variable_polymorphism(self):
        """Test setters work with variable polymorphism."""
        # Create variables as base TypeSafeVariable references
        length_var: TypeSafeVariable = Length("poly_length")
        pressure_var: TypeSafeVariable = Pressure("poly_pressure")
        
        # TypeSafeSetter should work with polymorphic variables
        TypeSafeSetter(length_var, 100.0).with_unit(LengthUnits.meter)
        TypeSafeSetter(pressure_var, 200.0).with_unit(PressureUnits.psi)
        
        assert length_var.quantity is not None and pressure_var.quantity is not None
        assert length_var.quantity.value == 100.0
        assert length_var.quantity.unit == LengthUnits.meter
        assert pressure_var.quantity.value == 200.0
        assert pressure_var.quantity.unit == PressureUnits.psi
    
    def test_multiple_assignments_to_same_variable(self):
        """Test multiple assignments to the same variable."""
        length_var = Length("multi_assign_test")
        
        # Multiple assignments should update the variable
        length_var.set(100.0).meters
        assert length_var.quantity is not None
        assert length_var.quantity.value == 100.0
        assert length_var.quantity.unit == LengthUnits.meter
        
        # Second assignment should overwrite
        length_var.set(2540.0).millimeters  
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
            setter.meters
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete 1000 operations in reasonable time (< 1 second)
        assert duration < 1.0
    
    def test_cached_fastquantity_performance(self):
        """Test that FastQuantity caching works in setters."""
        length_var = Length("cache_test")
        setter = LengthSetter(length_var, 100.0)
        
        # Set value and check caching
        result = setter.millimeters
        assert result.quantity is not None
        quantity = result.quantity
        
        # FastQuantity should have cached values
        assert hasattr(quantity, '_si_factor')
        assert hasattr(quantity, '_dimension_sig')
        assert quantity._si_factor == LengthUnits.millimeter.si_factor
        assert quantity._dimension_sig == LENGTH._signature


class TestSetterComprehensiveCoverage:
    """Comprehensive edge case coverage for complete testing."""
    
    @pytest.mark.parametrize("length_value,length_unit_prop", [
        (0.001, "millimeters"),
        (1.0, "meters"), 
        (12.0, "inches"),
        (3.28084, "feet"),
        (1e-6, "millimeters"),
        (1e6, "meters")
    ])
    def test_length_comprehensive_values_and_units(self, length_value, length_unit_prop):
        """Comprehensive test of length values and units."""
        length_var = Length(f"comprehensive_length_{length_unit_prop}")
        setter = LengthSetter(length_var, length_value)
        
        result = getattr(setter, length_unit_prop)
        
        assert result is length_var
        assert result.quantity is not None
        assert result.quantity.value == length_value
        assert result.quantity.dimension == LENGTH
    
    @pytest.mark.parametrize("pressure_value,pressure_unit_prop", [
        (14.7, "psi"),
        (101.325, "kPa"),
        (0.101325, "MPa"),
        (1.01325, "bar"),
        (1e-3, "kPa"),
        (1e3, "MPa")
    ])
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
        length_returns = [
            LengthSetter(length_var, 1.0).meters,
            LengthSetter(length_var, 1.0).millimeters,
            LengthSetter(length_var, 1.0).inches,
            LengthSetter(length_var, 1.0).feet
        ]
        
        for returned_var in length_returns:
            assert returned_var is length_var
            assert isinstance(returned_var, Length)
        
        # All pressure setter properties should return Pressure
        pressure_returns = [
            PressureSetter(pressure_var, 1.0).psi,
            PressureSetter(pressure_var, 1.0).kPa,
            PressureSetter(pressure_var, 1.0).MPa,
            PressureSetter(pressure_var, 1.0).bar
        ]
        
        for returned_var in pressure_returns:
            assert returned_var is pressure_var
            assert isinstance(returned_var, Pressure)
        
        # TypeSafeSetter should return the variable
        typesafe_returns = [
            TypeSafeSetter(length_var, 1.0).with_unit(LengthUnits.meter),
            TypeSafeSetter(pressure_var, 1.0).with_unit(PressureUnits.psi)
        ]
        
        assert typesafe_returns[0] is length_var
        assert typesafe_returns[1] is pressure_var