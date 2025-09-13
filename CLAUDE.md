# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qnty is a high-performance unit system library for Python that provides dimensional safety and fast unit conversions for engineering calculations. The library achieves 18-25x performance improvements over established libraries like Pint through pre-computed conversion tables and optimized dimensional analysis.

**Key Features:**
- Type-safe quantities with dimensional analysis at compile time
- 100+ engineering variable types (Length, Pressure, Temperature, Mass, Volume, etc.)
- Automatic equation solving with the Problem class
- Mathematical expression building with operator overloading
- Fast unit conversions using pre-computed tables

## Common Development Commands

### Testing
```bash
pytest                    # Run all tests
pytest tests/test_dimension.py -v    # Run specific test file
pytest tests/test_dimension.py::TestDimensionSignatureCreation::test_basic_dimension_creation -v  # Run single test
python tests/test_benchmark.py       # Run performance benchmarks
```

### Code Quality
```bash
ruff check src/ tests/    # Lint code (line length: 200)
ruff format src/ tests/   # Format code
mypy src/qnty/           # Type checking (if installed)
```

### Release Process
```bash
python release.py         # Interactive release (patch/minor/major)
python release.py --patch # Increment patch version
python release.py --minor # Increment minor version
python release.py --major # Increment major version
```

The release script automatically:
1. Increments version using Poetry
2. Commits version bump to main branch
3. Creates git tag with version
4. Pushes commit and tag to origin

## High-Level Architecture

The library follows a strict dependency hierarchy to prevent circular imports:

```
core/dimension → core/unit → core/quantity → algebra/expressions → algebra/equations → problems → solving
```

### Core Components

- **core/dimension.py**: Dimensional analysis with prime number encoding for fast compatibility checks
- **core/unit.py**: Unit registry with pre-computed conversion tables and SI prefix system
- **core/quantity.py**: Field-based quantity system (FieldQuantity base class) with 100+ variable types
- **algebra/expressions/**: Mathematical expression trees with auto-evaluation capabilities
- **algebra/equations/**: Equation representation and auto-solving when printed
- **problems/**: Engineering problem container with automatic equation solving
- **solving/**: Solution algorithms and dependency management

### Key Implementation Details

**Quantity System**: The library uses a field-based architecture where all variable types (Length, Pressure, etc.) extend FieldQuantity. Each variable supports:
- Fluent setter API: `length.set(100).millimeters`
- Unit conversion: `length.to_unit.inches` or `length.as_unit.inches`
- Mathematical operations that return expressions
- Auto-evaluation when all variables are known

**Expression System**: Uses BinaryOperation class for all arithmetic and comparison operators. Expressions auto-evaluate when printed if all referenced variables have values.

**Performance**: Achieves speed through:
- Pre-computed conversion tables
- Prime number encoding for dimensions
- `__slots__` for memory efficiency
- Cached SI factors and dimension signatures

## Code Generation System

The library uses code generation for many core files. Files are generated from `codegen/generators/`:

### Generated Files (DO NOT EDIT DIRECTLY)
- `src/qnty/core/dimension_catalog.py` - Dimensional constants
- `src/qnty/core/unit_catalog.py` - Unit definitions and namespace classes
- `src/qnty/core/quantity_catalog.py` - Quantity classes

### Regeneration Commands
```bash
python codegen/cli.py  # Regenerate all files
```

**Important**: If you need to modify behavior in generated files, update the generator scripts in `codegen/generators/`, not the generated files themselves.

## Key Development Patterns

### Recent Refactor Notice
The library underwent a major restructuring moving from separate dimensions/units/quantities modules to a unified core module. The algebra system (expressions, equations) was also reorganized. There may be import paths or references that need updating.

### Type Safety
- Always check `variable.quantity is not None` before accessing quantity attributes
- Use `TYPE_CHECKING` guards for type-only imports to avoid circular dependencies

### Performance Optimizations
- Prime number encoding for dimensional analysis
- Pre-computed conversion tables
- `__slots__` for memory efficiency
- Cached SI factors and dimension signatures

### Problem Solving
Variables need symbol assignment for equation solving:
```python
t = Length("Pressure Design Thickness", is_known=False)
t.symbol = "t"  # Required for equation.solve_for("t", variables)
```
- My tests are currently useless until I finish a major refactor.
- You really seem to like them but try to avoid type checking imports.