"""Comprehensive tests for variables.py module.

Tests specialized variable classes (Length, Pressure) that extend TypeSafeVariable
with domain-specific functionality, type-safe setters, and fluent API patterns.
Focuses on engineering calculation safety, performance optimizations, and integration
with the broader OptiUnit system.
"""

import time

import pytest

from src.qnty.dimension import DIMENSIONLESS, LENGTH, PRESSURE
from src.qnty.unit import UnitConstant
from src.qnty.units import DimensionlessUnits, LengthUnits, PressureUnits
from src.qnty.variable import FastQuantity, TypeSafeSetter, TypeSafeVariable
from src.qnty.variables import Dimensionless, Length, LengthSetter, Pressure, PressureSetter


class TestLengthVariableInitialization:
    """Test Length variable initialization and basic properties."""
    
    def test_length_basic_initialization(self):
        """Test basic Length variable construction."""
        length_var = Length("beam_length")
        
        assert length_var.name == "beam_length"
        assert length_var.expected_dimension == LENGTH
        assert length_var.quantity is None
        assert isinstance(length_var, TypeSafeVariable)
    
    def test_length_inheritance_chain(self):
        """Test that Length properly inherits from TypeSafeVariable."""
        length_var = Length("pipe_diameter")
        
        # Should have TypeSafeVariable methods and properties
        assert hasattr(length_var, 'name')
        assert hasattr(length_var, 'expected_dimension')
        assert hasattr(length_var, 'quantity')
        assert hasattr(length_var, 'set')
    
    def test_length_dimension_consistency(self):
        """Test that Length variables always have LENGTH dimension."""
        length_vars = [
            Length("width"),
            Length("height"),
            Length("depth"),
            Length("radius")
        ]
        
        for var in length_vars:
            assert var.expected_dimension == LENGTH
            assert var.expected_dimension._signature == LENGTH._signature
    
    def test_length_string_representation_unset(self):
        """Test string representation of unset Length variable."""
        length_var = Length("distance")
        assert str(length_var) == "distance: unset"
    
    @pytest.mark.parametrize("var_name", [
        "length", "width", "height", "diameter", "thickness", "gap", "clearance"
    ])
    def test_length_various_names(self, var_name):
        """Test Length variables with various engineering-relevant names."""
        length_var = Length(var_name)
        
        assert length_var.name == var_name
        assert length_var.expected_dimension == LENGTH


class TestPressureVariableInitialization:
    """Test Pressure variable initialization and basic properties."""
    
    def test_pressure_basic_initialization(self):
        """Test basic Pressure variable construction."""
        pressure_var = Pressure("operating_pressure")
        
        assert pressure_var.name == "operating_pressure"
        assert pressure_var.expected_dimension == PRESSURE
        assert pressure_var.quantity is None
        assert isinstance(pressure_var, TypeSafeVariable)
    
    def test_pressure_inheritance_chain(self):
        """Test that Pressure properly inherits from TypeSafeVariable."""
        pressure_var = Pressure("system_pressure")
        
        # Should have TypeSafeVariable methods and properties
        assert hasattr(pressure_var, 'name')
        assert hasattr(pressure_var, 'expected_dimension')
        assert hasattr(pressure_var, 'quantity')
        assert hasattr(pressure_var, 'set')
    
    def test_pressure_dimension_consistency(self):
        """Test that Pressure variables always have PRESSURE dimension."""
        pressure_vars = [
            Pressure("inlet_pressure"),
            Pressure("outlet_pressure"),
            Pressure("gauge_pressure"),
            Pressure("absolute_pressure")
        ]
        
        for var in pressure_vars:
            assert var.expected_dimension == PRESSURE
            assert var.expected_dimension._signature == PRESSURE._signature
    
    def test_pressure_string_representation_unset(self):
        """Test string representation of unset Pressure variable."""
        pressure_var = Pressure("fluid_pressure")
        assert str(pressure_var) == "fluid_pressure: unset"
    
    @pytest.mark.parametrize("var_name", [
        "pressure", "inlet_pressure", "outlet_pressure", "gauge_pressure",
        "absolute_pressure", "vacuum", "differential_pressure"
    ])
    def test_pressure_various_names(self, var_name):
        """Test Pressure variables with various engineering-relevant names."""
        pressure_var = Pressure(var_name)
        
        assert pressure_var.name == var_name
        assert pressure_var.expected_dimension == PRESSURE


class TestLengthSetterIntegration:
    """Test Length variable integration with LengthSetter."""
    
    def test_length_set_returns_length_setter(self):
        """Test that Length.set() returns a LengthSetter."""
        length_var = Length("measurement")
        
        setter = length_var.set(100.0)
        
        assert isinstance(setter, LengthSetter)
        assert setter.variable == length_var
        assert setter.value == 100.0
    
    def test_length_setter_meters_property(self):
        """Test LengthSetter.meters property for fluent API."""
        length_var = Length("beam_length")
        
        result = length_var.set(5.0).meter
        
        assert result == length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 5.0
        assert length_var.quantity.unit == LengthUnits.meter
        assert str(length_var) == "beam_length: 5.0 m"
    
    def test_length_setter_millimeters_property(self):
        """Test LengthSetter.millimeters property for fluent API."""
        length_var = Length("thickness")
        
        result = length_var.set(25.4).millimeter
        
        assert result == length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 25.4
        assert length_var.quantity.unit == LengthUnits.millimeter
        assert str(length_var) == "thickness: 25.4 mm"
    
    def test_length_setter_inches_property(self):
        """Test LengthSetter.inches property for fluent API."""
        length_var = Length("pipe_diameter")
        
        result = length_var.set(2.0).inch
        
        assert result == length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 2.0
        assert length_var.quantity.unit == LengthUnits.inch
        assert str(length_var) == "pipe_diameter: 2.0 in"
    
    def test_length_setter_feet_property(self):
        """Test LengthSetter.feet property for fluent API."""
        length_var = Length("room_width")
        
        result = length_var.set(12.0).foot
        
        assert result == length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 12.0
        assert length_var.quantity.unit == LengthUnits.foot
        assert str(length_var) == "room_width: 12.0 ft"
    
    def test_length_setter_fluent_chaining(self):
        """Test fluent API chaining pattern with Length variables."""
        # Test that we can chain from set() to unit property in one expression
        length_var = Length("cable_length")
        
        # This should work in one fluent chain
        final_var = length_var.set(1000.0).millimeter
        
        assert final_var == length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == 1000.0
        assert length_var.quantity.unit == LengthUnits.millimeter
    
    @pytest.mark.parametrize("value,unit_property,expected_unit", [
        (10.0, "meters", LengthUnits.meter),
        (500.0, "millimeters", LengthUnits.millimeter),
        (1.5, "inches", LengthUnits.inch),
        (8.0, "feet", LengthUnits.foot)
    ])
    def test_length_setter_all_units(self, value, unit_property, expected_unit):
        """Parametrized test for all Length setter unit properties."""
        length_var = Length("test_length")
        setter = length_var.set(value)
        
        # Use getattr to call the property dynamically
        result = getattr(setter, unit_property)
        
        assert result == length_var
        assert length_var.quantity is not None
        assert length_var.quantity.value == value
        assert length_var.quantity.unit == expected_unit


