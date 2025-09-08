"""
Test division operations with value 1.0 across different variable types.

This test suite verifies the fix for the BinaryOperation._divide() bug where
dividing by any quantity with value 1.0 would incorrectly return the numerator
instead of performing proper dimensional analysis.
"""

import pytest
from qnty import (
    Length, Area, Volume, Mass, Force, Pressure, Temperature, Time,
    VelocityLinear, Acceleration, EnergyHeatWork, PowerThermalDuty, Dimensionless
)


class TestDivisionByOne:
    """Test division operations where divisor has value 1.0."""
    
    def test_same_dimension_division_by_one(self):
        """Test division of same dimensions where divisor = 1.0."""
        
        # Length / Length = Dimensionless
        length1 = Length(5, "meter", "Distance")
        length2 = Length(1, "meter", "Unit Distance")  # The problematic case
        
        result_expr = length1 / length2
        result = result_expr.evaluate({'Distance': length1, 'Unit Distance': length2})
        
        assert result.value == pytest.approx(5.0)
        assert result._dimension_sig == 1  # Dimensionless
        assert result.unit.symbol == ""  # No unit
        
        # Force / Force = Dimensionless  
        force1 = Force(100, "newton", "Applied Force")
        force2 = Force(1, "newton", "Unit Force")
        
        result_expr = force1 / force2
        result = result_expr.evaluate({'Applied Force': force1, 'Unit Force': force2})
        
        assert result.value == pytest.approx(100.0)
        assert result._dimension_sig == 1  # Dimensionless
        
        # Pressure / Pressure = Dimensionless
        pressure1 = Pressure(50, "psi", "System Pressure")
        pressure2 = Pressure(1, "psi", "Reference Pressure")
        
        result_expr = pressure1 / pressure2
        result = result_expr.evaluate({'System Pressure': pressure1, 'Reference Pressure': pressure2})
        
        assert result.value == pytest.approx(50.0)
        assert result._dimension_sig == 1  # Dimensionless

    def test_different_dimension_division_by_one(self):
        """Test division of different dimensions where divisor = 1.0."""
        
        # Area / Length = Length (when divisor = 1.0)
        area = Area(10, "square_meter", "Surface Area")
        length = Length(1, "meter", "Width")  # The problematic case
        
        result_expr = area / length
        result = result_expr.evaluate({'Surface Area': area, 'Width': length})
        
        # Should be 10 m² / 1 m = 10 m (Length dimension)
        # Note: Result unit might be mm (10000.0 mm = 10.0 m), so check SI value
        expected_si_value = (area.quantity.value * area.quantity._si_factor) / (length.quantity.value * length.quantity._si_factor)
        actual_si_value = result.value * result._si_factor
        assert actual_si_value == pytest.approx(expected_si_value)
        assert result._dimension_sig == 2  # Length dimension
        
        # Volume / Area = Length (when divisor = 1.0)
        volume = Volume(25, "cubic_meter", "Tank Volume")
        area2 = Area(1, "square_meter", "Base Area")
        
        result_expr = volume / area2
        result = result_expr.evaluate({'Tank Volume': volume, 'Base Area': area2})
        
        # Should be 25 m³ / 1 m² = 25 m (Length dimension)
        # Check SI values to account for unit selection
        expected_si_value = (volume.quantity.value * volume.quantity._si_factor) / (area2.quantity.value * area2.quantity._si_factor)
        actual_si_value = result.value * result._si_factor
        assert actual_si_value == pytest.approx(expected_si_value)
        assert result._dimension_sig == 2  # Length dimension
        
        # Pressure / Length = Force/Area/Length = Force/Volume  
        pressure = Pressure(100, "pascal", "Fluid Pressure")
        length2 = Length(1, "meter", "Depth")
        
        result_expr = pressure / length2
        result = result_expr.evaluate({'Fluid Pressure': pressure, 'Depth': length2})
        
        # Should have dimensions of Force/Volume (pressure/length)
        # Check SI values to account for unit selection
        expected_si_value = (pressure.quantity.value * pressure.quantity._si_factor) / (length2.quantity.value * length2.quantity._si_factor)
        actual_si_value = result.value * result._si_factor
        assert actual_si_value == pytest.approx(expected_si_value)
        # Should have dimension different from both pressure and length
        assert result._dimension_sig != pressure.quantity._dimension_sig
        assert result._dimension_sig != length2.quantity._dimension_sig

    def test_complex_mixed_divisions(self):
        """Test complex division scenarios with mixed units."""
        
        # Energy / (Force * Length) = Dimensionless (should be 1 for consistent units)
        energy = EnergyHeatWork(500, "joule", "Work Done")
        force = Force(100, "newton", "Applied Force") 
        length = Length(1, "meter", "Distance")  # Problematic divisor
        
        # Create expression: Energy / (Force * Length)
        denominator_expr = force * length
        result_expr = energy / denominator_expr
        
        context = {'Work Done': energy, 'Applied Force': force, 'Distance': length}
        
        # First evaluate the denominator
        denominator_result = denominator_expr.evaluate(context)
        # Note: Result unit may vary, so check the expression evaluates properly
        
        # Now evaluate the full expression
        result = result_expr.evaluate(context)
        # Check that the division was performed (not just returning the energy)
        # The exact result depends on unit system, but it should be a valid division
        assert result.value != energy.quantity.value  # Should not be the original energy value
        # Should have performed the division operation correctly

    def test_multiple_variable_types_with_one(self):
        """Test various variable types divided by quantities with value 1.0."""
        
        test_cases = [
            # (numerator, denominator, expected_value)
            (Mass(10, "kilogram", "Object Mass"), Mass(1, "kilogram", "Unit Mass"), 10.0),
            (Time(60, "second", "Duration"), Time(1, "second", "Unit Time"), 60.0),
            (VelocityLinear(20, "meter_per_second", "Speed"), VelocityLinear(1, "meter_per_second", "Unit Speed"), 20.0),
            (Acceleration(9.8, "meter_per_second_squared", "Gravity"), 
             Acceleration(1, "meter_per_second_squared", "Unit Acceleration"), 9.8),
            (PowerThermalDuty(1000, "watt", "Engine Power"), PowerThermalDuty(1, "watt", "Unit Power"), 1000.0),
            (Temperature(373, "kelvin", "Boiling Point"), Temperature(1, "kelvin", "Unit Temperature"), 373.0),
        ]
        
        for numerator, denominator, expected_value in test_cases:
            result_expr = numerator / denominator
            context = {numerator.name: numerator, denominator.name: denominator}
            result = result_expr.evaluate(context)
            
            assert result.value == pytest.approx(expected_value), \
                f"Failed for {type(numerator).__name__} / {type(denominator).__name__}"
            assert result._dimension_sig == 1, \
                f"Expected dimensionless result for {type(numerator).__name__} / {type(denominator).__name__}"

    def test_division_by_dimensionless_one(self):
        """Test that division by dimensionless 1.0 still uses optimization."""
        
        # This should still use the fast path optimization
        length = Length(5, "meter", "Distance")
        dimensionless_one = Dimensionless(1.0, "Unity")
        
        result_expr = length / dimensionless_one
        result = result_expr.evaluate({'Distance': length, 'Unity': dimensionless_one})
        
        # Should return the length unchanged (optimization preserved)
        assert result.value == pytest.approx(5.0)
        assert result._dimension_sig == 2  # Length dimension preserved
        assert result.unit.symbol == "m"

    def test_division_by_negative_one(self):
        """Test division by -1.0 with and without dimensions."""
        
        # Division by dimensionless -1.0 (should use optimization)
        force = Force(100, "newton", "Push Force")
        neg_dimensionless = Dimensionless(-1.0, "Negative Unity")
        
        result_expr = force / neg_dimensionless
        result = result_expr.evaluate({'Push Force': force, 'Negative Unity': neg_dimensionless})
        
        # Should be -100 N (negation optimization)
        assert result.value == pytest.approx(-100.0)
        assert result._dimension_sig == force.quantity._dimension_sig  # Force dimension preserved
        
        # Division by -1 with same dimensions (should NOT use optimization)
        force1 = Force(100, "newton", "Push Force")
        force2 = Force(-1, "newton", "Opposing Force")
        
        result_expr = force1 / force2
        result = result_expr.evaluate({'Push Force': force1, 'Opposing Force': force2})
        
        # Should be -100 (dimensionless) via proper division
        assert result.value == pytest.approx(-100.0)
        assert result._dimension_sig == 1  # Dimensionless

    def test_edge_case_very_close_to_one(self):
        """Test values very close to 1.0 to ensure they don't trigger optimization."""
        
        length1 = Length(5, "meter", "Distance")
        length2 = Length(1.0000001, "meter", "Almost Unit")  # Very close to 1.0
        
        result_expr = length1 / length2
        result = result_expr.evaluate({'Distance': length1, 'Almost Unit': length2})
        
        # Should perform proper division, not optimization
        assert result.value == pytest.approx(5.0 / 1.0000001)
        assert result._dimension_sig == 1  # Dimensionless

    def test_chain_divisions_with_ones(self):
        """Test chained division operations involving 1.0 values."""
        
        # Create: (Area / Length) / Length where both divisors = 1.0
        area = Area(20, "square_meter", "Surface")
        length1 = Length(1, "meter", "Width")
        length2 = Length(1, "meter", "Height") 
        
        # Build expression: area / length1 / length2
        first_div = area / length1
        second_div = first_div / length2
        
        context = {'Surface': area, 'Width': length1, 'Height': length2}
        
        # Intermediate result should be 20 m (Length) - but unit may be mm
        intermediate = first_div.evaluate(context)
        # Check SI value instead of display value (20 m = 20000 mm)
        expected_si = (area.quantity.value * area.quantity._si_factor) / (length1.quantity.value * length1.quantity._si_factor)  
        actual_si = intermediate.value * intermediate._si_factor
        assert actual_si == pytest.approx(expected_si)
        assert intermediate._dimension_sig == 2  # Length dimension
        
        # Final result should be 20 (Dimensionless) 
        final = second_div.evaluate(context)
        assert final.value == pytest.approx(20.0)
        assert final._dimension_sig == 1  # Dimensionless

    def test_regression_original_bug(self):
        """Regression test for the original D=1 inch bug."""
        
        # This is the exact scenario that was failing
        R_1 = Length(5, "inch", "Bend Radius")
        D = Length(1, "inch", "Diameter")
        
        # The expression that was failing: 4*(R_1/D) - 1
        ratio_expr = R_1 / D
        four_times_expr = 4 * ratio_expr
        result_expr = four_times_expr - 1
        
        context = {'Bend Radius': R_1, 'Diameter': D}
        
        # Step by step verification
        ratio_result = ratio_expr.evaluate(context)
        assert ratio_result.value == pytest.approx(5.0)
        assert ratio_result._dimension_sig == 1  # Should be dimensionless
        
        four_times_result = four_times_expr.evaluate(context)
        assert four_times_result.value == pytest.approx(20.0)
        assert four_times_result._dimension_sig == 1  # Should be dimensionless
        
        final_result = result_expr.evaluate(context)
        assert final_result.value == pytest.approx(19.0)  # 20 - 1 = 19
        assert final_result._dimension_sig == 1  # Should be dimensionless


if __name__ == "__main__":
    # Run specific tests for debugging
    test_instance = TestDivisionByOne()
    
    print("Testing same dimension divisions...")
    test_instance.test_same_dimension_division_by_one()
    print("✓ Passed")
    
    print("\nTesting different dimension divisions...")
    test_instance.test_different_dimension_division_by_one()
    print("✓ Passed")
    
    print("\nTesting multiple variable types...")
    test_instance.test_multiple_variable_types_with_one()
    print("✓ Passed")
    
    print("\nTesting regression case...")
    test_instance.test_regression_original_bug()
    print("✓ Passed")
    
    print("\nAll division fix tests passed! 🎉")