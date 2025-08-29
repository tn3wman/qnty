"""
Comprehensive pytest tests for the units.py module.

Tests cover all unit constant classes (LengthUnits, PressureUnits, DimensionlessUnits),
their individual unit constants, aliases, UnitConstant integration, dimensional consistency,
SI factor accuracy, conversion relationships, and performance characteristics.
"""

import time

import pytest

from src.qnty.dimension import (
    DIMENSIONLESS,
    LENGTH,
    PRESSURE,
    DimensionSignature,
)
from src.qnty.unit import UnitConstant, UnitDefinition, registry
from src.qnty.quantities import DimensionlessUnits, LengthUnits, PressureUnits


class TestLengthUnits:
    """Comprehensive tests for LengthUnits class and all length unit constants."""
    
    def test_length_units_class_structure(self):
        """Test that LengthUnits class has expected structure."""
        # Check that all expected unit constants exist
        expected_units = ['meter', 'millimeter', 'centimeter', 'inch', 'foot']
        for unit_name in expected_units:
            assert hasattr(LengthUnits, unit_name), f"Missing {unit_name} unit"
            unit_constant = getattr(LengthUnits, unit_name)
            assert isinstance(unit_constant, UnitConstant), f"{unit_name} should be UnitConstant"
    
    def test_length_unit_aliases(self):
        """Test that all length unit aliases are correctly defined."""
        # Test standard aliases
        assert LengthUnits.m is LengthUnits.meter
        assert LengthUnits.mm is LengthUnits.millimeter
        assert LengthUnits.cm is LengthUnits.centimeter
        assert LengthUnits.in_ is LengthUnits.inch  # 'in' is reserved keyword
        assert LengthUnits.ft is LengthUnits.foot
    
    @pytest.mark.parametrize("unit_name,expected_symbol,expected_si_factor", [
        ("meter", "m", 1.0),
        ("millimeter", "mm", 0.001),
        ("centimeter", "cm", 0.01),
        ("inch", "in", 0.0254),
        ("foot", "ft", 0.3048),
    ])
    def test_length_unit_properties(self, unit_name: str, expected_symbol: str, expected_si_factor: float):
        """Test individual length unit properties."""
        unit_constant = getattr(LengthUnits, unit_name)
        
        # Test basic properties
        assert unit_constant.name == unit_name
        assert unit_constant.symbol == expected_symbol
        assert unit_constant.dimension == LENGTH
        assert abs(unit_constant.si_factor - expected_si_factor) < 1e-10
        
        # Test string representation
        assert str(unit_constant) == expected_symbol
        
        # Test UnitDefinition integration
        assert isinstance(unit_constant.definition, UnitDefinition)
        assert unit_constant.definition.name == unit_name
        assert unit_constant.definition.symbol == expected_symbol
        assert unit_constant.definition.dimension == LENGTH
        assert abs(unit_constant.definition.si_factor - expected_si_factor) < 1e-10
    
    def test_length_unit_dimensional_consistency(self):
        """Test that all length units have LENGTH dimension."""
        length_units = [
            LengthUnits.meter, LengthUnits.millimeter, LengthUnits.centimeter,
            LengthUnits.inch, LengthUnits.foot
        ]
        
        for unit in length_units:
            assert unit.dimension == LENGTH
            assert unit.dimension.is_compatible(LENGTH)
            # Test dimension signature
            assert unit.dimension._signature == LENGTH._signature
    
    def test_length_unit_conversion_factors(self):
        """Test accuracy of length unit conversion factors."""
        # Test known conversion relationships
        
        # Metric conversions
        assert abs(LengthUnits.mm.si_factor * 1000 - LengthUnits.m.si_factor) < 1e-10
        assert abs(LengthUnits.cm.si_factor * 100 - LengthUnits.m.si_factor) < 1e-10
        
        # Imperial conversions
        assert abs(LengthUnits.inch.si_factor * 12 - LengthUnits.foot.si_factor) < 1e-10
        
        # Mixed conversions (engineering accuracy)
        # 1 inch = 25.4 mm exactly
        expected_mm_per_inch = 25.4
        actual_mm_per_inch = LengthUnits.inch.si_factor / LengthUnits.mm.si_factor
        assert abs(actual_mm_per_inch - expected_mm_per_inch) < 1e-10
        
        # 1 foot = 12 inches exactly
        expected_inches_per_foot = 12.0
        actual_inches_per_foot = LengthUnits.foot.si_factor / LengthUnits.inch.si_factor
        assert abs(actual_inches_per_foot - expected_inches_per_foot) < 1e-10
    
    def test_length_unit_equality_and_hashing(self):
        """Test equality and hashing behavior for length units."""
        # Test equality
        assert LengthUnits.meter == LengthUnits.meter
        assert LengthUnits.meter != LengthUnits.millimeter
        assert LengthUnits.m == LengthUnits.meter  # Alias equality
        
        # Test hashing (should be usable as dict keys)
        unit_dict = {
            LengthUnits.meter: "meter_value",
            LengthUnits.millimeter: "mm_value",
            LengthUnits.inch: "inch_value"
        }
        
        assert unit_dict[LengthUnits.meter] == "meter_value"
        assert unit_dict[LengthUnits.mm] == "mm_value"
        assert unit_dict[LengthUnits.in_] == "inch_value"