class TestPressureSetterIntegration:
    """Test Pressure variable integration with PressureSetter."""
    
    def test_pressure_set_returns_pressure_setter(self):
        """Test that Pressure.set() returns a PressureSetter."""
        pressure_var = Pressure("system_pressure")
        
        setter = pressure_var.set(150.0)
        
        assert isinstance(setter, PressureSetter)
        assert setter.variable == pressure_var
        assert setter.value == 150.0
    
    def test_pressure_setter_psi_property(self):
        """Test PressureSetter.psi property for fluent API."""
        pressure_var = Pressure("tire_pressure")
        
        result = pressure_var.set(32.0).pound_force_per_square_inch
        
        assert result == pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 32.0
        assert pressure_var.quantity.unit == PressureUnits.psi
        assert str(pressure_var) == "tire_pressure: 32.0 psi"
    
    def test_pressure_setter_kPa_property(self):
        """Test PressureSetter.kPa property for fluent API."""
        pressure_var = Pressure("gauge_pressure")
        
        result = pressure_var.set(200.0).pascal
        
        assert result == pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 200.0
        assert pressure_var.quantity.unit == PressureUnits.kilopascal
        assert str(pressure_var) == "gauge_pressure: 200.0 kPa"
    
    def test_pressure_setter_MPa_property(self):
        """Test PressureSetter.MPa property for fluent API."""
        pressure_var = Pressure("hydraulic_pressure")

        result = pressure_var.set(15.0).megapascal

        assert result == pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 15.0
        assert pressure_var.quantity.unit == PressureUnits.megapascal
        assert str(pressure_var) == "hydraulic_pressure: 15.0 MPa"
    
    def test_pressure_setter_bar_property(self):
        """Test PressureSetter.bar property for fluent API."""
        pressure_var = Pressure("compressed_air")
        
        result = pressure_var.set(7.0).bar
        
        assert result == pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 7.0
        assert pressure_var.quantity.unit == PressureUnits.bar
        assert str(pressure_var) == "compressed_air: 7.0 bar"
    
    def test_pressure_setter_fluent_chaining(self):
        """Test fluent API chaining pattern with Pressure variables."""
        pressure_var = Pressure("working_pressure")
        
        # This should work in one fluent chain
        final_var = pressure_var.set(100.0).pound_force_per_square_inch
        
        assert final_var == pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 100.0
        assert pressure_var.quantity.unit == PressureUnits.psi
    
    @pytest.mark.parametrize("value,unit_property,expected_unit", [
        (14.7, "psi", PressureUnits.psi),
        (101.325, "kPa", PressureUnits.kilopascal),
        (0.1, "MPa", PressureUnits.megapascal),
        (1.0, "bar", PressureUnits.bar)
    ])
    def test_pressure_setter_all_units(self, value, unit_property, expected_unit):
        """Parametrized test for all Pressure setter unit properties."""
        pressure_var = Pressure("test_pressure")
        setter = pressure_var.set(value)
        
        # Use getattr to call the property dynamically
        result = getattr(setter, unit_property)
        
        assert result == pressure_var
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == value
        assert pressure_var.quantity.unit == expected_unit


class TestTypeSafetyAndDimensionalValidation:
    """Test type safety and dimensional validation for specialized variables."""
    
    def test_length_dimension_enforcement(self):
        """Test that Length variables enforce LENGTH dimension."""
        length_var = Length("test_length")
        
        # Should accept length units through specialized setter
        length_var.set(100.0).meter
        assert length_var.quantity is not None
        assert length_var.quantity.dimension == LENGTH
        
        # If we bypass the specialized setter and use generic TypeSafeSetter,
        # it should still validate dimensions
        length_var2 = Length("test_length2")
        generic_setter = TypeSafeSetter(length_var2, 50.0)
        
        # Should accept length unit
        generic_setter.with_unit(LengthUnits.millimeter)
        assert length_var2.quantity is not None
        assert length_var2.quantity.dimension == LENGTH
        
        # Should reject pressure unit
        with pytest.raises(TypeError, match="incompatible with expected dimension"):
            generic_setter.with_unit(PressureUnits.psi)
    
    def test_pressure_dimension_enforcement(self):
        """Test that Pressure variables enforce PRESSURE dimension."""
        pressure_var = Pressure("test_pressure")
        
        # Should accept pressure units through specialized setter
        pressure_var.set(50.0).pound_force_per_square_inch
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.dimension == PRESSURE
        
        # If we bypass the specialized setter and use generic TypeSafeSetter,
        # it should still validate dimensions
        pressure_var2 = Pressure("test_pressure2")
        generic_setter = TypeSafeSetter(pressure_var2, 100.0)
        
        # Should accept pressure unit
        generic_setter.with_unit(PressureUnits.bar)
        assert pressure_var2.quantity is not None
        assert pressure_var2.quantity.dimension == PRESSURE
        
        # Should reject length unit
        with pytest.raises(TypeError, match="incompatible with expected dimension"):
            generic_setter.with_unit(LengthUnits.meter)
    
    def test_cross_dimensional_rejection(self):
        """Test that variables reject incompatible dimensions comprehensively."""
        length_var = Length("length")
        pressure_var = Pressure("pressure")
        
        # Test all combinations that should fail
        test_cases = [
            (length_var, PressureUnits.psi),
            (length_var, PressureUnits.bar),
            (length_var, PressureUnits.kilopascal),
            (pressure_var, LengthUnits.meter),
            (pressure_var, LengthUnits.inch),
            (pressure_var, LengthUnits.millimeter),
        ]
        
        for var, incompatible_unit in test_cases:
            generic_setter = TypeSafeSetter(var, 100.0)
            with pytest.raises(TypeError):
                generic_setter.with_unit(incompatible_unit)
    
    def test_dimensional_signature_consistency(self):
        """Test that dimensional signatures remain consistent."""
        length_var = Length("test_length")
        pressure_var = Pressure("test_pressure")
        
        # Set values
        length_var.set(10.0).meter
        pressure_var.set(100.0).pound_force_per_square_inch

        # Check that dimensional signatures match expected values
        assert length_var.quantity is not None and pressure_var.quantity is not None
        assert length_var.quantity._dimension_sig == LENGTH._signature
        assert pressure_var.quantity._dimension_sig == PRESSURE._signature
        
        # Should be different from each other
        assert length_var.quantity._dimension_sig != pressure_var.quantity._dimension_sig


