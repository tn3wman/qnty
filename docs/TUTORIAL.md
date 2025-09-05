# Qnty Tutorial: Getting Started

Welcome to Qnty! This tutorial will guide you through the essential concepts and features of this high-performance unit system library.

## What You'll Learn

1. Creating and manipulating quantities with units
2. Mathematical operations with dimensional safety
3. Building and solving engineering equations
4. Using the Problem system for complex calculations

## Prerequisites

```bash
pip install qnty
```

## Lesson 1: Creating Your First Quantities

Let's start with the basics - creating quantities with units:

```python
from qnty import Length, Pressure, Temperature, Mass

# Create quantities by specifying value, unit, and description
beam_length = Length(5.2, "meter", "Beam Length")
tire_pressure = Pressure(32, "pound_force_per_square_inch", "Tire Pressure")
room_temp = Temperature(22, "celsius", "Room Temperature")
steel_mass = Mass(1500, "kilogram", "Steel Mass")

print(f"Beam length: {beam_length}")
print(f"Tire pressure: {tire_pressure}")
print(f"Room temperature: {room_temp}")
print(f"Steel mass: {steel_mass}")
```

### Key Points

- Each quantity type enforces dimensional consistency
- Units are specified as strings
- The third parameter is a descriptive name
- Qnty automatically formats output with appropriate symbols

## Lesson 2: Mathematical Operations

Qnty prevents dimensional errors while enabling natural mathematical operations:

```python
from qnty import Length, Area, Volume

# Create some measurements
width = Length(3.0, "meter", "Width")
height = Length(2.5, "meter", "Height")
depth = Length(4.0, "meter", "Depth")

print(f"Given dimensions:")
print(f"  Width: {width}")
print(f"  Height: {height}")
print(f"  Depth: {depth}")
print()

# Method 1: solve_from() - creates equation and solves immediately
area = Area("area", is_known=False)
area.solve_from(width * height)
print(f"Area = width × height = {area}")

# Method 2: Create equations with .equals() and solve separately
volume = Volume("volume", is_known=False)
volume_equation = volume.equals(area * depth)
volume.solve()
print(f"Volume = area × depth = {volume}")

# Calculate perimeter
perimeter = Length("perimeter", is_known=False)
perimeter.solve_from(2 * (width + height))
print(f"Perimeter = 2 × (width + height) = {perimeter}")
```

### Dimensional Safety in Action

Try to do something dimensionally incorrect:

```python
from qnty import Length, Pressure

length = Length(100, "millimeter", "Test Length")
pressure = Pressure(50, "kilopascal", "Test Pressure")

# This will raise a TypeError!
try:
    result = length + pressure  # Can't add length to pressure!
except TypeError as e:
    print(f"Error caught: {e}")
```

## Lesson 3: Mixed Units

Qnty automatically handles unit conversions in operations:

```python
from qnty import Length

# Mix metric and imperial units
metric_length = Length(2, "meter", "Length in meters")
imperial_length = Length(500, "millimeter", "Length in millimeters")

print(f"Length 1: {metric_length}")
print(f"Length 2: {imperial_length}")

# Add different units - qnty handles conversion automatically
total_length = Length("total_length", is_known=False)
total_length.solve_from(metric_length + imperial_length)
print(f"Total length: {total_length}")
```

## Lesson 4: Comparisons and Logic

Use comparison methods for engineering decisions:

```python
from qnty import Pressure

# Define pressures
operating_pressure = Pressure(120, "kilopascal", "Operating Pressure")
design_limit = Pressure(150, "kilopascal", "Design Limit")
safety_threshold = Pressure(100, "kilopascal", "Safety Threshold")

print(f"Operating: {operating_pressure}")
print(f"Design limit: {design_limit}")
print(f"Safety threshold: {safety_threshold}")

# Using comparison methods
print("Using comparison methods:")
print(f"  operating.lt(design_limit): {operating_pressure.lt(design_limit)}")
print(f"  operating.gt(safety_threshold): {operating_pressure.gt(safety_threshold)}")

# Using Python operators
print("Using Python operators:")
print(f"  operating < design_limit: {operating_pressure < design_limit}")
print(f"  operating > safety_threshold: {operating_pressure > safety_threshold}")

# Engineering decision logic
if operating_pressure < design_limit:
    print("✓ Operating within design limits")
else:
    print("⚠ Exceeds design limits!")
```

