# Troubleshooting Guide

Common issues and solutions when using Qnty.

## Common Errors

### `TypeError: Cannot add Length and Pressure`

**Problem**: Trying to perform operations on incompatible dimensions.

```python
# This will fail:
length = Length(100, "meter", "Distance")
pressure = Pressure(50, "pascal", "Pressure")
result = length + pressure  # TypeError!
```

**Solution**: Only perform operations on compatible quantities.

```python
# This works:
length1 = Length(100, "meter", "Length 1")
length2 = Length(50, "meter", "Length 2")
total = Length("total", is_known=False)
total.solve_from(length1 + length2)  # OK!
```

### `ValueError: No equations found for variable`

**Problem**: Trying to solve a variable without creating an equation.

```python
# This will fail:
thickness = Length("thickness", is_known=False)
thickness.solve()  # ValueError - no equations!
```

**Solution**: Create an equation first using `.equals()` or use `.solve_from()`.

```python
# Method 1: Use solve_from()
thickness = Length("thickness", is_known=False)
thickness.solve_from(pressure * diameter / (2 * stress))

# Method 2: Create equation then solve
equation = thickness.equals(pressure * diameter / (2 * stress))
thickness.solve()
```

### `AttributeError: 'NoneType' object has no attribute 'value'`

**Problem**: Trying to access quantity attributes without checking for None.

```python
# This might fail:
var = Length("test", is_known=False)
value = var.quantity.value  # AttributeError if quantity is None
```

**Solution**: Always check for None before accessing quantity attributes.

```python
# Safe approach:
var = Length("test", is_known=False)
if var.quantity is not None:
    value = var.quantity.value
    unit = var.quantity.unit
else:
    print("Variable has no quantity assigned")
```

## Missing Name Parameter

**Problem**: Forgetting the required name parameter in quantity constructors.

```python
# This will fail in some contexts:
length = Length(100, "meter")  # Missing name parameter
```

**Solution**: Always provide the three-parameter form for consistency.

```python
# This works:
length = Length(100, "meter", "Test Length")  # Clear and consistent
```

## Best Practices

### 1. Always Use Descriptive Names

```python
# Good:
beam_length = Length(5, "meter", "Main Beam Length")
design_pressure = Pressure(150, "pascal", "Design Pressure")

# Less clear:
l = Length(5, "meter", "l")
p = Pressure(150, "pascal", "p")
```

### 2. Check Variable States

```python
# Before solving, verify variables are properly set up
if not pressure.is_known:
    print(f"Warning: {pressure.symbol} is unknown")

if thickness.quantity is None:
    print(f"Warning: {thickness.symbol} has no equation")
```

### 3. Use Type Hints

```python
from qnty import Length, Pressure

def calculate_thickness(pressure: Pressure, diameter: Length) -> Length:
    """Calculate pipe wall thickness."""
    thickness = Length("thickness", is_known=False)
    thickness.solve_from(pressure * diameter / (2 * allowable_stress))
    return thickness
```

## Getting Help

- Check the [API Reference](API_REFERENCE.md) for complete documentation
- Review [Examples](../examples/) for working code patterns
- Look at [Tutorial](TUTORIAL.md) for step-by-step guidance

## Reporting Issues

If you encounter a bug:

1. Create a minimal example that reproduces the issue
2. Include the full error traceback
3. Specify your Python version and qnty version
4. Report at the project repository