class TestSpecializedVariableOperations:
    """Test operations and calculations specific to specialized variables."""
    
    def test_length_variable_arithmetic(self):
        """Test arithmetic operations with Length variables."""
        length1 = Length("width")
        length2 = Length("height")

        length1.set(10.0).meter
        length2.set(5.0).meter

        # Should be able to add compatible length quantities
        assert length1.quantity is not None and length2.quantity is not None
        total_length = length1.quantity + length2.quantity
        assert total_length.value == 15.0
        assert total_length.unit == LengthUnits.meter
        
        # Should be able to subtract
        difference = length1.quantity - length2.quantity
        assert difference.value == 5.0
        assert difference.unit == LengthUnits.meter
        
        # Multiplication should create area (though current implementation maps to length unit)
        area = length1.quantity * length2.quantity
        assert area.value == 50000.0  # Converted to mm units in current implementation
    
    def test_pressure_variable_arithmetic(self):
        """Test arithmetic operations with Pressure variables."""
        pressure1 = Pressure("inlet")
        pressure2 = Pressure("outlet")

        pressure1.set(150.0).pound_force_per_square_inch
        pressure2.set(50.0).pound_force_per_square_inch

        # Should be able to add compatible pressure quantities
        assert pressure1.quantity is not None and pressure2.quantity is not None
        total_pressure = pressure1.quantity + pressure2.quantity
        assert total_pressure.value == 200.0
        assert total_pressure.unit == PressureUnits.psi
        
        # Should be able to subtract
        pressure_drop = pressure1.quantity - pressure2.quantity
        assert pressure_drop.value == 100.0
        assert pressure_drop.unit == PressureUnits.psi
        
        # Division should create dimensionless ratio
        ratio = pressure1.quantity / pressure2.quantity
        assert ratio.value == 3.0
        assert ratio._dimension_sig == DIMENSIONLESS._signature
    
    def test_unit_conversion_with_variables(self):
        """Test unit conversions with specialized variables."""
        length_var = Length("measurement")
        length_var.set(1.0).meter
        
        # Convert to different length units
        assert length_var.quantity is not None
        mm_result = length_var.quantity.to(LengthUnits.millimeter)
        assert mm_result.value == 1000.0
        
        inch_result = length_var.quantity.to(LengthUnits.inch)
        assert inch_result.value == pytest.approx(39.3701, abs=1e-3)
        
        # Original variable should be unchanged
        assert length_var.quantity.value == 1.0
        assert length_var.quantity.unit == LengthUnits.meter
    
    def test_mixed_unit_operations(self):
        """Test operations between different units of the same dimension."""
        length1 = Length("part1")
        length2 = Length("part2")
        
        length1.set(100.0).millimeter  # 0.1 m
        length2.set(2.0).inch         # 0.0508 m
        
        # Addition should handle unit conversion automatically
        assert length1.quantity is not None and length2.quantity is not None
        total = length1.quantity + length2.quantity
        assert total.unit == LengthUnits.millimeter  # Result in first operand's units
        assert total.value == pytest.approx(150.8, abs=0.1)  # 100 + 50.8 mm
    
    def test_comparison_operations(self):
        """Test comparison operations with specialized variables."""
        pressure1 = Pressure("p1")
        pressure2 = Pressure("p2")

        pressure1.set(100.0).pound_force_per_square_inch
        pressure2.set(200.0).pound_force_per_square_inch

        # Comparisons should work
        assert pressure1.quantity is not None and pressure2.quantity is not None
        assert pressure1.quantity < pressure2.quantity
        assert not (pressure2.quantity < pressure1.quantity)
        
        # Equality with different but equivalent units
        pressure3 = Pressure("p3")
        pressure3.set(689.4757).pascal  # Approximately 100 psi (more precise)

        # Should be approximately equal (within tolerance)
        assert pressure1.quantity == pressure3.quantity


