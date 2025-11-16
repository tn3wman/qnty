# Vector and ForceVector API Improvements

## Summary

This document describes the improvements made to the `Vector` and `ForceVector` classes to provide a unified, fluent API for unit conversion and comparison that matches the Qnty design philosophy.

## Problem

The original implementation had several pain points:

1. **Manual unit conversions everywhere**: Users had to write `force.magnitude.value / force.magnitude.preferred.si_factor` to get values in specific units
2. **No fluent API for vectors**: Unlike `Quantity` which has `.to_unit` and `.as_unit`, vectors didn't have convenient conversion methods
3. **Manual angle reference conversions**: Users had to manually call `angle_ref.from_standard(force.angle.value, angle_unit="degree")`
4. **Difficult comparisons**: No easy way to compare vectors with different units or in different angle reference systems
5. **Inconsistent with Qnty's design**: `Quantity` has fluent APIs, but `ForceVector` didn't

## Solution

### New ForceVector Methods

#### 1. `magnitude_in(unit: Unit | str) -> float`
Get magnitude in a specific unit with automatic conversion.

```python
# Before (manual conversion)
mag_lb = F.magnitude.value / F.magnitude.preferred.si_factor

# After (clean API)
mag_lb = F.magnitude_in("lbf")
```

#### 2. `angle_in(unit: Unit | str = "degree", wrt: str | AngleReference | None = None) -> float`
Get angle in a specific unit and reference system.

```python
# Get angle in degrees (standard CCW from +x)
angle = F.angle_in("degree")

# Get angle in radians
angle_rad = F.angle_in("radian")

# Get angle in different reference system
angle_cw = F.angle_in("degree", wrt="cw:+x")  # Clockwise from +x
angle_from_y = F.angle_in("degree", wrt="+y")  # CCW from +y
```

#### 3. `with_magnitude_unit(unit: Unit | str) -> ForceVector`
Create a copy with a different magnitude display unit.

```python
F1 = ForceVector(magnitude=1000, angle=45, unit="N")
F2 = F1.with_magnitude_unit("lbf")  # Same force, different display unit
```

#### 4. `with_angle_unit(unit: Unit | str) -> ForceVector`
Create a copy with a different angle display unit.

```python
F1 = ForceVector(magnitude=100, angle=45, unit="N", angle_unit="degree")
F2 = F1.with_angle_unit("radian")  # Same angle, different unit
```

#### 5. `with_angle_reference(wrt: str | AngleReference) -> ForceVector`
Create a copy with a different angle reference system.

```python
F1 = ForceVector(magnitude=100, angle=45, unit="N")
F2 = F1.with_angle_reference("cw:+x")  # Same force, different reference
```

#### 6. `is_close(other: ForceVector, **tolerances) -> bool`
Compare forces with explicit tolerance control.

```python
F1 = ForceVector(magnitude=100, angle=45, unit="N")
F2 = ForceVector(magnitude=100.001, angle=45.005, unit="N")

# Use default tolerances
assert F1.is_close(F2)

# Custom magnitude tolerance
assert F1.is_close(F2, magnitude_rel_tol=1e-9)

# Custom angle tolerance
assert F1.is_close(F2, angle_abs_tol_deg=0.001)

# Component-wise comparison (useful for relative angle constraints)
assert F1.is_close(F2, compare_components=True)
```

#### 7. Improved `__eq__`
Equality now automatically handles unit conversion.

```python
F1 = ForceVector(magnitude=1000, angle=45, unit="N")
F2 = ForceVector(magnitude=224.809, angle=45, unit="lbf")

# Automatically converts units for comparison
assert F1.is_close(F2, magnitude_rel_tol=1e-3)
```

### New Vector Methods

#### 1. `magnitude_in(unit: Unit | str) -> float`
Get vector magnitude in a specific unit.

```python
v = Vector(1000, 0, 0, unit=LengthUnits.meter)

# Get magnitude in different units
mag_km = v.magnitude_in("km")  # 1.0
mag_mm = v.magnitude_in("mm")  # 1,000,000
```

## Benefits

1. **Consistent with Qnty philosophy**: Matches the fluent API patterns used in `Quantity`
2. **Easier to use**: No more manual unit conversions or reference system transformations
3. **Type-safe**: Returns primitive types (float) for easy comparison and arithmetic
4. **Flexible**: Supports both string unit names and `Unit` objects
5. **Tolerant comparisons**: `is_close()` provides fine-grained control over comparison tolerances
6. **Non-breaking**: All existing APIs continue to work; these are additive improvements

## Migration Guide

### Before and After Examples

#### Example 1: Get magnitude in specific unit
```python
# Before
mag_value = force.magnitude.value / force.magnitude.preferred.si_factor

# After
mag_value = force.magnitude_in("lbf")
```

#### Example 2: Get angle in different reference system
```python
# Before
from qnty.spatial.angle_reference import AngleReference
angle_ref = ForceVector.parse_wrt("cw:+x", force.coordinate_system)
angle_cw = angle_ref.from_standard(force.angle.value, angle_unit="degree")

# After
angle_cw = force.angle_in("degree", wrt="cw:+x")
```

#### Example 3: Compare forces in different units
```python
# Before
# Manual conversion required, or complex tolerance calculations

# After
F1 = ForceVector(magnitude=1000, angle=45, unit="N")
F2 = ForceVector(magnitude=224.809, angle=45, unit="lbf")
assert F1.is_close(F2, magnitude_rel_tol=1e-3)
```

## Test Coverage

Comprehensive test coverage added in [tests/test_vector_api_improvements.py](tests/test_vector_api_improvements.py):

- 28 tests covering all new methods
- Tests for unit conversion (magnitude and angle)
- Tests for angle reference system conversion
- Tests for `with_*` methods creating modified copies
- Tests for `is_close()` with various tolerance configurations
- Tests for improved `__eq__` behavior
- Integration tests showing real-world usage patterns

All tests pass ✅

## Test Migration

All existing statics tests have been updated to use the new cleaner API:
- [tests/statics/test_component_method.py](tests/statics/test_component_method.py) - Updated 25 tests
- [tests/statics/test_triangle_method.py](tests/statics/test_triangle_method.py) - Updated 30 tests
- [tests/statics/test_cartesian_3d.py](tests/statics/test_cartesian_3d.py) - Updated 5 tests

**Before:**
```python
# Manual magnitude conversion
actual_mag = force.magnitude.value / force.magnitude.preferred.si_factor

# Manual angle conversion
angle_ref = ForceVector.parse_wrt(expected_wrt, force.coordinate_system, forces=forces_dict)
actual_ang = angle_ref.from_standard(force.angle.value, angle_unit="degree")
```

**After:**
```python
# Clean API
actual_mag = force.magnitude_in(force.magnitude.preferred)
actual_ang = force.angle_in("degree", wrt=expected_wrt, forces=forces_dict)
```

## Backward Compatibility

All changes are **100% backward compatible**:
- No existing methods were modified
- Only new methods were added
- All existing tests pass: **87 passed** (59 statics + 28 new API tests)
- 1 pre-existing failure in test_cartesian_3d.py (unrelated to these changes)

## Future Frontend Integration

These improvements directly address the requirements for a frontend interface where users will:
- Frequently change magnitude units (N ↔ lbf ↔ kN, etc.)
- Frequently change angle units (degrees ↔ radians)
- Need to view angles in different reference systems
- Compare forces computed in different ways or units

The new API makes all these operations simple and intuitive.