## Lesson 5: Mathematical Functions

Qnty includes mathematical functions that respect dimensional analysis:

```python
from qnty import Length, Area, sqrt, AnglePlane, sin, cos

# Area to length using square root
area = Area(25, "square_meter", "Square Area")
side_length_unknown = Length("side_length", is_known=False)
side_length_unknown.solve_from(sqrt(area))
print(f"Square with area {area} has side length: {side_length_unknown}")

# Trigonometry
angle = AnglePlane(30, "degree", "Test Angle")
sine_val = sin(angle)    # Returns dimensionless
cosine_val = cos(angle)  # Returns dimensionless

print(f"sin(30°) = {sine_val}")
print(f"cos(30°) = {cosine_val}")
```

## Lesson 6: Building Equations

Create and solve engineering equations:

```python
from qnty import Length, Pressure

# Define variables for pipe thickness calculation
pressure = Pressure(150, "pound_force_per_square_inch", "Design Pressure")
diameter = Length(6, "inch", "Pipe Diameter")
allowable_stress = Pressure(20000, "pound_force_per_square_inch", "Allowable Stress")
thickness = Length("wall_thickness", is_known=False)

# Create equation: t = (P * D) / (2 * S)
equation = thickness.equals((pressure * diameter) / (2 * allowable_stress))

print(f"Equation: {equation}")

# Solve for thickness
thickness.solve()
print(f"Required thickness: {thickness}")
```

## Lesson 7: The Problem System

For complex engineering problems, use the Problem class:

```python
from qnty import Problem, Length, Pressure

class SimplePipeDesign(Problem):
    """Simple pipe wall thickness calculation"""
    
    # Known variables
    internal_pressure = Pressure(100, "kilopascal", "Internal Pressure")
    outer_diameter = Length(200, "millimeter", "Outer Diameter")
    allowable_stress = Pressure(150000, "kilopascal", "Allowable Stress")
    
    # Unknown variable - what we want to find
    wall_thickness = Length("wall_thickness", is_known=False)
    
    # Equation: t = (P * D) / (2 * S)
    thickness_equation = wall_thickness.equals(
        (internal_pressure * outer_diameter) / (2 * allowable_stress)
    )

# Create and solve the problem
problem = SimplePipeDesign()
print("Solving pipe design problem...")

problem.solve()

print(f"✓ Solution found!")
print(f"Required wall thickness: {problem.wall_thickness}")
```

## Next Steps

Congratulations! You've learned the fundamentals of Qnty. Here's what to explore next:

1. **[API Reference](API_REFERENCE.md)** - Complete list of all quantity types and functions
2. **[Examples](../examples/)** - Real-world engineering examples
3. **Advanced Features:**
   - Sub-problem composition
   - Complex equation systems
   - Custom validation rules

## Common Patterns Summary

```python
# 1. Create quantities with value, unit, and name
length = Length(100, "millimeter", "Beam Length")

# 2. Solve expressions immediately
area = Area("area", is_known=False)
area.solve_from(width * height)

# 3. Create equations and solve separately
equation = thickness.equals(expression)
thickness.solve()

# 4. Build Problem classes
class MyProblem(Problem):
    # Define variables and equations
    pass

problem = MyProblem()
problem.solve()
```

## Tips for Success

1. **Always specify units** - Qnty's power comes from dimensional safety
2. **Use descriptive variable names** - Include the third parameter for clarity
3. **Leverage type safety** - Let Qnty catch dimensional errors early
4. **Start simple** - Build complex problems from simple components
5. **Use the Problem system** - It handles dependencies and solving automatically

Ready to build robust engineering calculations? Check out the [examples](../examples/) directory for real-world applications!
