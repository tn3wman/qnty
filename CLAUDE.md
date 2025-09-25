# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Qnty** is a high-performance unit system library for Python designed for engineering calculations. It provides dimensional safety, fast unit conversions, and equation solving capabilities. The library uses prime number encoding for ultra-fast performance (18.9x faster than Pint) and targets Python 3.11+.

## Development Commands

```bash
# Testing
pytest                          # Run all tests
pytest tests/test_benchmark.py  # Performance benchmarks against other libraries
pytest -k "test_name"           # Run specific test

# Code quality
ruff check src/ tests/          # Linting
ruff format src/ tests/         # Code formatting

# Code generation (critical - regenerates catalogs)
python codegen/cli.py          # Regenerate dimension_catalog.py, unit_catalog.py, quantity_catalog.py
```

**Important**: Never edit `*_catalog.py` files directly - they are auto-generated from `codegen/generators/`.

## Architecture Overview

### Strict Import Hierarchy
The codebase follows a strict dependency hierarchy to prevent circular imports:
```
dimension → unit → quantity → quantity_meta → catalogs
```

### Core Modules
- **`core/dimension.py`**: Prime number encoding for dimensional analysis using `PRIMES = (2, 3, 5, 7, 11, 13, 17)` for L,M,T,A,Θ,N,J
- **`core/unit.py`**: Unit registry with pre-computed conversion tables via `si_factor`
- **`core/quantity.py`**: Unified quantity class handling both concrete values and symbolic placeholders
- **`core/quantity_meta.py`**: Metaclass system generating fluent APIs like `length.set(5).meter`

### Expression System
- **`algebra/`**: Mathematical expression trees for equation solving
- **`problems/`**: Engineering problem framework with automatic equation reconstruction
- **`solving/`**: Multi-algorithm equation solving system

### Performance Architecture
- Prime number dimensional encoding for O(1) compatibility checks
- Pre-computed conversion tables stored as `si_factor` attributes
- `__slots__` throughout for memory efficiency
- Cached dimension signatures and SI factors

## Key Design Patterns

### Metaclass-Based Quantity Generation
```python
@quantity(uc.LengthUnits)
class Length:
    """Auto-generates fluent API: length.set(5).meter, length.to_unit.inches"""
    pass
```

### Unified Quantity System
The `Quantity` class handles both:
- Concrete values: `Length(5, "meter")`
- Named placeholders: `Length("x", is_known=False)` for equation solving

### Problem-Oriented Engineering
```python
class PipeThickness(Problem):
    pressure = Pressure(150, "psi", "Internal Pressure")
    thickness = Length("thickness", is_known=False)  # Unknown to solve
    equation = thickness.equals((pressure * diameter) / (2 * allowable_stress))
```

## Testing Strategy

- **187 comprehensive tests** with performance benchmarks
- Table-driven tests using `pytest.mark.parametrize`
- Hard-coded oracle values (never computed expectations)
- Performance tracking in `tests/.perf/` directory
- Real engineering problems in `test_engineering_problems.py`

## Code Generation System

Three critical files are auto-generated and should NEVER be edited directly:
1. **`dimension_catalog.py`** - Pre-defined dimensional constants
2. **`unit_catalog.py`** - Unit definitions with SI conversion factors
3. **`quantity_catalog.py`** - Quantity classes with decorators

Always run `python codegen/cli.py` after modifying generators.

## Extensions Architecture

- **`extensions/reporting/`**: PDF generation with LaTeX rendering (implemented)
- **`extensions/plotting/`**: Visualization capabilities (placeholder)
- **`extensions/integration/`**: External tool integration (placeholder)

## Development Notes

- Line length limit: 200 characters
- Python 3.11+ required
- Uses Poetry for build system
- Runtime dependency: numpy>=2.3.2
- Beta status - include disclaimers for production use
- Always validate critical calculations independently

## Performance Considerations

When working with this codebase:
- Leverage pre-computed `si_factor` for conversions
- Use prime number encoding for dimensional compatibility
- Maintain zero-cost abstractions for common operations
- Consider memory efficiency with `__slots__` for new classes