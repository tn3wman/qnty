"""
Comprehensive pytest tests for the unit.py module.

Tests cover UnitDefinition dataclass, UnitConstant class, HighPerformanceRegistry,
and all performance-critical functionality including pre-computed conversion tables.
"""

import time

import pytest

from src.qnty.dimension import DIMENSIONLESS, LENGTH, MASS, PRESSURE, TIME, DimensionSignature
from src.qnty.unit import HighPerformanceRegistry, UnitConstant, UnitDefinition, registry
from src.qnty.units import LengthUnits, PressureUnits


class TestUnitDefinition:
    """Test UnitDefinition dataclass functionality."""
    
    def test_unit_definition_creation(self):
        """Test basic UnitDefinition creation."""
        unit_def = UnitDefinition("meter", "m", LENGTH, 1.0)
        
        assert unit_def.name == "meter"
        assert unit_def.symbol == "m"
        assert unit_def.dimension == LENGTH
        assert unit_def.si_factor == 1.0
        assert unit_def.si_offset == 0.0
    
    def test_unit_definition_with_offset(self):
        """Test UnitDefinition creation with offset (e.g., temperature)."""
        celsius = UnitDefinition("celsius", "C", DimensionSignature.create(temp=1), 1.0, 273.15)
        
        assert celsius.name == "celsius"
        assert celsius.symbol == "C"
        assert celsius.si_factor == 1.0
        assert celsius.si_offset == 273.15
    
    def test_unit_definition_immutability(self):
        """Test that UnitDefinition is immutable (frozen dataclass)."""
        unit_def = UnitDefinition("meter", "m", LENGTH, 1.0)
        
        with pytest.raises(AttributeError):
            unit_def.name = "foot"  # type: ignore[misc]
        
        with pytest.raises(AttributeError):
            unit_def.si_factor = 2.0  # type: ignore[misc]
    
    def test_unit_definition_equality(self):
        """Test UnitDefinition equality comparison."""
        unit1 = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit2 = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit3 = UnitDefinition("foot", "ft", LENGTH, 0.3048)
        
        assert unit1 == unit2
        assert unit1 != unit3
    
    @pytest.mark.parametrize("name,symbol,dimension,si_factor,si_offset", [
        ("millimeter", "mm", LENGTH, 0.001, 0.0),
        ("pascal", "Pa", PRESSURE, 1.0, 0.0),
        ("kilogram", "kg", MASS, 1.0, 0.0),
        ("second", "s", TIME, 1.0, 0.0),
        ("dimensionless", "", DIMENSIONLESS, 1.0, 0.0),
    ])
    def test_unit_definition_parametrized(self, name, symbol, dimension, si_factor, si_offset):
        """Test UnitDefinition creation with various parameter combinations."""
        unit_def = UnitDefinition(name, symbol, dimension, si_factor, si_offset)
        
        assert unit_def.name == name
        assert unit_def.symbol == symbol
        assert unit_def.dimension == dimension
        assert unit_def.si_factor == si_factor
        assert unit_def.si_offset == si_offset


class TestUnitConstant:
    """Test UnitConstant class functionality."""
    
    def test_unit_constant_creation(self):
        """Test UnitConstant creation from UnitDefinition."""
        unit_def = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit_const = UnitConstant(unit_def)
        
        assert unit_const.name == "meter"
        assert unit_const.symbol == "m"
        assert unit_const.dimension == LENGTH
        assert unit_const.si_factor == 1.0
        assert unit_const.definition == unit_def
    
    def test_unit_constant_string_representation(self):
        """Test UnitConstant string representation returns symbol."""
        unit_def = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit_const = UnitConstant(unit_def)
        
        assert str(unit_const) == "m"
        
        # Test with empty symbol (dimensionless)
        dimensionless_def = UnitDefinition("dimensionless", "", DIMENSIONLESS, 1.0)
        dimensionless_const = UnitConstant(dimensionless_def)
        assert str(dimensionless_const) == ""
    
    def test_unit_constant_equality(self):
        """Test UnitConstant equality is based on name."""
        unit_def1 = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit_def2 = UnitDefinition("meter", "m", LENGTH, 1.0)  # Same name
        unit_def3 = UnitDefinition("foot", "ft", LENGTH, 0.3048)  # Different name
        
        unit1 = UnitConstant(unit_def1)
        unit2 = UnitConstant(unit_def2)
        unit3 = UnitConstant(unit_def3)
        
        assert unit1 == unit2  # Same name
        assert unit1 != unit3  # Different name
        assert unit1 != "meter"  # Different type
    
    def test_unit_constant_hash(self):
        """Test UnitConstant can be used as dictionary keys."""
        unit_def1 = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit_def2 = UnitDefinition("meter", "m", LENGTH, 1.0)
        unit_def3 = UnitDefinition("foot", "ft", LENGTH, 0.3048)
        
        unit1 = UnitConstant(unit_def1)
        unit2 = UnitConstant(unit_def2)
        unit3 = UnitConstant(unit_def3)
        
        # Test hash consistency
        assert hash(unit1) == hash(unit2)  # Same name should have same hash
        assert hash(unit1) != hash(unit3)  # Different names should have different hash
        
        # Test as dictionary keys
        unit_dict = {unit1: "value1", unit3: "value3"}
        assert unit_dict[unit2] == "value1"  # unit2 should match unit1 key
        assert len(unit_dict) == 2
    
    def test_unit_constant_attributes_immutable(self):
        """Test that UnitConstant attributes reference the definition correctly."""
        unit_def = UnitDefinition("pascal", "Pa", PRESSURE, 1.0)
        unit_const = UnitConstant(unit_def)
        
        # Attributes should match definition
        assert unit_const.name is unit_def.name
        assert unit_const.symbol is unit_def.symbol
        assert unit_const.dimension is unit_def.dimension
        assert unit_const.si_factor is unit_def.si_factor


