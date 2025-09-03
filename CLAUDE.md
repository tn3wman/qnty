# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qnty (formerly OptiUnit) is a high-performance unit system library for Python that provides dimensional safety and fast unit conversions for engineering calculations. The library is designed around type safety and performance optimization using compile-time dimensional analysis.

### User-Focused API

The qnty library provides a simple, focused API for users:

1. **100+ Variable Types** (from `variables.py`): Length, Pressure, Temperature, Mass, Volume, Area, Force, etc.
2. **Problem Class** (from `problem.py`): Engineering problem container with automatic equation solving
3. **Validation System** (`add_check` from `qnty.problem_system.checks`): Code compliance and engineering checks
4. **Expression Methods**: Built into variables for mathematical operations (e.g., `pressure.geq(limit)`, `length * width`)

All other modules and classes are internal implementation details that users should not access directly.

## Common Development Commands

### Dependencies and Environment

- Install dependencies: `pip install -r requirements.txt` or `poetry install`
- Run all tests: `pytest`
- Run specific test file: `pytest tests/test_dimension.py -v`
- Run single test: `pytest tests/test_dimension.py::TestDimensionSignatureCreation::test_basic_dimension_creation -v`
- Run benchmarks: `python tests/test_benchmark.py`

### Code Quality

- Lint code: `ruff check src/ tests/` (configured with line length of 200 characters in pyproject.toml)
- Format code: `ruff format src/ tests/`  
- Type checking: `mypy src/qnty/` (if mypy is installed)
- The project uses Poetry for dependency management but also supports pip

### Package Management

- Package name: `qnty` (renamed from optiunit)
- Source code located in `src/qnty/`
- Uses Poetry build system with `poetry-core>=1.0.0`
- Supports Python 3.11+ (up to 3.13)

### Release Management

- **Automated Release**: `python release.py` - Increments patch version, creates git tag, and pushes to origin
- **Version Control**: Uses semantic versioning with Poetry version management
- **Current Version**: 0.0.8 (as of latest update)

## Architecture Overview

### Clean Dependency Hierarchy

The codebase has been carefully structured to eliminate circular imports with a strict hierarchy:

```python
dimension → unit_system/core → variable_system/core → variables → expression → equation
```

This ensures clean dependencies and enables proper type checking throughout the system.

### Modular Architecture

The system uses a layered approach with separate concerns:

- **Core Layer** (`dimension.py`): Dimensional analysis system using prime number encoding
- **Unit System Layer** (`unit_system/`): Unit definitions, registry, and constants
- **Variable System Layer** (`variable_system/`): Base classes for quantities and typed variables  
- **Generated Layer** (`variables.py`, `units.py`): Auto-generated domain-specific classes
- **Expression Layer** (`expression.py`, `equation.py`): Mathematical expression and equation system

### Core Components

**Dimensional System (`dimension.py`)**

- `DimensionSignature`: Immutable dimension signatures using prime number encoding for ultra-fast dimensional compatibility checks
- `BaseDimension`: Enum of base dimensions (LENGTH, MASS, TIME, etc.) as prime numbers for efficient bit operations
- Enables zero-cost dimensional analysis at compile time

**Unit System (`unit_system/`)**

- `UnitDefinition` (`unit_system/core.py`): Immutable dataclass for unit definitions with SI conversion factors
- `UnitConstant` (`unit_system/core.py`): Type-safe unit constants that provide performance optimizations
- `HighPerformanceRegistry` (`unit_system/core.py`): Central registry with pre-computed conversion tables for fast unit conversions
- `SIPrefix` (`unit_system/prefixes.py`): Comprehensive SI prefix system for automatic unit generation

**Base Variables and Quantities (`variable_system/`)**