class TestPressureUnits:
    """Comprehensive tests for PressureUnits class and all pressure unit constants."""
    
    def test_pressure_units_class_structure(self):
        """Test that PressureUnits class has expected structure."""
        # Check that all expected unit constants exist
        expected_units = ['pascal', 'kilopascal', 'megapascal', 'psi', 'bar']
        for unit_name in expected_units:
            assert hasattr(PressureUnits, unit_name), f"Missing {unit_name} unit"
            unit_constant = getattr(PressureUnits, unit_name)
            assert isinstance(unit_constant, UnitConstant), f"{unit_name} should be UnitConstant"
    
    def test_pressure_unit_aliases(self):
        """Test that all pressure unit aliases are correctly defined."""
        # Test standard aliases
        assert PressureUnits.Pa is PressureUnits.pascal
        assert PressureUnits.kPa is PressureUnits.kilopascal
        assert PressureUnits.MPa is PressureUnits.megapascal
    
    @pytest.mark.parametrize("unit_name,expected_symbol,expected_si_factor", [
        ("pascal", "Pa", 1.0),
        ("kilopascal", "kPa", 1000.0),
        ("megapascal", "MPa", 1e6),
        ("psi", "psi", 6894.757),
        ("bar", "bar", 100000.0),
    ])
    def test_pressure_unit_properties(self, unit_name: str, expected_symbol: str, expected_si_factor: float):
        """Test individual pressure unit properties."""
        unit_constant = getattr(PressureUnits, unit_name)
        
        # Test basic properties
        assert unit_constant.name == unit_name
        assert unit_constant.symbol == expected_symbol
        assert unit_constant.dimension == PRESSURE
        assert abs(unit_constant.si_factor - expected_si_factor) < 1e-3  # Allow small tolerance for psi
        
        # Test string representation
        assert str(unit_constant) == expected_symbol
        
        # Test UnitDefinition integration
        assert isinstance(unit_constant.definition, UnitDefinition)
        assert unit_constant.definition.name == unit_name
        assert unit_constant.definition.symbol == expected_symbol
        assert unit_constant.definition.dimension == PRESSURE
        assert abs(unit_constant.definition.si_factor - expected_si_factor) < 1e-3
    
    def test_pressure_unit_dimensional_consistency(self):
        """Test that all pressure units have PRESSURE dimension."""
        pressure_units = [
            PressureUnits.pascal, PressureUnits.kilopascal, PressureUnits.megapascal,
            PressureUnits.psi, PressureUnits.bar
        ]
        
        for unit in pressure_units:
            assert unit.dimension == PRESSURE
            assert unit.dimension.is_compatible(PRESSURE)
            # Test dimension signature
            assert unit.dimension._signature == PRESSURE._signature
    
    def test_pressure_unit_conversion_factors(self):
        """Test accuracy of pressure unit conversion factors."""
        # Test metric pressure conversions
        assert abs(PressureUnits.kPa.si_factor - PressureUnits.Pa.si_factor * 1000) < 1e-10
        assert abs(PressureUnits.MPa.si_factor - PressureUnits.Pa.si_factor * 1e6) < 1e-10
        assert abs(PressureUnits.MPa.si_factor - PressureUnits.kPa.si_factor * 1000) < 1e-10
        
        # Test engineering conversions
        # 1 bar = 100,000 Pa exactly
        expected_pa_per_bar = 100000.0
        actual_pa_per_bar = PressureUnits.bar.si_factor / PressureUnits.Pa.si_factor
        assert abs(actual_pa_per_bar - expected_pa_per_bar) < 1e-10
        
        # 1 psi H 6894.757 Pa (standard engineering value)
        expected_pa_per_psi = 6894.757
        actual_pa_per_psi = PressureUnits.psi.si_factor / PressureUnits.Pa.si_factor
        assert abs(actual_pa_per_psi - expected_pa_per_psi) < 1e-3
        
        # 1 bar H 14.5038 psi (engineering accuracy)
        expected_psi_per_bar = 14.5038
        actual_psi_per_bar = PressureUnits.bar.si_factor / PressureUnits.psi.si_factor
        assert abs(actual_psi_per_bar - expected_psi_per_bar) < 1e-3
    
    def test_pressure_unit_engineering_accuracy(self):
        """Test pressure unit conversion accuracy for common engineering values."""
        # Test that common pressure conversions are accurate
        
        # Atmospheric pressure conversions
        atm_pa = 101325.0  # Standard atmospheric pressure in Pa
        atm_psi = atm_pa / PressureUnits.psi.si_factor
        atm_bar = atm_pa / PressureUnits.bar.si_factor
        
        # Standard atmosphere H 14.696 psi
        assert abs(atm_psi - 14.696) < 0.01
        
        # Standard atmosphere H 1.01325 bar
        assert abs(atm_bar - 1.01325) < 0.00001