class TestHighPerformanceRegistry:
    """Test HighPerformanceRegistry functionality."""
    
    def test_registry_initialization(self):
        """Test registry initializes with correct units."""
        test_registry = HighPerformanceRegistry()
        
        # Check all expected units are registered
        expected_units = [
            "meter", "millimeter", "centimeter", "inch", "foot",
            "pascal", "kilopascal", "megapascal", "psi", "bar",
            "dimensionless"
        ]
        
        for unit_name in expected_units:
            assert unit_name in test_registry.units
            assert isinstance(test_registry.units[unit_name], UnitDefinition)
    
    def test_registry_unit_definitions(self):
        """Test specific unit definitions in registry."""
        test_registry = HighPerformanceRegistry()
        
        # Test length units
        meter = test_registry.units["meter"]
        assert meter.name == "meter"
        assert meter.symbol == "m"
        assert meter.dimension == LENGTH
        assert meter.si_factor == 1.0
        
        millimeter = test_registry.units["millimeter"]
        assert millimeter.si_factor == 0.001
        
        inch = test_registry.units["inch"]
        assert inch.si_factor == 0.0254
        
        # Test pressure units
        pascal = test_registry.units["pascal"]
        assert pascal.dimension == PRESSURE
        assert pascal.si_factor == 1.0
        
        psi_unit = test_registry.units["psi"]
        assert psi_unit.si_factor == 6894.757
        
        # Test dimensionless
        dimensionless = test_registry.units["dimensionless"]
        assert dimensionless.dimension == DIMENSIONLESS
        assert dimensionless.si_factor == 1.0
    
    def test_registry_dimensional_groups(self):
        """Test that units are correctly grouped by dimension."""
        test_registry = HighPerformanceRegistry()
        
        # Length dimension group
        length_sig = LENGTH._signature
        length_units = test_registry.dimensional_groups[length_sig]
        length_names = [unit.name for unit in length_units]
        
        expected_length_units = ["meter", "millimeter", "centimeter", "inch", "foot"]
        for unit_name in expected_length_units:
            assert unit_name in length_names
        
        # Pressure dimension group
        pressure_sig = PRESSURE._signature
        pressure_units = test_registry.dimensional_groups[pressure_sig]
        pressure_names = [unit.name for unit in pressure_units]
        
        expected_pressure_units = ["pascal", "kilopascal", "megapascal", "psi", "bar"]
        for unit_name in expected_pressure_units:
            assert unit_name in pressure_names
        
        # Dimensionless group
        dimensionless_sig = DIMENSIONLESS._signature
        dimensionless_units = test_registry.dimensional_groups[dimensionless_sig]
        assert len(dimensionless_units) == 1
        assert dimensionless_units[0].name == "dimensionless"
    
    def test_registry_precomputed_conversions(self):
        """Test that conversion table is pre-computed correctly."""
        test_registry = HighPerformanceRegistry()
        
        # Test length conversions
        meter_to_mm = test_registry.conversion_table[("meter", "millimeter")]
        assert meter_to_mm == pytest.approx(1000.0)
        
        mm_to_meter = test_registry.conversion_table[("millimeter", "meter")]
        assert mm_to_meter == pytest.approx(0.001)
        
        inch_to_meter = test_registry.conversion_table[("inch", "meter")]
        assert inch_to_meter == pytest.approx(0.0254)
        
        meter_to_inch = test_registry.conversion_table[("meter", "inch")]
        assert meter_to_inch == pytest.approx(1.0 / 0.0254)
        
        # Test pressure conversions
        psi_to_pascal = test_registry.conversion_table[("psi", "pascal")]
        assert psi_to_pascal == pytest.approx(6894.757)
        
        pascal_to_psi = test_registry.conversion_table[("pascal", "psi")]
        assert pascal_to_psi == pytest.approx(1.0 / 6894.757)
    
    def test_registry_conversion_table_completeness(self):
        """Test that conversion table includes all valid conversions."""
        test_registry = HighPerformanceRegistry()
        
        # Count expected conversions for each dimensional group
        total_expected = 0
        for group in test_registry.dimensional_groups.values():
            n_units = len(group)
            # n*(n-1) conversions for n units (excluding self-conversions)
            total_expected += n_units * (n_units - 1)
        
        assert len(test_registry.conversion_table) == total_expected
    
    def test_registry_convert_same_unit(self):
        """Test conversion between same units returns original value."""
        test_registry = HighPerformanceRegistry()
        
        meter_unit = UnitConstant(test_registry.units["meter"])
        
        result = test_registry.convert(5.0, meter_unit, meter_unit)
        assert result == 5.0
    
    def test_registry_convert_different_units(self):
        """Test conversion between different units."""
        test_registry = HighPerformanceRegistry()
        
        meter_unit = UnitConstant(test_registry.units["meter"])
        mm_unit = UnitConstant(test_registry.units["millimeter"])
        
        # 1 meter = 1000 mm
        result = test_registry.convert(1.0, meter_unit, mm_unit)
        assert result == pytest.approx(1000.0)
        
        # 1000 mm = 1 meter
        result = test_registry.convert(1000.0, mm_unit, meter_unit)
        assert result == pytest.approx(1.0)
        
        # Test pressure conversion
        psi_unit = UnitConstant(test_registry.units["psi"])
        pascal_unit = UnitConstant(test_registry.units["pascal"])
        
        result = test_registry.convert(1.0, psi_unit, pascal_unit)
        assert result == pytest.approx(6894.757)
    
    def test_registry_convert_fallback(self):
        """Test conversion fallback for units not in conversion table."""
        test_registry = HighPerformanceRegistry()
        
        # Create custom units not in the registry
        custom_unit1 = UnitConstant(UnitDefinition("custom1", "c1", LENGTH, 2.0))
        custom_unit2 = UnitConstant(UnitDefinition("custom2", "c2", LENGTH, 4.0))
        
        # Should use fallback calculation
        result = test_registry.convert(1.0, custom_unit1, custom_unit2)
        expected = 2.0 / 4.0  # si_factor1 / si_factor2
        assert result == pytest.approx(expected)
    
    @pytest.mark.parametrize("value,from_unit,to_unit,expected", [
        (1.0, "meter", "millimeter", 1000.0),
        (1000.0, "millimeter", "meter", 1.0),
        (12.0, "inch", "foot", 1.0),
        (1.0, "foot", "inch", 12.0),
        (1.0, "bar", "pascal", 100000.0),
        (100000.0, "pascal", "bar", 1.0),
        (1.0, "megapascal", "kilopascal", 1000.0),
    ])
    def test_registry_convert_parametrized(self, value, from_unit, to_unit, expected):
        """Test various unit conversions with parametrized inputs."""
        test_registry = HighPerformanceRegistry()
        
        from_unit_const = UnitConstant(test_registry.units[from_unit])
        to_unit_const = UnitConstant(test_registry.units[to_unit])
        
        result = test_registry.convert(value, from_unit_const, to_unit_const)
        assert result == pytest.approx(expected, rel=1e-6)


