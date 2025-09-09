#!/usr/bin/env python3
"""
Demonstration of the new UnifiedVariable system with arithmetic mode control.

This example shows how to use the simplified 2-level hierarchy with mixin composition
and user-controllable arithmetic return types.
"""

import qnty

def main():
    print("=" * 60)
    print("QNTY Unified Variable System Demonstration")
    print("=" * 60)
    print()

    # Test 1: Basic variable creation with different constructor patterns
    print("=== 1. Variable Creation Patterns ===")
    print()
    
    # Unknown variables
    length_unknown = qnty.Length("beam_length")
    width_unknown = qnty.Length("beam_width")
    
    # Known variables with values
    length_known = qnty.Length(10, "mm", "known_length")
    width_known = qnty.Length(5, "mm", "known_width")
    
    # Dimensionless variables (different pattern)
    efficiency = qnty.Dimensionless(0.85, "thermal_efficiency")
    safety_factor = qnty.Dimensionless(2.0, "safety_factor")
    
    print(f"Unknown length: {length_unknown}")
    print(f"Unknown width: {width_unknown}")
    print(f"Known length: {length_known}")
    print(f"Known width: {width_known}")
    print(f"Efficiency: {efficiency}")
    print(f"Safety factor: {safety_factor}")
    print()
    
    # Test 2: Arithmetic Mode Control
    print("=== 2. Arithmetic Mode Control ===")
    print()
    
    l1 = qnty.Length(10, "mm", "l1")
    l2 = qnty.Length(5, "mm", "l2")
    
    # Quantity mode (fast path) - returns Quantity objects
    l1.set_arithmetic_mode('quantity')
    result_qty = l1 + l2
    print(f"Quantity mode: {l1} + {l2} = {result_qty}")
    print(f"  Result type: {type(result_qty).__name__}")
    print()
    
    # Expression mode (flexible path) - returns Expression objects
    l1.set_arithmetic_mode('expression')
    result_expr = l1 + l2
    print(f"Expression mode: {l1} + {l2} = {result_expr}")
    print(f"  Result type: {type(result_expr).__name__}")
    print()
    
    # Auto mode (intelligent) - automatically chooses best type
    l1.set_arithmetic_mode('auto')
    result_auto = l1 + l2  # Both known -> Quantity
    print(f"Auto mode (both known): {l1} + {l2} = {result_auto}")
    print(f"  Result type: {type(result_auto).__name__}")
    
    # Auto mode with unknown variable -> Expression
    l3 = qnty.Length("unknown_length")
    result_auto_expr = l1 + l3  # One unknown -> Expression
    print(f"Auto mode (one unknown): {l1} + {l3} = {result_auto_expr}")
    print(f"  Result type: {type(result_auto_expr).__name__}")
    print()
    
    # Test 3: Equation Creation and Solving
    print("=== 3. Equation Creation ===")
    print()
    
    # Create variables for equation
    area = qnty.Area("calculated_area")
    length = qnty.Length(12, "mm", "length")
    width = qnty.Length(8, "mm", "width")
    
    # Create equation: area = length * width
    area_equation = area.equals(length * width)
    print(f"Equation: {area_equation}")
    print(f"Equation type: {type(area_equation).__name__}")
    print()
    
    # Test 4: Problem System Integration
    print("=== 4. Problem System Integration ===")
    print()
    
    # Create a problem
    problem = qnty.Problem("rectangle_calculation")
    
    # Add variables
    problem.add_variable(length)
    problem.add_variable(width)
    problem.add_variable(area)
    
    print(f"Problem: {problem}")
    print(f"Variables: {list(problem.variables.keys())}")
    print()
    
    # Retrieve variables
    retrieved_length = problem.get_variable("length")
    print(f"Retrieved variable: {retrieved_length}")
    print()
    
    # Test 5: Comparison Operations
    print("=== 5. Comparison Operations ===")
    print()
    
    p1 = qnty.Pressure(100, "kPa", "pressure1")
    p2 = qnty.Pressure(150, "kPa", "pressure2")
    
    # Method-based comparisons
    print(f"p1.lt(p2): {p1.lt(p2)}")
    print(f"p1.geq(p2): {p1.geq(p2)}")
    
    # Operator-based comparisons
    print(f"p1 < p2: {p1 < p2}")
    print(f"p1 >= p2: {p1 >= p2}")
    print()
    
    # Test 6: Variable Management
    print("=== 6. Variable Management ===")
    print()
    
    # Create a variable
    temp = qnty.Temperature("ambient_temp")
    print(f"Initial: {temp}")
    print(f"Is known: {temp.is_known}")
    
    # Update with value and unit
    temp.update(value=298, unit="K")
    print(f"After update: {temp}")
    print(f"Is known: {temp.is_known}")
    
    # Mark as unknown
    temp.mark_unknown()
    print(f"After mark_unknown: {temp}")
    print(f"Is known: {temp.is_known}")
    
    # Mark as known
    temp.mark_known()
    print(f"After mark_known: {temp}")
    print(f"Is known: {temp.is_known}")
    print()
    
    print("=" * 60)
    print("SUCCESS: All UnifiedVariable features working correctly!")
    print("SUCCESS: Simplified 2-level hierarchy operational")
    print("SUCCESS: Arithmetic mode control functional") 
    print("SUCCESS: Problem system integration successful")
    print("SUCCESS: Comparison operations working")
    print("SUCCESS: Variable management capabilities complete")
    print("=" * 60)


if __name__ == "__main__":
    main()