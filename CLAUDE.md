# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qnty (formerly OptiUnit) is a high-performance unit system library for Python that provides dimensional safety and fast unit conversions for engineering calculations. The library is designed around type safety and performance optimization using compile-time dimensional analysis.

### User-Focused API

The qnty library provides a simple, focused API for users:

1. **100+ Variable Types** (from `variables.py`): Length, Pressure, Temperature, Mass, Volume, Area, Force, etc.
2. **Problem Class** (from `problem/`): Engineering problem container with automatic equation solving
3. **Validation System** (`validate` from `validation.py`): Code compliance and engineering checks
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
generated/dimensions → units → quantities → generated → expressions → equations → problem
```

This ensures clean dependencies and enables proper type checking throughout the system.

### Simplified Variable Architecture

The system uses a clean 2-level hierarchy with mixin-based composition:

```
UnifiedVariable (Base with mixins)
└── Domain Variables (Length, Pressure, etc.) - 100+ classes

Mixins:
├── QuantityManagementMixin
├── FlexibleConstructorMixin  
├── UnifiedArithmeticMixin
├── ExpressionMixin
├── SetterCompatibilityMixin
└── ErrorHandlerMixin
```

### Modular Architecture

The system uses a layered approach with separate concerns:

- **Core Layer** (`generated/dimensions.py`): Dimensional analysis system using prime number encoding
- **Quantities Layer** (`quantities/`): Unified variable system with mixin composition
- **Units Layer** (`units/`): Unit definitions, registry, and constants
- **Generated Layer** (`generated/`): Auto-generated domain-specific variable classes
- **Expression Layer** (`expressions/`): Mathematical expression system with nodes and functions
- **Equation Layer** (`equations/`): Equation handling and system solving
- **Problem Solving Layer** (`problem/`): Modular problem system with focused components
- **Code Generation** (`codegen/`): Automated code generation system for all generated files

### Core Components

**Dimensional System (`generated/dimensions.py`)**

- `DimensionSignature`: Immutable dimension signatures using prime number encoding for ultra-fast dimensional compatibility checks
- `BaseDimension`: Enum of base dimensions (LENGTH, MASS, TIME, etc.) as prime numbers for efficient bit operations
- Enables zero-cost dimensional analysis at compile time

**Units System (`units/`)**

- `UnitDefinition` (`units/registry.py`): Immutable dataclass for unit definitions with SI conversion factors
- `UnitConstant` (`units/registry.py`): Type-safe unit constants that provide performance optimizations
- `registry` (`units/registry.py`): Central registry with pre-computed conversion tables for fast unit conversions
- Comprehensive SI prefix system for automatic unit generation

**Unified Variable System (`quantities/`)**

- `Quantity` (`quantities/quantity.py`): High-performance quantity class optimized for engineering calculations
- `UnifiedVariable` (`quantities/unified_variable.py`): Unified base class combining all variable capabilities through focused mixins
- Uses mixin composition for clean separation of concerns and reduced inheritance complexity
- **Variable Management Methods**: `update()`, `mark_known()`, `mark_unknown()` for flexible variable state management
- **Arithmetic Mode Control**: `set_arithmetic_mode('quantity'|'expression'|'auto')` for user-controlled return types

**Generated Variables and Units (`generated/`)**

- `quantities.py`: 100+ domain-specific variable types including `Length`, `Pressure`, `Temperature`, `Mass`, `Volume`, etc.
- All extend `UnifiedVariable` with complete mathematical operation and expression capabilities
- Provides fluent API patterns for type-safe value setting with specialized setters
- **Arithmetic Mode Support**: Each variable supports quantity, expression, and auto arithmetic modes
- **Comparison Methods**: `lt()`, `leq()`, `geq()`, `gt()` methods and Python operators (`<`, `<=`, `>`, `>=`) for conditional logic
- Auto-generated from comprehensive unit database with consistent patterns

**Unit Constants (`generated/units.py`)**

- Type-safe unit constant classes: `LengthUnits`, `PressureUnits`, `DimensionlessUnits`
- Provides both full names and common aliases (e.g., `m`, `mm`, `Pa`, `kPa`)
- No string-based unit handling - all type-safe constants

**Mathematical Expression System (`expressions/`)**

- `Expression`: Abstract base class for mathematical expression trees
- `BinaryOperation`: Unified operation class handling arithmetic (`+`, `-`, `*`, `/`, `**`) and comparison (`<`, `<=`, `>`, `>=`, `==`, `!=`) operators
- `VariableReference`, `Constant`: Core expression implementations
- `UnaryFunction`, `ConditionalExpression`: Advanced expression types
- `wrap_operand()`: Duck-typing utility to convert various types to expressions
- Comprehensive mathematical function support (sin, cos, tan, sqrt, ln, exp, etc.)
- **Auto-evaluation**: Expressions automatically evaluate and display results when all variables have known values

**Equation System (`equations/`)**

- `Equation`: Represents mathematical equations (lhs = rhs) with solving capabilities
- `EquationSystem`: System of equations that can be solved together
- Variables can participate in mathematical operations, returning expressions
- Supports equation solving and residual checking for engineering calculations
- **Auto-solving**: Equations automatically solve and display results when printed and only one unknown variable exists

**Problem System Architecture (`problem/`)**

The Problem system has been decomposed into focused modules using multiple inheritance:

- **`base.py`**: Core Problem state, initialization, caching, and utility methods
- **`variables.py`**: Variable lifecycle management, adding/getting variables, known/unknown state
- **`equations.py`**: Equation processing pipeline, validation, missing variable handling
- **`solving.py`**: High-level solve orchestration, dependency graphs, solution verification
- **`validation.py`**: Problem-validation integration and check management
- **`composition_mixin.py`**: Sub-problem composition, namespacing, and composite equation creation
- **`composition.py`**: Additional composition utilities and helpers
- **`reconstruction.py`**: Equation reconstruction and variable reference management
- **`metaclass.py`**: Problem metaclass for class-level variable and equation processing
- **`__init__.py`**: Reassembled Problem class using multiple inheritance with `ProblemMeta` metaclass

The Problem class combines all mixins: `Problem(ProblemBase, VariablesMixin, EquationsMixin, SolvingMixin, ValidationMixin, CompositionMixin, metaclass=ProblemMeta)`

### Key Architecture Patterns

**Clean Import Strategy**: The codebase uses several techniques to avoid circular imports:

- Strict dependency hierarchy: `generated/dimensions → units → quantities → generated → expressions → equations → problem`
- `TYPE_CHECKING` guards for type-only imports
- Duck typing with `hasattr()` and `getattr()` checks to avoid importing classes
- Delayed imports where necessary
- Strategic use of try/except blocks for safe attribute access

**Public API Design**: The library exposes a focused public API for users:

```python
# Core variable types (100+ available)
from qnty import Length, Pressure, Temperature, Mass, Volume, Area, Force, etc.