class TestGlobalRegistry:
    """Test the global registry instance."""
    
    def test_global_registry_exists(self):
        """Test that global registry is properly instantiated."""
        assert registry is not None
        assert isinstance(registry, HighPerformanceRegistry)
    
    def test_global_registry_units(self):
        """Test that global registry has all expected units."""
        expected_units = [
            "meter", "millimeter", "centimeter", "inch", "foot",
            "pascal", "kilopascal", "megapascal", "psi", "bar",
            "dimensionless"
        ]
        
        for unit_name in expected_units:
            assert unit_name in registry.units
    
    def test_global_registry_conversion_table(self):
        """Test that global registry has pre-computed conversion table."""
        assert len(registry.conversion_table) > 0
        
        # Test a few key conversions
        assert ("meter", "millimeter") in registry.conversion_table
        assert ("psi", "pascal") in registry.conversion_table


class TestIntegrationWithUnits:
    """Test integration with units.py constants."""
    
    def test_length_units_integration(self):
        """Test that LengthUnits work with registry conversions."""
        meter = LengthUnits.meter
        millimeter = LengthUnits.millimeter
        
        assert meter.name == "meter"
        assert millimeter.name == "millimeter"
        
        # Test conversion using global registry
        result = registry.convert(1.0, meter, millimeter)
        assert result == pytest.approx(1000.0)
    
    def test_pressure_units_integration(self):
        """Test that PressureUnits work with registry conversions."""
        psi_unit = PressureUnits.psi
        pascal_unit = PressureUnits.pascal
        
        assert psi_unit.name == "psi"
        assert pascal_unit.name == "pascal"
        
        # Test conversion using global registry
        result = registry.convert(1.0, psi_unit, pascal_unit)
        assert result == pytest.approx(6894.757)
    
    def test_unit_aliases(self):
        """Test that unit aliases work correctly."""
        # Test length aliases
        assert LengthUnits.m == LengthUnits.meter
        assert LengthUnits.mm == LengthUnits.millimeter
        assert LengthUnits.cm == LengthUnits.centimeter
        assert LengthUnits.ft == LengthUnits.foot
        assert LengthUnits.in_ == LengthUnits.inch
        
        # Test pressure aliases
        assert PressureUnits.Pa == PressureUnits.pascal
        assert PressureUnits.kPa == PressureUnits.kilopascal
        assert PressureUnits.MPa == PressureUnits.megapascal


