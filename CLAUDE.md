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
pytest tests/test_dimension.py -v  # Run specific test module with verbose output

# Code quality
ruff check src/ tests/          # Linting
ruff format src/ tests/         # Code formatting

# Code generation (critical - regenerates catalog stubs)
python3 codegen/generators/generate_dimension_stubs.py
python3 codegen/generators/generate_unit_stubs.py
python3 codegen/generators/generate_quantity_stubs.py
```

**Important**: The `*_catalog.py` files in `src/qnty/core/` are hand-written and define the actual units, dimensions, and quantities. The generators create corresponding `.pyi` stub files for type checking. Never edit `.pyi` files directly.

## Architecture Overview

### Strict Import Hierarchy
The codebase follows a strict dependency hierarchy to prevent circular imports:
```
dimension → unit → quantity → quantity_meta → catalogs
```
This hierarchy MUST be respected when adding new functionality.

### Core Modules (`src/qnty/core/`)
- **`dimension.py`**: Prime number encoding for dimensional analysis using `PRIMES = (2, 3, 5, 7, 11, 13, 17)` for L,M,T,A,Θ,N,J (7 base dimensions)
- **`unit.py`**: Unit registry with pre-computed conversion tables via `si_factor` for O(1) conversions
- **`quantity.py`**: Unified quantity class handling both concrete values (`Length(5, "meter")`) and symbolic placeholders (`Length("x", is_known=False)` for equation solving)
- **`quantity_meta.py`**: Metaclass system that generates fluent APIs like `length.set(5).meter` and `length.to_unit.inches`
- **`dimension_catalog.py`**, **`unit_catalog.py`**, **`quantity_catalog.py`**: Hand-written catalogs that define all available dimensions, units, and quantity types

### Expression System (`src/qnty/algebra/`)
- **`nodes.py`**: Mathematical expression tree nodes (BinaryOperation, UnaryOperation, etc.)
- **`equation.py`**: Equation and EquationSystem classes for representing engineering equations
- **`functions.py`**: Mathematical functions (sqrt, sin, cos, etc.) that preserve dimensional correctness
- **`formatter.py`**: Pretty-printing of expressions and equations

### Problem Framework (`src/qnty/problems/`)
- **`problem.py`**: Main Problem base class for engineering problems with automatic equation reconstruction
- **`solving.py`**: EquationReconstructor that builds equation systems from Problem class attributes
- **`composition.py`**: Support for composing sub-problems into larger systems
- **`validation.py`**: Validation logic for problem constraints and solutions
- **`vector_equilibrium.py`**: Specialized solver for statics problems with force equilibrium

### Solving System (`src/qnty/solving/`)
- **`manager.py`**: SolverManager coordinates between different solving strategies
- **`order.py`**: Topological sort and dependency graph analysis for solving order
- **`solvers/base.py`**: BaseSolver interface and SolveResult dataclass
- **`solvers/simultaneous.py`**: SimultaneousEquationSolver using SymPy for symbolic solving
- **`solvers/iterative.py`**: IterativeSolver for numerical solutions when symbolic fails
- **`component_solver.py`**: ComponentSolver for vector component method in statics
- **`triangle_solver.py`**: TriangleSolver for triangle method in statics

### Spatial System (`src/qnty/spatial/`)
- **`vector.py`**: Vector class for 2D/3D engineering vectors with magnitude and direction
- **`force_vector.py`**: ForceVector specialization with point of application and equilibrium support
- **`point.py`**: Point class for coordinate geometry
- **`coordinate_system.py`**: Coordinate system definitions and transformations
- **`angle_reference.py`**: Angle reference systems for vector directions

### Extensions (`src/qnty/extensions/`)
- **`reporting/`**: PDF generation with LaTeX rendering (implemented)
- **`plotting/`**: Visualization capabilities (placeholder)
- **`integration/`**: External tool integration (placeholder)

### Code Generation (`codegen/generators/`)
Three scripts generate `.pyi` stub files for type checking:
1. **`generate_dimension_stubs.py`** → `dimension_catalog.pyi`
2. **`generate_unit_stubs.py`** → `unit_catalog.pyi`
3. **`generate_quantity_stubs.py`** → `quantity_catalog.pyi`

Run these after modifying the corresponding catalog files to update type hints.

## Key Design Patterns

### Prime Number Dimensional Encoding
Each base dimension (Length, Mass, Time, Current, Temperature, Amount, Luminous Intensity) is assigned a prime number (2, 3, 5, 7, 11, 13, 17). Dimensional signatures are computed by multiplying these primes raised to their exponents:
```python
# Force = Mass * Length / Time^2 = M^1 * L^1 * T^-2
# Signature = 3^1 * 2^1 * 5^-2 (using PRIMES indexing)
```
This allows O(1) dimensional compatibility checking and prevents the need for tuple comparisons.

### Metaclass-Based Quantity Generation
The `QuantityMeta` metaclass automatically generates fluent APIs for each quantity type:
```python
# In quantity_catalog.py (hand-written):
class Length(Quantity, metaclass=QuantityMeta):
    UNIT_NS = LengthUnits