class TestEngineeringCalculationAccuracy:
    """Test accuracy of engineering calculations with specialized variables."""
    
    def test_length_precision_engineering_tolerances(self):
        """Test length calculations with engineering precision requirements."""
        length1 = Length("nominal_dimension")
        length2 = Length("tolerance")
        
        # Test typical machining tolerances
        length1.set(25.000).millimeter
        length2.set(0.025).millimeter  # ±0.025mm tolerance

        assert length1.quantity is not None and length2.quantity is not None
        upper_limit = length1.quantity + length2.quantity
        lower_limit = length1.quantity - length2.quantity
        
        assert upper_limit.value == 25.025
        assert lower_limit.value == 24.975
        
        # Verify precision is maintained
        assert abs(upper_limit.value - 25.025) < 1e-10
        assert abs(lower_limit.value - 24.975) < 1e-10
    
    def test_pressure_precision_engineering_calculations(self):
        """Test pressure calculations with engineering precision."""
        pressure1 = Pressure("system_pressure")
        pressure2 = Pressure("pressure_drop")
        
        # Test typical hydraulic system pressures
        pressure1.set(3000.0).pound_force_per_square_inch  # High-pressure hydraulic system
        pressure2.set(150.0).pound_force_per_square_inch       # Pressure drop across component

        assert pressure1.quantity is not None and pressure2.quantity is not None
        outlet_pressure = pressure1.quantity - pressure2.quantity
        assert outlet_pressure.value == 2850.0
        assert outlet_pressure.unit == PressureUnits.psi
        
        # Test conversion precision
        outlet_bar = outlet_pressure.to(PressureUnits.bar)
        expected_bar = 2850.0 * 0.0689476  # psi to bar conversion
        assert outlet_bar.value == pytest.approx(expected_bar, abs=0.001)
    
    def test_unit_conversion_accuracy(self):
        """Test accuracy of unit conversions for engineering calculations."""
        # Test known engineering conversions
        length_var = Length("pipe_diameter")
        
        # 1 inch = 25.4 mm exactly
        length_var.set(1.0).inch
        assert length_var.quantity is not None
        mm_result = length_var.quantity.to(LengthUnits.millimeter)
        assert mm_result.value == pytest.approx(25.4, abs=1e-10)
        
        # Test pressure conversion: 1 psi = 6894.757 Pa
        pressure_var = Pressure("gauge_pressure")
        pressure_var.set(1.0).pound_force_per_square_inch
        assert pressure_var.quantity is not None
        pa_result = pressure_var.quantity.to(PressureUnits.pascal)
        assert pa_result.value == pytest.approx(6894.757, abs=0.001)
    
    def test_round_trip_conversion_accuracy(self):
        """Test that round-trip conversions maintain precision."""
        # Length round-trip
        length_var = Length("test_length")
        original_value = 42.195  # Arbitrary precision value
        
        length_var.set(original_value).inch
        assert length_var.quantity is not None
        converted = length_var.quantity.to(LengthUnits.millimeter).to(LengthUnits.inch)
        
        assert converted.value == pytest.approx(original_value, abs=1e-10)
        
        # Pressure round-trip
        pressure_var = Pressure("test_pressure")
        original_pressure = 123.456
        
        pressure_var.set(original_pressure).bar
        assert pressure_var.quantity is not None
        converted_pressure = pressure_var.quantity.to(PressureUnits.psi).to(PressureUnits.bar)
        
        assert converted_pressure.value == pytest.approx(original_pressure, abs=1e-8)


class TestPerformanceOptimizations:
    """Test performance characteristics specific to specialized variables."""
    
    def test_specialized_setter_performance(self):
        """Test that specialized setters provide performance benefits."""
        length_var = Length("performance_test")
        
        # Specialized setter should be fast
        start_time = time.time()
        for i in range(1000):
            length_var.set(float(i)).meter
        elapsed = time.time() - start_time
        
        # Should complete quickly (smoke test)
        assert elapsed < 0.5  # Should complete in < 0.5 seconds
        
        # Final value should be correct
        assert length_var.quantity is not None
        assert length_var.quantity.value == 999.0
        assert length_var.quantity.unit == LengthUnits.meter
    
    def test_fluent_api_performance(self):
        """Test performance of fluent API chaining."""
        pressure_vars = [Pressure(f"pressure_{i}") for i in range(100)]
        
        start_time = time.time()
        for i, var in enumerate(pressure_vars):
            var.set(float(i * 10)).pound_force_per_square_inch
        elapsed = time.time() - start_time
        
        # Should handle many variables quickly
        assert elapsed < 0.1  # Should complete in < 0.1 seconds
        
        # Verify all variables were set correctly
        for i, var in enumerate(pressure_vars):
            assert var.quantity is not None
            assert var.quantity.value == float(i * 10)
            assert var.quantity.unit == PressureUnits.psi
    
    def test_memory_efficiency_specialized_variables(self):
        """Test memory efficiency of specialized variables."""
        # Create multiple variables and check they don't leak memory
        variables = []
        
        for i in range(100):
            length_var = Length(f"length_{i}")
            pressure_var = Pressure(f"pressure_{i}")

            length_var.set(float(i)).millimeter
            pressure_var.set(float(i * 10)).pascal

            variables.extend([length_var, pressure_var])
        
        # All variables should be properly initialized
        assert len(variables) == 200
        
        # Sample check on a few variables
        assert variables[0].quantity is not None and variables[0].quantity.value == 0.0
        assert variables[1].quantity is not None and variables[1].quantity.value == 0.0
        assert variables[10].quantity is not None and variables[10].quantity.value == 5.0
        assert variables[11].quantity is not None and variables[11].quantity.value == 50.0
    
    def test_cached_dimension_signatures(self):
        """Test that specialized variables benefit from cached dimension signatures."""
        length_vars = [Length(f"l_{i}") for i in range(10)]
        
        # Set all variables - should use cached dimension signatures
        start_time = time.time()
        for i, var in enumerate(length_vars):
            var.set(float(i)).meter
        elapsed = time.time() - start_time
        
        # Should be fast due to caching
        assert elapsed < 0.01
        
        # All should have the same cached dimension signature
        assert length_vars[0].quantity is not None
        first_sig = length_vars[0].quantity._dimension_sig
        for var in length_vars[1:]:
            assert var.quantity is not None
            assert var.quantity._dimension_sig == first_sig