class TestPerformanceOptimizations:
    """Test performance-critical aspects of the unit system."""
    
    def test_conversion_table_lookup_speed(self):
        """Test that conversion table lookups are O(1) fast."""
        meter = UnitConstant(registry.units["meter"])
        millimeter = UnitConstant(registry.units["millimeter"])
        
        # Time multiple conversions
        start_time = time.perf_counter()
        
        for _ in range(10000):
            registry.convert(1.0, meter, millimeter)
        
        elapsed = time.perf_counter() - start_time
        
        # Should complete 10k conversions very quickly (under 0.1 seconds on modern hardware)
        assert elapsed < 0.1, f"Conversions took too long: {elapsed:.3f}s"
    
    def test_same_unit_fast_path(self):
        """Test that same-unit conversions use fast path."""
        meter = UnitConstant(registry.units["meter"])
        
        # Time same-unit conversions (should be nearly instant)
        start_time = time.perf_counter()
        
        for _ in range(100000):
            result = registry.convert(5.0, meter, meter)
            assert result == 5.0
        
        elapsed = time.perf_counter() - start_time
        
        # Same-unit conversions should be extremely fast
        assert elapsed < 0.05, f"Same-unit conversions took too long: {elapsed:.3f}s"
    
    def test_unit_constant_equality_performance(self):
        """Test that UnitConstant equality checks are fast."""
        meter1 = UnitConstant(registry.units["meter"])
        meter2 = UnitConstant(registry.units["meter"])
        millimeter = UnitConstant(registry.units["millimeter"])
        
        # Time equality checks
        start_time = time.perf_counter()
        
        for _ in range(100000):
            assert meter1 == meter2
            assert meter1 != millimeter
        
        elapsed = time.perf_counter() - start_time
        
        # Equality checks should be very fast (string comparison)
        assert elapsed < 0.1, f"Equality checks took too long: {elapsed:.3f}s"
    
    def test_dimensional_signature_compatibility(self):
        """Test that dimensional compatibility checks are fast."""
        meter = UnitConstant(registry.units["meter"])
        millimeter = UnitConstant(registry.units["millimeter"])
        pascal_unit = UnitConstant(registry.units["pascal"])
        
        # Test compatible dimensions
        assert meter.dimension.is_compatible(millimeter.dimension)
        
        # Test incompatible dimensions
        assert not meter.dimension.is_compatible(pascal_unit.dimension)
        
        # Time many compatibility checks
        start_time = time.perf_counter()
        
        for _ in range(100000):
            meter.dimension.is_compatible(millimeter.dimension)
            meter.dimension.is_compatible(pascal_unit.dimension)
        
        elapsed = time.perf_counter() - start_time
        
        # Dimensional checks should be very fast (integer comparison)
        assert elapsed < 0.1, f"Dimensional checks took too long: {elapsed:.3f}s"