# Generates fluent API:
x = Length("distance").set(5).meter  # Concrete value
y = Length("unknown", is_known=False)  # Symbolic placeholder
```

### Unified Quantity System
The single `Quantity` class handles both:
- **Concrete values**: `Length(5, "meter")` for actual measurements
- **Named placeholders**: `Length("x", is_known=False)` for unknowns in equation solving

This unification allows seamless mixing of concrete and symbolic quantities in engineering problems.

### Problem-Oriented Engineering
Engineering problems inherit from `Problem` and use class-level attributes:
```python
class PipeThickness(Problem):
    pressure = Pressure(150, "psi", "Internal Pressure")  # Known
    thickness = Length("thickness", is_known=False)  # Unknown to solve
    equation = thickness.equals((pressure * diameter) / (2 * allowable_stress))
```
The `Problem` class automatically:
1. Discovers all quantities and equations defined as class attributes
2. Builds a dependency graph
3. Determines topological solving order
4. Solves symbolically (SymPy) or numerically (iterative)
5. Validates results

## Testing Strategy

- **~4,800 lines of tests** across 19 test modules
- Table-driven tests using `pytest.mark.parametrize` for comprehensive coverage
- Hard-coded oracle values (never computed expectations) to prevent circular validation
- Performance tracking in `tests/test_benchmark.py` comparing against Pint
- Real engineering problems in:
  - `tests/test_engineering_problems.py` - General engineering
  - `tests/asme/` - ASME code calculations
  - `tests/statics/` - Statics problems (component method, triangle method)
  - `tests/spatial/` - Spatial vector and geometry tests

## Performance Architecture

### Pre-Computed Conversion Tables
All units store their `si_factor` (conversion factor to SI base units) at definition time:
```python
meter = Unit("meter", "m", length_dim, si_factor=1.0)
inch = Unit("inch", "in", length_dim, si_factor=0.0254)
```
Conversions use simple multiplication: `value_in_unit_b = value_in_unit_a * (unit_a.si_factor / unit_b.si_factor)`

### Memory Efficiency
- `__slots__` used throughout core classes (Dimension, Unit, Quantity) to minimize memory overhead
- Cached dimension signatures and SI factors
- LRU caches on hot paths (e.g., unit name normalization)

### Zero-Cost Abstractions
The fluent API and metaclass magic compile down to simple attribute access and method calls with no runtime overhead beyond standard Python.

## Development Notes

- **Line length limit**: 200 characters (enforced by ruff)
- **Python version**: 3.11+ required (uses match statements, modern type hints)
- **Build system**: Poetry
- **Runtime dependency**: numpy>=2.3.2
- **Beta status**: Include disclaimers for production use; always validate critical calculations independently
- **Linting exceptions**: F403/F405 allowed for star imports in auto-generated `__init__.py` files

## Common Development Patterns

### Adding a New Quantity Type
1. Add to `src/qnty/core/quantity_catalog.py`:
   ```python
   class MyNewQuantity(Quantity, metaclass=QuantityMeta):
       UNIT_NS = MyNewQuantityUnits
   ```
2. Define units in `src/qnty/core/unit_catalog.py`:
   ```python
   class MyNewQuantityUnits(UnitNamespace):
       my_unit = Unit("my_unit", "mu", my_dim, si_factor=1.0)
   ```
3. Regenerate stubs: `python3 codegen/generators/generate_quantity_stubs.py` and `python3 codegen/generators/generate_unit_stubs.py`
4. Add comprehensive tests

### Adding a New Solver Strategy
1. Create solver in `src/qnty/solving/solvers/my_solver.py`
2. Inherit from `BaseSolver` and implement `solve()` returning `SolveResult`
3. Register in `SolverManager` (in `src/qnty/solving/manager.py`)
4. Add tests in `tests/test_simple_problem.py` or similar

### Working with Vector Problems
For statics problems involving forces and moments:
1. Use `ForceVector` from `qnty.spatial` for forces with magnitude, direction, and point of application
2. Inherit from `VectorEquilibriumProblem` for automatic equilibrium equation generation
3. Use `ComponentSolver` or `TriangleSolver` for specialized solving strategies
4. See `tests/statics/test_component_method.py` for examples

## Type Checking and IDE Support

The `.pyi` stub files provide IDE autocomplete and type checking for dynamically generated APIs. If your IDE doesn't recognize a unit or quantity:
1. Check if it exists in the corresponding `*_catalog.py` file
2. Regenerate stubs using the appropriate generator script
3. Restart your IDE's language server