- `FastQuantity` (`variable_system/core.py`): High-performance quantity class optimized for engineering calculations
- `TypeSafeVariable` (`variable_system/core.py`): Base class for dimension-specific variables with generic type safety
- `TypeSafeSetter` (`variable_system/core.py`): Generic setter with dimensional validation and fluent API
- `ExpressionVariable` (`variable_system/expression_variable.py`): Extended variable class with mathematical operations
- Uses `__slots__` for memory efficiency and caches commonly used values  
- Implements fast arithmetic operations with dimensional checking
- **Variable Management Methods**: `update()`, `mark_known()`, `mark_unknown()` for flexible variable state management

**Specialized Variables (`variables.py`)**

- 100+ domain-specific variable types including `Length`, `Pressure`, `Temperature`, `Mass`, `Volume`, etc.
- All extend `ExpressionVariable` with mathematical operation capabilities and comparison methods
- Provides fluent API patterns for type-safe value setting with specialized setters
- **Comparison Methods**: `lt()`, `leq()`, `geq()`, `gt()` methods and Python operators (`<`, `<=`, `>`, `>=`) for conditional logic
- Auto-generated from comprehensive unit database with consistent patterns

**Unit Constants (`units.py`)**

- Type-safe unit constant classes: `LengthUnits`, `PressureUnits`, `DimensionlessUnits`
- Provides both full names and common aliases (e.g., `m`, `mm`, `Pa`, `kPa`)
- No string-based unit handling - all type-safe constants

**Mathematical Expression System (`expression.py`)**

- `Expression`: Abstract base class for mathematical expression trees
- `BinaryOperation`: Unified operation class handling arithmetic (`+`, `-`, `*`, `/`, `**`) and comparison (`<`, `<=`, `>`, `>=`, `==`, `!=`) operators
- `VariableReference`, `Constant`: Core expression implementations
- `UnaryFunction`, `ConditionalExpression`: Advanced expression types
- `wrap_operand()`: Duck-typing utility to convert various types to expressions
- Comprehensive mathematical function support (sin, cos, tan, sqrt, ln, exp, etc.)
- **Auto-evaluation**: Expressions automatically evaluate and display results when all variables have known values

**Equation System (`equation.py`)**

- `Equation`: Represents mathematical equations (lhs = rhs) with solving capabilities
- `EquationSystem`: System of equations that can be solved together
- Variables can participate in mathematical operations, returning expressions
- Supports equation solving and residual checking for engineering calculations
- **Auto-solving**: Equations automatically solve and display results when printed and only one unknown variable exists

### Key Architecture Patterns

**Clean Import Strategy**: The codebase uses several techniques to avoid circular imports:

- Strict dependency hierarchy: `dimension → unit_system → variable_system → variables → expression → equation`
- `TYPE_CHECKING` guards for type-only imports
- Duck typing with `hasattr()` checks to avoid importing classes
- Delayed imports where necessary
- Strategic use of `cast()` for type safety without runtime dependencies

**Public API Design**: The library exposes a focused public API for users:

```python
# Core variable types (100+ available)
from qnty import Length, Pressure, Temperature, Mass, Volume, Area, Force, etc.

# Engineering problem system
from qnty import Problem
from qnty.problem_system.checks import add_check
```

**Restricted User Access**: Users should ONLY access these public components:
- **All variables from `variables.py`**: Length, Pressure, Temperature, etc. (100+ engineering variable types)
- **Problem class from `problem.py`**: Main container for engineering problems with solving capabilities
- **`add_check` function from `qnty.problem_system.checks`**: Validation and compliance checking system
- **Expression methods**: Available through variables (e.g., `length * width`, `pressure.geq(limit)`)

All other classes, modules, and functions are internal implementation details and should not be used directly by users.

**Fluent API Design**: Variables use specialized setters that return the variable itself for method chaining:

```python
length_var = Length("beam_length")
length_var.set(100.0).millimeters  # Returns Length instance
```

**Mathematical Expression Building**: Variables support arithmetic and comparison operations that return expressions:

