# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qnty (formerly OptiUnit) is a high-performance unit system library for Python that provides dimensional safety and fast unit conversions for engineering calculations. The library is designed around type safety and performance optimization using compile-time dimensional analysis.

## Common Development Commands

### Dependencies and Environment

- Install dependencies: `pip install -r requirements.txt` or `poetry install`
- Run all tests: `pytest`
- Run specific test file: `pytest tests/test_dimension.py -v`
- Run single test: `pytest tests/test_dimension.py::TestDimensionSignatureCreation::test_basic_dimension_creation -v`
- Run benchmarks: `python tests/test_benchmark.py`

### Code Quality

- Lint code: Use `ruff` with line length of 200 characters (configured in pyproject.toml)
- The project uses Poetry for dependency management but also supports pip

### Package Management

- Package name: `qnty` (renamed from optiunit)
- Source code located in `src/qnty/`
- Uses Poetry build system with `poetry-core>=1.0.0`

## Architecture Overview

### Core Components

**Dimensional System (`dimension.py`)**

- `DimensionSignature`: Immutable dimension signatures using prime number encoding for ultra-fast dimensional compatibility checks
- `BaseDimension`: Enum of base dimensions (LENGTH, MASS, TIME, etc.) as prime numbers for efficient bit operations
- Enables zero-cost dimensional analysis at compile time

**Unit System (`unit.py`)**

- `UnitDefinition`: Immutable dataclass for unit definitions with SI conversion factors
- `UnitConstant`: Type-safe unit constants that provide performance optimizations
- `HighPerformanceRegistry`: Central registry with pre-computed conversion tables for fast unit conversions

**Quantities (`variable.py`)**

- `FastQuantity`: High-performance quantity class optimized for engineering calculations
- Uses `__slots__` for memory efficiency and caches commonly used values
- Implements fast arithmetic operations with dimensional checking

**Specialized Variables (`variables.py`)**

- `Length`: Type-safe length variable with fluent API
- `Pressure`: Type-safe pressure variable with fluent API
- Extends `TypeSafeVariable` with domain-specific functionality

**Setters (`setters.py`)**

- `TypeSafeSetter`: Generic setter with dimensional validation
- `LengthSetter`: Length-specific setter with unit properties (meters, millimeters, inches, feet)
- `PressureSetter`: Pressure-specific setter with unit properties (psi, kPa, MPa, bar)
- Provides fluent API patterns for type-safe value setting

**Unit Constants (`units.py`)**

- Type-safe unit constant classes: `LengthUnits`, `PressureUnits`, `DimensionlessUnits`
- Provides both full names and common aliases (e.g., `m`, `mm`, `Pa`, `kPa`)
- No string-based unit handling - all type-safe constants

**Type System (`types.py`)**

- `TypeSafeVariable`: Base class for dimension-specific variables with generic type safety
- Factory patterns and duck typing utilities to avoid circular imports
- Shared type definitions used across the system

**Mathematical System (`equation.py` & `expression.py`)**

- `Equation`: Represents mathematical equations (lhs = rhs) with solving capabilities
- `Expression`: Abstract base class for mathematical expression trees
- `BinaryOperation`, `VariableReference`, `Constant`: Expression implementations
- Variables can participate in mathematical operations, returning expressions
- Supports equation solving and residual checking for engineering calculations

### Key Architecture Patterns

**Fluent API Design**: Variables use specialized setters that return the variable itself for method chaining:

```python
length_var = Length("beam_length")
length_var.set(100.0).millimeters  # Returns Length instance
```

**Mathematical Expression Building**: Variables support arithmetic operations that return expressions:

```python
# Variables can be combined in mathematical expressions
T = Length("Wall Thickness", is_known=False)
T_bar = Length(0.147, "inches", "Nominal Wall Thickness")
U_m = Dimensionless(0.125, "Mill Undertolerance")

# Create equation: T = T_bar * (1 - U_m)
equation = T.equals(T_bar * (1 - U_m))

# Solve equations and check residuals
equation.solve_for("T", known_variables)
```

**Type Safety**: The system prevents dimensional errors at the type level:

- `TypeSafeVariable.quantity` is `Optional[FastQuantity]` - always check for None before accessing attributes
- Specialized variables (Length, Pressure) enforce their expected dimensions
- Setters validate unit compatibility before assignment

**Performance Optimization**:

- Pre-computed conversion tables to avoid runtime calculations
- Cached SI factors and dimension signatures for fast operations
- Prime number encoding for dimensional analysis
- `__slots__` usage for memory efficiency
- Fast path optimizations for same-unit operations

### Key Dependencies

- `numpy==2.3.2`: Numerical computations
- `Pint==0.24.4`: Comparison/benchmarking against established unit library
- `pytest==8.4.1`: Testing framework

### Reference Data

- `data/`: Contains comprehensive unit definition reference data for validation and testing

## Testing and Benchmarking

The project includes comprehensive test coverage with **457 tests** across 8 test files:

- **Dimension tests**: `test_dimension.py` - 80 tests covering dimensional analysis
- **Unit tests**: `test_unit.py` - 48 tests covering unit definitions and registry
- **Variable tests**: `test_variable.py` - 81 tests covering FastQuantity and TypeSafeVariable
- **Specialized variable tests**: `test_variables.py` - 111 tests covering Length and Pressure variables
- **Setter tests**: `test_setters.py` - 78 tests covering fluent API and type safety
- **Unit constant tests**: `test_units.py` - 42 tests covering unit constants
- **Equation tests**: `test_equations.py` - 17 tests covering mathematical equations and expressions
- **Benchmarks**: `test_benchmark.py` - Performance comparisons against Pint library

### Important Testing Notes

- Always add `assert variable.quantity is not None` before accessing `.value`, `.unit`, `.dimension`, or `._dimension_sig` attributes
- Use parametrized tests extensively for comprehensive coverage
- Follow existing test patterns for consistency
- Tests demonstrate significant performance advantages over established libraries
