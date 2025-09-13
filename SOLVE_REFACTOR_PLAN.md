# Qnty Solve System Refactor - Path Forward

## Current State Analysis

### What I Found

1. **`solve_methods_demo.py`** tries to use outdated patterns:
   - `T.equals()` method (doesn't exist)
   - `T.solve()` method (doesn't exist)
   - Old quantity creation syntax like `Length(10.0, "inch", "D")`
   - Missing `Pressure` class

2. **`simple_problem_demo.py`** shows the **intended pattern**:
   - Problem class with declarative variables and equations
   - `T.equals(expression)` creates `Equation` objects
   - Problem-level solving with `.solve()`

3. **Current algebra system** has:
   - `solve(quantity, expression)` function ✅
   - `Equation` class for equation representation ✅
   - Expression system with operators ✅

## Recommended Path Forward

### 1. Immediate Fix for `test_equation_based_solve()`

Since you don't want `.equals()` on quantities anymore, replace the equation-based approach with direct `solve()` calls:

```python
def test_equation_based_solve():
    """Test sequential solving approach."""
    print("\n=== Testing sequential solve() method ===")

    # Multi-step problem: T = T_bar * (1 - U_m), then d = D - 2*T
    D = Length("D").set(10.0).inch
    T_bar = Length("T_bar").set(0.147).inch
    U_m = Dimensionless("U_m").set(0.125).dimensionless

    # Unknown variables
    T = Length("T")
    d = Length("d")

    print(f"Given: D = {D}, T_bar = {T_bar}, U_m = {U_m}")
    print(f"Unknown: T = {T}, d = {d}")

    # Solve T first using algebra.solve()
    print("Solving T...")
    solve(T, T_bar * (1 - U_m))
    print(f"T = {T}")

    # Solve d second using algebra.solve()
    print("Solving d...")
    solve(d, D - 2 * T)
    print(f"d = {d}")

    # ... rest of verification code
```

### 2. Create Algebra Helper Functions

Add equation creation functions to the algebra module:

```python
# In src/qnty/algebra/__init__.py
def equation(lhs: FieldQuantity, rhs: Expression, name: str = None) -> Equation:
    """Create an equation: lhs = rhs"""
    eq_name = name or f"{lhs.name}_equation"
    return Equation(eq_name, lhs, rhs)
```

### 3. Add Missing Quantity Classes

Add `Pressure` to `quantity_catalog.py` or generate it:

```python
@quantity(uc.PressureUnits)
class Pressure:
    """Pressure quantity with automatic boilerplate."""
    pass
```

### 4. Problem Class Integration Pattern

For the Problem-based workflow, the pattern should be:

```python
from qnty.algebra import equation

class MyProblem(Problem):
    # Variables
    T = Length("T")
    D = Length("D").set(10.0).inch

    # Equations using algebra functions
    T_eq = equation(T, T_bar * (1 - U_m))
    d_eq = equation(d, D - 2 * T)
```

### 5. Proposed API Design

**For simple solving (current working approach):**
```python
from qnty.algebra import solve
solve(quantity, expression)  # ✅ Already works
```

**For equation-based problems:**
```python
from qnty.algebra import equation, EquationSystem

# Create equations
eq1 = equation(T, T_bar * (1 - U_m))
eq2 = equation(d, D - 2 * T)

# Solve system
system = EquationSystem([eq1, eq2])
system.solve()
```

**For Problem classes:**
```python
class MyProblem(Problem):
    # The Problem metaclass should scan for Equation objects
    # and automatically build the equation system
    pass
```

## Implementation Priority

### Phase 1: Fix Immediate Issues
1. ✅ Fix `test_solve_from_method()` - **COMPLETED**
2. 🔄 Fix `test_equation_based_solve()` using sequential solve() approach
3. 🔄 Add missing Pressure class to quantity catalog
4. 🔄 Fix quantity creation syntax throughout demo files

### Phase 2: Enhance Algebra Module
1. 🔄 Add `equation()` helper function to algebra module
2. 🔄 Ensure EquationSystem works with solve() pattern
3. 🔄 Add equation creation utilities

### Phase 3: Problem Class Integration
1. 🔄 Ensure Problem metaclass integrates with new equation system
2. 🔄 Test simple_problem_demo.py with new patterns
3. 🔄 Update documentation and examples

## Key Insights

### What's Working Well
- ✅ Core `solve(quantity, expression)` function works great
- ✅ Reverse arithmetic operations (`1 - U_m`) now work correctly
- ✅ Expression system handles complex mathematical operations
- ✅ Unit conversion and dimensional safety are preserved

### What Needs Work
- 🔄 Missing quantity classes (Pressure, etc.)
- 🔄 Declarative equation creation patterns
- 🔄 Problem class integration with algebra system
- 🔄 Demo file syntax updates

### Architecture Decision
**Keep quantities focused on basic arithmetic when all values are known. All solving infrastructure lives in the algebra module.** This maintains clean separation of concerns and prevents the quantity classes from becoming bloated.

## Summary

The path forward is:

1. **Short term**: Fix `solve_methods_demo.py` by replacing equation-based tests with sequential `solve()` calls
2. **Medium term**: Add missing quantity classes and algebra helper functions
3. **Long term**: Ensure Problem class integration works seamlessly with the algebra system

The core `solve(quantity, expression)` function works great and represents the right architectural approach. The main gaps are in the declarative equation creation patterns and Problem class integration.