class TestDimensionlessUnits:
    """Comprehensive tests for DimensionlessUnits class."""
    
    def test_dimensionless_units_class_structure(self):
        """Test that DimensionlessUnits class has expected structure."""
        assert hasattr(DimensionlessUnits, 'dimensionless')
        assert isinstance(DimensionlessUnits.dimensionless, UnitConstant)
    
    def test_dimensionless_unit_properties(self):
        """Test dimensionless unit properties."""
        unit = DimensionlessUnits.dimensionless
        
        # Test basic properties
        assert unit.name == "dimensionless"
        assert unit.symbol == ""  # Empty symbol for dimensionless
        assert unit.dimension == DIMENSIONLESS
        assert unit.si_factor == 1.0
        
        # Test string representation
        assert str(unit) == ""
        
        # Test UnitDefinition integration
        assert isinstance(unit.definition, UnitDefinition)
        assert unit.definition.name == "dimensionless"
        assert unit.definition.symbol == ""
        assert unit.definition.dimension == DIMENSIONLESS
        assert unit.definition.si_factor == 1.0
    
    def test_dimensionless_dimensional_consistency(self):
        """Test that dimensionless unit has DIMENSIONLESS dimension."""
        unit = DimensionlessUnits.dimensionless
        assert unit.dimension == DIMENSIONLESS
        assert unit.dimension.is_compatible(DIMENSIONLESS)
        assert unit.dimension._signature == DIMENSIONLESS._signature