# Engineering problem system
from qnty import Problem
from qnty.validation import validate
```

**Restricted User Access**: Users should ONLY access these public components:

- **All variables from `generated/quantities.py`**: Length, Pressure, Temperature, etc. (100+ engineering variable types)
- **Problem class from `problem/`**: Main container for engineering problems with solving capabilities
- **`validate` function from `validation.py`**: Validation and compliance checking system
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

The project uses a sophisticated code generation pipeline located in `src/qnty/codegen/`:

- **`dimensions_gen.py`**: Generates `dimensions.py` with dimensional constants from parsed unit data
- **`units_gen.py`**: Generates `units.py` with comprehensive unit class definitions  
- **`quantities_gen.py`**: Generates `quantities.py` with type-safe variable classes
- **`setters_gen.py`**: Generates setter classes with unit properties
- **`stubs_gen.py`**: Generates type stubs for better IDE support
- **`cli.py`**: Command-line interface that orchestrates the entire generation pipeline

**Key Generation Features:**

- Uses `codegen/generators/data/unit_data.json` as the single source of truth for 800+ engineering units
- Automatically generates prefixed units (milli-, kilo-, etc.) for applicable base units
- Maintains dimensional consistency across all generated code
- Supports both manual edits and regeneration without conflicts

**Running Generation Scripts:**

```bash
python -m qnty.codegen.cli                # Generate everything
python -m qnty.codegen.generators.dimensions_gen  # Update dimensions only
python -m qnty.codegen.generators.units_gen       # Update units only
python -m qnty.codegen.generators.quantities_gen  # Update quantities only
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

- `codegen/generators/data/`: Contains comprehensive unit definition reference data for validation and testing
- `codegen/generators/data/unit_data.json`: Single source of truth for all unit definitions
- `codegen/generators/out/`: Generated mapping files for code generation pipeline

## Testing and Benchmarking

The project includes comprehensive test coverage with **187 tests** across 6 test files:

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
from .quantities.quantity import Quantity
from .quantities.typed_quantity import TypedQuantity
from .units.registry import UnitDefinition, UnitConstant, registry
from .expressions.nodes import Expression, wrap_operand
from .equations.equation import Equation
from .problem.solving import SolverManager
```

**User API Boundaries**: The public API is intentionally minimal to ensure users only need to learn and use the essential components. All other modules contain implementation details that should remain hidden from users.

### Type Safety Best Practices

- Always check `variable.quantity is not None` before accessing quantity attributes
- Use `getattr(obj, 'attr', default)` for safe attribute access on dynamic objects
- Use try/except blocks with `setattr()` for safe dynamic attribute assignment
- Prefer `TYPE_CHECKING` guards for type-only imports
- Follow the established dependency hierarchy when adding new modules
- Use `hasattr()` checks before accessing potentially missing attributes
- The core quantity class is now `Quantity` (formerly `FastQuantity`)
- Variable types now extend `TypedQuantity` and `ExpressionQuantity`

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

**Problem System Composition**: The refactored Problem system supports complex sub-problem composition:

- **Variable Namespacing**: Sub-problem variables are automatically namespaced (e.g., `header.P` becomes `header_P`)
- **Expression Namespacing**: All expression types (BinaryOperation, ConditionalExpression, VariableReference) are properly namespaced
- **ConfigurableVariable**: Proxy variables with arithmetic delegation for composed problems
- **Type Preservation**: Variable cloning preserves original types using `type(variable)(variable.name)` pattern
- **Automatic Composite Equations**: Common patterns like `P = min(header.P, branch.P)` are auto-generated

## important-instruction-reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
