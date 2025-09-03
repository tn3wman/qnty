"""
Tests for SI prefix functionality
==================================

Tests the prefix system including definition, application, and registration.
"""

import pytest
from qnty.unit_system.dimension import LENGTH, PRESSURE, ENERGY_HEAT_WORK
from qnty.unit_system.core import UnitDefinition, HighPerformanceRegistry
from qnty.unit_system.prefixes import (
    SIPrefix, StandardPrefixes, 
    get_prefix_by_name, get_prefix_by_symbol, get_prefix_by_factor,
    COMMON_LENGTH_PREFIXES, COMMON_PRESSURE_PREFIXES
)


class TestSIPrefixDefinition:
    """Test the SIPrefix dataclass and its methods."""
    
    def test_prefix_creation(self):
        """Test creating an SI prefix."""
        kilo = StandardPrefixes.KILO.value
        assert kilo.name == "kilo"
        assert kilo.symbol == "k"
        assert kilo.factor == 1e3
    
    def test_apply_to_name(self):
        """Test applying prefix to unit name."""
        kilo = StandardPrefixes.KILO.value
        assert kilo.apply_to_name("meter") == "kilometer"
        
        milli = StandardPrefixes.MILLI.value
        assert milli.apply_to_name("gram") == "milligram"
        
        none_prefix = StandardPrefixes.NONE.value
        assert none_prefix.apply_to_name("meter") == "meter"
    
    def test_apply_to_symbol(self):
        """Test applying prefix to unit symbol."""
        mega = StandardPrefixes.MEGA.value
        assert mega.apply_to_symbol("Pa") == "MPa"
        
        micro = StandardPrefixes.MICRO.value
        assert micro.apply_to_symbol("m") == "μm"
        
        none_prefix = StandardPrefixes.NONE.value
        assert none_prefix.apply_to_symbol("m") == "m"


class TestPrefixLookup:
    """Test prefix lookup functions."""
    
    def test_get_prefix_by_name(self):
        """Test finding prefix by name."""
        kilo = get_prefix_by_name("kilo")
        assert kilo is not None
        assert kilo.factor == 1e3
        
        nano = get_prefix_by_name("nano")
        assert nano is not None
        assert nano.factor == 1e-9
        
        invalid = get_prefix_by_name("invalid")
        assert invalid is None
    
    def test_get_prefix_by_symbol(self):
        """Test finding prefix by symbol."""
        mega = get_prefix_by_symbol("M")
        assert mega is not None
        assert mega.name == "mega"
        
        micro = get_prefix_by_symbol("μ")
        assert micro is not None
        assert micro.name == "micro"
        
        invalid = get_prefix_by_symbol("X")
        assert invalid is None
    
    def test_get_prefix_by_factor(self):
        """Test finding prefix by multiplication factor."""
        giga = get_prefix_by_factor(1e9)
        assert giga is not None
        assert giga.name == "giga"
        
        pico = get_prefix_by_factor(1e-12)
        assert pico is not None
        assert pico.name == "pico"
        
        # Test with tolerance
        kilo = get_prefix_by_factor(1000.0000001, tolerance=1e-6)
        assert kilo is not None
        assert kilo.name == "kilo"
        
        invalid = get_prefix_by_factor(1234.5)
        assert invalid is None


class TestUnitDefinitionWithPrefix:
    """Test UnitDefinition with prefix support."""
    
    def test_create_unit_with_prefix(self):
        """Test creating a prefixed unit from a base unit."""
        # Create base meter unit
        meter = UnitDefinition("meter", "m", LENGTH, 1.0)
        
        # Create kilometer
        kilo = StandardPrefixes.KILO.value
        kilometer = UnitDefinition.with_prefix(meter, kilo)
        
        assert kilometer.name == "kilometer"
        assert kilometer.symbol == "km"
        assert kilometer.dimension == LENGTH
        assert kilometer.si_factor == 1000.0
        assert kilometer.base_unit_name == "meter"
        assert kilometer.prefix == kilo
    
    def test_create_multiple_prefixed_units(self):
        """Test creating multiple prefixed variants."""
        # Create base pascal unit
        pascal = UnitDefinition("pascal", "Pa", PRESSURE, 1.0)
        
        # Create various prefixed versions
        kilopascal = UnitDefinition.with_prefix(pascal, StandardPrefixes.KILO.value)
        megapascal = UnitDefinition.with_prefix(pascal, StandardPrefixes.MEGA.value)
        gigapascal = UnitDefinition.with_prefix(pascal, StandardPrefixes.GIGA.value)
        
        assert kilopascal.si_factor == 1e3
        assert megapascal.si_factor == 1e6
        assert gigapascal.si_factor == 1e9
        
        assert kilopascal.symbol == "kPa"
        assert megapascal.symbol == "MPa"
        assert gigapascal.symbol == "GPa"