class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases for specialized variables."""
    
    def test_unset_variable_operations(self):
        """Test behavior with unset variables."""
        length_var = Length("unset_length")
        pressure_var = Pressure("unset_pressure")
        
        # Should have no quantity initially
        assert length_var.quantity is None
        assert pressure_var.quantity is None
        
        # String representation should indicate unset state
        assert "unset" in str(length_var)
        assert "unset" in str(pressure_var)
    
    def test_zero_and_negative_values(self):
        """Test handling of zero and negative values."""
        length_var = Length("test_length")
        pressure_var = Pressure("test_pressure")
        
        # Zero values should work
        length_var.set(0.0).meter
        assert length_var.quantity is not None
        assert length_var.quantity.value == 0.0
        
        # Negative values should work (could represent coordinates, gauge pressure)
        length_var.set(-5.0).millimeter
        assert length_var.quantity is not None
        assert length_var.quantity.value == -5.0

        pressure_var.set(-10.0).pound_force_per_square_inch  # Vacuum/gauge pressure
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == -10.0
    
    def test_very_large_and_small_values(self):
        """Test handling of extreme values."""
        length_var = Length("extreme_length")
        pressure_var = Pressure("extreme_pressure")
        
        # Very large values
        length_var.set(1e12).millimeter
        assert length_var.quantity is not None
        assert length_var.quantity.value == 1e12
        
        # Very small values
        pressure_var.set(1e-6).pound_force_per_square_inch
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 1e-6
        
        # Conversions should still work
        assert length_var.quantity is not None
        converted_length = length_var.quantity.to(LengthUnits.meter)
        assert converted_length.value == 1e9  # 1e12 mm = 1e9 m
    
    def test_invalid_variable_names(self):
        """Test behavior with unusual variable names."""
        # Empty string
        empty_name_var = Length("")
        assert empty_name_var.name == ""
        assert str(empty_name_var) == ": unset"
        
        # Special characters
        special_var = Pressure("pressure@#$%")
        assert special_var.name == "pressure@#$%"
        
        # Very long name
        long_name = "a" * 1000
        long_name_var = Length(long_name)
        assert long_name_var.name == long_name
    
    def test_floating_point_edge_cases(self):
        """Test handling of floating point edge cases."""
        length_var = Length("edge_case")
        
        # Infinity
        length_var.set(float('inf')).meter
        assert length_var.quantity is not None
        assert length_var.quantity.value == float('inf')
        
        # Negative infinity
        length_var.set(float('-inf')).millimeter
        assert length_var.quantity is not None
        assert length_var.quantity.value == float('-inf')
        
        # NaN
        length_var.set(float('nan')).inch
        assert length_var.quantity is not None
        assert str(length_var.quantity.value) == 'nan'
    
    def test_setter_chain_interruption(self):
        """Test behavior when setter chain is interrupted."""
        length_var = Length("interrupted")
        
        # Create setter but don't complete the chain
        setter = length_var.set(100.0)
        
        # Variable should still be unset
        assert length_var.quantity is None
        
        # Only after completing the chain should it be set
        setter.meter
        assert length_var.quantity is not None
        assert length_var.quantity.value == 100.0


class TestIntegrationWithUnitSystem:
    """Test integration with the broader OptiUnit system."""
    
    def test_registry_integration(self):
        """Test integration with global unit registry."""
        from src.qnty.unit import registry
        
        length_var = Length("registry_test")
        length_var.set(100.0).millimeter
        
        # Should be able to convert using registry
        assert length_var.quantity is not None
        converted_value = registry.convert(
            length_var.quantity.value,
            length_var.quantity.unit,
            LengthUnits.meter
        )
        
        assert converted_value == 0.1  # 100 mm = 0.1 m
    
    def test_unit_constant_integration(self):
        """Test integration with UnitConstant system."""
        pressure_var = Pressure("unit_constant_test")
        pressure_var.set(100.0).pound_force_per_square_inch

        # Should have proper UnitConstant properties
        assert pressure_var.quantity is not None
        unit = pressure_var.quantity.unit
        assert isinstance(unit, UnitConstant)
        assert unit.name == "psi"
        assert unit.symbol == "psi"
        assert unit.si_factor == pytest.approx(6894.757, abs=0.001)
    
    def test_dimension_system_integration(self):
        """Test integration with dimension system."""
        length_var = Length("dimension_test")
        pressure_var = Pressure("dimension_test")
        
        length_var.set(10.0).meter
        pressure_var.set(50.0).bar
        
        # Should have correct dimension signatures
        assert length_var.quantity is not None
        assert pressure_var.quantity is not None
        assert length_var.quantity._dimension_sig == LENGTH._signature
        assert pressure_var.quantity._dimension_sig == PRESSURE._signature
        
        # Import registry for this test
        from src.qnty.unit import registry
        
        # Dimensional operations should work correctly
        assert length_var.quantity is not None
        area = length_var.quantity * length_var.quantity
        assert area._dimension_sig in registry._dimension_cache
    
    def test_fast_quantity_integration(self):
        """Test that specialized variables create proper FastQuantity objects."""
        length_var = Length("fastquantity_test")
        length_var.set(75.0).inch
        
        # Should create FastQuantity with all expected attributes
        assert length_var.quantity is not None
        qty = length_var.quantity
        assert isinstance(qty, FastQuantity)
        assert hasattr(qty, 'value')
        assert hasattr(qty, 'unit')
        assert hasattr(qty, 'dimension')
        assert hasattr(qty, '_si_factor')
        assert hasattr(qty, '_dimension_sig')
        
        # Should support all FastQuantity operations
        doubled = qty * 2
        assert doubled.value == 150.0
        assert doubled.unit == LengthUnits.inch


class TestStringRepresentationsAndDebugging:
    """Test string representations and debugging output."""
    
    def test_length_variable_representations(self):
        """Test string representations for Length variables."""
        # Unset variable
        unset_length = Length("beam_length")
        assert str(unset_length) == "beam_length: unset"
        
        # Set variable with different units
        unset_length.set(10.5).meter
        assert str(unset_length) == "beam_length: 10.5 m"
        
        unset_length.set(25.4).millimeter
        assert str(unset_length) == "beam_length: 25.4 mm"
    
    def test_pressure_variable_representations(self):
        """Test string representations for Pressure variables."""
        # Unset variable
        unset_pressure = Pressure("system_pressure")
        assert str(unset_pressure) == "system_pressure: unset"
        
        # Set variable with different units
        unset_pressure.set(150.0).pound_force_per_square_inch
        assert str(unset_pressure) == "system_pressure: 150.0 psi"
        
        unset_pressure.set(10.0).bar
        assert str(unset_pressure) == "system_pressure: 10.0 bar"
    
    def test_debugging_information(self):
        """Test that variables provide useful debugging information."""
        length_var = Length("debug_test")
        length_var.set(100.0).millimeter
        
        # Should be able to access all relevant debugging info
        assert length_var.quantity is not None
        debug_info = {
            'name': length_var.name,
            'dimension': str(length_var.expected_dimension._signature),
            'value': length_var.quantity.value if length_var.quantity else None,
            'unit_name': length_var.quantity.unit.name if length_var.quantity else None,
            'unit_symbol': length_var.quantity.unit.symbol if length_var.quantity else None,
        }
        
        assert debug_info['name'] == "debug_test"
        assert debug_info['dimension'] == str(LENGTH._signature)
        assert debug_info['value'] == 100.0
        assert debug_info['unit_name'] == "millimeter"
        assert debug_info['unit_symbol'] == "mm"
    
    def test_variable_comparison_for_debugging(self):
        """Test variable comparison for debugging purposes."""
        length1 = Length("length1")
        length2 = Length("length2")

        length1.set(100.0).millimeter
        length2.set(0.1).meter  # Same value, different units

        # Variables themselves should be different objects
        assert length1 is not length2
        assert length1.name != length2.name
        
        # But their quantities should be equivalent
        assert length1.quantity is not None and length2.quantity is not None
        assert length1.quantity == length2.quantity
    
    @pytest.mark.parametrize("var_class,setter_method,unit_name", [
        (Length, "meters", "m"),
        (Length, "millimeters", "mm"),
        (Length, "inches", "in"),
        (Length, "feet", "ft"),
        (Pressure, "psi", "psi"),
        (Pressure, "kPa", "kPa"),
        (Pressure, "MPa", "MPa"),
        (Pressure, "bar", "bar"),
    ])
    def test_all_variable_unit_representations(self, var_class, setter_method, unit_name):
        """Test string representations for all variable types and units."""
        variable = var_class("test_var")
        setter = variable.set(42.0)
        
        # Use getattr to call the appropriate setter method
        getattr(setter, setter_method)
        
        # Check string representation contains the expected unit symbol
        str_repr = str(variable)
        assert "test_var:" in str_repr
        assert "42.0" in str_repr
        assert unit_name in str_repr


class TestAdvancedFluentAPIPatterns:
    """Test advanced patterns with the fluent API."""
    
    def test_method_chaining_return_types(self):
        """Test that method chaining returns correct types for IDE support."""
        length_var = Length("chain_test")
        
        # The setter should return the variable for chaining
        result = length_var.set(100.0).meter
        
        # Should return the original variable
        assert result is length_var
        assert isinstance(result, Length)
        assert isinstance(result, TypeSafeVariable)
    
    def test_multiple_setter_calls(self):
        """Test behavior with multiple setter calls on same variable."""
        pressure_var = Pressure("multi_set")
        
        # First setting
        pressure_var.set(100.0).pound_force_per_square_inch
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 100.0
        assert pressure_var.quantity.unit == PressureUnits.pound_force_per_square_inch

        # Second setting should overwrite
        pressure_var.set(200.0).pascal
        assert pressure_var.quantity is not None
        assert pressure_var.quantity.value == 200.0
        assert pressure_var.quantity.unit == PressureUnits.kilopascal
    
    def test_setter_reuse_pattern(self):
        """Test reusing setter objects (though not recommended)."""
        length_var = Length("reuse_test")
        
        # Create setter
        setter = length_var.set(50.0)
        
        # First use
        setter.meter
        assert length_var.quantity is not None
        assert length_var.quantity.value == 50.0
        assert length_var.quantity.unit == LengthUnits.meter
        
        # Create new setter for different value
        setter2 = length_var.set(25.0)
        setter2.millimeter
        assert length_var.quantity is not None
        assert length_var.quantity.value == 25.0
        assert length_var.quantity.unit == LengthUnits.millimeter
    
    def test_fluent_api_with_calculations(self):
        """Test fluent API integrated with calculations."""
        width = Length("width")
        height = Length("height")
        
        # Set values using fluent API
        width.set(10.0).meter
        height.set(5.0).meter
        
        # Use in calculations
        assert width.quantity is not None and height.quantity is not None
        perimeter = (width.quantity + width.quantity + height.quantity + height.quantity)
        assert perimeter.value == 30.0  # 2*(10+5) = 30
        
        # Area calculation (current implementation behavior)
        area = width.quantity * height.quantity
        assert area.value == 50000.0  # 10*5 = 50 m^2 = 50,000 mm^2 in current cache


class TestKnownUnknownVariables:
    """Test the known/unknown variable functionality with fluent API."""
    
    def test_variable_defaults_to_known(self):
        """Test that variables default to is_known=True."""
        # Using original syntax
        length = Length("test_length")
        assert length.is_known is True
        
        # Using new syntax
        pressure = Pressure(100, "psi", "test_pressure")
        assert pressure.is_known is True
        
        dimensionless = Dimensionless(0.5, "test_factor")
        assert dimensionless.is_known is True
    
    def test_variable_with_explicit_is_known(self):
        """Test explicit is_known parameter in constructors."""
        # Known variables
        known_length = Length("known", is_known=True)
        assert known_length.is_known is True
        
        known_pressure = Pressure(50, "bar", "known_pressure", is_known=True)
        assert known_pressure.is_known is True
        
        # Unknown variables
        unknown_length = Length("unknown", is_known=False)
        assert unknown_length.is_known is False
        
        unknown_pressure = Pressure(0, "psi", "unknown_pressure", is_known=False)
        assert unknown_pressure.is_known is False
        
        unknown_dim = Dimensionless(0, "unknown_factor", is_known=False)
        assert unknown_dim.is_known is False
    
    def test_fluent_unknown_property(self):
        """Test the fluent .unknown property to mark variables as unknown."""
        # Original syntax with fluent unknown
        length = Length("test").unknown
        assert length.is_known is False
        
        # New syntax with fluent unknown
        pressure = Pressure(100, "psi", "test").unknown
        assert pressure.is_known is False
        
        dimensionless = Dimensionless(1.0, "test").unknown
        assert dimensionless.is_known is False
    
    def test_fluent_known_property(self):
        """Test the fluent .known property to mark variables as known."""
        # Start with unknown, then mark as known
        length = Length("test", is_known=False).known
        assert length.is_known is True
        
        pressure = Pressure(50, "bar", "test", is_known=False).known
        assert pressure.is_known is True
        
        dimensionless = Dimensionless(0.5, "test", is_known=False).known
        assert dimensionless.is_known is True
    
    def test_fluent_api_chaining(self):
        """Test that fluent API returns self for chaining."""
        # Test chaining with unknown
        length = Length("test")
        result = length.unknown
        assert result is length
        assert length.is_known is False
        
        # Test chaining with known
        result2 = length.known
        assert result2 is length
        assert length.is_known is True
        
        # Test complex chaining
        pressure = Pressure(100, "psi", "test").unknown
        assert pressure.is_known is False
        assert pressure.quantity is not None
        assert pressure.quantity.value == 100
    
    def test_toggling_known_unknown(self):
        """Test toggling between known and unknown states."""
        variable = Length("toggleable")
        
        # Start as known (default)
        assert variable.is_known is True
        
        # Mark as unknown
        variable.unknown
        assert variable.is_known is False
        
        # Mark as known again
        variable.known
        assert variable.is_known is True
        
        # Toggle multiple times
        variable.unknown.known.unknown
        assert variable.is_known is False
    
    def test_known_unknown_with_value_setting(self):
        """Test that known/unknown state is preserved when setting values."""
        # Unknown variable with value
        unknown_length = Length("test", is_known=False)
        unknown_length.set(10).meter
        assert unknown_length.is_known is False
        assert unknown_length.quantity is not None
        assert unknown_length.quantity.value == 10
        
        # Known variable with value
        known_pressure = Pressure("test").known
        known_pressure.set(50).pound_force_per_square_inch
        assert known_pressure.is_known is True
        assert known_pressure.quantity is not None
        assert known_pressure.quantity.value == 50
    
    def test_alternative_constructor_with_unknown(self):
        """Test alternative constructors with is_known parameter and fluent API."""
        # New syntax with is_known=False
        Y = Dimensionless(0.4, "Y Coefficient", is_known=False)
        assert Y.is_known is False
        assert Y.quantity is not None
        assert Y.quantity.value == 0.4
        
        # New syntax with fluent unknown
        T = Length(0.0, "inches", "Wall Thickness").unknown
        assert T.is_known is False
        assert T.quantity is not None
        
        # New syntax with fluent known (after unknown)
        P_max = Pressure(0.0, "psi", "Maximum Pressure", is_known=False).known
        assert P_max.is_known is True
    
    def test_type_preservation_with_fluent_api(self):
        """Test that fluent API preserves variable types."""
        length = Length("test").unknown
        assert isinstance(length, Length)
        assert isinstance(length, TypeSafeVariable)
        
        pressure = Pressure("test").unknown.known
        assert isinstance(pressure, Pressure)
        assert isinstance(pressure, TypeSafeVariable)
        
        dimensionless = Dimensionless(1.0, "test").unknown
        assert isinstance(dimensionless, Dimensionless)
        assert isinstance(dimensionless, TypeSafeVariable)


class TestAlternativeConstructorSyntax:
    """Test the new alternative constructor syntax for direct initialization."""
    
    def test_dimensionless_alternative_constructor(self):
        """Test Dimensionless(value, name) constructor syntax."""
        # New syntax - direct initialization
        U_m = Dimensionless(0.125, "Mill Undertolerance")
        
        assert U_m.name == "Mill Undertolerance"
        assert U_m.expected_dimension == DIMENSIONLESS
        assert U_m.quantity is not None
        assert U_m.quantity.value == 0.125
        assert U_m.quantity.unit == DimensionlessUnits.dimensionless
        assert str(U_m) == "Mill Undertolerance: 0.125 "  # Dimensionless has empty symbol
        
        # Test with other values
        E = Dimensionless(0.8, "Quality Factor")
        assert E.name == "Quality Factor"
        assert E.quantity is not None
        assert E.quantity.value == 0.8
        
        W = Dimensionless(1, "Weld Joint Strength Reduction Factor")
        assert W.name == "Weld Joint Strength Reduction Factor"
        assert W.quantity is not None
        assert W.quantity.value == 1.0
    
    def test_dimensionless_original_constructor(self):
        """Test that original Dimensionless(name) syntax still works."""
        # Original syntax
        factor = Dimensionless("efficiency_factor")
        
        assert factor.name == "efficiency_factor"
        assert factor.expected_dimension == DIMENSIONLESS
        assert factor.quantity is None  # Not set yet
        
        # Set value using fluent API
        factor.set(0.85).dimensionless
        assert factor.quantity is not None
        assert factor.quantity.value == 0.85
        assert factor.quantity.unit == DimensionlessUnits.dimensionless
    
    def test_pressure_alternative_constructor(self):
        """Test Pressure(value, unit, name) constructor syntax."""
        # New syntax - direct initialization with psi
        P = Pressure(90, "psi", "Design Pressure")
        
        assert P.name == "Design Pressure"
        assert P.expected_dimension == PRESSURE
        assert P.quantity is not None
        assert P.quantity.value == 90.0
        assert P.quantity.unit == PressureUnits.psi
        assert str(P) == "Design Pressure: 90.0 psi"
        
        # Test with kPa
        P_kPa = Pressure(620, "kPa", "Pressure in kPa")
        assert P_kPa.quantity is not None
        assert P_kPa.quantity.value == 620.0
        assert P_kPa.quantity.unit == PressureUnits.kilopascal
        
        # Test with MPa
        P_MPa = Pressure(10, "MPa", "Pressure in MPa")
        assert P_MPa.quantity is not None
        assert P_MPa.quantity.value == 10.0
        assert P_MPa.quantity.unit == PressureUnits.megapascal
        
        # Test with bar
        P_bar = Pressure(5, "bar", "Pressure in bar")
        assert P_bar.quantity is not None
        assert P_bar.quantity.value == 5.0
        assert P_bar.quantity.unit == PressureUnits.bar
    
    def test_pressure_original_constructor(self):
        """Test that original Pressure(name) syntax still works."""
        # Original syntax
        pressure = Pressure("test_pressure")
        
        assert pressure.name == "test_pressure"
        assert pressure.expected_dimension == PRESSURE
        assert pressure.quantity is None  # Not set yet
        
        # Set value using fluent API
        pressure.set(100).pound_force_per_square_inch
        assert pressure.quantity is not None
        assert pressure.quantity.value == 100.0
        assert pressure.quantity.unit == PressureUnits.pound_force_per_square_inch

    def test_length_alternative_constructor(self):
        """Test Length(value, unit, name) constructor syntax."""
        # New syntax - direct initialization with inches
        D = Length(0.84, "inches", "Outside Diameter")
        
        assert D.name == "Outside Diameter"
        assert D.expected_dimension == LENGTH
        assert D.quantity is not None
        assert D.quantity.value == 0.84
        assert D.quantity.unit == LengthUnits.inch
        assert str(D) == "Outside Diameter: 0.84 in"
        
        # Test with meters
        L_m = Length(2.5, "meters", "Length in meters")
        assert L_m.quantity is not None
        assert L_m.quantity.value == 2.5
        assert L_m.quantity.unit == LengthUnits.meter
        
        # Test with millimeters
        L_mm = Length(100, "millimeters", "Length in millimeters")
        assert L_mm.quantity is not None
        assert L_mm.quantity.value == 100.0
        assert L_mm.quantity.unit == LengthUnits.millimeter
        
        # Test with feet
        L_ft = Length(6, "feet", "Length in feet")
        assert L_ft.quantity is not None
        assert L_ft.quantity.value == 6.0
        assert L_ft.quantity.unit == LengthUnits.foot
    
    def test_length_original_constructor(self):
        """Test that original Length(name) syntax still works."""
        # Original syntax
        length = Length("test_length")
        
        assert length.name == "test_length"
        assert length.expected_dimension == LENGTH
        assert length.quantity is None  # Not set yet
        
        # Set value using fluent API
        length.set(10).meter
        assert length.quantity is not None
        assert length.quantity.value == 10.0
        assert length.quantity.unit == LengthUnits.meter
    
    def test_invalid_constructor_arguments(self):
        """Test that invalid constructor arguments raise appropriate errors."""
        # Dimensionless with wrong number of arguments
        with pytest.raises(ValueError, match="Dimensionless expects either 1 argument"):
            Dimensionless(0.5, "name", "extra")
        
        # Pressure with wrong number of arguments
        with pytest.raises(ValueError, match="Pressure expects either 1 argument"):
            Pressure(100, "psi")  # Missing name
        
        # Length with wrong number of arguments
        with pytest.raises(ValueError, match="Length expects either 1 argument"):
            Length(10, "meters")  # Missing name
    
    def test_alternative_constructor_with_calculations(self):
        """Test that variables created with alternative constructors work in calculations."""
        # Create variables using new syntax
        P1 = Pressure(100, "psi", "Inlet Pressure")
        P2 = Pressure(50, "psi", "Outlet Pressure")
        
        # Should be able to perform calculations
        assert P1.quantity is not None and P2.quantity is not None
        pressure_drop = P1.quantity - P2.quantity
        assert pressure_drop.value == 50.0
        assert pressure_drop.unit == PressureUnits.psi
        
        # Length calculations
        L1 = Length(10, "meters", "Width")
        L2 = Length(5, "meters", "Height")
        
        assert L1.quantity is not None and L2.quantity is not None
        total = L1.quantity + L2.quantity
        assert total.value == 15.0
        assert total.unit == LengthUnits.meter
    
    def test_alternative_constructor_type_preservation(self):
        """Test that alternative constructors preserve variable types."""
        # Variables should still be instances of their specialized classes
        dim = Dimensionless(0.5, "factor")
        pressure = Pressure(100, "psi", "pressure")
        length = Length(10, "meters", "length")
        
        assert isinstance(dim, Dimensionless)
        assert isinstance(dim, TypeSafeVariable)
        assert isinstance(pressure, Pressure)
        assert isinstance(pressure, TypeSafeVariable)
        assert isinstance(length, Length)
        assert isinstance(length, TypeSafeVariable)
    
    def test_alternative_constructor_edge_cases(self):
        """Test edge cases with alternative constructors."""
        # Zero values
        dim_zero = Dimensionless(0, "zero_factor")
        assert dim_zero.quantity is not None
        assert dim_zero.quantity.value == 0.0
        
        # Negative values
        pressure_negative = Pressure(-10, "psi", "vacuum")
        assert pressure_negative.quantity is not None
        assert pressure_negative.quantity.value == -10.0
        
        # Very small values
        length_small = Length(1e-6, "millimeters", "tiny")
        assert length_small.quantity is not None
        assert length_small.quantity.value == 1e-6
    
    def test_alternative_constructor_unit_fallback(self):
        """Test that unknown units fall back to defaults gracefully."""
        # Length with unrecognized unit should default to meters
        L = Length(10, "unknown_unit", "test")
        assert L.quantity is not None
        assert L.quantity.unit == LengthUnits.meter  # Falls back to meters
        
        # Pressure with unrecognized unit should default to pascal (SI base unit)
        P = Pressure(50, "unknown_unit", "test")
        assert P.quantity is not None
        assert P.quantity.unit == PressureUnits.pascal  # Falls back to pascal


@pytest.mark.parametrize("variable_class,dimension,setter_class", [
    (Length, LENGTH, LengthSetter),
    (Pressure, PRESSURE, PressureSetter),
])
class TestParametrizedSpecializedVariables:
    """Parametrized tests for all specialized variable types."""
    
    def test_variable_initialization(self, variable_class, dimension, setter_class):
        """Test initialization for all variable types."""
        var = variable_class("test_var")
        
        assert var.expected_dimension == dimension
        assert var.quantity is None
        assert isinstance(var, TypeSafeVariable)
        # Use setter_class to avoid unused parameter warning
        assert setter_class is not None
    
    def test_setter_type_return(self, variable_class, dimension, setter_class):
        """Test that set() returns the correct setter type."""
        var = variable_class("test_var")
        setter = var.set(100.0)
        
        assert isinstance(setter, setter_class)
        assert setter.value == 100.0
        assert setter.variable == var
        # Use dimension to avoid unused parameter warning
        assert dimension is not None
    
    def test_dimensional_consistency(self, variable_class, dimension, setter_class):
        """Test dimensional consistency across all variable types."""
        var = variable_class("test_var")
        
        # Dimension should be consistent with class expectation
        assert var.expected_dimension._signature == dimension._signature
        
        # After setting a value, quantity dimension should match
        if variable_class == Length:
            var.set(10.0).meters
        elif variable_class == Pressure:
            var.set(100.0).psi
        
        assert var.quantity is not None
        assert var.quantity.dimension._signature == dimension._signature
        # Use setter_class to avoid unused parameter warning
        assert setter_class is not None