class TestErrorHandlingAndEdgeCases:
    """Test error handling and edge cases."""
    
    def test_unit_definition_with_zero_si_factor(self):
        """Test UnitDefinition with zero SI factor."""
        # This should be allowed but would cause division by zero in conversions
        unit_def = UnitDefinition("zero_unit", "0", LENGTH, 0.0)
        assert unit_def.si_factor == 0.0
    
    def test_unit_definition_with_negative_si_factor(self):
        """Test UnitDefinition with negative SI factor."""
        # This should be allowed for some theoretical units
        unit_def = UnitDefinition("negative_unit", "-u", LENGTH, -1.0)
        assert unit_def.si_factor == -1.0
    
    def test_conversion_with_incompatible_dimensions(self):
        """Test that conversions don't validate dimensional compatibility."""
        # Note: The current implementation doesn't check dimensional compatibility
        # This is likely by design for performance, but we should document the behavior
        
        meter = UnitConstant(registry.units["meter"])
        pascal_unit = UnitConstant(registry.units["pascal"])
        
        # This should work (fallback calculation) but is dimensionally incorrect
        result = registry.convert(1.0, meter, pascal_unit)
        expected = 1.0 / 1.0  # Both have si_factor 1.0
        assert result == expected
    
    def test_unit_constant_with_complex_dimension(self):
        """Test UnitConstant with complex derived dimensions."""
        # Create a complex dimension (force = mass * length / time^2)
        force_dim = DimensionSignature.create(mass=1, length=1, time=-2)
        newton_def = UnitDefinition("newton", "N", force_dim, 1.0)
        newton = UnitConstant(newton_def)
        
        assert newton.name == "newton"
        assert newton.symbol == "N"
        assert newton.dimension == force_dim
    
    def test_empty_registry(self):
        """Test behavior with empty registry."""
        empty_registry = HighPerformanceRegistry.__new__(HighPerformanceRegistry)
        empty_registry.units = {}
        empty_registry.conversion_table = {}
        empty_registry.dimensional_groups = {}
        empty_registry._dimension_cache = {}
        
        assert len(empty_registry.units) == 0
        assert len(empty_registry.conversion_table) == 0
        assert len(empty_registry.dimensional_groups) == 0
    
    def test_registry_cache_attributes(self):
        """Test that registry has proper cache attributes."""
        test_registry = HighPerformanceRegistry()
        
        assert hasattr(test_registry, '_dimension_cache')
        assert isinstance(test_registry._dimension_cache, dict)
        
        # Cache should initially be empty
        assert len(test_registry._dimension_cache) == 0


class TestRegistryMemoryEfficiency:
    """Test memory efficiency aspects of the registry."""
    
    def test_conversion_table_storage_efficiency(self):
        """Test that conversion table uses efficient storage."""
        test_registry = HighPerformanceRegistry()
        
        # Conversion table should use tuples as keys for memory efficiency
        for key in test_registry.conversion_table.keys():
            assert isinstance(key, tuple)
            assert len(key) == 2
            assert isinstance(key[0], str)
            assert isinstance(key[1], str)
    
    def test_dimensional_groups_organization(self):
        """Test that dimensional groups are organized efficiently."""
        test_registry = HighPerformanceRegistry()
        
        # Each dimension should map to a list of unit definitions
        for dim_sig, unit_list in test_registry.dimensional_groups.items():
            assert isinstance(dim_sig, int | float)  # Dimension signature (can be float for negative exponents)
            assert isinstance(unit_list, list)
            
            # All units in the group should have the same dimension
            if unit_list:
                expected_dim_sig = unit_list[0].dimension._signature
                for unit in unit_list:
                    assert unit.dimension._signature == expected_dim_sig
    
    def test_unit_definition_references(self):
        """Test that UnitDefinition objects are properly referenced."""
        test_registry = HighPerformanceRegistry()
        
        # Units dict should contain UnitDefinition objects
        for unit_name, unit_def in test_registry.units.items():
            assert isinstance(unit_name, str)
            assert isinstance(unit_def, UnitDefinition)
            assert unit_def.name == unit_name


if __name__ == "__main__":
    pytest.main([__file__])