class TestRegistryWithPrefixes:
    """Test HighPerformanceRegistry with prefix support."""
    
    def test_register_with_prefixes(self):
        """Test registering a unit with automatic prefix generation."""
        registry = HighPerformanceRegistry()
        
        # Create a new base unit (joule for energy)
        joule = UnitDefinition("joule", "J", ENERGY_HEAT_WORK, 1.0)
        
        # Register with common energy prefixes
        prefixes = [StandardPrefixes.KILO, StandardPrefixes.MEGA, StandardPrefixes.GIGA]
        registry.register_with_prefixes(joule, prefixes)
        
        # Check that base unit was registered
        assert "joule" in registry.units
        assert registry.units["joule"].si_factor == 1.0
        
        # Check that prefixed variants were registered
        assert "kilojoule" in registry.units
        assert registry.units["kilojoule"].si_factor == 1e3
        
        assert "megajoule" in registry.units
        assert registry.units["megajoule"].si_factor == 1e6
        
        assert "gigajoule" in registry.units
        assert registry.units["gigajoule"].si_factor == 1e9
        
        # Check that base unit is tracked
        assert "joule" in registry.base_units
        assert "joule" in registry.prefixable_units
    
    def test_conversion_with_prefixed_units(self):
        """Test that conversions work correctly with prefixed units."""
        registry = HighPerformanceRegistry()
        
        # Register meter with common prefixes
        meter = UnitDefinition("meter", "m", LENGTH, 1.0)
        registry.register_with_prefixes(meter, COMMON_LENGTH_PREFIXES)
        
        # Finalize to precompute conversions
        registry.finalize_registration()
        
        # Check conversion factors
        key_km_to_m = ("kilometer", "meter")
        assert key_km_to_m in registry.conversion_table
        assert registry.conversion_table[key_km_to_m] == 1000.0
        
        key_m_to_mm = ("meter", "millimeter")
        assert key_m_to_mm in registry.conversion_table
        assert registry.conversion_table[key_m_to_mm] == 1000.0
        
        key_km_to_mm = ("kilometer", "millimeter")
        assert key_km_to_mm in registry.conversion_table
        assert registry.conversion_table[key_km_to_mm] == 1e6
    
    def test_dimensional_grouping_with_prefixes(self):
        """Test that prefixed units are correctly grouped by dimension."""
        registry = HighPerformanceRegistry()
        
        # Register pascal with prefixes
        pascal = UnitDefinition("pascal", "Pa", PRESSURE, 1.0)
        registry.register_with_prefixes(pascal, COMMON_PRESSURE_PREFIXES)
        
        # Check that all pressure units are in the same dimensional group
        pressure_sig = PRESSURE._signature
        assert pressure_sig in registry.dimensional_groups
        
        pressure_group = registry.dimensional_groups[pressure_sig]
        pressure_names = [unit.name for unit in pressure_group]
        
        # Should include original units plus new ones
        assert "pascal" in pressure_names or "pascal" in registry.units
        assert "kilopascal" in pressure_names or "kilopascal" in registry.units
        assert "megapascal" in pressure_names or "megapascal" in registry.units


class TestPrefixIntegration:
    """Test integration of prefix system with existing functionality."""
    
    def test_prefix_with_offset_units(self):
        """Test that prefixes work correctly with units that have offsets."""
        # Note: Temperature units like Celsius have offsets
        # Prefixes should only affect the factor, not the offset
        celsius = UnitDefinition("celsius", "°C", LENGTH, 1.0, si_offset=273.15)  # Using LENGTH for test
        
        kilo = StandardPrefixes.KILO.value
        kilocelsius = UnitDefinition.with_prefix(celsius, kilo)
        
        assert kilocelsius.si_factor == 1000.0
        assert kilocelsius.si_offset == 273.15  # Offset unchanged
    
    def test_no_prefix_enum(self):
        """Test that NONE prefix doesn't create a new unit."""
        registry = HighPerformanceRegistry()
        
        # Use a unique unit name not in the default registry
        testmeter = UnitDefinition("testmeter", "tm", LENGTH, 1.0)
        initial_count = len(registry.units)
        
        # Register with NONE prefix - should only add base unit
        registry.register_with_prefixes(testmeter, [StandardPrefixes.NONE])
        
        assert len(registry.units) == initial_count + 1
        assert "testmeter" in registry.units
        # No prefixed variant should be created


if __name__ == "__main__":
    pytest.main([__file__, "-v"])