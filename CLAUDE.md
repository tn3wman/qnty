# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest

# Run specific test files
pytest tests/test_dimension.py -v
pytest tests/test_unit.py -v
pytest tests/test_quantity.py -v

# Run single test
pytest tests/test_dimension.py::test_dimension_multiplication -v

# Run benchmarks
python tests/test_benchmark.py

# Lint and format code
ruff check src/ tests/
ruff format src/ tests/
```

### Testing Guidelines
- Follow strict test authoring rules in `tests/CLAUDE.md`
- Use hard-coded expected values (never compute from function under test)
- Use `pytest.mark.parametrize` for table-driven tests
- Include boundary cases and error conditions
- Use `pytest.approx` for floating-point comparisons with tight tolerances

## Architecture Overview

Qnty is a high-performance unit system library for Python with dimensional safety. The architecture follows a strict dependency hierarchy to prevent circular imports:

```
dimension → unit → quantity → quantity_meta → catalogs → algebra → problems → solving
```

### Core Module Structure (`src/qnty/core/`)
- **`dimension.py`**: Prime number encoding for dimensional analysis using base dimensions (L,M,T,A,Θ,N,J)
- **`unit.py`**: Unit registry with pre-computed conversion tables and SI prefix system
- **`quantity.py`**: Unified Quantity class combining concrete values and named placeholders
- **`quantity_meta.py`**: Metaclass system for automatic quantity class generation via `@quantity` decorator
- **Generated Catalogs**: `dimension_catalog.py`, `unit_catalog.py`, `quantity_catalog.py` (auto-generated - do not edit)

### Key Components
- **Algebra System** (`src/qnty/algebra/`): Expression trees, equations, mathematical functions
- **Problem System** (`src/qnty/problems/`): Engineering problem class with equation solving
- **Solving System** (`src/qnty/solving/`): Iterative and simultaneous equation solvers

### Performance Features
- Prime number encoding for O(1) dimensional compatibility checks
- Pre-computed conversion tables via `si_factor`
- `__slots__` used throughout for memory efficiency
- Cached dimension signatures and SI factors
- 18.9x average speedup over Pint library

## Development Patterns

### Import Guidelines
- Use `TYPE_CHECKING` guards for type-only imports to avoid circular dependencies
- Follow strict dependency hierarchy (never import from higher-level modules)
- Import order: `dimension → unit → quantity → quantity_meta → catalogs`

### Code Generation
Three files are auto-generated from `codegen/generators/`:
- `src/qnty/core/dimension_catalog.py`
- `src/qnty/core/unit_catalog.py`
- `src/qnty/core/quantity_catalog.py`

To modify these files, update generators and run:
```bash
python codegen/cli.py
```

### Quantity Creation Pattern
```python
from qnty.core.unit_catalog import LengthUnits
from qnty.core.quantity_meta import quantity

@quantity(LengthUnits)
class Length:
    """Length quantity with automatic boilerplate."""
    pass
```

### Problem Definition Pattern
```python
from qnty import Problem, Length, Pressure

class PipeThickness(Problem):
    # Known parameters
    pressure = Pressure(150, "psi", "Internal Pressure")
    diameter = Length(6, "inch", "Pipe Diameter")

    # Unknown to solve for
    thickness = Length("thickness", is_known=False)

    # Engineering equation
    equation = thickness.equals((pressure * diameter) / (2 * allowable_stress))
```

## Project Structure
- **`src/qnty/`**: Main package
  - `core/`: Foundation (dimensions, units, quantities)
  - `algebra/`: Mathematical expressions and equations
  - `problems/`: Engineering problem framework
  - `solving/`: Equation solving algorithms
  - `utils/`: Utilities and helpers
- **`tests/`**: Comprehensive test suite (187 tests)
- **`examples/`**: Real-world engineering examples
- **`docs/`**: Documentation files

## Key Files to Understand
- **Core Architecture**: `src/qnty/core/CLAUDE.md` (detailed core module documentation)
- **Test Rules**: `tests/CLAUDE.md` (strict test authoring guidelines)
- **Public API**: `src/qnty/__init__.py` (main exports)
- **Performance**: `tests/test_benchmark.py` (performance comparisons)