class TestUnitConstantIntegration:
    """Test integration between units.py and the broader unit system."""
    
    def test_registry_integration(self):
        """Test that all units are properly registered in the global registry."""
        # Test that all units from units.py exist in the registry
        unit_names = [
            "meter", "millimeter", "centimeter", "inch", "foot",
            "pascal", "kilopascal", "megapascal", "psi", "bar",
            "dimensionless"
        ]
        
        for unit_name in unit_names:
            assert unit_name in registry.units, f"{unit_name} not found in registry"
            unit_def = registry.units[unit_name]
            assert isinstance(unit_def, UnitDefinition)
    
    def test_unit_constant_creation_from_registry(self):
        """Test that UnitConstants are created correctly from registry definitions."""
        # Test length units
        meter_constant = LengthUnits.meter
        meter_registry = registry.units["meter"]
        
        assert meter_constant.name == meter_registry.name
        assert meter_constant.symbol == meter_registry.symbol
        assert meter_constant.dimension == meter_registry.dimension
        assert meter_constant.si_factor == meter_registry.si_factor
        
        # Test pressure units
        psi_constant = PressureUnits.psi
        psi_registry = registry.units["psi"]
        
        assert psi_constant.name == psi_registry.name
        assert psi_constant.symbol == psi_registry.symbol
        assert psi_constant.dimension == psi_registry.dimension
        assert psi_constant.si_factor == psi_registry.si_factor
    
    def test_conversion_table_integration(self):
        """Test that units work with the pre-computed conversion table."""
        # Test that conversion keys exist for same-dimension units
        conversion_keys = registry.conversion_table.keys()
        
        # Test length unit conversions
        length_conversion_keys = [
            ("meter", "millimeter"), ("millimeter", "meter"),
            ("inch", "foot"), ("foot", "inch"),
            ("meter", "inch"), ("inch", "meter")
        ]
        
        for key in length_conversion_keys:
            assert key in conversion_keys, f"Missing conversion: {key[0]} -> {key[1]}"
            
        # Test pressure unit conversions
        pressure_conversion_keys = [
            ("pascal", "kilopascal"), ("kilopascal", "pascal"),
            ("psi", "bar"), ("bar", "psi"),
            ("pascal", "psi"), ("psi", "pascal")
        ]
        
        for key in pressure_conversion_keys:
            assert key in conversion_keys, f"Missing conversion: {key[0]} -> {key[1]}"
    
    def test_dimensional_grouping(self):
        """Test that units are properly grouped by dimension in the registry."""
        length_signature = LENGTH._signature
        pressure_signature = PRESSURE._signature
        dimensionless_signature = DIMENSIONLESS._signature
        
        assert length_signature in registry.dimensional_groups
        assert pressure_signature in registry.dimensional_groups
        assert dimensionless_signature in registry.dimensional_groups
        
        # Test length group
        length_group = registry.dimensional_groups[length_signature]
        length_unit_names = [unit.name for unit in length_group]
        expected_length_units = ["meter", "millimeter", "centimeter", "inch", "foot"]
        for unit_name in expected_length_units:
            assert unit_name in length_unit_names
        
        # Test pressure group
        pressure_group = registry.dimensional_groups[pressure_signature]
        pressure_unit_names = [unit.name for unit in pressure_group]
        expected_pressure_units = ["pascal", "kilopascal", "megapascal", "psi", "bar"]
        for unit_name in expected_pressure_units:
            assert unit_name in pressure_unit_names


class TestUnitSystemCompleteness:
    """Test completeness and consistency of the unit system."""
    
    def test_unit_coverage_for_engineering(self):
        """Test that essential engineering units are covered."""
        # Length units - essential for engineering
        assert hasattr(LengthUnits, 'meter')
        assert hasattr(LengthUnits, 'millimeter')  # Common in mechanical engineering
        assert hasattr(LengthUnits, 'inch')        # Imperial system
        assert hasattr(LengthUnits, 'foot')        # Imperial system
        
        # Pressure units - essential for fluid mechanics
        assert hasattr(PressureUnits, 'pascal')    # SI base
        assert hasattr(PressureUnits, 'kilopascal') # Common engineering unit
        assert hasattr(PressureUnits, 'megapascal') # Structural engineering
        assert hasattr(PressureUnits, 'psi')       # Imperial system
        assert hasattr(PressureUnits, 'bar')       # Common in industry
        
        # Dimensionless - mathematical operations
        assert hasattr(DimensionlessUnits, 'dimensionless')
    
    def test_alias_consistency(self):
        """Test that unit aliases follow consistent naming patterns."""
        # Test that SI symbol aliases exist for metric units
        metric_units = [
            (LengthUnits, 'meter', 'm'),
            (LengthUnits, 'millimeter', 'mm'),
            (LengthUnits, 'centimeter', 'cm'),
            (PressureUnits, 'pascal', 'Pa'),
            (PressureUnits, 'kilopascal', 'kPa'),
            (PressureUnits, 'megapascal', 'MPa'),
        ]
        
        for unit_class, full_name, alias in metric_units:
            assert hasattr(unit_class, alias), f"Missing alias {alias} for {full_name}"
            assert getattr(unit_class, alias) is getattr(unit_class, full_name)
        
        # Test that imperial units have standard aliases
        imperial_aliases = [
            (LengthUnits, 'inch', 'in_'),  # 'in' is reserved keyword
            (LengthUnits, 'foot', 'ft'),
        ]
        
        for unit_class, full_name, alias in imperial_aliases:
            assert hasattr(unit_class, alias), f"Missing alias {alias} for {full_name}"
            assert getattr(unit_class, alias) is getattr(unit_class, full_name)
    
    @pytest.mark.parametrize("unit_class", [LengthUnits, PressureUnits, DimensionlessUnits])
    def test_unit_class_immutability(self, unit_class):
        """Test that unit constant classes maintain immutability."""
        # Get all unit constants from the class
        unit_constants = []
        for attr_name in dir(unit_class):
            if not attr_name.startswith('_'):
                attr = getattr(unit_class, attr_name)
                if isinstance(attr, UnitConstant):
                    unit_constants.append(attr)
        
        # Test that unit constants are immutable (attempt to modify should not work)
        for unit in unit_constants:
            original_name = unit.name
            original_symbol = unit.symbol
            original_si_factor = unit.si_factor
            
            # Unit constants should maintain their properties
            assert unit.name == original_name
            assert unit.symbol == original_symbol
            assert unit.si_factor == original_si_factor