```python
# Variables can be combined in mathematical expressions
T = Length("Wall Thickness", is_known=False)
T_bar = Length(0.147, "inches", "Nominal Wall Thickness")
U_m = Dimensionless(0.125, "Mill Undertolerance")

# Create equation: T = T_bar * (1 - U_m)
equation = T.equals(T_bar * (1 - U_m))

# Auto-solving: equations solve automatically when printed
print(equation)  # Automatically solves for T and displays result

# Comparison expressions for conditional logic
constraint = T.geq(minimum_thickness)  # T >= minimum_thickness
print(constraint)  # Automatically evaluates when variables are known
```

**Auto-Evaluation System**: The library includes sophisticated auto-evaluation capabilities:

```python
# Expressions auto-evaluate when all variables have known values
length = Length(10, "mm", "beam_length") 
width = Length(5, "mm", "beam_width")
area_expr = length * width
print(area_expr)  # Displays: 50.0 mm²

# Equations auto-solve when exactly one variable is unknown
thickness = Length("t", is_known=False)
equation = thickness.equals(area_expr / width)
print(equation)  # Automatically solves and displays: t = 10.0 mm
```

**Variable Management**: The system provides flexible variable state management:

```python
# Update variable properties flexibly  
pressure = Pressure("p")
pressure.update(value=100, unit="Pa")  # Set value with unit
pressure.update(is_known=False)        # Mark as unknown
pressure.update(quantity=other_var.quantity)  # Copy quantity

# Mark variables as known/unknown
pressure.mark_known()     # Mark as known
pressure.mark_unknown()   # Mark as unknown
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

### Code Generation System

The project uses a sophisticated code generation pipeline located in `scripts/`:

- **`_1_generate_dimensions.py`**: Generates `dimension.py` with dimensional constants from parsed unit data
- **`_2_generate_units.py`**: Generates `units.py` with comprehensive unit class definitions  
- **`_3_generate_variables.py`**: Generates `variables.py` with type-safe variable classes
- **`_4_generate_variable_pyi.py`**: Generates type stubs for better IDE support
- **`_5_generate_package_init.py`**: Generates package initialization files
- **`generate_all.py`**: Orchestrates the entire generation pipeline

**Key Generation Features:**
- Uses `scripts/input/unit_data.json` as the single source of truth for 800+ engineering units
- Automatically generates prefixed units (milli-, kilo-, etc.) for applicable base units
- Maintains dimensional consistency across all generated code
- Supports both manual edits and regeneration without conflicts

**Running Generation Scripts:**
```bash
python scripts/_1_generate_dimensions.py  # Update dimensions
python scripts/_2_generate_units.py       # Update units  
python scripts/_3_generate_variables.py   # Update variables
python scripts/generate_all.py            # Regenerate everything
```

### Critical Type System Updates

Recent architectural improvements include enhanced dimensional signature handling:

- **Mixed Type Signatures**: Dimensional signatures now support `int | float` types for precision in operations like `(Length * Pressure) / Length`
- **True Division Fix**: Dimensional division now uses `/` instead of `//` to prevent precision loss in compound unit operations
- **Registry Compatibility**: Updated `HighPerformanceRegistry` to handle mixed-type dimensional signatures

### Key Dependencies

- `numpy>=2.3.2`: Numerical computations  
- `pytest>=8.4.1`: Testing framework (dev dependency)
- `ruff>=0.1.0`: Code formatting and linting (dev dependency)
- `Pint>=0.24.4`: Comparison/benchmarking against established unit library (benchmark dependency)

### Reference Data

- `data/`: Contains comprehensive unit definition reference data for validation and testing
- `scripts/input/unit_data.json`: Single source of truth for all unit definitions
- `scripts/output/`: Generated mapping files for code generation pipeline

## Testing and Benchmarking

The project includes comprehensive test coverage with **234 tests** across 6 test files:

- **Dimension tests**: `test_dimension.py` - Dimensional analysis and signature operations
- **Equation tests**: `test_equations.py` - Mathematical equations, expressions, and auto-solving
- **Setter tests**: `test_setters.py` - Fluent API and type safety for variable setters
- **Prefix tests**: `test_prefixes.py` - SI prefix system and unit generation
- **Type hinting tests**: `test_type_hinting.py` - Type safety and generic type validation
- **Benchmarks**: `test_benchmark.py` - Performance comparisons against Pint library

### Important Testing Notes

- Always add `assert variable.quantity is not None` before accessing `.value`, `.unit`, `.dimension`, or `._dimension_sig` attributes
- Use parametrized tests extensively for comprehensive coverage
- Follow existing test patterns for consistency
- Tests demonstrate significant performance advantages (18-25x faster than Pint)

## Development Guidelines

### Import Strategy

**User-facing imports** (what users should use):

```python
# All variable types
from qnty import Length, Pressure, Temperature, Mass, Volume, Area, Force
# ... and 90+ other variable types

# Engineering problem system
from qnty import Problem
from qnty.problem_system.checks import add_check
```

**Internal development** (for library development only):

```python
# Internal systems - users should NOT import these
from .variable_system.core import FastQuantity, TypeSafeVariable, TypeSafeSetter
from .unit_system.core import UnitDefinition, UnitConstant, registry
from .expression_system.expression import Expression, wrap_operand
from .equation_system.equation import Equation
```

**User API Boundaries**: The public API is intentionally minimal to ensure users only need to learn and use the essential components. All other modules contain implementation details that should remain hidden from users.

### Type Safety Best Practices

- Always check `variable.quantity is not None` before accessing quantity attributes
- Use `cast()` with duck typing for type safety without circular imports
- Prefer `TYPE_CHECKING` guards for type-only imports
- Follow the established dependency hierarchy when adding new modules

### Performance Considerations

- The library achieves 18-25x performance improvements over established libraries
- Maintain `__slots__` usage for memory efficiency
- Cache frequently accessed values (SI factors, dimension signatures)
- Use pre-computed lookup tables where possible
- Optimize for the common case (same-unit operations, compatible dimensions)

### Critical Development Patterns

**Variable Symbol Management**: Variables need proper symbol assignment for equation solving:
```python
# Correct: Set symbols explicitly for equation system
t = Length(0.0, "inch", "Pressure Design Thickness", is_known=False)
t.symbol = "t"  # Required for equation.solve_for("t", variables)
```

**Dimensional Signature Precision**: When working with dimensional operations, ensure proper division handling:
- Always use `/` (true division) for dimensional signatures, never `//` (floor division)
- Mixed `int | float` dimensional signatures are supported for precision in compound operations

**Expression String Representation**: The `BinaryOperation.__str__()` method handles operator precedence carefully:
- Right-associative operations need parentheses when precedence is equal and operator is left-associative (`-`, `/`)
- This ensures expressions like `(P * D) / (2 * (S * E * W + P * Y))` maintain mathematical correctness

**Unit Registry Type Safety**: When modifying the registry system:
- `_dimension_cache` and `dimensional_groups` must support `dict[int | float, ...]` types
- This accommodates the mixed-type dimensional signatures from precision fixes

**Auto-Evaluation System**: The expression and equation systems use Python's `inspect` module for automatic evaluation:
- Expressions auto-evaluate when all referenced variables are available in the calling scope
- Equations auto-solve when exactly one unknown variable exists
- This eliminates the need for manual variable dictionary creation in most cases

**Comparison Operations**: All comparison operators are handled by `BinaryOperation` instead of a separate class:
- Comparisons return dimensionless quantities (1.0 for True, 0.0 for False)  
- Unit conversion is automatic for same-dimension comparisons
- Both method calls (`var.lt(other)`) and operators (`var < other`) are supported

**Variable State Management**: New methods enable flexible variable property updates:
- `update(value=..., unit=..., quantity=..., is_known=...)` for flexible updates
- `mark_known()` and `mark_unknown()` for state changes
- All methods support method chaining and return the variable instance

## important-instruction-reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.