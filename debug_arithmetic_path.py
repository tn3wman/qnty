#!/usr/bin/env python3
"""Debug which arithmetic path is being taken."""

from src.qnty import Length, Pressure, Area
from src.qnty.units.field_units import LengthUnits, PressureUnits

# Create test variables
length_10 = Length(10.0, LengthUnits.millimeter, "test_length")
width_5 = Length(5.0, LengthUnits.millimeter, "test_width")

print("=== Variable Analysis ===")
print(f"length_10.is_known: {length_10.is_known}")
print(f"width_5.is_known: {width_5.is_known}")
print(f"length_10.quantity: {length_10.quantity}")
print(f"width_5.quantity: {width_5.quantity}")
print(f"length_10._arithmetic_mode: {length_10._arithmetic_mode}")

# Test the should_return_quantity logic directly
should_return_quantity = length_10._should_return_quantity(length_10, width_5)
print(f"_should_return_quantity(length_10, width_5): {should_return_quantity}")

# Test what path is taken
print("\n=== Arithmetic Path Testing ===")

# Monkey patch to debug
original_quantity_multiply = length_10._quantity_multiply
original_expression_multiply = length_10._expression_multiply

def debug_quantity_multiply(left, right):
    print("Taking QUANTITY path (fast)")
    return original_quantity_multiply(left, right)

def debug_expression_multiply(left, right):
    print("Taking EXPRESSION path (slow)")
    return original_expression_multiply(left, right)

length_10._quantity_multiply = debug_quantity_multiply
length_10._expression_multiply = debug_expression_multiply

# Test multiplication
result = length_10 * width_5
print(f"Result: {result}")
print(f"Result type: {type(result)}")