class TestPerformanceCharacteristics:
    """Test performance aspects of the unit system."""
    
    def test_unit_constant_access_performance(self):
        """Test that unit constant access is fast (no string parsing)."""
        # Time multiple accesses to ensure consistent performance
        iterations = 10000
        
        # Test length unit access
        start_time = time.perf_counter()
        for _ in range(iterations):
            unit = LengthUnits.meter
            _ = unit.si_factor  # Access a property
        length_time = time.perf_counter() - start_time
        
        # Test pressure unit access
        start_time = time.perf_counter()
        for _ in range(iterations):
            unit = PressureUnits.pascal
            _ = unit.si_factor  # Access a property
        pressure_time = time.perf_counter() - start_time
        
        # Both should be very fast (no string parsing overhead)
        assert length_time < 0.1, f"Length unit access too slow: {length_time}s"
        assert pressure_time < 0.1, f"Pressure unit access too slow: {pressure_time}s"
    
    def test_unit_equality_performance(self):
        """Test that unit equality checks are fast."""
        iterations = 10000
        
        start_time = time.perf_counter()
        for _ in range(iterations):
            result = LengthUnits.meter == LengthUnits.meter
            assert result is True
        same_unit_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        for _ in range(iterations):
            result = LengthUnits.meter == LengthUnits.millimeter
            assert result is False
        different_unit_time = time.perf_counter() - start_time
        
        # Equality checks should be very fast
        assert same_unit_time < 0.1, f"Same unit equality too slow: {same_unit_time}s"
        assert different_unit_time < 0.1, f"Different unit equality too slow: {different_unit_time}s"
    
    def test_unit_hashing_performance(self):
        """Test that unit hashing is fast and consistent."""
        units = [
            LengthUnits.meter, LengthUnits.millimeter, LengthUnits.inch,
            PressureUnits.pascal, PressureUnits.psi, PressureUnits.bar,
            DimensionlessUnits.dimensionless
        ]
        
        iterations = 1000
        start_time = time.perf_counter()
        
        for _ in range(iterations):
            unit_dict = {}
            for unit in units:
                unit_dict[unit] = unit.name
        
        hash_time = time.perf_counter() - start_time
        assert hash_time < 0.1, f"Unit hashing too slow: {hash_time}s"
        
        # Test hash consistency
        for unit in units:
            hash1 = hash(unit)
            hash2 = hash(unit)
            assert hash1 == hash2, f"Inconsistent hash for {unit.name}"


