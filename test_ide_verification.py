#!/usr/bin/env python3
"""Test script to verify IDE autocomplete functionality after type stub changes."""

from src.qnty import Length, Pressure

def test_basic_functionality():
    """Test basic functionality and IDE autocomplete."""
    
    # Test creating unknown variable
    length = Length("beam_length")
    
    # Test setter functionality - IDE should provide autocomplete for units
    length_setter = length.set(100.0)
    
    # These should show autocomplete for length units
    # length_setter.millimeters
    # length_setter.inches 
    # length_setter.meters
    
    # Test known variable creation
    pressure = Pressure(150.0, "psi", "operating_pressure")
    
    # Test unit conversion methods - should show autocomplete
    # pressure.to_unit.pascals
    # pressure.as_unit.bar
    
    print(f"Length: {length}")
    print(f"Pressure: {pressure}")
    
    return True

if __name__ == "__main__":
    test_basic_functionality()