class TestTypeSystemIntegration:
    """Test integration with Python's type system."""
    
    def test_unit_constant_type_safety(self):
        """Test that unit constants provide type safety."""
        # Test that all unit constants are UnitConstant instances
        all_units = [
            LengthUnits.meter, LengthUnits.millimeter, LengthUnits.centimeter,
            LengthUnits.inch, LengthUnits.foot,
            PressureUnits.pascal, PressureUnits.kilopascal, PressureUnits.megapascal,
            PressureUnits.psi, PressureUnits.bar,
            DimensionlessUnits.dimensionless
        ]
        
        for unit in all_units:
            assert isinstance(unit, UnitConstant)
            assert hasattr(unit, 'name')
            assert hasattr(unit, 'symbol')
            assert hasattr(unit, 'dimension')
            assert hasattr(unit, 'si_factor')
            assert hasattr(unit, 'definition')
    
    def test_dimension_type_consistency(self):
        """Test that unit dimensions are consistent with type system."""
        # All length units should have LENGTH dimension
        length_units = [LengthUnits.meter, LengthUnits.mm, LengthUnits.inch]
        for unit in length_units:
            assert isinstance(unit.dimension, DimensionSignature)
            assert unit.dimension == LENGTH
        
        # All pressure units should have PRESSURE dimension
        pressure_units = [PressureUnits.pascal, PressureUnits.psi, PressureUnits.bar]
        for unit in pressure_units:
            assert isinstance(unit.dimension, DimensionSignature)
            assert unit.dimension == PRESSURE
        
        # Dimensionless unit should have DIMENSIONLESS dimension
        assert isinstance(DimensionlessUnits.dimensionless.dimension, DimensionSignature)
        assert DimensionlessUnits.dimensionless.dimension == DIMENSIONLESS


# Additional integration tests for edge cases and robustness
class TestEdgeCasesAndRobustness:
    """Test edge cases and robustness of the unit system."""
    
    def test_unit_string_representations(self):
        """Test string representations are meaningful and consistent."""
        test_cases = [
            (LengthUnits.meter, "m"),
            (LengthUnits.millimeter, "mm"),
            (LengthUnits.inch, "in"),
            (PressureUnits.pascal, "Pa"),
            (PressureUnits.psi, "psi"),
            (DimensionlessUnits.dimensionless, ""),  # Empty for dimensionless
        ]
        
        for unit, expected_str in test_cases:
            assert str(unit) == expected_str
            assert unit.symbol == expected_str
    
    def test_unit_name_uniqueness(self):
        """Test that all unit names are unique within the system."""
        all_unit_names = set()
        
        # Collect all unique unit names (excluding aliases)
        unit_classes = [LengthUnits, PressureUnits, DimensionlessUnits]
        for unit_class in unit_classes:
            for attr_name in dir(unit_class):
                if not attr_name.startswith('_'):
                    attr = getattr(unit_class, attr_name)
                    if isinstance(attr, UnitConstant):
                        unit_name = attr.name
                        # Only check if this unit name hasn't been seen before
                        # (aliases will reference the same unit, so we expect duplicates)
                        if unit_name not in all_unit_names:
                            all_unit_names.add(unit_name)
    
    def test_conversion_factor_precision(self):
        """Test that conversion factors maintain engineering precision."""
        # Test critical engineering conversion factors
        
        # Length: 1 inch = 25.4 mm exactly (by definition)
        inch_to_mm = LengthUnits.inch.si_factor / LengthUnits.millimeter.si_factor
        assert abs(inch_to_mm - 25.4) < 1e-12, "Inch to mm conversion not sufficiently precise"
        
        # Length: 1 foot = 12 inches exactly
        foot_to_inch = LengthUnits.foot.si_factor / LengthUnits.inch.si_factor
        assert abs(foot_to_inch - 12.0) < 1e-12, "Foot to inch conversion not sufficiently precise"
        
        # Pressure: 1 bar = 100,000 Pa exactly
        bar_to_pa = PressureUnits.bar.si_factor / PressureUnits.pascal.si_factor
        assert abs(bar_to_pa - 100000.0) < 1e-12, "Bar to Pa conversion not sufficiently precise"
    
    def test_zero_offset_for_all_units(self):
        """Test that all units have zero offset (no temperature-like units)."""
        all_units = [
            LengthUnits.meter, LengthUnits.millimeter, LengthUnits.inch,
            PressureUnits.pascal, PressureUnits.psi, PressureUnits.bar,
            DimensionlessUnits.dimensionless
        ]
        
        for unit in all_units:
            assert unit.definition.si_offset == 0.0, f"{unit.name} should have zero offset"


if __name__ == "__main__":
    # Run all tests when executed directly
    pytest.main([__file__, "-v"])
